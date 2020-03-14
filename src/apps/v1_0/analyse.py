# -*- encoding: utf-8 -*-
"""
@File    : language.py
@Time    : 2019/06/22 14:07:21
@Author  : 
@License : Copyright (c) 2004-2019 New H3C Tech. Co., Ltd. All rights reserved.
@Desc    : 
"""

import threading
import os
import sys
import stat
import zipfile 
import shutil
import time
from flask import request, json
from flask import make_response
from flask_restful import Resource

from apps.errcode import ErrCode
from apps.util import g_dt, g_ana, g_sim, g_allFlows, g_tunrec, g_sdnply
from apps.util import get_start_end_time,get_start_end_time_fix
from apps.util import info_logger,error_logger
from apps.v1_0.flowsimulate import OneDirectLink, OneLinkInfo, PeriodLinkInfo
from apps.v1_0.bginterface import *

# 5.1.2	获得某个时间的故障前后的topo图
def get_analys_topo():
    try:     
        # 无论是增量仿真还是继承仿真，在仿真分析时，获取的topo都是sim.topo,g_sim.af_topo.
        # 因为在开始仿真的时候，已经根据增量仿真和重新仿真填好左右TOPO了
        topoBefore = g_sim.topo.to_json()
        topoAfter = g_sim.af_topo.to_json()

        data = {
            "before":topoBefore,
            "after":topoAfter
        }
        ret = ErrCode.SUCCESS
    except Exception as e:
        print("get_analys_topo Exception:", e)
        data = {
            "before":{},
            "after":{}
        }
        ret = ErrCode.FAILED

    return ret, data

# 5.1.3	下拉框统计信息的界面
def get_summary_info(input_time):
    try:
        ret = ErrCode.SUCCESS

        flowUnchangedNum = 0
        flowUnchangedPercent = 0
        flowChangedNum = 0
        flowChangedPercent = 0
        flowInterruptNum = 0
        flowInterruptPercent = 0

        tunnelUnchange = 0
        tunnel_unchanged_percent = 0
        tunnelChange = 0
        tunnel_changed_percent = 0
        tunnelInterrupt = 0
        tunnel_interrupt_precent = 0

        start_time, _ = get_start_end_time(input_time)
        # 统计Tunnel的状态变化
        if start_time in g_tunrec.unchange_tuns.keys():
            tunnelUnchange = len(g_tunrec.unchange_tuns[start_time])
        else:
            tunnelUnchange = 0

        if start_time in g_tunrec.change_tuns.keys():    
            tunnelChange = len(g_tunrec.change_tuns[start_time])
        else:
            tunnelChange = 0

        if start_time in g_tunrec.interrupt_tuns.keys():
            tunnelInterrupt = len(g_tunrec.interrupt_tuns[start_time])
        else:
            tunnelInterrupt = 0
        total_tunnel = tunnelUnchange + tunnelChange + tunnelInterrupt
        if total_tunnel > 0:
            tunnel_unchanged_percent = round(100 * tunnelUnchange / total_tunnel)
            tunnel_changed_percent = round(100 * tunnelChange / total_tunnel)
            tunnel_interrupt_precent = round(100 * tunnelInterrupt / total_tunnel)
        else:
            tunnel_unchanged_percent = 0
            tunnel_changed_percent = 0
            tunnel_interrupt_precent = 0

        # 统计Flow变化的数据
        
        if start_time in g_sim.statis_flow:
            flow_cences_info = g_sim.statis_flow[start_time]
            total_flow = flow_cences_info.unchanged_flow_num + flow_cences_info.changed_flow_num + flow_cences_info.interrupt_flow_num
            if 0 != total_flow:
                flowUnchangedNum = flow_cences_info.unchanged_flow_num
                flowUnchangedPercent = round(100 * flow_cences_info.unchanged_flow_num / total_flow)
                flowChangedNum = flow_cences_info.changed_flow_num
                flowChangedPercent = round(100 * flow_cences_info.changed_flow_num / total_flow)
                flowInterruptNum = flow_cences_info.interrupt_flow_num
                flowInterruptPercent = round(100 * flow_cences_info.interrupt_flow_num / total_flow)

        # 统计负载变化
        load_num_other = g_sim.statis_load.other_num
        load_num_other_pec = g_sim.statis_load.other_percent
        load_num_overload = g_sim.statis_load.overload_num
        load_num_overload_pec = g_sim.statis_load.overload_percent

        # 数据拼装 
        data = {
                    "summary" : {	
                                "flows" : { 
                                            "flow_unchanged" : flowUnchangedNum,
                                            "flow_unchange_percent":flowUnchangedPercent,
                                            "flow_changed" : flowChangedNum,
                                            "flow_change_percent":flowChangedPercent,
                                            "flow_interrupted" : flowInterruptNum,
                                            "flow_interrupted_percent":flowInterruptPercent
                                        },
                                "tunnels" : {
                                                "tunnel_unchanged" : tunnelUnchange,
                                                "tunnel_changed" : tunnelChange,
                                                "tunnel_interrupted" : tunnelInterrupt,
                                                "tunnel_unchanged_percent" : tunnel_unchanged_percent,
                                                "tunnel_changed_percent" : tunnel_changed_percent,
                                                "tunnel_interrupted_percent" : tunnel_interrupt_precent
                                            },
                                "loads"   :{	
                                                "other_percent" : load_num_other_pec,
                                                "other_num":load_num_other,
                                                "overload_percent" : load_num_overload_pec,
                                                "overload_num":load_num_overload
                                            }
                                }
            }
    except Exception as e:
        print("get_summary_info Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        ret = ErrCode.FAILED
        data = {}
    return ret, data

# 5.1.4子函数：FLOWS信息及FLOWS的ShowPath信息数据拼装
def cal_flows_and_path_dara(flow_type, id, st_time, flow_info_list):
    try:
        # 数据拼装
        flow_info = {}
        pathInfo_before = {}
        pathInfo_after = {}
        cur_flow = g_sim.flow_info[id]
        #print('cur_flow = ', cur_flow)
        # data 拼装
        flow_info['name'] = cur_flow.flow_name
        flow_info['failReason'] = 'N/A'
        flow_info['pathInfo'] = {}
        if flow_type == 'interrupt':
            flow_info['staus'] = 'Interrupt'
        elif flow_type == 'change':
            flow_info['staus'] = 'Change'
        else:
            flow_info['staus'] = 'Unchange'

        if cur_flow.tun_name == "":
            if g_sim.type_flow == True:
                flow_info['hopCount'] = 'N/A'+ '->' + str(cur_flow.af_jump["all"])
                flow_info['pathDelay'] = 'N/A' + '->' + str(cur_flow.af_delay["all"])

                flow_info['pathInfo']['beforeFault']= pathInfo_before
                pathInfo_before['flowInfo'] = {
                    'flowName':cur_flow.flow_name,
                    'flowIsReach':'N/A',
                    'flowHopNum':'N/A',
                    'flowDelay':'N/A' 
                }
                pathInfo_before['flowPathNum'] = len(cur_flow.b4_path["all"])
                pathInfo_before['flowPath'] = cur_flow.b4_path["all"]
            else:
                flow_info['hopCount'] = str(cur_flow.b4_jump["all"]) + '->' + str(cur_flow.af_jump["all"])
                flow_info['pathDelay'] = str(cur_flow.b4_delay["all"]) + '->' + str(cur_flow.af_delay["all"])
                if cur_flow.b4_jump["all"] != 0:
                    isReach = "Reachable"
                else:
                    isReach = "Unreachable"

                # beforeFault 赋值
                flow_info['pathInfo']['beforeFault'] = pathInfo_before

                pathInfo_before['flowInfo'] = {
                    'flowName':cur_flow.flow_name,
                    'flowIsReach':isReach,
                    'flowHopNum':cur_flow.b4_jump["all"],
                    'flowDelay':cur_flow.b4_delay["all"]
                }
                pathInfo_before['flowPathNum'] = len(cur_flow.b4_path["all"])
                pathInfo_before['flowPath'] = cur_flow.b4_path["all"]

            # afterFault 赋值
            flow_info['pathInfo']['afterFault'] = pathInfo_after
            if flow_type != 'interrupt':
                if cur_flow.af_jump["all"] != 0:
                    isReach = "Reachable"
                else:
                    isReach = "Unreachable"

                pathInfo_after['flowInfo'] = {
                    'flowName':cur_flow.flow_name,
                    'flowIsReach':isReach,
                    'flowHopNum':cur_flow.af_jump["all"],
                    'flowDelay':cur_flow.af_delay["all"]
                }
                pathInfo_after['flowPathNum'] = len(cur_flow.af_path["all"])
                pathInfo_after['flowPath'] = cur_flow.af_path["all"]
            else:
                pathInfo_after['flowInfo'] = {
                    'flowName':cur_flow.flow_name,
                    'flowIsReach':"Unreachable",
                    'flowHopNum':0,
                    'flowDelay':0
                }
                pathInfo_after['flowPathNum'] = len(cur_flow.af_path["all"])
                pathInfo_after['flowPath'] = cur_flow.af_path["all"]

            flow_info_list.append(flow_info)

        else:
            if g_sim.type_flow == True:
                flow_info['hopCount'] = 'N/A'+ '->' + str(cur_flow.af_jump[st_time])
                flow_info['pathDelay'] = 'N/A' + '->' + str(cur_flow.af_delay[st_time])

                flow_info['pathInfo']['beforeFault'] = pathInfo_before
                
                pathInfo_before['flowInfo'] = {
                    'flowName':cur_flow.flow_name,
                    'flowIsReach':'N/A',
                    'flowHopNum':'N/A',
                    'flowDelay':'N/A' 
                }
                pathInfo_before['flowPathNum'] = len(cur_flow.b4_path[st_time])
                pathInfo_before['flowPath'] = cur_flow.b4_path[st_time]

            else:
                flow_info['hopCount'] = str(cur_flow.b4_jump[st_time]) + '->' + str(cur_flow.af_jump[st_time])
                flow_info['pathDelay'] = str(cur_flow.b4_delay[st_time]) + '->' + str(cur_flow.af_delay[st_time])
                # beforeFault 赋值
                flow_info['pathInfo']['beforeFault'] = pathInfo_before
                if cur_flow.b4_jump[st_time] != 0:
                    isReach = "Reachable"
                else:
                    isReach = "Unreachable"

                pathInfo_before['flowInfo'] = {
                    'flowName':cur_flow.flow_name,
                    'flowIsReach':isReach,
                    'flowHopNum':cur_flow.b4_jump[st_time],
                    'flowDelay':cur_flow.b4_delay[st_time]
                }
                pathInfo_before['flowPathNum'] = len(cur_flow.b4_path[st_time])
                pathInfo_before['flowPath'] = cur_flow.b4_path[st_time]

            # afterFault 赋值
            flow_info['pathInfo']['afterFault'] = pathInfo_after
            if flow_type != 'interrupt':
                if cur_flow.af_jump[st_time]:
                    isReach = "Reachable"
                else:
                    isReach = "Unreachable"

                pathInfo_after['flowInfo'] = {
                    'flowName':cur_flow.flow_name,
                    'flowIsReach':isReach,
                    'flowHopNum':cur_flow.af_jump[st_time],
                    'flowDelay':cur_flow.af_delay[st_time]
                }
                pathInfo_after['flowPathNum'] = len(cur_flow.af_path[st_time])
                pathInfo_after['flowPath'] = cur_flow.af_path[st_time]
            else:
                pathInfo_after['flowInfo'] = {
                    'flowName':cur_flow.flow_name,
                    'flowIsReach':"Unreachable",
                    'flowHopNum':0,
                    'flowDelay':0
                }
                pathInfo_after['flowPathNum'] = len(cur_flow.af_path[st_time])
                pathInfo_after['flowPath'] = cur_flow.af_path[st_time]

            flow_info_list.append(flow_info)
    
    except Exception as e:# 正式时，打开
        print("cal_flows_and_path_dara Exception:", e)
        info_logger.error(e)
        error_logger.error(e)

# 5.1.4	FLOWS信息及FLOWS的ShowPath信息 
def get_flows_and_path_info(st_time, flow_type):

    ret = ErrCode.SUCCESS

    # 获取起始时间 
    try:
        time_start, _ = get_start_end_time(st_time)
        if not g_sim.statis_flow:
            data = {}
            return ret, data
        if time_start not in g_sim.statis_flow.keys():
            ret = ErrCode.SUCCESS
            data = {}
            return ret, data

        # 需要返回的流量内容列表
        flow_info_list = []
        
        # 编程规范里有说避免使用中文,故把“中断”等中文字段改成英文
        if flow_type == 'all':
            for id1 in g_sim.statis_flow[time_start].flow_interrupt_info.keys():
                cal_flows_and_path_dara('interrupt',id1, time_start, flow_info_list)
            for id2 in g_sim.statis_flow[time_start].flow_changed_info.keys():
                cal_flows_and_path_dara('change',id2, time_start, flow_info_list)
            # unchange的部分，10.26协商不显示，包含Flow、load和tunnel

        elif flow_type == 'interrupt':
            for id1 in g_sim.statis_flow[time_start].flow_interrupt_info.keys():
                cal_flows_and_path_dara('interrupt',id1,time_start, flow_info_list)
        elif flow_type == 'change':
            for id2 in g_sim.statis_flow[time_start].flow_changed_info.keys():
                cal_flows_and_path_dara('change',id2, time_start, flow_info_list)
        elif flow_type == 'unchange':
            for id3 in g_sim.statis_flow[time_start].flow_unchanged_info.keys():
                cal_flows_and_path_dara('unchange',id3,time_start, flow_info_list)
        else:
            ret = ErrCode.SUCCESS
            data = {}
            return ret, data
        
        data = {
            "flowNum":len(flow_info_list),
            "flowsInfo":flow_info_list
        }
        return ret, data

    except Exception as e:
        print("get_flows_and_path_info Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        data = {}
        return ret, data

def get_before_link_stage_info():
    """获得故障前的所有链路的带宽利用率所在的阈值区间
       注：此函数是基于某一时刻，已经计算了这个“某一时刻”的阈值设置，得到了带宽利用率区间了的。
    
    Args:
        none
    Returns:
        none
    Raise:
        none
    """
    try:
        sum_threshold_before = {}
        threshold_before = []
        topo_links = g_sim.topo.links

        for linkid,link_info in topo_links.items():
            temp = {'linkId':linkid, 'stage1to2':link_info.bandwidthStage1to2, 'stage2to1':link_info.bandwidthStage2to1}
            threshold_before.append(temp)

        sum_threshold_before['before'] = threshold_before
        return sum_threshold_before
    except Exception as e:
        print("get_before_link_stage_info Exception:", e)
        sum_threshold_before = []
        info_logger.error(e)
        error_logger.error(e)
        return sum_threshold_before

def get_after_link_stage_info():
    """获得故障后的所有链路的带宽利用率所在的阈值区间
       注：此函数是基于某一时刻，已经计算了这个“某一时刻”的阈值设置，得到了带宽利用率区间了的。
    
    Args:
        none
    Returns:
        none
    Raise:
        none
    """
    try:
        sum_threshold_after = {}
        threshold_after = []
        topo_links = g_sim.af_topo.links
        
        for linkid,link_info in topo_links.items():
            temp = {'linkId':linkid, 'stage1to2':link_info.bandwidthStage1to2, 'stage2to1':link_info.bandwidthStage2to1}
            threshold_after.append(temp)

        sum_threshold_after['after'] = threshold_after
        return sum_threshold_after
    except Exception as e:
        print("get_after_link_stage_info Exception:", e)
        sum_threshold_after = []
        info_logger.error(e)
        error_logger.error(e)
        return sum_threshold_after

def get_before_and_after_link_stage_info():
    """获得故障前及故障后的所有链路的带宽利用率所在的阈值区间
       注：此函数是基于某一时刻，已经计算了这个“某一时刻”的阈值设置，得到了带宽利用率区间了的。
    
    Args:
        none
    Returns:
        none
    Raise:
        none
    """
    sum_threshold = {}
    threshold_before = []
    threshold_after = []

    for linkid,link_info in g_sim.topo.links.items():
        temp_before = {'linkId':linkid, 'stage1to2':link_info.bandwidthStage1to2, 'stage2to1':link_info.bandwidthStage2to1}
        threshold_before.append(temp_before)
    for linkid,link_info in g_sim.af_topo.links.items():
        temp_after = {'linkId':linkid, 'stage1to2':link_info.bandwidthStage1to2, 'stage2to1':link_info.bandwidthStage2to1}
        threshold_after.append(temp_after)

    sum_threshold['before'] = threshold_before
    sum_threshold['after'] = threshold_after
    return sum_threshold
       
#5.1.7	故障定义
def get_fault_def():
    try:
        faultDefList = []
        if g_sim.topo and g_sim.af_topo:
            #遍历字典寻找设置了故障的nodes
            if g_sim.topo.nodes:
                for key in g_sim.topo.nodes:
                    if g_sim.topo.nodes[key].fault == "yes":
                        faultDef = {}
                        faultDef["name"] = g_sim.topo.nodes[key].name
                        faultDef["faultType"] = "Node"
                        faultDef["describe"] = 'Node Fault'

                        if g_sim.af_topo.nodes[key].fault == "yes":
                            faultDef["message"] = 'Before & After Definition'
                        else:
                            faultDef["message"] = 'Before Definition'

                        faultDefList.append(faultDef)
            #遍历字典寻找设置了故障的link
            if g_sim.topo.links:
                for key in g_sim.topo.links:
                    if g_sim.topo.links[key].fault == "yes":
                        faultDef = {}
                        faultDef["name"] = g_sim.topo.links[key].name
                        faultDef["faultType"] = "Link"
                        faultDef["describe"] = 'Link Fault'
                        if g_sim.af_topo.links[key].fault == "yes":
                            faultDef["message"] = 'Before & After Definition'
                        else:
                            faultDef["message"] = 'Before Definition'
                        faultDefList.append(faultDef)
            
            if g_sim.af_topo.nodes:
                for key in g_sim.af_topo.nodes:
                    if g_sim.af_topo.nodes[key].fault == "yes" and g_sim.topo.nodes[key].fault != "yes":
                        faultDef = {}
                        faultDef["name"] = g_sim.af_topo.nodes[key].name
                        faultDef["faultType"] = "Node"
                        faultDef["describe"] = 'Node Fault'
                        faultDef["message"] = 'After Definition'
                        #dic["description"] = g_dt.phy_topo.nodes[key].description
                        # 将dic字典加入集合
                        faultDefList.append(faultDef)

            #遍历字典 寻找错误的link
            if g_sim.af_topo.links:
                for key in g_sim.af_topo.links:
                    if g_sim.af_topo.links[key].fault == "yes" and g_sim.topo.links[key].fault != "yes":
                        faultDef = {}
                        faultDef["name"] = g_sim.af_topo.links[key].name
                        faultDef["faultType"] = "Link"
                        faultDef["describe"] = 'Link Fault'
                        faultDef["message"] = 'After Definition'
                        #dic["description"] = g_dt.phy_topo.nodes[key].description
                        # 将dic字典加入集合
                        faultDefList.append(faultDef)
            data = {
                        "faultDefNum":len(faultDefList),
                        "faultDef": faultDefList
                }
        else:
            data = {"faultDefNum":0,
                    "faultDef": []
                    }
        return data
    except Exception as e:
        print("get_fault_def Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        
        data = {"faultDefNum":0,
                "faultDef": faultDefList
                }
        return data

# 5.2.1	查看某条选择路径承载的flow
def get_select_flow_load(anlyseStep, st_time, linkId):
    try:
        ret = ErrCode.SUCCESS
        time_start, _ = get_start_end_time(st_time)

        # 通过linkid找到nodeid，再用nodeid找到nodename
        nodeid1 = g_sim.topo.links[linkId].nodeid1
        nodeid2 = g_sim.topo.links[linkId].nodeid2
        name1 = g_sim.topo.nodes[nodeid1].name
        name2 = g_sim.topo.nodes[nodeid2].name

        data = {
            "time": time_start, #时间
            "flowLoad1": {
                            "source": name1,
                            "dest": name2,
                            "loadNum":0,
                            "loadInfo": []
                        },
            "flowLoad2": {
                        "source": name2,
                        "dest": name1,
                        "loadNum":0,
                        "loadInfo": []
                    }
        }

        # 获取时间片段 
        # flow_info
        if time_start in g_sim.statis_flow.keys():
            flow_info = g_sim.statis_flow[time_start]
        else:
            ret = ErrCode.SUCCESS
            return ret, data

        # 获取到当前时间段内的所有flow的id
        if anlyseStep == 'before':
            if linkId in flow_info.b4_link_to_flow.keys():
                flow_id_list = flow_info.b4_link_to_flow[linkId]
            else:
                ret = ErrCode.SUCCESS
                return ret, data
        elif anlyseStep == 'after':
            if linkId in flow_info.after_link_to_flow.keys():
                flow_id_list = flow_info.after_link_to_flow[linkId]
            else:
                ret = ErrCode.SUCCESS
                return ret, data

        # 根据flow的id把"flowName"、"payLoad"、"bandPercent" 加到下面的infoList列表中
        infoList1 = []
        infoList2 = []
        for flow_id in flow_id_list:
            cur_flow = g_sim.flow_info[flow_id]
            if cur_flow.tun_name == "":
                
                # 确定当前的flow是1to2还是2to1：根据nodeid起点来判断 
                # 当前的 cur_flow 的cur_flow['source_node_id'] 不一定是 nodeid1 ，因为
                # cur_flow['source_node_id']是整体某条flow的source_node、des_node 
                # 所以根据这个list去判断： 
                if anlyseStep == 'before':
                    pathList = g_sim.flow_info[flow_id].b4_path['all']
                else:    
                    pathList = g_sim.flow_info[flow_id].af_path['all']

                # 前台页面显示的单位是Mbps,所以需要处以 1000
                cur_payLoad = round(float(cur_flow.bandwidth['all']) / (1000), 2)
                cur_percent = round(float(cur_flow.bandwidth['all']) / float(g_sim.topo.links[linkId].snmpIfHighSpeed) * 100, 2)

            else:
                if anlyseStep == 'before':
                    pathList = g_sim.flow_info[flow_id].b4_path[time_start]
                else:    
                    pathList = g_sim.flow_info[flow_id].af_path[time_start]
                
                cur_payLoad = round(float(cur_flow.bandwidth[time_start]) / (1000), 2)
                cur_percent = round(float(cur_flow.bandwidth[time_start]) / float(g_sim.topo.links[linkId].snmpIfHighSpeed) * 100, 2)

            flag = 2 #空
            # 在这个列表中，首先出现的  start_node_id 若等于   cur_flow的source id，说明是以他起始
            # 且 第一次出现即可判断，因为list是一头一尾重叠的，第一次出现cur_flow时，看他在头还是尾上就能判断
            for path in pathList:
                id1 = path['start_node_id'] 
                id2 = path['end_node_id'] 

                if id1 == g_sim.topo.links[linkId].nodeid1 and id2 == g_sim.topo.links[linkId].nodeid2:     
                    flag = 0
                    break
                if id1 == g_sim.topo.links[linkId].nodeid2 and id2 == g_sim.topo.links[linkId].nodeid1:
                    flag = 1
                    break
            
            cur_name = cur_flow.flow_name
            info = {
                "flowName":cur_name,
                "payLoad": cur_payLoad,  
                "bandPercent": cur_percent
            }

            if flag == 0: # 判断此link上的flow是1to2还是2to1，后续修改
                infoList1.append(info)

            elif flag == 1: #2to1
                infoList2.append(info)
            else:
                pass

        flowLoad1 = {
            "source": name1,
            "dest": name2,
            "loadNum":len(infoList1),
            "loadInfo": infoList1
        }

        flowLoad2 = {
            "source": name2,
            "dest": name1,
            "loadNum":len(infoList2),
            "loadInfo": infoList2
        }

        data = {
            "time": time_start, #时间
            "flowLoad1": flowLoad1,
            "flowLoad2": flowLoad2
        }
        return ret, data
    except Exception as e:
        print("get_select_flow_load Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        ret = ErrCode.SUCCESS
        data = {}
        return ret, data         

def get_tunnel_flow_info(cur_time, anlyseStep, tunnelId, path_type):
    try:
        ret = ErrCode.SUCCESS
        loadInfoList = []
        start_time, _ = get_start_end_time(cur_time)

        if anlyseStep == 'before':
            if not g_sim.type_flow:  # 流量仿真时，仿真定义前无导入流量以及隧道流量信息
                if start_time in g_tunrec.sim_b4tuns.keys():
                    tun_step = g_tunrec.sim_b4tuns[start_time]
                    if tunnelId in tun_step.keys():
                        tun_name = tun_step[tunnelId].name
                        tun_srcid = tun_step[tunnelId].src_id
                        tun_desid = tun_step[tunnelId].des_id

                        for _, flow in g_sim.flow_info.items():
                            if tun_name == flow.tun_name and tun_srcid == flow.src_id and tun_desid == flow.des_id:
                                if path_type == tun_step[tunnelId].active_path or path_type == 'all':
                                    payLoad = round(float((flow.bandwidth[start_time]) / 1000), 2)    # 除以1000,把kbps转换为mbps
                                    flowName = flow.flow_name
                                    tunInfo = {
                                        "flowName": flowName,
                                        "payLoad": ('%.2f'%(payLoad)),  # 单位是 Mbps
                                    }
                                    loadInfoList.append(tunInfo)
                            
                        #else:
                        #    error_logger.error("b4 get_tunnel_flow_info:name: %s, %s, src_id: %s, %s, des_id:%s,%s"%(tun_name, flow['tunnel_name'], tun_srcid, flow['source_node_id'], tun_desid, flow['des_node_id']))
        else:
            if start_time in g_tunrec.sim_aftuns.keys():
                tun_step = g_tunrec.sim_aftuns[start_time]
                if tunnelId in tun_step.keys():
                    tun_name = tun_step[tunnelId].name
                    tun_srcid = tun_step[tunnelId].src_id
                    tun_desid = tun_step[tunnelId].des_id

                    for _,flow in g_sim.flow_info.items():
                        if tun_name == flow.tun_name and tun_srcid == flow.src_id and tun_desid == flow.des_id:
                            if path_type == tun_step[tunnelId].active_path or path_type == 'all':  
                                payLoad = round(float((flow.bandwidth[start_time]) / 1000), 2)    # 除以1000,把kbps转换为mbps
                                flowName = flow.flow_name
                                tunInfo = {
                                    "flowName": flowName,
                                    "payLoad": ('%.2f'%(payLoad))  # 单位是 Mbps
                                }
                                loadInfoList.append(tunInfo)
                    #else:
                    #    error_logger.error("af get_tunnel_flow_info:name: %s, %s, src_id: %s, %s, des_id:%s,%s"%(tun_name, flow['tunnel_name'], tun_srcid, flow['source_node_id'], tun_desid, flow['des_node_id']))

        data = {
            "tunnelFlow": 
            {
                "loadNum":len(loadInfoList),
                "loadInfo": loadInfoList
            }
        }
        return ret, data
    except Exception as e:
        print("get_tunnel_flow_info Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        data = {
            "tunnelFlow": 
            {
                "loadNum":0,
                "loadInfo": []
            }
        }
        return ErrCode.FAILED, data

#5.2.4 获取故障前某个时刻的流量列表 用get_all_loaded_flow函数中的方式实现
def get_flow_list(anlyseStep, input_time):
    try:
        ret = ErrCode.SUCCESS
        data = {}

        time_start, _ = get_start_end_time(input_time)

        # 首先 根据故障前或故障后的标志和当前时间，获取所有的flowId
        flow_list = []
        if anlyseStep == 'before':
            if not g_sim.flow_list_before_fault:
                return ret, data
            if time_start in g_sim.flow_list_before_fault.keys():
                flow_list = g_sim.flow_list_before_fault[time_start]['flowinfo']
            else:
                ret = ErrCode.SUCCESS
                return ret, data
        else:
            if not g_sim.flow_list_after_fault:
                return ret, data
            if time_start in g_sim.flow_list_after_fault.keys():
                flow_list = g_sim.flow_list_after_fault[time_start]['flowinfo']
            else:
                ret = ErrCode.SUCCESS
                return ret, data

        type_num = 0
        b_add = 0
        all_type_info = [] # 输出的数据 结构


        if not flow_list:
            #无流量的时候，直接返回为空,这样前台不会显示错误，以便界面更合理
            data ={}
            ret = ErrCode.SUCCESS
            return ret, data
    
        for value in flow_list:
            if isinstance (value, dict):
                b_add = 0
                flow_id = value['flowId']           
                flow_name = value['flow_name']
                flow_source = value['source_node_name']
                flow_dest = value['des_node_name']
                flow_type = value['flow_type']
                # add 
                flow_desnode_id = value['des_node_id']
                flow_sourcenode_id = value['source_node_id']

                for all_type_item in all_type_info:
                    if all_type_item['flow_type'] == flow_type:                    
                        flow_detail = all_type_item['flowsDetail']
                        for flow_detail_item in  flow_detail:
                            if flow_detail_item['sourceFlow'] == flow_source:
                                flows = flow_detail_item['flows']
                                for flows_item in  flows:
                                    if flows_item['desFlow'] == flow_dest:
                                        b_add = 1
                                        flows_item['flowNum'] += 1                                                
                                        new_dic_msg = {'flowId':flow_id, 'flowName':flow_name,'flowSourceNodeId':flow_sourcenode_id,'flowDesNodeId':flow_desnode_id}
                                        flows_item['flow_info'].append(new_dic_msg)
                                        continue # 退出for flows_item in  flows 循环
                                if b_add == 0: # source 相同，但是目的地址没有相同的，新加一条
                                    b_add = 1
                                    new_dic_msg ={'desFlow': flow_dest, 'flowNum':1, 'flow_info':[{'flowId':flow_id, 'flowName':flow_name,'flowSourceNodeId':flow_sourcenode_id,'flowDesNodeId':flow_desnode_id}]}
                                    flow_detail_item['desFlowNum'] += 1
                                    flows.append(new_dic_msg)
                                    continue # 退出flow_detail_item in  flow_detail
                        if b_add == 0: #flow type 相同，但是源不相同
                            b_add = 1
                            new_dic_msg ={'sourceFlow':flow_source, 'desFlowNum':1, 'flows':[{'desFlow': flow_dest, 'flowNum':1, 'flow_info':[{'flowId':flow_id, 'flowName':flow_name,'flowSourceNodeId':flow_sourcenode_id,'flowDesNodeId':flow_desnode_id}]}]}
                            all_type_item['thisTypeSurceNum'] += 1
                            flow_detail.append(new_dic_msg)    
                            continue
                if  b_add == 0:
                    new_dic_msg ={'flow_type':flow_type, 'thisTypeSurceNum':1, 'flowsDetail':[{'sourceFlow':flow_source, 'desFlowNum':1, 'flows':[{'desFlow': flow_dest, 'flowNum':1, 'flow_info':[{'flowId':flow_id, 'flowName':flow_name,'flowSourceNodeId':flow_sourcenode_id,'flowDesNodeId':flow_desnode_id}]}]}]}
                    all_type_info.append(new_dic_msg)
                    type_num += 1  

        data = {
                'typeNum':type_num,
                'allFlowInfo':all_type_info              
                }
        return ret, data
    except Exception as e:
        print("get_flow_list Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        data = {
            'typeNum':0,
            'allFlowInfo':{}  
        }
        return ErrCode.FAILED, data

#5.2.6 显示选中的流量路径
def get_flow_direction(anlyseStep, curTime, flowId):
    try:
        ret = ErrCode.SUCCESS
        data = {}
        time_start, _ = get_start_end_time(curTime)
        if not time_start:
            ret = ErrCode.SUCCESS
            return ret, data

        sourceAssetId = ''
        desAssetId = ''

        # 获取起始点和终点
        if anlyseStep == 'before':
            if time_start in g_sim.flow_list_before_fault.keys():
                flow_list = g_sim.flow_list_before_fault[time_start]['flowinfo']
                for cur_flow in flow_list:
                    if cur_flow['flowId'] == flowId:
                        sourceAssetId = cur_flow['source_node_id']
                        desAssetId = cur_flow['des_node_id']
            else:
                ret = ErrCode.SUCCESS
                return ret, data
        else:
            if time_start in g_sim.flow_list_after_fault.keys():
                flow_list = g_sim.flow_list_after_fault[time_start]['flowinfo']
                for cur_flow in flow_list:
                    if cur_flow['flowId'] == flowId:
                        sourceAssetId = cur_flow['source_node_id']
                        desAssetId = cur_flow['des_node_id']
            else:
                ret = ErrCode.SUCCESS
                return ret, data

        data = {
            "curTime":curTime, # time
            "sourceAssetId":sourceAssetId,  
            "desAssetId":desAssetId
        }
        return ret, data
    except Exception as e:
        print("get_flow_direction Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        data = {
            "curTime":curTime, # time
            "sourceAssetId":"",  
            "desAssetId":""
        }
        return ErrCode.FAILED, data

#5.2.7 选择某条Flow,进行查看
def get_select_flow_info(anlyseStep, curTime, flowId):
    ret = ErrCode.SUCCESS
    flowInfoList = []
    # 用于topo图显示用 
    flowPathInfoList = []    
    selectFlowInfoList = []
    totalJump = 0
    flowManner = "IPV4/ETHERNET" 
    flowPathNum = 0
    data = {}

    try:
        start_time, _ =  get_start_end_time(curTime)
        
        if start_time in g_sim.b4_flow.keys():
            flow_id_list = g_sim.b4_flow[start_time]
            # 判断当前的flowId是否在当前时刻的flow列表里 
            if flowId in flow_id_list:
                #flow_dict = g_sim.flow_info[flowId]
                if anlyseStep == 'before':
                    if "all" in g_sim.flow_info[flowId].b4_path.keys():
                        pathList = g_sim.flow_info[flowId].b4_path["all"]
                        if len(pathList) > 0:
                            totalJump = len(pathList) + 1
                        else:
                            totalJump = len(pathList)
                    elif start_time in g_sim.flow_info[flowId].b4_path.keys():
                        pathList = g_sim.flow_info[flowId].b4_path[start_time]
                        if len(pathList) > 0:
                            totalJump = len(pathList) + 1
                        else:
                            totalJump = len(pathList)
                    else:
                        pathList = []
                        totalJump = 0
                else:
                    if "all" in g_sim.flow_info[flowId].af_path.keys():
                        pathList = g_sim.flow_info[flowId].af_path["all"]
                        if len(pathList) > 0:
                            totalJump = len(pathList) + 1
                        else:
                            totalJump = len(pathList)
                    elif start_time in g_sim.flow_info[flowId].af_path.keys():
                        pathList = g_sim.flow_info[flowId].af_path[start_time]
                        if len(pathList) > 0:
                            totalJump = len(pathList) + 1
                        else:
                            totalJump = len(pathList)
                    else:
                        pathList = []
                        totalJump = 0
                    
                # 获取topo图上flowPathInfoList
                jumpId = 0
                flowName = g_sim.flow_info[flowId].flow_name
                if len(pathList) == 0:
                    data = {
                        "totalJump":0,	    #总跳数
                        "flowManner":flowManner,	#承载方式 
                        "flowPathNum":0,
                        # 右侧下方表格 
                        "flowInfo":[],
                        "selectFlowInfo":[{'flowName':flowName, 'type':'Flow','payLoad':0, 'isReach':"Unreachable"}],
                        # 用于展现topo上的路径信息
                        "flowPathInfo":[]
                    }
                    return ret, data

                for path in pathList:
                    # 通过start_node_id 找到nodeId，然后再找到nodename (有修改，不用name用id)
                    flowPathInfo = {}
                    nodeId1 = path['start_node_id']
                    nodeId2 = path['end_node_id']
                    # 判断是头是尾 

                    flowPathInfo['sourceAssetId'] = nodeId1
                    flowPathInfo['desAssetId'] = nodeId2

                    flowPathInfoList.append(flowPathInfo)

                    # 根据node id 找到对应的link 
                    for _,value in g_sim.topo.links.items():
                        if value.nodeid1 == nodeId1 and value.nodeid2 == nodeId2:
                            outPortName = value.ifdesc1  # Ginet1/0/1
                            portCosts = value.ifdesc1cost
                            outPortType = str(outPortName.split('net', -1)[0]) + 'net'
                            break
                        elif value.nodeid1 == nodeId2 and value.nodeid2 == nodeId1:
                            outPortName = value.ifdesc2  # Ginet1/0/1
                            portCosts = value.ifdesc2cost
                            outPortType = str(outPortName.split('net', -1)[0]) + 'net'
                            break
                        else:
                            outPortName = 'N/A'
                            outPortType = 'N/A'
                            portCosts = 0

                    # 获取flow的起始节点
                    netName = g_sim.topo.nodes[nodeId1].name
                    netEleType = g_sim.topo.nodes[nodeId1].nettypedesc 

                    flowInfo = {
                        "jumpId":jumpId,	        #跳数编号    #暂时不要
                        "netEleType":netEleType, 	#网元类型    
                        "netEleName": netName, #网元名称
                        "branchPoint":" no",			#是否分支点
                        "convergencePoint":"no",		#是否为汇聚点	
                        "fowardPrecent":100,		#转发量百分比
                        "outPortName":outPortName,		#出接口名称
                        "outPortType": outPortType,	    #出接口类型
                        "bandPrecent":252.56,	#带宽利用率  #暂时不要
                        "loadManner":"IPV4",	#承载方式
                        "protocal":"OSPF",		#路由协议  #暂时不要
                        "outPortCost":portCosts		#出接口cost
                    }
                    flowInfoList.append(flowInfo)
                    jumpId += 1
                    #print('flowInfoList = ',flowInfoList)

                # 执行完后，还需加上最后一个path的尾节点
                flowInfo = {
                    "jumpId":jumpId,	        #跳数编号    #暂时不要
                    "netEleType":g_sim.topo.nodes[nodeId2].nettypedesc, 	#网元类型    
                    "netEleName": g_sim.topo.nodes[nodeId2].name, #网元名称
                    "branchPoint":" no",			#是否分支点
                    "convergencePoint":"no",		#是否为汇聚点	
                    "fowardPrecent":100,		#转发量百分比
                    "outPortName":'N/A',		#出接口名称
                    "outPortType":'N/A',	    #出接口类型
                    "bandPrecent":252.56,	#带宽利用率  #暂时不要
                    "loadManner":"IPV4",	#承载方式
                    "protocal":"OSPF",		#路由协议  #暂时不要
                    "outPortCost":'N/A'		#出接口cost
                }
                flowInfoList.append(flowInfo)

                # 获取左侧下方 selectFlowInfo
                # 目前根据视频一次显示一个flow，因此没有把入参flowId做成list，后续做list后下面改成for循环即可
                selectFlowInfo = {}
                flowName = g_sim.flow_info[flowId].flow_name
                selectFlowInfo['flowName'] = flowName
                selectFlowInfo['ECMP'] = 1      # 暂时不知道什么用 先用视频上的1 来代替
                tun_name = g_sim.flow_info[flowId].tun_name
                if tun_name == "":
                    selectFlowInfo['payLoad'] = ('%.2f'%(round(float(g_sim.flow_info[flowId].bandwidth["all"] / 1000), 2)))
                else:
                    selectFlowInfo['payLoad'] = ('%.2f'%(round(float(g_sim.flow_info[flowId].bandwidth[start_time] / 1000), 2)))
                if totalJump > 0:
                    selectFlowInfo['isReach'] = "Reachable"
                else:
                    selectFlowInfo['isReach'] = "Unreachable"
                selectFlowInfo['path'] = flowPathInfoList     # 填写具体的流量路径信息
                selectFlowInfo['type'] = 'Flow'
                selectFlowInfoList.append(selectFlowInfo)
            else:
                return ret, data

        flowPathNum = len(flowPathInfoList)
        
        data = {
            "totalJump":totalJump,	    #总跳数
            "flowManner":flowManner,	#承载方式 
            "flowPathNum":flowPathNum,
            # 右侧下方表格 
            "flowInfo":flowInfoList,
            "selectFlowInfo":selectFlowInfoList,
            # 用于展现topo上的路径信息
            "flowPathInfo":flowPathInfoList
        }
        return ret, data
    except Exception as e:
        print("get_select_flow_info exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.FAILED,{}
 

# 5.1.5	Tunnel信息的界面及其ShowPath
def get_tunnels_info(curTime, anlyseType):
    try:
        ret = ErrCode.SUCCESS
        tunnels_list = []
        tunid_list = []
        time_start, _ = get_start_end_time(curTime)

        info_logger.error("get_tunnels_info time:%d"%(time_start))

        if anlyseType == "unchange" and time_start in g_tunrec.unchange_tuns.keys():
            tunid_list = g_tunrec.unchange_tuns[time_start] 
        elif anlyseType == "interrupt" and time_start in g_tunrec.interrupt_tuns.keys():
            tunid_list = g_tunrec.interrupt_tuns[time_start]
        elif anlyseType == "change" and time_start in g_tunrec.change_tuns.keys():
            tunid_list = g_tunrec.change_tuns[time_start]
        else:
            # unchange的部分，10.26协商不显示，包含Flow、load和tunnel
            if time_start in g_tunrec.change_tuns.keys() and time_start in g_tunrec.interrupt_tuns.keys(): 
                tunid_list = g_tunrec.change_tuns[time_start] + g_tunrec.interrupt_tuns[time_start]
            elif time_start in g_tunrec.change_tuns.keys():
                tunid_list = g_tunrec.change_tuns[time_start]
            elif time_start in g_tunrec.interrupt_tuns.keys(): 
                tunid_list = g_tunrec.interrupt_tuns[time_start]  
        if len(tunid_list) == 0:
            data = {
                "tunnelNum": 0,
                "tunnels":[]
            }
            return ret, data

        for tun_id in tunid_list:
            af_pri_path_info = {}
            af_std_path_info = {}
            b4_pri_path_info = {}
            b4_std_path_info = {}
            
            if time_start in g_tunrec.sim_b4tuns.keys(): 
                tun_step = g_tunrec.sim_b4tuns[time_start]
                if tun_id in tun_step: 
                    value = tun_step[tun_id]  
                    flowgroup_info = g_sdnply.flowgroup[value.flowgroup_id]
                    pathNum = flowgroup_info.pathNum
                    # 增加主备路径的判断
                    # if pathNum == 1:
                    #     b4_active = value.active_path
                    #     b4_std_path_info = {
                    #                 "tunnelInfo":{
                    #                     "tunnelStatus":'DOWN',
                    #                     "tunnelHopNum":0,
                    #                     "tunnelDelay":0
                    #                 }
                    #             } 
                    #     if value.primary_path.path_status == 'UP':
                    #             b4_pri_path_info = {
                    #                 "tunnelInfo":{
                    #                     "tunnelName":value.name,
                    #                     "tunnelStatus":value.primary_path.path_status,
                    #                     "tunnelHopNum":value.primary_path.hop_num,
                    #                     "tunnelDelay":value.primary_path.delay
                    #                 },
                    #                 "tunnelPathNum":value.path_num,
                    #                 "tunnelPath":value.primary_path.path
                    #             }

                    # else:
                        # 故障前主路径信息
                    b4_path = value.path_num
                    b4_active = value.active_path
                    info_logger.error("tun_id:%s, value.path_num:%d, path_status:%s-%s, path:%s,path:%s"
                                    %(tun_id, value.path_num, value.primary_path.path_status, value.standby_path.path_status,value.primary_path.path, value.standby_path.path))
                    if b4_path == 2:

                        if value.primary_path.path_status == 'UP':
                            b4_pri_path_info = {
                                "tunnelInfo":{
                                    "tunnelName":value.name,
                                    "tunnelStatus":value.primary_path.path_status,
                                    "tunnelHopNum":value.primary_path.hop_num,
                                    "tunnelDelay":value.primary_path.delay,
                                    "tunnelStrict":value.primary_path.strict_result

                                },
                                "tunnelPathNum":value.path_num,
                                "tunnelPath":value.primary_path.path
                            }
                        else:
                            b4_pri_path_info = {
                                "tunnelInfo":{
                                    #"tunnelName":value.name,
                                    "tunnelStatus":'DOWN',
                                    "tunnelHopNum":0,
                                    "tunnelDelay":0,
                                    "tunnelStrict":value.primary_path.strict_result
                                }
                            }

                        # 故障前备路径信息
                        if value.standby_path.path_status == 'UP':
                            b4_std_path_info = {
                                "tunnelInfo":{
                                    "tunnelName":value.name,
                                    "tunnelStatus":value.standby_path.path_status,
                                    "tunnelHopNum":value.standby_path.hop_num,
                                    "tunnelDelay":value.standby_path.delay,
                                    "tunnelStrict":value.standby_path.strict_result
                                },
                                "tunnelPathNum":value.path_num,
                                "tunnelPath":value.standby_path.path
                            }
                        else:
                            b4_std_path_info = {
                                "tunnelInfo":{
                                    #"tunnelName":value.name,
                                    "tunnelStatus":'DOWN',
                                    "tunnelHopNum":0,
                                    "tunnelDelay":0,
                                    "tunnelStrict":value.standby_path.strict_result
                                }
                            }                            
                    elif b4_path == 1:
                        if b4_active == "primary":
                            if value.primary_path.path_status == 'UP':
                                b4_pri_path_info = {
                                    "tunnelInfo":{
                                        "tunnelName":value.name,
                                        "tunnelStatus":value.primary_path.path_status,
                                        "tunnelHopNum":value.primary_path.hop_num,
                                        "tunnelDelay":value.primary_path.delay,
                                        "tunnelStrict":value.primary_path.strict_result
                                    },
                                    "tunnelPathNum":value.path_num,
                                    "tunnelPath":value.primary_path.path
                                }
                            else:
                                b4_pri_path_info = {
                                    "tunnelInfo":{
                                        #"tunnelName":value.name,
                                        "tunnelStatus":'DOWN',
                                        "tunnelHopNum":0,
                                        "tunnelDelay":0,
                                        "tunnelStrict":value.primary_path.strict_result
                                    }
                                }

                            b4_std_path_info = {
                                "tunnelInfo":{
                                    "tunnelStatus":'DOWN',
                                    "tunnelHopNum":0,
                                    "tunnelDelay":0,
                                    "tunnelStrict":value.standby_path.strict_result
                                }
                            }
                        elif b4_active == "standby":
                            if value.standby_path.path_status == 'UP':
                                b4_std_path_info = {
                                    "tunnelInfo":{
                                        "tunnelName":value.name,
                                        "tunnelStatus":value.standby_path.path_status,
                                        "tunnelHopNum":value.standby_path.hop_num,
                                        "tunnelDelay":value.standby_path.delay,
                                        "tunnelStrict":value.standby_path.strict_result
                                    },
                                    "tunnelPathNum":value.path_num,
                                    "tunnelPath":value.standby_path.path
                                }
                            else:
                                b4_std_path_info = {
                                    "tunnelInfo":{
                                        #"tunnelName":value.name,
                                        "tunnelStatus":'DOWN',
                                        "tunnelHopNum":0,
                                        "tunnelDelay":0,
                                        "tunnelStrict":value.standby_path.strict_result
                                    }
                                }

                            b4_pri_path_info = {
                                "tunnelInfo":{
                                    "tunnelStatus":'DOWN',
                                    "tunnelHopNum":0,
                                    "tunnelDelay":0,
                                    "tunnelStrict":value.primary_path.strict_result
                                }
                            }
                    else:
                        b4_pri_path_info = {
                            "tunnelInfo":{
                                "tunnelStatus":'DOWN',
                                "tunnelHopNum":0,
                                "tunnelDelay":0,
                                "tunnelStrict":value.primary_path.strict_result
                            }
                        }
                        b4_std_path_info = {
                                "tunnelInfo":{
                                    "tunnelStatus":'DOWN',
                                    "tunnelHopNum":0,
                                    "tunnelDelay":0,
                                    "tunnelStrict":value.standby_path.strict_result
                                }
                            }
            if time_start in g_tunrec.sim_aftuns.keys():
                tun_step = g_tunrec.sim_aftuns[time_start]
                if tun_id in tun_step:
                    value2 = tun_step[tun_id]
                    # 故障后主路径信息
                    af_path = value2.path_num
                    af_active = value2.active_path
                    if af_path == 2:
                        if value2.primary_path.path_status == 'UP':
                            af_pri_path_info = {
                                "tunnelInfo":{
                                    "tunnelName":value2.name,
                                    "tunnelStatus":value2.primary_path.path_status,
                                    "tunnelHopNum":value2.primary_path.hop_num,
                                    "tunnelDelay":value2.primary_path.delay,
                                    "tunnelStrict":value2.primary_path.strict_result
                                },
                                "tunnelPathNum":value2.path_num,
                                "tunnelPath":value2.primary_path.path
                            }           
                        else:
                            af_pri_path_info = {
                                "tunnelInfo":{
                                    "tunnelStatus":'DOWN',
                                    "tunnelHopNum":0,
                                    "tunnelDelay":0,
                                    "tunnelStrict":value2.primary_path.strict_result
                                }
                            }
                        if value2.standby_path.path_status == 'UP':
                            # 故障后备路径信息
                            af_std_path_info = {
                                "tunnelInfo":{
                                    "tunnelName":value2.name,
                                    "tunnelStatus":value2.standby_path.path_status,
                                    "tunnelHopNum":value2.standby_path.hop_num,
                                    "tunnelDelay":value2.standby_path.delay,
                                    "tunnelStrict":value2.standby_path.strict_result
                                },
                                "tunnelPathNum":value2.path_num,
                                "tunnelPath":value2.standby_path.path
                            }
                        else:
                            af_std_path_info = {
                                "tunnelInfo":{
                                    "tunnelStatus":'DOWN',
                                    "tunnelHopNum":0,
                                    "tunnelDelay":0,
                                    "tunnelStrict":value2.standby_path.strict_result
                                }
                            }
                    elif af_path == 1:   
                        if af_active == "primary":
                            af_pri_path_info = {
                                "tunnelInfo":{
                                    "tunnelName":value2.name,
                                    "tunnelStatus":value2.primary_path.path_status,
                                    "tunnelHopNum":value2.primary_path.hop_num,
                                    "tunnelDelay":value2.primary_path.delay,
                                    "tunnelStrict":value2.primary_path.strict_result
                                },
                                "tunnelPathNum":value2.path_num,
                                "tunnelPath":value2.primary_path.path
                            } 
                            af_std_path_info = {
                            "tunnelInfo":{
                                "tunnelStatus":'DOWN',
                                "tunnelHopNum":0,
                                "tunnelDelay":0,
                                "tunnelStrict":value2.standby_path.strict_result
                            }
                        }          
                        elif af_active == "standby":
                            af_std_path_info = {
                                "tunnelInfo":{
                                    "tunnelName":value2.name,
                                    "tunnelStatus":value2.standby_path.path_status,
                                    "tunnelHopNum":value2.standby_path.hop_num,
                                    "tunnelDelay":value2.standby_path.delay,
                                    "tunnelStrict":value2.standby_path.strict_result
                                },
                                "tunnelPathNum":value2.path_num,
                                "tunnelPath":value2.standby_path.path
                            }
                            af_pri_path_info = {
                                "tunnelInfo":{
                                    "tunnelStatus":'DOWN',
                                    "tunnelHopNum":0,
                                    "tunnelDelay":0,
                                    "tunnelStrict":value2.primary_path.strict_result
                                }
                            } 
                    else:
                        af_pri_path_info = {
                            "tunnelInfo":{
                                "tunnelStatus":'DOWN',
                                "tunnelHopNum":0,
                                "tunnelDelay":0,
                                "tunnelStrict":value2.primary_path.strict_result
                            }
                        } 
                        af_std_path_info = {
                            "tunnelInfo":{
                                "tunnelStatus":'DOWN',
                                "tunnelHopNum":0,
                                "tunnelDelay":0,
                                "tunnelStrict":value2.standby_path.strict_result
                            }
                        }

            if value.primary_path.path_status == 'UP' and value2.primary_path.path_status == 'UP':
                hopNumShow = str(value.primary_path.hop_num) + '->' + str(value2.primary_path.hop_num)
                delayShow = str(value.primary_path.delay) + '->' + str(value2.primary_path.delay)
            elif value.primary_path.path_status == 'DOWN' and value2.primary_path.path_status == 'UP':
                hopNumShow = '0' + '->' + str(value2.primary_path.hop_num)
                delayShow = '0' + '->' + str(value2.primary_path.delay)
            elif value.primary_path.path_status == 'UP' and value2.primary_path.path_status == 'DOWN':
                hopNumShow = str(value.primary_path.hop_num) + '->' + '0'
                delayShow = str(value.primary_path.delay) + '->' + '0'
            elif value.primary_path.path_status == 'DOWN' and value2.primary_path.path_status == 'DOWN':
                hopNumShow = '0' + '->' + '0'
                delayShow = '0' + '->' + '0'
            
            tun_status = 'Unchange'
            if time_start in g_tunrec.unchange_tuns:
                if tun_id in g_tunrec.unchange_tuns[time_start]:
                    tun_status = 'Unchange'

            if time_start in g_tunrec.interrupt_tuns:
                if tun_id in g_tunrec.interrupt_tuns[time_start]:   
                    tun_status = 'Interrupt'

            if time_start in g_tunrec.change_tuns:
                if tun_id in g_tunrec.change_tuns[time_start]:   
                    tun_status = 'Change'
            # 暂时固定为 SR-TE，因为当前只有一种类型
            tun_type = 'SR-TE'
            
            if pathNum == 1:
                tunnel = {
                    "assetName"	: value.node_name,
                    "pathNum": pathNum,
                    "businseeName"	: value.business_name, 
                    "tunnelName": value.name,
                    "tunnelId": tun_id,
                    "SIP" : value.src_ip,
                    "DIP" : value.des_ip,
                    "tunnelType" : tun_type,
                    "failReason" : "N/A",
                    "hopNum": hopNumShow, # 主路径的变化
                    "dalay" : delayShow,
                    "tunnelsStatus" : tun_status,
                    "pathInfo":{
                        "beforeFault":
                        {
                            "primary":b4_pri_path_info
                        },
                        "afterFault":
                        {
                            "primary":af_pri_path_info
                        }
                    }
                }
                tunnels_list.append(tunnel)
            else:
                tunnel = {
                    "assetName"	: value.node_name,
                    "pathNum": pathNum,
                    "businseeName"	: value.business_name, 
                    "tunnelName": value.name,
                    "tunnelId": tun_id,
                    "SIP" : value.src_ip,
                    "DIP" : value.des_ip,
                    "tunnelType" : tun_type,
                    "failReason" : "N/A",
                    "hopNum": hopNumShow, # 主路径的变化
                    "dalay" : delayShow,
                    "tunnelsStatus" : tun_status,
                    "pathInfo":{
                        "beforeFault":
                        {
                            "primary":b4_pri_path_info,
                            "standby":b4_std_path_info
                        },
                        "afterFault":
                        {
                            "primary":af_pri_path_info,
                            "standby":af_std_path_info
                        }
                    }
                }
                tunnels_list.append(tunnel)                
        
        data = {
            "tunnelNum": len(tunnels_list),
            "tunnels":tunnels_list
        }
    except Exception as e:
        print("get_tunnels_info Exception:", e)
        data = {
            "tunnelNum": 0,
            "tunnels":[]
        }
        info_logger.error(e)
        error_logger.error(e)
    return ret, data

def get_te_name_list(curTime, anlyseStep):
    try:
        nameList = []
        node_list = []
        start_time, _ = get_start_end_time(curTime)
        # 查找有Tunnel并且以其为始发点的node
        if anlyseStep == 'before':       
            if start_time in g_tunrec.sim_b4tuns.keys():
                tun_step = g_tunrec.sim_b4tuns[start_time]
                for _,value in tun_step.items():
                    if value.src_id not in node_list:
                        node_list.append(value.src_id)
                        pod = {
                            "name":value.node_name,
                            "nodeId":value.src_id,
                        }
                        nameList.append(pod)
        else:
            if start_time in g_tunrec.sim_aftuns.keys(): 
                tun_step = g_tunrec.sim_aftuns[start_time]
                for _,value in tun_step.items():
                    if value.src_id not in node_list:
                        node_list.append(value.src_id)
                        pod = {
                            "name":value.node_name,
                            "nodeId":value.src_id,
                        }
                        nameList.append(pod)
        data = {
            "nameNum":len(nameList),
            "nameList":nameList
        }
        return data
    except Exception as e:
        print("get_te_name_list Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        data = {
            "nameNum":0,
            "nameList":[]
        }
        return data

def get_te_path_info(curTime, anlyseStep, nodeId):

    try:
        tunnels_list = []
        desId_list = []
        start_time, _ = get_start_end_time(curTime)
        if anlyseStep == 'before':
            if start_time in g_tunrec.sim_b4tuns.keys():
                tun_step = g_tunrec.sim_b4tuns[start_time]
                for key,value in tun_step.items():
                    # 同一个起始终止节点，只显示一条路径
                    if nodeId != value.src_id or value.des_id in desId_list:
                        continue

                    src_id = value.src_id
                    des_id = value.des_id
                    desId_list.append(des_id)
                    # 找到起始节点对应的
                    tun_num = 0 
                    for value2 in tun_step.values():
                        if src_id == value2.src_id and des_id == value2.des_id:
                            tun_num += 1
                    tunnel = {
                        "totolTunnelNum": tun_num,
                        "stratNodeId":src_id,	   #起点
                        "endNodeId":des_id,	   #终点
                        "showId":key, 
                    } 
                    tunnels_list.append(tunnel)

        else:
            if start_time in g_tunrec.sim_aftuns.keys():                   
                tun_step = g_tunrec.sim_aftuns[start_time]
                for key,value in tun_step.items():
                    # 同一个起始终止节点，只显示一条路径
                    if nodeId != value.src_id or value.des_id in desId_list:
                        continue

                    src_id = value.src_id
                    des_id = value.des_id
                    desId_list.append(des_id)
                    # 找到起始节点对应的
                    tun_num = 0 
                    for value2 in tun_step.values():
                        if src_id == value2.src_id and des_id == value2.des_id:
                            tun_num += 1

                    tunnel = {
                        "totolTunnelNum": tun_num,
                        "stratNodeId":src_id,	   #起点
                        "endNodeId":des_id,	    #终点
                        "showId":key, 
                    } 
                    tunnels_list.append(tunnel)

        data = {
            "tunnelList":tunnels_list
        }

        return data
    except Exception as e:
        print("get_te_path_info Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return None


def get_all_te_path(cur_time, anlyseStep, showId):

    try:
        tunnels_list = []
        start_time, _ = get_start_end_time(cur_time)
        if anlyseStep == 'before':
            if start_time in g_tunrec.sim_b4tuns.keys():
                tun_step = g_tunrec.sim_b4tuns[start_time]
                if showId in tun_step.keys(): 
                    sid = tun_step[showId].src_id
                    did = tun_step[showId].des_id
                else:
                    data = {
                        "tunnelNum": 0,
                        "tunnels":[]
                    }
                    return data
                for key,value in tun_step.items(): 
                    #找出起始点和终点相同的Tunnel
                    if value.src_id == sid and value.des_id == did:    
                        if value.active_path == "primary":
                            delay = value.primary_path.delay
                        else:
                            delay = value.standby_path.delay
                            
                        tunnel = {
                            "tunnelName":value.name,    #名称需要在topo上显示出来
                            "stratNodeId":value.src_id,	#起点
                            "endNodeId":value.des_id,	#终点
                            "tunnelId":key, 
                            "delay":delay
                        }
                        tunnels_list.append(tunnel)
        else:
            if start_time in g_tunrec.sim_b4tuns.keys():
                tun_step = g_tunrec.sim_aftuns[start_time]
                if showId in tun_step.keys(): 
                    sid = tun_step[showId].src_id
                    did = tun_step[showId].des_id
                else:
                    data = {
                        "tunnelNum": 0,
                        "tunnels":[]
                    }
                    return data
                for key,value in tun_step.items(): 
                    #找出起始点和终点相同的Tunnel
                    if value.src_id == sid and value.des_id == did:    
                        if value.active_path == "primary":
                            delay = value.primary_path.delay
                        else:
                            delay = value.standby_path.delay
                        tunnel = {
                            "tunnelName":value.name,    #名称需要在topo上显示出来
                            "stratNodeId":value.src_id,	#起点
                            "endNodeId":value.des_id,	#终点
                            "tunnelId":key, 
                            "delay":delay
                        }
                        tunnels_list.append(tunnel)
        data = {
            "tunnelNum": len(tunnels_list),
            "tunnels":tunnels_list
        }
        ret = ErrCode.SUCCESS
        return ret,data

    except Exception as e:
        print("get_all_te_path Exception:", e)
        data = {
            "tunnelNum": 0,
            "tunnels":[]
        }
        ret = ErrCode.FAILED

        return ret,data

def get_port_type(out_interface):
    """将出接口转化成出接口类型，比如GigabitEthernet4/0转换成GigabitEthernet
    
    Args:
        出接口
    Returns:
        出接口类型
    Raise:
        none
    """
    try:
        #楼上环境ifdesc是GigabitEthernet4/0类型的，长度是18，楼下是GigabitEthernet3/2/2类型的，
        # 长度是20，所以小于19是楼上环境的，大于19是楼下环境的
        # if len(out_interface) < 19: 
        #     return out_interface[:-3]
        # else:
        #     return out_interface[:-5]
        outPortType = str(out_interface.split('net', -1)[0]) + 'net'
        return outPortType

    except Exception as e:
        print("get_port_type Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return "N/A"      

#5.2.3	选择某条TE,进行查看
def get_select_te_info(cur_time, anlyseStep, tunnelId):

    ret = ErrCode.SUCCESS
    try:
        start_time, _ = get_start_end_time(cur_time)
        if anlyseStep == 'before':
            # before 的内容
            if start_time in g_tunrec.sim_b4tuns.keys():
                tun_step = g_tunrec.sim_b4tuns[start_time]
                if tunnelId not in tun_step.keys():
                    info_logger.error("tunnelId: %s not in bt_tuns"%(tunnelId))
                
                value = tun_step[tunnelId]  
                flowgroup_info = g_sdnply.flowgroup[value.flowgroup_id]
                pathNum = flowgroup_info.pathNum
                pri_include = flowgroup_info.phyIncludeNodeAndLink["primary"]
                pri_exclude = flowgroup_info.phyExcludeNodeAndLink["primary"]
                std_include = flowgroup_info.phyIncludeNodeAndLink["standby"]
                std_exclude = flowgroup_info.phyExcludeNodeAndLink["standby"]

                teName = tun_step[tunnelId].name
                if tun_step[tunnelId].status == 'UP':
                    isReach = "Reachable"
                    jumpCnt = tun_step[tunnelId].primary_path.hop_num
                    pri_strict = tun_step[tunnelId].primary_path.strict_result
                else:
                    isReach = "Unreachable"
                    jumpCnt = 0
                    pri_strict = tun_step[tunnelId].primary_path.strict_result
                
                # 主
                if tun_step[tunnelId].status == 'UP' and tun_step[tunnelId].primary_path.path_status == 'UP':
                    pri_tunnel_hops = tun_step[tunnelId].primary_path.hops
                    pri_jump = tun_step[tunnelId].primary_path.hop_num
                    pri_tunnelPath = tun_step[tunnelId].primary_path.path
                else:
                    pri_tunnelPath = []
                    pri_jump = 0
                    pri_tunnel_hops = []
                pri_tunnelPathNum = len(pri_tunnel_hops)
                pri_tunnelNodeInfo = []
                pri_igp_cost = 0
                jumpId = 0

                # 路径可达时，才进行路径信息收集
                for path in pri_tunnelPath:
                    # 找到链路中的cost
                    portCosts = 0
                    nodeid1 = path['start_node_id']
                    nodeid2 = path['end_node_id']
                    for _,value in g_sim.topo.links.items():
                        if value.nodeid1==nodeid1 and value.nodeid2==nodeid2:
                            portCosts=value.ifdesc1cost 
                            break
                        if value.nodeid1==nodeid2 and value.nodeid2==nodeid1:
                            portCosts=value.ifdesc2cost 
                            break

                    hop = pri_tunnel_hops[nodeid1]
                    out_port_type = get_port_type(hop.out_interface)
                    info = {
                        "jumpId":jumpId,	            #跳数编号
                        "netEleType":'Router', 	            #网元类型
                        "netEleName":hop.node_name, 	            #网元名称
                        "outPortName":hop.out_interface,	#出接口名称  
                        "outPortType":out_port_type,	#出接口类型
                        "outPortCost":portCosts,	  #出接口cost
                        "tunnelType":"Auto"
                    } 
                    jumpId += 1
                    pri_igp_cost += portCosts
                    pri_tunnelNodeInfo.append(info)

                # 路径不为空的时候，才需要把最后一个结束点的信息填上。
                if len(pri_tunnelPath) != 0:
                    last_node = pri_tunnelPath[-1]['end_node_id']
                    hop = pri_tunnel_hops[last_node]  
                    info = {
                        "jumpId":jumpId,	            #跳数编号
                        "netEleType":'Router', 	            #网元类型
                        "netEleName":hop.node_name, 	            #网元名称
                        "outPortName":"N/A",	#出接口名称  
                        "outPortType":"N/A",	#出接口类型
                        "outPortCost":"N/A",	  #出接口cost
                        "tunnelType":"Auto"
                    } 
                    jumpId += 1
                    pri_tunnelNodeInfo.append(info)
                        

                # 备
                if tun_step[tunnelId].status == 'UP' and tun_step[tunnelId].standby_path.path_status == 'UP':
                    std_jump = tun_step[tunnelId].standby_path.hop_num
                    std_tunnel_hops = tun_step[tunnelId].standby_path.hops
                    std_tunnelPath = tun_step[tunnelId].standby_path.path
                    std_strict = tun_step[tunnelId].standby_path.strict_result
                else:
                    std_tunnelPath = []
                    std_jump = 0
                    std_tunnel_hops = []
                    std_strict = tun_step[tunnelId].standby_path.strict_result

                std_tunnelPathNum = len(std_tunnel_hops)
                std_tunnelNodeInfo = []
                std_igp_cost = 0
                jumpId = 0

                for path in std_tunnelPath:
                    portCosts = 0
                    nodeid1 = path['start_node_id']
                    nodeid2 = path['end_node_id']
                    for _,value in g_sim.topo.links.items():
                        if value.nodeid1==nodeid1 and value.nodeid2==nodeid2:
                            portCosts=value.ifdesc1cost 
                            break
                        if value.nodeid1==nodeid2 and value.nodeid2==nodeid1:
                            portCosts=value.ifdesc2cost 
                            break
                    hop = std_tunnel_hops[nodeid1]
                    out_port_type = get_port_type(hop.out_interface)
                    info = {
                        "jumpId":jumpId,	            #跳数编号
                        "netEleType":'Router', 	            #网元类型
                        "netEleName":hop.node_name, 	            #网元名称
                        "outPortName":hop.out_interface,	#出接口名称  
                        "outPortType":out_port_type,	#出接口类型
                        "outPortCost":portCosts,	  #出接口cost
                        "tunnelType":"Auto"
                    } 
                    jumpId += 1
                    std_igp_cost += portCosts
                    std_tunnelNodeInfo.append(info)

                # 路径不为空的时候，才需要把最后一个结束点的信息填上。
                if len(std_tunnelPath) != 0:
                    last_node = std_tunnelPath[-1]['end_node_id']
                    hop = std_tunnel_hops[last_node] 
                    info = {
                        "jumpId":jumpId,	            #跳数编号
                        "netEleType":'Router', 	            #网元类型
                        "netEleName":hop.node_name, 	            #网元名称
                        "outPortName":"N/A",	#出接口名称  
                        "outPortType":"N/A",	#出接口类型
                        "outPortCost":"N/A",	  #出接口cost
                        "tunnelType":"Auto"
                    } 
                    jumpId += 1
                    std_tunnelNodeInfo.append(info)

        else:
            # after 的内容
            if start_time in g_tunrec.sim_aftuns.keys():
                tun_step = g_tunrec.sim_aftuns[start_time]
                teName = tun_step[tunnelId].name
                value = tun_step[tunnelId]  
                flowgroup_info = g_sdnply.flowgroup[value.flowgroup_id]
                pathNum = flowgroup_info.pathNum

                pri_include = flowgroup_info.phyIncludeNodeAndLink["primary"]
                pri_exclude = flowgroup_info.phyExcludeNodeAndLink["primary"]
                std_include = flowgroup_info.phyIncludeNodeAndLink["standby"]
                std_exclude = flowgroup_info.phyExcludeNodeAndLink["standby"]

                if tun_step[tunnelId].status == 'UP':
                    isReach = "Reachable"
                    jumpCnt = tun_step[tunnelId].primary_path.hop_num
                    pri_strict = tun_step[tunnelId].primary_path.strict_result
                else:
                    isReach = "Unreachable"
                    jumpCnt = 0
                    pri_strict = tun_step[tunnelId].primary_path.strict_result
                
                # 主
                if tun_step[tunnelId].status == 'UP' and tun_step[tunnelId].primary_path.path_status == 'UP':
                    pri_tunnel_hops = tun_step[tunnelId].primary_path.hops
                    pri_jump = tun_step[tunnelId].primary_path.hop_num
                    pri_tunnelPath = tun_step[tunnelId].primary_path.path
                else:
                    pri_tunnelPath = []
                    pri_jump = 0
                    pri_tunnel_hops = []
                pri_tunnelPathNum = len(pri_tunnelPath)
                pri_tunnelNodeInfo = []
                pri_igp_cost = 0
                jumpId = 0
                for path in pri_tunnelPath:
                    # 找到链路中的cost
                    portCosts = 0
                    nodeid1 = path['start_node_id']
                    nodeid2 = path['end_node_id']
                    for _,value in g_sim.topo.links.items():
                        if value.nodeid1==nodeid1 and value.nodeid2==nodeid2:
                            portCosts=value.ifdesc1cost 
                            break
                        if value.nodeid1==nodeid2 and value.nodeid2==nodeid1:
                            portCosts=value.ifdesc2cost 
                            break
                    hop = pri_tunnel_hops[nodeid1]
                    out_port_type = get_port_type(hop.out_interface)
                    info = {
                        "jumpId":jumpId,	            #跳数编号
                        "netEleType":'Router', 	            #网元类型
                        "netEleName":hop.node_name, 	            #网元名称
                        "outPortName":hop.out_interface,	#出接口名称  
                        "outPortType":out_port_type,	#出接口类型
                        "outPortCost":portCosts,	  #出接口cost
                        "tunnelType":"Auto"
                    } 
                    jumpId += 1
                    pri_igp_cost += portCosts
                    pri_tunnelNodeInfo.append(info)

                # 路径不为空的时候，才需要把最后一个结束点的信息填上。
                if len(pri_tunnelPath) != 0:
                    last_node = pri_tunnelPath[-1]['end_node_id']
                    hop = pri_tunnel_hops[last_node] 
                    info = {
                        "jumpId":jumpId,	            #跳数编号
                        "netEleType":'Router', 	            #网元类型
                        "netEleName":hop.node_name, 	            #网元名称
                        "outPortName":"N/A",	#出接口名称  
                        "outPortType":"N/A",	#出接口类型
                        "outPortCost":"N/A",	  #出接口cost
                        "tunnelType":"Auto"
                    } 
                    jumpId += 1
                    pri_tunnelNodeInfo.append(info)


                # 备
                if tun_step[tunnelId].status == 'UP' and tun_step[tunnelId].standby_path.path_status == 'UP':
                    std_jump = tun_step[tunnelId].standby_path.hop_num
                    std_tunnel_hops = tun_step[tunnelId].standby_path.hops
                    std_tunnelPath = tun_step[tunnelId].standby_path.path
                    std_strict = tun_step[tunnelId].standby_path.strict_result
                else:
                    std_tunnelPath = []
                    std_jump = 0
                    std_tunnel_hops =[]
                    std_strict = tun_step[tunnelId].standby_path.strict_result

                std_tunnelPathNum = len(std_tunnelPath)
                std_tunnelNodeInfo = []
                std_igp_cost = 0
                jumpId = 0
                for path in std_tunnelPath:
                    # 找到链路中的cost
                    portCosts = 0
                    nodeid1 = path['start_node_id']
                    nodeid2 = path['end_node_id']
                    for _,value in g_sim.topo.links.items():
                        if value.nodeid1==nodeid1 and value.nodeid2==nodeid2:
                            portCosts=value.ifdesc1cost 
                            break
                        if value.nodeid1==nodeid2 and value.nodeid2==nodeid1:
                            portCosts=value.ifdesc2cost 
                            break
                    hop = std_tunnel_hops[nodeid1]
                    out_port_type = get_port_type(hop.out_interface)
                    info = {
                        "jumpId":jumpId,	            #跳数编号
                        "netEleType":'Router', 	            #网元类型
                        "netEleName":hop.node_name, 	            #网元名称
                        "outPortName":hop.out_interface,	#出接口名称  
                        "outPortType":out_port_type,	#出接口类型
                        "outPortCost":portCosts,	  #出接口cost
                        "tunnelType":"Auto"
                    } 
                    jumpId += 1
                    std_igp_cost += portCosts
                    std_tunnelNodeInfo.append(info)

                # 路径不为空的时候，才需要把最后一个结束点的信息填上。
                if len(std_tunnelPath) != 0:
                    last_node = std_tunnelPath[-1]['end_node_id']
                    hop = std_tunnel_hops[last_node] 
                    info = {
                        "jumpId":jumpId,	            #跳数编号
                        "netEleType":'Router', 	            #网元类型
                        "netEleName":hop.node_name, 	            #网元名称
                        "outPortName":"N/A",	#出接口名称  
                        "outPortType":"N/A",	#出接口类型
                        "outPortCost":"N/A",	  #出接口cost
                        "tunnelType":"Auto"
                    } 
                    jumpId += 1
                    std_tunnelNodeInfo.append(info)
        if pathNum == 1:
            data = {
                        # 下侧信息
                        "selectFlowInfo":[
                            {
                                "teName":teName,
                                "pathNum":pathNum,
                                "isReach":isReach, 	
                                "jumpCnt":jumpCnt,	 # 主路径跳数
                                "type":"SR-TE"       # 显示SR-TE
                            } 
                        ],
                        # 右侧表格 
                        "primary":{
                            "totalJump":pri_jump,	#总跳数
                            "tunnelInfo":"N/A",	#承载方式 
                            "IGP PATH COST":pri_igp_cost,
                            "tunnelNodeInfo":pri_tunnelNodeInfo,
                            "tunnelPathNum":pri_tunnelPathNum,
                            # 上面路径信息
                            "tunnelPath":pri_tunnelPath,
                            "tunnelStrict":pri_strict,
                            "include":pri_include,
                            "exclude":pri_exclude
                        }
            }
        else:
            data = {
                        # 下侧信息
                        "selectFlowInfo":[
                            {
                                "teName":teName,
                                "pathNum":pathNum,
                                "isReach":isReach, 	
                                "jumpCnt":jumpCnt,	 # 主路径跳数
                                "type":"SR-TE"       # 显示SR-TE
                            } 
                        ],
                        # 右侧表格 
                        "primary":{
                            "totalJump":pri_jump,	#总跳数
                            "tunnelInfo":"N/A",	#承载方式 
                            "IGP PATH COST":pri_igp_cost,
                            "tunnelNodeInfo":pri_tunnelNodeInfo,
                            "tunnelPathNum":pri_tunnelPathNum,
                            # 上面路径信息
                            "tunnelPath":pri_tunnelPath,
                            "tunnelStrict":pri_strict,
                            "include":pri_include,
                            "exclude":pri_exclude
                        },
                        "standby":{
                            "totalJump":std_jump,	#总跳数
                            "tunnelInfo":"N/A",	#承载方式 
                            "IGP PATH COST":std_igp_cost,
                            "tunnelNodeInfo":std_tunnelNodeInfo,
                            "tunnelPathNum":std_tunnelPathNum,
                            # 上面路径信息
                            "tunnelPath":std_tunnelPath,
                            "tunnelStrict":std_strict,
                            "include":std_include,
                            "exclude":std_exclude
                        }
            }
    except Exception as e:
        print("get_select_te_info Exception:", e)
        info_logger.error(e)
        error_logger.error(e)

        return ErrCode.FAILED, None       
  
    return ret, data

def from_out_interface_to_interface_type(out_interface):
    """将出接口转化为出接口类型
    
    Args:
        出接口
    Returns:
        出接口类型
    Raise:
        none
    """
    try:
        if (out_interface[0] == "g"):
            out_interface.replace("g","GigabitEthernet")
        elif (out_interface[0] == 'e'):
            out_interface.replace("e","ETHERNET_INTERFACE")
    except Exception as e:
        print("from_out_interface_to_interface_type Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
