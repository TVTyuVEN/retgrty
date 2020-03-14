# -*- encoding: utf-8 -*-
"""
@File    : simulate.py
@Time    : 2019/06/26 14:28:16
@Author  : leijuyan 11389
@License : Copyright (c) 2004-2019 New H3C Tech. Co., Ltd. All rights reserved.
@Desc    : 仿真流程控制
"""
import math
import threading
import copy
import time
import ctypes
import inspect
from functools import reduce
from flask import request
from datetime import datetime

from apps.errcode import ErrCode
from apps.util import g_dt, g_sim, g_allFlows, g_ana, g_tunrec
from apps.util import SIMLATAE_STATE_LOCK
from apps.util import get_current_time_str, get_start_end_time, get_end_time
from apps.util import error_logger,info_logger 
from apps.util import generate_uuid

from apps.v1_0.topo import Topo, L3Topo
from apps.v1_0.bginterface import get_link_load_data_from_bigdata
from apps.v1_0.flow import FlowObj
from apps.v1_0.record import report_xls_in_advance, cal_load_info_by_threshold
from apps.v1_0.routesimulate import built_before_dijkstra_network, built_after_fault_dijkstra_network
from apps.v1_0.language import get_language_setting_index
from apps.v1_0.tunnel import *
from apps.v1_0.sdnsimctrl import *
from apps.v1_0.flowsimulate import *
from apps.v1_0.test import *
from param import *

g_thd_ident = []
class BackGroundDiff():
    def __init__(self, id):
        # 以网元的出接口改变或者负载超过overload则记录,asset_id的值为这个网元的ID
        self.asset_id = id  # 网元ID
        self.asset_name = '' # 网元名称
        self.port_ip_address = 0 # 网元Ip名称
        self.status = ''  #'changed'.'overload'
        self.if_descr = 0 # 网元端口 
        self.net_element_type = 0   # 网元接口类型 （这个需要跟博峰确认一下是不是这个）
        self.band_width = ''  # 带宽
        self.b4_fault_out_use_ratio = 0 # 故障前带宽利用率
        self.after_fault_out_use_ratio = 0 # 故障后带宽利用率

class PeriodBackLoadInfo():
    """某一时间段内故障前故障后的背景流量统计信息
    
    Attributes:
        none
    """
    
    def __init__(self, start_time):
        self.start_time = 0 # 查看的分析时刻点所在的仿真时间片的起始时间
        self.end_time = 0  # 查看的分析时刻点所在的仿真时间片的结束时间

        self.overload_threshold = 0  # 仿真分析，overload的阈值
        self.overload_num = 0  # 当前时间段overload的负载端口个数
        self.overload_percent = 0 # overload_num / (overload_num + changed_num)

        self.changed_num = 0 # 故障前与故障后相比较，带宽利用率有改变的负载的个数

        self.load_info = {} # 故障前后负载有改变或者超过阈值的所有的负载的信息。对应 BackGroundDiff 
    
    def add_load_diff_info(self,id):
        self.load_info[id] = BackGroundDiff(id)

    def clear_load_statis(self):
        """清除所有load 统计信息"""
        self.start_time = 0 # 查看的分析时刻点所在的仿真时间片的起始时间
        self.end_time = 0  # 查看的分析时刻点所在的仿真时间片的结束时间

        self.overload_threshold = 0  # 仿真分析，overload的阈值
        self.overload_num = 0  # 当前时间段overload的负载端口个数
        self.overload_percent = 0 # overload_num / (overload_num + changed_num)

        self.changed_num = 0 # 故障前与故障后相比较，带宽利用率有改变的负载的个数

        self.load_info.clear() # 清空字典里的所有内容

class SimStepStatisAll(object):
    def __init__(self, key):
        self.sim_creat_time = 0  # 仿真创建时间
        self.sim_net_start_time = 0  # 仿真网络的起始时间
        self.cycle = 0  # 周期时长
        self.cycle_num = 0  # 周期个数
        self.flow_data_type = ''   # 流量数据类型
        self.sim_agreement = ''  # 仿真协议
        self.sim_ospf_num = 0   # OSPF协议路由数量
        self.sim_isis_num =0   # ISIS协议路由数量
        self.sim_bgp_num = 0   # BGP协议路由数量
        self.flow_num = 0   # FLOW数量
        self.tunnel_num = 0   # TUNNEL数量
        self.fail_tunnel_num = 0   # 失败的TUNNEL数量
        self.overload_100_link_num = 0   # 利用率超过100%的链路总数
        self.link_max_used_ratio = 0   # 链路最大利用率
        self.whole_net_throughput =0   # 整网吞吐率
        self.whole_net_used_ratio = 0   # 整网利用率
        self.business_flow_num = 0   # 业务流数量
        self.unrouter_business_flow_num = 0   # 不可路由的业务流数量
        self.router_business_flow_num = 0   # 可路由的业务流数量

class SimulateRate(object):
    """仿真进度
    
    Attributes:
        none
    """
    
    def __init__(self):
        self.sim_step = 0

        # 数据加载
        self.sim_data_load_msg_num = 0
        self.sim_data_load_english = []
        self.sim_data_load_chinese = []
        self.sim_org_flow_num = 0

        # 故障前仿真
        self.sim_b4_data_pre_progress = 0
        self.sim_b4_route_sim_progress = 0
        self.sim_b4_flow_sim_progress = 0
        self.sim_b4_isis_num = 0
        self.sim_b4_ospf_num = 0
        self.sim_b4_bgp_num = 0
        self.sim_b4_turnnel_num = 0
        self.sim_b4_flow_num = 0
        self.sim_b4_if_num = 0
 
        # 故障后仿真
        self.sim_after_data_pre_progress = 0
        self.sim_after_route_sim_progress = 0
        self.sim_after_flow_sim_progress = 0
        self.sim_after_isis_num = 0
        self.sim_after_ospf_num = 0
        self.sim_after_bgp_num = 0
        self.sim_after_turnnel_num = 0
        self.sim_after_flow_num = 0
        self.sim_after_if_num = 0
    
    def init_simulate_status(self):
        # 数据加载
        self.sim_data_load_msg_num = 0
        self.sim_data_load_english = []
        self.sim_data_load_chinese = []

        # 故障前仿真
        self.sim_b4_flow_sim_progress = 0
        self.sim_b4_flow_num = 0
 
        # 故障后仿真
        self.sim_after_flow_sim_progress = 0
        self.sim_after_flow_num = 0

sim_rate = SimulateRate()

class SimDataSyncCode:
    """自定义数据同步状态。"""

    SIM_CLEAR_DATA_BEGIN = 1
    SIM_CLERA_DATA_SUCCESS = 2
    SIM_SAVE_TOPO_BEGIN = 3
    SIM_SAVE_TOPO_SUCCESS = 4
    SIM_SYNC_DATA_BEGIN = 5
    SIM_SYNC_DATA_FIFTY = 6
    SIM_SYNC_DATA_FINISH = 7

    SYNC_MSG = {
        SIM_CLEAR_DATA_BEGIN: [{"time":"", "title":"清除数据","info":"开始清除上次仿真的数据"}, {"time":"", "title":"clear data","info":"clear the latest simulate data"}],
        SIM_CLERA_DATA_SUCCESS:[{"time":"", "title":"清除数据","info":"清除成功"},{"time":"", "title":"clear data","info":"success clear"}],
        SIM_SAVE_TOPO_BEGIN:[{"time":"", "title":"保存拓扑和flow","info":"开始保存拓扑和导入的flow信息"}, {"time":"", "title":"save topo","info":"save topo and flow"}],
        SIM_SAVE_TOPO_SUCCESS:[{"time":"", "title":"保存拓扑和flow","info":"保存成功"},{"time":"", "title":"save topo","info":"success saved"}],
        SIM_SYNC_DATA_BEGIN:[{"time":"", "title":"同步数据","info":"开始同步背景数据"}, {"time":"", "title":"data syncing","info":"beging to sync"}],
        SIM_SYNC_DATA_FIFTY:[{"time":"", "title":"同步数据","info":"同步进度50%"},{"time":"", "title":"data syncing","info":"Synchronization progress 50%"}],
        SIM_SYNC_DATA_FINISH:[{"time":"", "title":"同步数据","info":"同步成功"},{"time":"", "title":"data syncing","info":"Synchronization finish"}]
        }

def assemb_data_sim_message(msg_code):
    try:
        cur_time = get_current_time_str()
        ch_detail = SimDataSyncCode.SYNC_MSG[msg_code][0]
        ch_detail["time"] = cur_time
        sim_rate.sim_data_load_chinese.append(ch_detail)
        eg_detail = SimDataSyncCode.SYNC_MSG[msg_code][1]
        eg_detail["time"] = cur_time
        sim_rate.sim_data_load_english.append(eg_detail)
        sim_rate.sim_data_load_msg_num += 1
    except Exception as e:
        print("assemb_data_sim_message Exception:", e)
        error_logger.error(e)
        error_logger.info(e)    

def load_data():
    """数据加载处理,轮询时间段，把背景流量取出来，根据仿真数据设置，解析数据，存储到sim.all_link_payload()里
       然后再deepcopy到sim.after_fault_link_info(), g_sim.before_fault_link_info()里。
       这个时候两份数据是相同的背景流量数据
        
    Args:
        none
    Returns:
        none
    Raise:
        ErrCode.SUCCESS
    """
    try:
        start_time = g_sim.time_start
        end_time = g_sim.time_end
        cycle = g_sim.time_cycle
        cycle_num = int(g_sim.time_cycle_num)

        data = {}
        one_cycle_start = start_time
        one_cycle_end_time = min(start_time + cycle, end_time)
        if cycle_num > 1:
            half_cycle = int(cycle_num / 2)
        else:
            half_cycle = 0

        # 前面n-1次均取一整个周期的数据
        for i in range(cycle_num):
            if g_sim.object_load:
                for linkid in g_sim.topo.links:    
                    data = get_link_load_data_from_bigdata(one_cycle_start, one_cycle_end_time, linkid)
                    if data != None:
                        parse_background_info(one_cycle_start, linkid, data)
                    else:
                        set_background_info_to_fix_value(one_cycle_start, linkid)
            else:
                for linkid in g_sim.topo.links: 
                    set_background_info_to_fix_value(one_cycle_start, linkid)

            # 把这一时间段的背景流量按时间切片的方式保存    
            sim_end_time = get_end_time(one_cycle_start)
            if one_cycle_end_time != sim_end_time:
                copy_all_linkd_background_flow(one_cycle_start, sim_end_time, one_cycle_end_time)

            one_cycle_start = one_cycle_end_time
            one_cycle_end_time = min(one_cycle_start + cycle, end_time)

            if i == half_cycle:
                assemb_data_sim_message(SimDataSyncCode.SIM_SYNC_DATA_FIFTY)
       
        return ErrCode.SUCCESS
    except Exception as e:
        print("load_data Exception:", e)
        error_logger.error(e)
        error_logger.info(e)
        return ErrCode.FAILED


# sprint 3 add
def load_sim_before_payload():
    try:
        """ 增量仿真前的背景流量和tunnel流量直接从上次仿真的故障后直接copy，同时把导入的流量清理掉(因为导入的流量前后可能不一致，需要计算一遍)
            sprint4 连导入的流都是一样的，不把流清除
        Args:
            none
        Returns:
            none
        Raise:
            none
        """
        g_sim.before_fault_link_info = copy.deepcopy(g_sim.after_fault_link_info)

        # 把导入的flow清除掉。
        for s_time in g_sim.before_fault_link_info.keys():
            period_link = g_sim.before_fault_link_info[s_time] 
            for linkid in period_link.link_info.keys():
                linkInfo = period_link.link_info[linkid]
                linkInfo.a_to_b.flow_speed = 0
                linkInfo.a_to_b.add_flow_id.clear()
                linkInfo.b_to_a.flow_speed = 0
                linkInfo.b_to_a.add_flow_id.clear()  
    except Exception as e:
        print("load_sim_before_payload Exception:", e)
        error_logger.error(e)
        error_logger.info(e)

def get_neighbour_node(node_id, node_port):
    try:
        """根据节点的ID和节点的端口，找到跟他相连接的节点和端口
        
        Args:
            node_id：节点的ID
            node_port:port口
        Returns:
            neighbour_id: 邻居节点id
            neighbour_port：邻居节点ifindex
        Raise:
            none
        """    
        neighbour_id = '0'
        neighbour_port = 0
        for _,value in g_sim.topo.links.items():
            if value.ifindex1 == node_port and value.nodeid1 == node_id:
                neighbour_id = value.nodeid2
                neighbour_port = value.ifindex2
                break
            elif value.ifindex2 == node_port and value.nodeid2 == node_id:
                neighbour_id = value.nodeid1
                neighbour_port = value.ifindex1
                break
        return neighbour_id, neighbour_port
    except Exception as e:
        print("get_neighbour_node Exception:", e)
        error_logger.error(e)
        error_logger.info(e)
        return None, None

def get_node_mgrip(node_id):
    try:
        node_value = g_sim.topo.nodes[node_id]
        return node_value.mgrip
    except Exception as e:
        print("get_node_mgrip Exception:", e)
        error_logger.error(e)
        error_logger.info(e)
        return None


def save_sim_parm(input_data):
    try:
        if isinstance(input_data, dict):
            simu_type_dict = input_data['simType']

            if simu_type_dict['routeSim'] == 1:
                g_sim.type_route = True
            else:
                g_sim.type_route = False

            if simu_type_dict['flowSim'] == 1:
                g_sim.type_flow = True
            else:
                g_sim.type_flow = False
            
            if simu_type_dict['faultSim'] == 1:
                g_sim.type_fault = True
            else:
                g_sim.type_fault = False

            simu_obj_dict = input_data['simObj']
            if simu_obj_dict['load'] == 1:
                g_sim.object_load = True   # 负载
            else:
                g_sim.object_load = False

            if simu_obj_dict['tunnelFlow'] == 1:
                g_sim.object_tunnel_flow = True    # 基于TUNNEL 创建的流量
            else:
                g_sim.object_tunnel_flow = False

            if simu_obj_dict['inputFlow'] == 1:
                g_sim.object_input_flow = True    # 导入的流量 
            else:
                g_sim.object_input_flow = False
            
            data_manner_dict = input_data['dataManner']
            if data_manner_dict['everager'] == 1:
                g_sim.data_manner = 1
            elif data_manner_dict['peak'] == 1:
                g_sim.data_manner = 2
            else:
                g_sim.data_manner = 3

            agree_dict = input_data['agreement']
            if agree_dict['bgp'] == 1:
                g_sim.agree_bgp = True
            else:
                g_sim.agree_bgp = False

            if agree_dict['isis'] == 1:
                g_sim.agree_isis = True
            else:
                g_sim.agree_isis = False

            if agree_dict['ospf'] == 1:
                g_sim.agree_ospf = True
            else:
                g_sim.agree_ospf = False

            if agree_dict['mpls'] == 1:
                g_sim.agree_mpls = True
            else:
                g_sim.agree_mpls = False

            # 隧道优化参数记录
            if agree_dict['tunnelOptimize'] == 1:
                g_sim.tunnel_optimize = True
            else:
                g_sim.tunnel_optimize = False
            
            time_dict = input_data['simTime']
            g_sim.time_cycle = time_dict['duration'] # 仿真的时间周期，单位是毫秒（为了计算方便）
            
            g_sim.time_start = time_dict['timeBegin'] # 仿真的开始时间,毫秒时间戳
            g_sim.time_end = time_dict['timeEnd'] # 仿真的结束时间,毫秒时间戳
    except Exception as e:
        print("save_sim_parm Exception:", e)
        error_logger.error(e)
        error_logger.info(e)
   
############################################
# 故障前仿真
############################################
def cal_b4_fault_links_use_ratio():
    """计算故障前，各个时间段内，所有端口的带宽利用率
    
    Args:
        none
    Returns:
        none
    Raise:
        none
    """  
    try:
        for _, value in g_sim.before_fault_link_info.items():
            all_link_info = value.link_info
            # 轮询各个时刻下的所有的链路
            for linkid in all_link_info:
                one_link_info = all_link_info[linkid]
                a_b = one_link_info.a_to_b
                a_b.speed = a_b.back_speed + a_b.te_speed + a_b.flow_speed + a_b.flow_tun_speed  
                a_b.out_use_ratio = round(((100 * a_b.speed) / (a_b.band_width)), 2)
                
                b_a = one_link_info.b_to_a
                b_a.speed = b_a.back_speed + b_a.te_speed + b_a.flow_speed + b_a.flow_tun_speed 
                b_a.out_use_ratio = round(((100 * b_a.speed) / (b_a.band_width)), 2)
    except Exception as e:
        print("cal_b4_fault_links_use_ratio Exception:", e)
        error_logger.error(e)
        error_logger.info(e)


def before_fault_simulate():
    try:
        """ sprint 4 故障前仿真

        Args:
            none
        Returns:
            none
        Raise:
            none
        """
        # 如果是继承仿真，则把上次仿真的背景流量和tunnel信息及flow直接cop过来
        if g_sim.inherit_flag == True:
            g_sim.before_fault_link_info.clear()
            g_sim.before_fault_link_info = copy.deepcopy(g_sim.after_fault_link_info) 
            g_tunrec.sim_b4tuns.clear()
            g_tunrec.sim_b4tuns = copy.deepcopy(g_tunrec.sim_aftuns)
            g_sim.b4_flow.clear()
            g_sim.b4_flow = copy.deepcopy(g_sim.af_flow)
            for flowid in g_sim.flow_info.keys():
                g_sim.flow_info[flowid].b4_jump.clear()
                g_sim.flow_info[flowid].b4_path.clear()
                g_sim.flow_info[flowid].b4_jump = copy.deepcopy(g_sim.flow_info[flowid].af_jump)
                g_sim.flow_info[flowid].b4_path = copy.deepcopy(g_sim.flow_info[flowid].af_path)
        else:
            g_sim.before_fault_link_info.clear()
            g_sim.before_fault_link_info = copy.deepcopy(g_sim.all_link_payload)
            g_tunrec.sim_b4tuns.clear()
            g_tunrec.sim_b4tuns = copy.deepcopy(g_tunrec.sim_orgtuns)
            g_sim.b4_flow.clear()
            g_sim.b4_flow = copy.deepcopy(g_sim.org_flow)
            
            if g_sim.object_tunnel_flow == True or g_sim.object_input_flow == True:
                if g_sim.type_flow != True:
                    add_b4_flows_to_links()
                    delay_s(1)
                sim_rate.sim_b4_flow_sim_progress = 40

            # 计算故障前，所有链路各个时间段的带宽利用率
            cal_b4_fault_links_use_ratio()
            delay_s(1)
            sim_rate.sim_b4_flow_sim_progress = 80
        
        sim_rate.sim_b4_flow_num = cal_before_fault_flow_num()
        if 'before' in g_sim.sim_step_statis.keys():
            g_sim.sim_step_statis['before'].flow_num = sim_rate.sim_b4_flow_num 

        return ErrCode.SUCCESS
    except Exception as e:
        print("before_fault_simulate Exception:", e)
        error_logger.error(e)
        error_logger.info(e)

def cal_before_fault_flow_num():
    try:
        """计算故障前的flow的条数
        
        Args:
            none
        Returns:
            none
        Raise:
            none
        """
        flow_num = 0
        for flow_info in g_sim.flow_info.values():
            info_logger.error("flow_info.b4_jump.values:%s"%(flow_info.b4_jump.values()))
            for value in flow_info.b4_jump.values():
                if value > 0:
                    flow_num += 1 
                    break
        info_logger.error("cal_before_fault_flow_num flow_num:%d"%(flow_num))
        print("cal_before_fault_flow_num flow_num:",flow_num)
        return flow_num  
    except Exception as e:
        print("cal_before_fault_flow_num Exception:", e)
        error_logger.error(e)
        error_logger.info(e)
        return None
############################################
# 故障后仿真
############################################
def cal_after_fault_flow_num():
    try:
        """计算故障后的flow的条数
        
        Args:
            none
        Returns:
            none
        Raise:
        """
        flow_num = 0
        info_logger.error("g_sim.flow_info:%s"%(g_sim.flow_info))
        for flow_info in g_sim.flow_info.values():
            info_logger.error("flow_info.af_jump.values:%s"%(flow_info.af_jump.values()))
            for value in flow_info.af_jump.values():
                if value > 0:
                    flow_num += 1 
                    break
        print("after info:", g_sim.flow_info)
        print("cal_after_fault_flow_num flow_num:",flow_num)
        info_logger.error("cal_after_fault_flow_num flow_num:%d"%(flow_num))
        return flow_num
    except Exception as e:
        print("cal_after_fault_flow_num Exception:", e)
        error_logger.error(e)
        error_logger.info(e)
        return None

def judge_all_nodes_is_fault():
    try:
        """判断所有节点是否均为故障
        
        Args:
            none
        Returns:
            none
        Raise:
            none
        """
        Flag = True 
        for key in g_dt.phy_topo.nodes:
            if g_dt.phy_topo.nodes[key].fault != "yes": 
                Flag = False
                break
        return  Flag
    except Exception as e:
        print("judge_all_nodes_is_fault Exception:", e)
        error_logger.error(e)
        error_logger.info(e)
        return None

def judge_all_links_is_fault():
    try:
        """判断所有链路是否均为故障
        
        Args:
            none
        Returns:
            none
        Raise:
            none
        """
        Flag = True 
        for key in g_dt.phy_topo.links:
            if g_dt.phy_topo.links[key].fault != "yes": 
                Flag = False
                break
        return  Flag
    except Exception as e:
        print("judge_all_links_is_fault Exception:", e)
        error_logger.error(e)
        error_logger.info(e)
        return None
                


def calc_fault_node_info():
    try:
        """统计fault节点和链路的设备IP和故障端口
        
        Args:
            none
        Returns:
            none
        Raise:
            none
        """
        all_faults = []
        for key,value in g_sim.topo.nodes.items():
            if value.fault == 'yes':
                # 如果节点设置为故障节点，则把节点的所有ifindex添加到故障列表里。同时把与其相连接的节点的port也添加到故障列表里
                for port_id in value.port:
                    node_id = value.id
                    temp = {'host':value.mgrip,'port':port_id}
                    all_faults.append(temp)
                
                    # 获得其邻居端口节点，若未曾加入故障列表,则把邻居节点加入故障列表里
                    # 注意，这里能放在上一个if里，因为这个代码是先遍历node的,故障点的node，邻节点设置故障一定是成对出现的
                    # 所以邻居节点也不需要再判是否在故障列表里，一定不在喽
                    nei_node_id, nei_port_id = get_neighbour_node(node_id, port_id)
                    nei_ip = get_node_mgrip(nei_node_id)
                    temp = {'host':nei_ip,'port':nei_port_id}
                    all_faults.append(temp) 
                        
        # 遍历链路,把设置为故障的链路的链路两端的节点和port信息加入故障列表                 
        for key,value in g_sim.topo.links.items():
            if value.fault == 'yes':
                node1 = value.nodeid1 
                node2 = value.nodeid2
                ifindex1 = value.ifindex1
                ifindex2 =value.ifindex2
                node1_ip = get_node_mgrip(node1)

                temp = {'host':node1_ip,'port':ifindex1}
                all_faults.append(temp)
                node2_ip = get_node_mgrip(node2)
                temp = {'host':node2_ip,'port':ifindex2}
                all_faults.append(temp) 
        
        # 去重
        if len(all_faults):
            run_function = lambda x, y: x if y in x else x + [y]
            g_sim.all_fault = reduce(run_function, [[], ] + all_faults)
    except Exception as e:
        print("calc_fault_node_info Exception:", e)
        error_logger.error(e)
        error_logger.info(e)


def cal_background_after_fault_link_speed():
    """根据路径，计算各个链路故障后的流量值
    
    Args:
        none
    Returns:
        none
    Raise:
        none
    """
    try:
        for key, value in g_sim.fault_backgrond_info.items():
            for background in value:
                # 这个if得合,因为有可能某条链路上就是没有流量跑，然后就没有添加了'before_route'了
                if 'before_route' in background.keys():
                    before_fault_route = background['before_route']
                    speed_value = background['speed'] * 8 
                    for path in before_fault_route:
                        # 因为after_fault_link_info原来是把before_fault_link_info直接进行copy的，因而，开始的时候，先把故障后的所有链路上的
                        # 故障节点的流，先进行减法，减掉
                        start_node_id = path['start_node_id']
                        end_node_id = path['end_node_id']
                        link_id = path['linkid']
                        after_fault_one_link = g_sim.after_fault_link_info[key].link_info[link_id]
                        if after_fault_one_link.asset_a == start_node_id and after_fault_one_link.asset_b == end_node_id:
                            one_Link = after_fault_one_link.a_to_b
                        else:
                            one_Link = after_fault_one_link.b_to_a

                        if one_Link.speed > speed_value:
                            one_Link.speed -= speed_value
                        else:
                            one_Link.speed = 0
                            

                if 'after_route' in background.keys():            
                    after_fault_route = background['after_route']
                    speed_value = background['speed'] * 8 
                    for path in after_fault_route:
                        # 再把故障节点上原来跑的背景流，在其新的路径上进行加法计算，得到新的背景流信息
                        start_node_id = path['start_node_id']
                        end_node_id = path['end_node_id']
                        link_id = path['linkid']
                        after_fault_one_link = g_sim.after_fault_link_info[key].link_info[link_id]
                        if after_fault_one_link.asset_a == start_node_id and after_fault_one_link.asset_b == end_node_id:
                            one_Link = after_fault_one_link.a_to_b
                        else:
                            one_Link = after_fault_one_link.b_to_a
            
                        one_Link.speed += speed_value

    except Exception as e:# 正式时，打开
        print("cal_background_after_fault_link_speed Exception:", e)
        error_logger.error(e)
        error_logger.info(e)
    
def background_fission():
    try:
        """由于之前的背景流是按前台下发的仿真周期来计算均值和路径的，如果一个周期内被切片了，这里把其进行裂变，对应切片的时间段。 
        
        Args:
            none
        Returns:
            none
        Raise:
            none
        """
        big_end_time = g_sim.time_sim_info[-1]['end_time']
        b_fission = False
        background_flow_add = {}
        for key, value in g_sim.fault_backgrond_info.items():
            end_time =  key + g_sim.time_cycle
            sim_end_time = get_end_time(key)

            if end_time >= big_end_time:
                end_time = big_end_time
            
            while end_time != sim_end_time:
                b_fission = True
                start_time = sim_end_time
                background_flow_add[start_time] = copy.deepcopy(value)
                sim_end_time = get_end_time(start_time)

        if b_fission == True:
            g_sim.fault_backgrond_info.update(background_flow_add)
    except Exception as e:# 正式时，打开
        print("background_fission Exception:", e)
        error_logger.error(e)
        error_logger.info(e)

def cal_after_fault_links_use_ratio():
    """计算故障后，各个时间段内，所有端口的带宽利用率
    
    Args:
        none
    Returns:
        none
    Raise:
        none
    """  
    try:
        for _, value in g_sim.after_fault_link_info.items():
            all_link_info = value.link_info
            # 轮询各个时刻下的所有的链路
            for linkid in all_link_info:
                one_link_info = all_link_info[linkid]
                a_b = one_link_info.a_to_b

                a_b.speed = a_b.back_speed + a_b.te_speed + a_b.flow_speed + a_b.flow_tun_speed # sprint 3 add
                a_b.out_use_ratio = round(((100 * a_b.speed) / (a_b.band_width)), 2)
                
                b_a = one_link_info.b_to_a
                b_a.speed = b_a.back_speed + b_a.te_speed + b_a.flow_speed + b_a.flow_tun_speed # sprint 3 add 
                b_a.out_use_ratio = round(((100 * b_a.speed) / (b_a.band_width)), 2)
    except Exception as e:
        print("cal_after_fault_links_use_ratio Exception:", e)
        error_logger.error(e)
        error_logger.info(e)

def cal_onetime_fault_links_use_ratio(s_time):
    """计算故障后，某个时间段内，所有端口的带宽利用率
       由于这个是在仿真分析阶段，重新算带宽利用率，需要把te_spped和flow_speed先删除
    
    Args:
        none
    Returns:
        none
    Raise:
        none
    """  
    try:
        all_link_info = g_sim.after_fault_link_info[s_time].link_info
        # 先清除te speed 和 flow speed
        for linkid in all_link_info:
            one_link_info = all_link_info[linkid]
            a_b = one_link_info.a_to_b
            a_b.te_speed = 0
            a_b.flow_speed = 0
            
            b_a = one_link_info.b_to_a
            b_a.te_speed = 0
            b_a.flow_speed = 0 
         
    except Exception as e:
        print("cal_onetime_fault_links_use_ratio Exception:", e)
        error_logger.error(e)
        error_logger.info(e)

# sprint 3 add
def get_af_payload():
    try:
        """首次仿真的故障后的背景流；或者增量仿真的背景流
        
        Args:
            none
        Returns:
            none
        Raise:
            none
        """
        g_sim.after_fault_link_info = copy.deepcopy(g_sim.all_link_payload)
    
        for key in g_sim.after_fault_link_info.keys():
            all_link_info = g_sim.after_fault_link_info[key].link_info
            for linkid in all_link_info.keys():
                one_link = all_link_info[linkid] 
                asset_a = one_link.asset_a  
                asset_b = one_link.asset_b 
                # 只保留back_speed的值,其他的值都根据故障后的路径重新计算
                one_link.a_to_b.flow_speed = 0
                one_link.b_to_a.flow_speed = 0
                one_link.a_to_b.te_speed = 0
                one_link.b_to_a.te_speed = 0
                one_link.a_to_b.flow_tun_speed = 0
                one_link.b_to_a.flow_tun_speed = 0
                one_link.a_to_b.speed = 0
                one_link.b_to_a.speed = 0
                one_link.a_to_b.out_use_ratio = 0
                one_link.b_to_a.out_use_ratio = 0
                one_link.a_to_b.add_flow_num = 0
                one_link.b_to_a.add_flow_num = 0
                one_link.a_to_b.add_flow_id.clear()
                one_link.b_to_a.add_flow_id.clear()
                one_link.a_to_b.te_id.clear()
                one_link.b_to_a.te_id.clear()

                if g_sim.af_topo.links[linkid].fault == 'yes' or g_sim.af_topo.nodes[asset_a].fault == 'yes' or g_sim.af_topo.nodes[asset_b].fault == 'yes':
                    one_link.a_to_b.back_speed = 0
                    one_link.b_to_a.back_speed = 0
    except Exception as e:
        print("get_af_payload Exception:", e)
        error_logger.error(e)
        error_logger.info(e)

#sprint3 add
def cal_link_tun_speed():
    try:
        """把基于tunnel创建的流量，加到其tunnel路径经过的各条链路上
        
        Args:
            none
        Returns:
            none
        Raise:
            none
        """  
        for time_step in g_tunrec.sim_aftuns.keys(): # 按时间段遍历
            tun_step = g_tunrec.sim_aftuns[time_step]
            for key in tun_step.keys():
                tun = tun_step[key]
                if tun.status == 'UP':
                    throughput =tun.throughput

                    if tun.active_path == "primary":
                        path = tun.primary_path.path
                    else:
                        path = tun.standby_path.path

                    #找到对应的链路，把tunnel流量加上这个流量的大小
                    for one_path in path: 
                        linkid = one_path["linkid"]
                        linkInfo = g_sim.after_fault_link_info[time_step].link_info[linkid]

                        if one_path["start_node_id"] == linkInfo.asset_a and one_path["end_node_id"] == linkInfo.asset_b:
                            linkInfo.a_to_b.te_speed += throughput
                        else:
                            linkInfo.b_to_a.te_speed += throughput
    except Exception as e:
        print("cal_link_tun_speed Exception:", e)
        error_logger.error(e)
        error_logger.info(e)

def clear_af_fault_onetime_te_speed(st_time):
    """清除定义后的tunnel流量
    
    Args:
        none
    Returns:
        none
    Raise:
        none
    """  
    try:
        all_link_info = g_sim.after_fault_link_info[st_time].link_info
        for linkid in all_link_info.keys():
            one_link = all_link_info[linkid] 
            asset_a = one_link.asset_a  
            asset_b = one_link.asset_b 
            one_link.a_to_b.te_speed = 0
            one_link.b_to_a.te_speed = 0
            one_link.a_to_b.flow_tun_speed = 0
            one_link.b_to_a.flow_tun_speed = 0
    except Exception as e:
        info_logger.error(e)
        error_logger.error(e)
        print("clear_af_fault_onetime_te_speed Exception:", e)

def cal_af_fault_all_link_flowspeed():
    try:
        for flow_id, value in g_sim.flow_info.items():
            start_time = value.start_time  # 用户导入的流的起始和结束时间
            end_time = value.end_time
            if start_time < g_sim.time_sim_info[0]["start_time"]:
                flow_begin_time = g_sim.time_sim_info[0]["start_time"]
            else:
                flow_begin_time = start_time

            if value.tun_name == '':
                ret, data = get_underlay_flow_path('after_fault', flow_id,flow_begin_time)

                if ret == ErrCode.FAILED:
                    # 如果获取路径失败,则构造成路径不可达
                    value.af_path["all"] = []
                    value.af_jump["all"] = 0
                    value.af_delay["all"] = 0
                    continue

                # start_time = value.start_time    # 用户导入的流的起始和结束时间
                # end_time = value.end_time
                throughput = value.bandwidth["all"]
                value.af_path["all"] = copy.deepcopy(data["path"])
                value.af_jump["all"] = data["jump"]
                value.af_delay["all"] = data["delay"]

                if value.af_jump["all"] != 0:
                    for time_info in g_sim.time_sim_info:    # 按时间片遍历 
                        s_time = time_info["start_time"]    # 切片的时间段
                        e_time = time_info["end_time"]
                        if start_time <= s_time and end_time >= e_time:
                            add_af_fault_input_flow_speed(flow_id, s_time, throughput, data["path"])
                        elif end_time < s_time:
                            break

    except Exception as e:
        print("cal_af_fault_all_link_flowspeed Exception:", e)
        info_logger.error(e)
        error_logger.error(e)

def get_path_add_flow(st_time):
    try:
        for tun_id, tun_info in g_tunrec.sim_aftuns[st_time].items():
            start_node = tun_info.src_id
            tun_name = tun_info.name

            if st_time in g_sim.af_flow.keys():
                for flowid in g_sim.af_flow[st_time]:
                    flow_throughput = 0
                    if tun_id == flowid:
                        if g_tunrec.sim_aftuns[st_time][tun_id].primary_path.path_status == 'UP':
                            g_sim.flow_info[flowid].af_path[st_time] = copy.deepcopy(g_tunrec.sim_aftuns[st_time][tun_id].primary_path.path) 
                            g_sim.flow_info[flowid].af_delay[st_time] = g_tunrec.sim_aftuns[st_time][tun_id].primary_path.delay 

                        elif (g_tunrec.sim_aftuns[st_time][tun_id].primary_path.path_status == 'DOWN' and 
                            g_tunrec.sim_aftuns[st_time][tun_id].standby_path.path_status == 'UP'): 
                            g_sim.flow_info[flowid].af_path[st_time] = copy.deepcopy(g_tunrec.sim_aftuns[st_time][tun_id].standby_path.path) 
                            g_sim.flow_info[flowid].af_delay[st_time] = g_tunrec.sim_aftuns[st_time][tun_id].standby_path.delay 
                        else:                      
                            g_sim.flow_info[flowid].af_path[st_time] = []
                            g_sim.flow_info[flowid].af_delay[st_time] = 0
              
                        
                        flow_throughput = g_sim.flow_info[flowid].bandwidth[st_time] 
                        if len(g_sim.flow_info[flowid].af_path[st_time]) == 0:
                            g_sim.flow_info[flowid].af_jump[st_time] = len(g_sim.flow_info[flowid].af_path[st_time])
                        else:
                            g_sim.flow_info[flowid].af_jump[st_time] = len(g_sim.flow_info[flowid].af_path[st_time]) + 1
                         
                    else:
                        if tun_name == g_sim.flow_info[flowid].tun_name and start_node == g_sim.flow_info[flowid].src_id:
                            if g_tunrec.sim_aftuns[st_time][tun_id].primary_path.path_status == 'UP':
                                g_sim.flow_info[flowid].af_path[st_time] = copy.deepcopy(g_tunrec.sim_aftuns[st_time][tun_id].primary_path.path)
                                g_sim.flow_info[flowid].af_delay[st_time] = g_tunrec.sim_aftuns[st_time][tun_id].primary_path.delay
                            elif (g_tunrec.sim_aftuns[st_time][tun_id].primary_path.path_status == 'DOWN' and 
                                g_tunrec.sim_aftuns[st_time][tun_id].standby_path.path_status == 'UP'): 
                                g_sim.flow_info[flowid].af_path[st_time] = copy.deepcopy(g_tunrec.sim_aftuns[st_time][tun_id].standby_path.path)
                                g_sim.flow_info[flowid].af_delay[st_time] = g_tunrec.sim_aftuns[st_time][tun_id].standby_path.delay
                            else:
                                g_sim.flow_info[flowid].af_path[st_time] = []
                                g_sim.flow_info[flowid].af_delay[st_time] = 0

                            flow_throughput = g_sim.flow_info[flowid].bandwidth[st_time]
                            if len(g_sim.flow_info[flowid].af_path[st_time]) == 0:
                                g_sim.flow_info[flowid].af_jump[st_time] = len(g_sim.flow_info[flowid].af_path[st_time])
                            else:
                                g_sim.flow_info[flowid].af_jump[st_time] = len(g_sim.flow_info[flowid].af_path[st_time]) + 1
                                  
                    if flow_throughput != 0:
                        add_af_fault_te_flow_speed(flowid, st_time, flow_throughput, g_sim.flow_info[flowid].af_path[st_time])
    except Exception as e:
        print("get_path_add_flow exception:", e)
        info_logger.error(e)
        error_logger.error(e)

def save_all_tunnel_path(data, st_time):
    try:
        """保存仿真定义后的主备路径
        
        Args:
            none
        Returns:
            none
        Raise:
            none
        """
        for path_info in data:
            if path_info:
                tun_id = path_info["tunnelId"]
            else:
                continue
            if st_time in g_tunrec.sim_aftuns and tun_id in g_tunrec.sim_aftuns[st_time].keys():
                primary_path = g_tunrec.sim_aftuns[st_time][tun_id].primary_path
                primary_path.path.clear()
                primary_path.hops.clear()

                standby_path = g_tunrec.sim_aftuns[st_time][tun_id].standby_path
                standby_path.path.clear()
                standby_path.hops.clear()

                if ("primary" in path_info.keys() and 
                    path_info["primary"] != None and
                    "linkList" in path_info["primary"].keys() and 
                    len(path_info["primary"]["linkList"]) > 0):

                    primary_path.strict_result = path_info["primary"]["strictStatus"]
                    if path_info["primary"]["strictStatus"] == 0 or path_info["primary"]["strictStatus"] == 1:
                        primary_path.path_status = "UP"
                    else:
                        primary_path.path_status = "DOWN"

                    for linkid in path_info["primary"]["linkList"]:
                        l3_src_id = g_sim.af_l3_topo.links[linkid].src_id
                        l3_des_id = g_sim.af_l3_topo.links[linkid].des_id
                        phy_linkid = g_sim.af_l3_topo.links[linkid].phy_id
                        path_step ={
                            "start_node_id": g_sim.af_l3_topo.nodes[l3_src_id].phy_id,
                            "end_node_id": g_sim.af_l3_topo.nodes[l3_des_id].phy_id,
                            "linkid": phy_linkid
                        }
                        primary_path.path.append(path_step)

                        one_hop = TunnelHop()
                        one_hop.node_id = g_sim.af_l3_topo.nodes[l3_src_id].phy_id
                        one_hop.node_name = g_sim.af_l3_topo.nodes[l3_src_id].name

                        if g_sim.af_topo.links[phy_linkid].nodeid1 == one_hop.node_id:
                            one_hop.out_interface = g_sim.af_topo.links[phy_linkid].ifdesc1 
                        elif g_sim.af_topo.links[phy_linkid].nodeid2 == one_hop.node_id:
                            one_hop.out_interface = g_sim.af_topo.links[phy_linkid].ifdesc2 

                        primary_path.hops[one_hop.node_id]= one_hop
                    
                    one_hop = TunnelHop()
                    one_hop.node_id = g_sim.af_l3_topo.nodes[l3_des_id].phy_id
                    one_hop.node_name =g_sim.af_l3_topo.nodes[l3_des_id].name
                    one_hop.out_interface = "N/A"
                    primary_path.hops[one_hop.node_id]= one_hop
                    primary_path.delay = cal_tunnel_paths_delay("after_fault", path_info["primary"]["linkList"],st_time)
                    primary_path.hop_num = len(path_info["primary"]["linkList"]) + 1
                else:
                    primary_path.path_status = "DOWN"
                    primary_path.hop_num = 0
                    primary_path.delay = 0
                    if ("primary" in path_info.keys() and "strictStatus" in path_info["primary"].keys()):
                        primary_path.strict_result = path_info["primary"]["strictStatus"]
                    else:
                        primary_path.strict_result = 3    # 未选路
                    
                if ("standby" in path_info.keys() and 
                    path_info["standby"] != None and
                    "linkList" in path_info["standby"].keys() and 
                    len(path_info["standby"]["linkList"]) > 0): 
                    standby_path.strict_result = path_info["standby"]["strictStatus"]
                    if path_info["standby"]["strictStatus"] == 0 or path_info["standby"]["strictStatus"] == 1:
                        standby_path.path_status = "UP"
                    else:
                        standby_path.path_status = "DOWN"
                    for linkid in path_info["standby"]["linkList"]:
                        l3_src_id = g_sim.af_l3_topo.links[linkid].src_id
                        l3_des_id = g_sim.af_l3_topo.links[linkid].des_id
                        phy_linkid = g_sim.af_l3_topo.links[linkid].phy_id
                        src_phy_node_id = g_sim.af_l3_topo.nodes[l3_src_id].phy_id
                        end_phy_node_id = g_sim.af_l3_topo.nodes[l3_des_id].phy_id

                        path_step ={
                            "start_node_id": src_phy_node_id,
                            "end_node_id": end_phy_node_id,
                            #"phy_src_node_name": g_sim.topo.nodes[src_phy_node_id].name,
                            #"phy_end_node_name": g_sim.topo.nodes[end_phy_node_id].name,
                            "linkid": phy_linkid
                        }
                        standby_path.path.append(path_step)

                        one_hop = TunnelHop()
                        one_hop.node_id = g_sim.af_l3_topo.nodes[l3_src_id].phy_id
                        one_hop.node_name =g_sim.af_l3_topo.nodes[l3_src_id].name

                        if g_sim.af_topo.links[phy_linkid].nodeid1 == one_hop.node_id:
                            one_hop.out_interface = g_sim.af_topo.links[phy_linkid].ifdesc1 
                        elif g_sim.af_topo.links[phy_linkid].nodeid2 == one_hop.node_id:
                            one_hop.out_interface = g_sim.af_topo.links[phy_linkid].ifdesc2 

                        standby_path.hops[one_hop.node_id]= one_hop
                    
                    one_hop = TunnelHop()
                    one_hop.node_id = g_sim.af_l3_topo.nodes[l3_des_id].phy_id
                    one_hop.node_name =g_sim.af_l3_topo.nodes[l3_des_id].name
                    one_hop.out_interface = "N/A"
                    standby_path.hops[one_hop.node_id]= one_hop
                    primary_path.delay = cal_tunnel_paths_delay("after_fault", path_info["standby"]["linkList"],st_time)
                    standby_path.hop_num = len(path_info["standby"]["linkList"]) + 1
                else:
                    standby_path.path_status = "DOWN"
                    standby_path.hop_num = 0
                    standby_path.delay = 0
                    if ("standby" in path_info.keys() and "strictStatus" in path_info["standby"].keys()):
                        standby_path.strict_result = path_info["standby"]["strictStatus"]
                    else:
                        standby_path.strict_result = 3    # 未选路


                if primary_path.path_status == "DOWN" and standby_path.path_status == "DOWN":
                    g_tunrec.sim_aftuns[st_time][tun_id].status = "DOWN"
                    g_tunrec.sim_aftuns[st_time][tun_id].path_num = 0
                elif primary_path.path_status == "UP" and standby_path.path_status == "DOWN":
                    g_tunrec.sim_aftuns[st_time][tun_id].status = "UP"
                    g_tunrec.sim_aftuns[st_time][tun_id].path_num = 1
                    g_tunrec.sim_aftuns[st_time][tun_id].active_path = "primary"
                elif primary_path.path_status == "DOWN" and standby_path.path_status == "UP":
                    g_tunrec.sim_aftuns[st_time][tun_id].status = "UP"
                    g_tunrec.sim_aftuns[st_time][tun_id].path_num = 1
                    g_tunrec.sim_aftuns[st_time][tun_id].active_path = "standby"
                elif primary_path.path_status == "UP" and standby_path.path_status == "UP":
                    g_tunrec.sim_aftuns[st_time][tun_id].status = "UP"
                    g_tunrec.sim_aftuns[st_time][tun_id].path_num = 2
                    g_tunrec.sim_aftuns[st_time][tun_id].active_path = "primary"

    except Exception as e:
        print("save_all_tunnel_path exception:", e)
        info_logger.error(e)
        error_logger.error(e)

def save_primary_tunnel_path(data,st_time):
    try:
        """保存仿真定义后的主路径
        
        Args:
            none
        Returns:
            none
        Raise:
            none
        """
        for path_info in data:
            tun_id = path_info["tunnelId"]
            if tun_id in g_tunrec.sim_aftuns[st_time].keys():
                primary_path = g_tunrec.sim_aftuns[st_time][tun_id].primary_path.path
                primary_path.clear()
                # 如果 path_info["primary"] 不为空 ，更新路径
                if path_info["primary"]:
                    g_tunrec.sim_aftuns[st_time][tun_id].primary_path.path_status = 'UP'
                    for linkid in path_info["primary"]["linkList"]:
                        l3_src_id = g_dt.l3_topo.links[linkid].src_id
                        l3_des_id = g_dt.l3_topo.links[linkid].des_id
                        path_step ={
                            "start_node_id": g_dt.l3_topo.nodes[l3_src_id].phy_id,
                            "end_node_id": g_dt.l3_topo.nodes[l3_des_id].phy_id,
                            "linkid": g_dt.l3_topo.links[linkid].phy_id
                        }
                        primary_path.append(path_step)
                else:
                    g_tunrec.sim_aftuns[st_time][tun_id].primary_path.path_status = 'DOWN'

    except Exception as e:
        print("save_primary_tunnel_path exception:", e)
        info_logger.error(e)
        error_logger.error(e)

def after_fault_simulate():
    try:
        """故障后仿真
        
        Args:
            none
        Returns:
            none
        Raise:
            none
        """
        flag = 'after_fault'
        # 把流量列表copy过来
        g_sim.af_flow.clear()
        g_sim.af_flow = copy.deepcopy(g_sim.org_flow)

        if g_sim.stop_simulate_flag != 1:
            # cal_background_after_fault_link_speed()    sprint 3 mark
            g_tunrec.sim_aftuns.clear()
            g_tunrec.sim_aftuns = copy.deepcopy(g_tunrec.sim_b4tuns)

            for flowid in g_sim.flow_info.keys():
                g_sim.flow_info[flowid].af_jump.clear()
                g_sim.flow_info[flowid].af_path.clear()

            get_af_payload()
            sim_rate.sim_after_flow_sim_progress = 5
        
        # 计算故障的链路的值
        if g_sim.stop_simulate_flag != 1:
            delay_s(1)
            sim_rate.sim_after_flow_sim_progress = 10
            ret = send_affinityEnable_to_sdn_simctrl()
            
            if ret != ErrCode.SUCCESS:
                error_logger.error("af_send_topo_to_sdn_simctrl not success")

            progress_start = sim_rate.sim_after_flow_sim_progress
            progress_end = 80
            count = 0
            section_num = len(g_sim.time_sim_info)
            if section_num > 0:
                step = float(progress_end - progress_start)/section_num
            else:
                step = progress_end - progress_start
            
            one_five_step = int(step / 5)

            # 计算从流量模板导入的各个时刻的普通流量的路径
            if g_sim.stop_simulate_flag != 1 and g_sim.object_input_flow == True:
                cal_af_fault_all_link_flowspeed()

            # 按时间发送SLA、流组、流组实例、流组实例隧道路径等信息
            for timeinfo in g_sim.time_sim_info:
                sim_rate.sim_after_flow_sim_progress = int(progress_start + count * step)
                count += 1

                st_time = timeinfo["start_time"]

                if st_time in g_tunrec.sim_aftuns.keys():
                    if len(g_tunrec.sim_aftuns[st_time]) > 0:
                        # 按时间来计算隧道路径的时候，需要把拓扑放到这里，是由于发送故障链路恢复的时候，需要有原始的拓扑
                        ret = send_topo_to_sdn_simctrl(st_time)  # 1.1 把仿真定义前的TOPO信息发给仿真控制器，这里要带入时间参数，那岂不是要调用sdn_simctrl很多次了
                        if ret != ErrCode.SUCCESS:
                            error_logger.error("af_send_topo_to_sdn_simctrl not success")
    
                        ret = send_slapolicy_to_sdn_simctrl() # 1.2 发送所有的SLA策略给仿真控制器
                        if ret != ErrCode.SUCCESS:
                            error_logger.error("send_slapolicy_to_sdn_simctrl not success")
                        
                        sim_rate.sim_after_flow_sim_progress += one_five_step

                        ret = send_flowgroup_to_sdn_simctrl(flag, st_time) # 1.3 添加流组 给仿真控制器
                        if ret != ErrCode.SUCCESS:
                            error_logger.error("af_send_flowgroup_to_sdn_simctrl not success")

                        ret = send_flowgroup_instance_to_sdn_simctrl(flag, st_time) # 1.4 发送流组实例给仿真控制器 
                        if ret != ErrCode.SUCCESS:
                            error_logger.error("af_send_flowgroup_instance_to_sdn_simctrl not success")

                        sim_rate.sim_after_flow_sim_progress += one_five_step

                        ret = send_flowgroup_instance_tunnel_to_sdn_simctrl(flag, st_time) # 1.5 发送流组实例隧道给仿真控制器
                        if ret != ErrCode.SUCCESS:
                            error_logger.error("af_send_flowgroup_instance_tunnel_to_sdn_simctrl not success")
                        
                        ret = recover_link_fault_to_sdn_simctrl(st_time) # 1.9 通知链路故障恢复给仿真控制器
                        if ret != ErrCode.SUCCESS:
                            error_logger.error("recover_link_fault_to_sdn_simctrl not success")

                        # 通知链路故障、通知节点故障、通知链路故障恢复、通知节点故障恢复、路径流量变化
                        ret = notify_link_fault_to_sdn_simctrl() # 通知链路故障给仿真控制器
                        if ret != ErrCode.SUCCESS:
                            error_logger.error("notify_link_fault_to_sdn_simctrl not success")
    
                        #流组实例路径计算（计算主备路径）
                        if g_sim.tunnel_optimize == True:
                            ret = calc_flowgroup_instance_tunnel_path(flag, st_time, mode = 0)
                            if ret != ErrCode.SUCCESS:
                                error_logger.error("af_calc_all_flowgroup_instance_tunnel_path not success===================")    
                        
                        sim_rate.sim_after_flow_sim_progress += one_five_step

                        ret = notify_te_flow_change_to_sdn_simctrl(st_time) # 1.11 通知路径流量变化
                        if ret != ErrCode.SUCCESS:
                            error_logger.error("notify_te_flow_change_to_sdn_simctrl not success")

                        # 获取流组实例隧道路径
                        ret, data1 = get_flowgroup_instance_tunnel_path(flag, st_time)
                        if ret == ErrCode.SUCCESS:
                            save_all_tunnel_path(data1, st_time) # 保存主路径提供链路流量计算
                        else:
                            error_logger.error("af_get_flowgroup_instance_tunnel_path not success===================")

                        ret = notify_link_overload_to_sdn_simctrl(st_time)   # 1.15 通知链路流量超载  
                        if ret != ErrCode.SUCCESS:
                            error_logger.error("notify_link_overload_to_sdn_simctrl not success")

                        ret, data2 = get_flowgroup_instance_tunnel_path(flag, st_time)  # 1.16 获取流组实例隧道路径
                        if ret != ErrCode.SUCCESS:
                            error_logger.error("af_get_flowgroup_instance_tunnel_path not success")
                        
                        sim_rate.sim_after_flow_sim_progress += one_five_step

                        if ret == ErrCode.SUCCESS:
                            ret1 = af_calc_same_path(data2)
                            if ret1 == ErrCode.CAL_DIFFERENT_PATH: # 如果计算出来没有主备同路，则直接保存主备路径
                                info_logger.error("tun path from sdn sim:%s"%(data2))
                                save_all_tunnel_path(data2,st_time)
                            else:
                                # # 获取流组实例隧道路径
                                ret2, data3 = get_flowgroup_instance_tunnel_path(flag, st_time)
                                if ret2 == ErrCode.SUCCESS: 
                                    save_all_tunnel_path(data3, st_time)
                                else:
                                    error_logger.error("af_get_flowgroup_instance_tunnel_path not success===================")
                        else:
                            error_logger.error("af_get_flowgroup_instance_tunnel_path not success===================")


        # 由于负载等计算在跟仿真控制器交互的时候，已经填了中间值，这里重新初始化
        get_af_payload() 

        if g_sim.stop_simulate_flag != 1 and (g_sim.object_input_flow == True or g_sim.object_tunnel_flow == True): 
            if len(g_sim.time_sim_info) > 0:
                for timeinfo in g_sim.time_sim_info:
                    st_time = timeinfo["start_time"]
                    get_path_add_flow(st_time)    

        sim_rate.sim_after_flow_sim_progress = 80
        # 计算从流量模板导入的各个时刻的普通流量的路径
        if g_sim.stop_simulate_flag != 1 and g_sim.object_input_flow == True:
            cal_af_fault_all_link_flowspeed()

        # idms:202001021304
        if g_sim.object_load == True:
            cal_link_tun_speed()

        sim_rate.sim_after_flow_sim_progress = 85  

        if g_sim.stop_simulate_flag != 1: 
            cal_after_fault_links_use_ratio()
            sim_rate.sim_after_flow_sim_progress = 90
        return ErrCode.SUCCESS
    except Exception as e:
        print("after_fault_simulate exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.FAILED

####################################################
# 前台接口
####################################################
def get_sim_para():
    try:
        if g_sim.time_sim_info and 'start_time' in g_sim.time_sim_info[0] and 'end_time' in g_sim.time_sim_info[-1]:
            s_time = g_sim.time_sim_info[0]['start_time']
            e_time = g_sim.time_sim_info[-1]['end_time']
        else:
            s_time = 0
            e_time = 0

        # 将仿真的状态告诉前台 1 为有结果，0 为无结果 
        if g_sim.status == 1:
            ana_result = 1
        else:
            ana_result = 0

        if g_sim.inherit_flag == True:
            inherit_flag = 1
        else:
            inherit_flag = 0

        option = {
			"simType": {		#仿真类型
                "faultSim":g_sim.type_fault, # 故障仿真(True 或 False)
                "flowSim":g_sim.type_flow,	#流量仿真(True 或 False)
                "routeSim":g_sim.type_route	#路由仿真(True 或 False)
            },					
			"simObj":{		    #仿真对象					 
			    "inputFlow": g_sim.object_input_flow,		#0或1
			    "load": g_sim.object_load,			#0或1
			    "tunnelFlow": g_sim.object_tunnel_flow,		#0或1
                "tunnelOptimize":g_sim.tunnel_optimize
            }
        }

        data = {
            'simStartTime':s_time,
            'simEndTime':e_time,
            'option':option,
            'hasAnaResult':ana_result,
            'hasInherit':inherit_flag,
            'time':g_dt.sync_data_finish_time
        }
        return data

    except Exception as e:
        print("get_init_sim_data Exception:", e)

        option = {
			"simType": {
                "flowSim":False,	
                "routeSim":False
            },					
			"simObj":{		 				 
			    "inputFlow": False,
			    "load": False,	
			    "tunnelFlow": False
            }
        }
        data = {
            'simStartTime':0,
            'simEndTime':0,
            'option':option,
            'hasAnaResult':1,
            'hasInherit':0,
            'time':0
        }
        return data



def get_simulate_progress():
    try:
        """获得仿真过程中，各个阶段的进度和信息
        
        Args:
            none
        Returns:
            none
        Raise:
            none
        """
        lang = get_language_setting_index()
        if lang == 1:
            data = {
                    "analyseStep":sim_rate.sim_step,
                    "dataLoad":{
                                "data_load_info_num":sim_rate.sim_data_load_msg_num,
                                "data_load_Info": sim_rate.sim_data_load_chinese
                                },
                    "beforeFault":{
                            "flowProgress":sim_rate.sim_b4_flow_sim_progress,
                            "flowNum":sim_rate.sim_b4_flow_num,
                            "orgFlowNum":sim_rate.sim_org_flow_num
                            },
                    "afterFault":{ 
                            "flowProgress":sim_rate.sim_after_flow_sim_progress,
                            "flowNum":sim_rate.sim_after_flow_num,
                            "orgFlowNum":sim_rate.sim_org_flow_num
                            }

            }
        else:
            data = {
                    "analyseStep":sim_rate.sim_step,
                    "dataLoad":{
                                "data_load_info_num":sim_rate.sim_data_load_msg_num,
                                "data_load_Info": sim_rate.sim_data_load_english
                                },
                    "beforeFault":{
                            "flowProgress":sim_rate.sim_b4_flow_sim_progress,
                            "flowNum":sim_rate.sim_b4_flow_num
                            },
                    "afterFault":{ 
                            "flowProgress":sim_rate.sim_after_flow_sim_progress,
                            "flowNum":sim_rate.sim_after_flow_num
                            }

            }
        return data
    except Exception as e:
        print("get_simulate_progress exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return None

def get_simulate_statisc_Info():
    """获得仿真的统计信息
    
    Args:
        none
    Returns:
        none
    Raise:
        none
    """
    try:
        # 避免多人操作异常
        if 'before' not in g_sim.sim_step_statis.keys() or 'after' not in g_sim.sim_step_statis.keys():
            data = {}   
            ret = ErrCode.FAILED 
            return ret, data

        before = g_sim.sim_step_statis['before']
        after = g_sim.sim_step_statis['after']
        data = {
                "beforeFault":{
                            "sim_creat_time":before.sim_net_start_time, #before.sim_creat_time,sprint3 前台显示错误，后台规避
                            "sim_net_start_time":before.sim_net_start_time,
                            "cycle":before.cycle,
                            "cycle_num":before.cycle_num,
                            "flow_data_type":before.flow_data_type, 
                            "sim_agreement":before.sim_agreement,
                            "sim_ospf_num":before.sim_ospf_num,
                            "sim_isis_num":before.sim_isis_num,
                            "sim_bgp_num":before.sim_bgp_num,
                            "flow_num":before.flow_num, 
                            "tunnel_num":before.tunnel_num,
                            "fail_tunnel_num":before.fail_tunnel_num,
                            "overload_100_link_num":before.overload_100_link_num,
                            "link_max_used_ratio":before.link_max_used_ratio,
                            "whole_net_throughput":before.whole_net_throughput, 
                            "whole_net_used_ratio":before.whole_net_used_ratio,
                            "business_flow_num":before.business_flow_num,
                            "unrouter_business_flow_num":before.unrouter_business_flow_num,
                            "router_business_flow_num":before.router_business_flow_num,
                            },
                "afterFault":{ 
                            "sim_creat_time":after.sim_net_start_time,#after.sim_creat_time,sprint3 前台显示错误，后台规避
                            "sim_net_start_time":after.sim_net_start_time,
                            "cycle":after.cycle,
                            "cycle_num":after.cycle_num,
                            "flow_data_type":after.flow_data_type, 
                            "sim_agreement":after.sim_agreement,
                            "sim_ospf_num":after.sim_ospf_num,
                            "sim_isis_num":after.sim_isis_num,
                            "sim_bgp_num":after.sim_bgp_num,
                            "flow_num":after.flow_num, 
                            "tunnel_num":after.tunnel_num,
                            "fail_tunnel_num":after.fail_tunnel_num,
                            "overload_100_link_num":after.overload_100_link_num,
                            "link_max_used_ratio":after.link_max_used_ratio,
                            "whole_net_throughput":after.whole_net_throughput, 
                            "whole_net_used_ratio":after.whole_net_used_ratio,
                            "business_flow_num":after.business_flow_num,
                            "unrouter_business_flow_num":after.unrouter_business_flow_num,
                            "router_business_flow_num":after.router_business_flow_num,
                            },
            }
        ret = ErrCode.SUCCESS
        return ret, data
    except Exception as e:
        print("get_simulate_statisc_Info Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        data = {}   
        ret = ErrCode.FAILED 
        return ret, data

    

########################
# 故障前故障后公共代码
#########################
#sprint 3 add
def split_time_flow_sprint3():
    try:
        """记录仿真的时间，只是在sprint3 使用，因为sprint3 只仿真一个时刻，所以简化了“split_time_flow”函数
        
        Args:
            none
        Returns:
            none
        Raise:
            none
        """
        time_sim_info = {
                        'start_time':g_sim.time_start,
                        'end_time':g_sim.time_end,
                        'has_flow':'true'
                        }  
        g_sim.time_sim_info.append(time_sim_info)
        g_sim.time_cycle_num = 1
        g_sim.time_section = 1
        return ErrCode.SUCCESS
    except Exception as e:
        print("split_time_flow_sprint3 Exception:", e)
        info_logger.error(e)
        error_logger.error(e) 
        return ErrCode.FAILED
    
def split_time_flow():
    try:
        """将所有Flow进行整理，切分时间片段，返回列表信息将所有Flow进行整理，切分时间片段，返回列表信息
        
        Args:
            none
        Returns:
            none
        Raise:
            none
        """   
        time_cycle = g_sim.time_cycle
        time_end = g_sim.time_end
        time_start = g_sim.time_start

        g_sim.time_sim_info.clear()
        
        # 向上取整,仅在python3上支持，所以还是改成判余
        # g_sim.time_cycle_num = math.ceil((g_sim.time_end - g_sim.time_start)/g_sim.time_cycle)
        if (g_sim.time_end - g_sim.time_start) % g_sim.time_cycle == 0:
            g_sim.time_cycle_num = int((g_sim.time_end - g_sim.time_start)/g_sim.time_cycle)
        else:
            g_sim.time_cycle_num = int((g_sim.time_end - g_sim.time_start)/g_sim.time_cycle) + 1

        print("g_sim.time_cycle_num:%d",g_sim.time_cycle_num)
        # 输出list的单元内容
        time_sim_info_list = g_sim.time_sim_info

        # 用于保存所有的时间节点
        time_split_list = []

        # 将当前周期分成多个片段的时间节点
        time_temp = time_start
        while time_temp < time_end:
            time_split_list.append(time_temp)
            time_temp = time_temp + time_cycle
            if time_temp >= time_end:
                break

        # 将最后一个不足一个周期的时间节点加上
        if time_temp == time_end:
            time_split_list.append(time_temp) 
        if time_temp > time_end:
            time_split_list.append(time_end) 

        if (not g_allFlows or 
            g_sim.object_input_flow == False):
            # 如果不存在打流,则把时间切片自己组成time_sim_info_list，即可返回
            for i in range(g_sim.time_cycle_num):
                # 将time_split_list的值，分片段，赋给各个时间周期
                time_sim_info = {
                                'start_time':time_split_list[i],
                                'end_time':time_split_list[i+1],
                                'has_flow':'false'
                                }        
                time_sim_info_list.append(time_sim_info)
            # 如果没有导入流量，仿真后的时间切片个数同time_cycle_num
            g_sim.time_section = g_sim.time_cycle_num
            return ErrCode.SUCCESS
        
        flow_start_time = []
        flow_end_time = []

        # 如果存在打流，则增加Flow中的时间节点
        for flow_id in g_allFlows.keys():
            # 如果内容为空，或者流里没有记录开始时间、结束时间，则这条流不记录 
            if not g_allFlows[flow_id] or g_allFlows[flow_id].start_time == '' or g_allFlows[flow_id].end_time == '':
                continue
                
            # 起始和结束时间 
            startTime = g_allFlows[flow_id].start_time
            endTime = g_allFlows[flow_id].end_time

            # 流本身的时间不符合逻辑
            if startTime >= endTime:
                continue

            # flow的时间不在仿真时间段内的，不做处理
            if startTime >= g_sim.time_end or endTime < g_sim.time_start: 
                continue
            else:
                if startTime < g_sim.time_start:
                    startTime = g_sim.time_start
                if endTime > g_sim.time_end:
                    endTime = g_sim.time_end

                if startTime not in time_split_list:
                    time_split_list.append(startTime)
                if endTime not in time_split_list:
                    time_split_list.append(endTime)

                # 然后维护一张临时表，确定在某个小周期内，是否有Flow            
                flow_start_time.append(startTime)
                flow_end_time.append(endTime)

        # 查看当前所有的时间节点表,进行排序   
        time_split_list.sort()
        time_splitlist_len_dec_one = len(time_split_list) - 1
        start_time_list_len = len(flow_start_time)
        g_sim.time_section = time_splitlist_len_dec_one

        for i in range(time_splitlist_len_dec_one):
            time_sim_info = {
                            'start_time':time_split_list[i],
                            'end_time':time_split_list[i+1],
                            'has_flow':'false'
                            }
            # 判断当前的周期是否有Flow
            middleTime = (time_sim_info['end_time'] + time_sim_info['start_time'])/2
            for j in range(start_time_list_len):
                if middleTime >= flow_start_time[j] and middleTime < flow_end_time[j]:
                    time_sim_info['has_flow'] = 'true'
                    break

            time_sim_info_list.append(time_sim_info)
        return ErrCode.SUCCESS     
    except Exception as e:
        print("split_time_flow Exception:", e)
        info_logger.error(e)
        error_logger.error(e) 
        return ErrCode.FAILED 

def copy_topo():
    try:
        """复制两份topo
        
        Args:
            none
        Returns:
            none
        Raise:
            none
        """
        # 如果没有TOPO信息,返回错误
        if not g_dt.phy_topo:
            return ErrCode.FAILED

        # sprint3 modify,故障后的二层topo，保存跟设置时的一样
        topo = Topo()
        topo.node_num = g_dt.phy_topo.node_num
        topo.link_num = g_dt.phy_topo.link_num
        topo.fault_num = g_dt.phy_topo.fault_num
        topo.nodes = copy.deepcopy(g_dt.phy_topo.nodes)
        topo.links = copy.deepcopy(g_dt.phy_topo.links)
        g_sim.af_topo = topo # sprint 3 modify

        # sprint3 modify,故障后的三层topo，保存跟设置时的一样
        layer3_topo = L3Topo()
        layer3_topo.node_num = g_dt.l3_topo.node_num
        layer3_topo.link_num = g_dt.l3_topo.link_num
        layer3_topo.nodes = copy.deepcopy(g_dt.l3_topo.nodes)
        layer3_topo.links = copy.deepcopy(g_dt.l3_topo.links)
        g_sim.af_l3_topo = layer3_topo # sprint 3 modify

        # sprint3 modify,故障前的二层topo，无故障点
        no_fault_topo = Topo()
        no_fault_topo.node_num = g_dt.phy_topo.node_num
        no_fault_topo.link_num = g_dt.phy_topo.link_num
        no_fault_topo.nodes = copy.deepcopy(g_dt.phy_topo.nodes)
        no_fault_topo.links = copy.deepcopy(g_dt.phy_topo.links)
        for key in no_fault_topo.nodes:
            no_fault_topo.nodes[key].fault = "no"
            
        for key in no_fault_topo.links:
            no_fault_topo.links[key].fault = "no"
        no_fault_topo.fault_num = 0
        g_sim.topo = no_fault_topo # sprint 3 modify

        # sprint3 modify,故障前的三层topo，无故障点
        nofault_l3_topo = L3Topo()
        nofault_l3_topo.node_num = g_dt.l3_topo.node_num
        nofault_l3_topo.link_num = g_dt.l3_topo.link_num
        nofault_l3_topo.nodes = copy.deepcopy(g_dt.l3_topo.nodes)
        nofault_l3_topo.links = copy.deepcopy(g_dt.l3_topo.links)
        for key in nofault_l3_topo.nodes:
            nofault_l3_topo.nodes[key].fault = 'no'
        for key in nofault_l3_topo.links:
            nofault_l3_topo.links[key].fault = 'no'
        g_sim.l3_topo = nofault_l3_topo # sprint 3 modify

        return ErrCode.SUCCESS
    except Exception as e:
        print("copy_topo Exception:", e)
        info_logger.error(e)
        error_logger.error(e) 
        return ErrCode.FAILED 

def load_flow():
    try:
        """复制一份流量信息和基于tunnel创建的流量信息
        
        Args:
            none
        Returns:
            none
        Raise:
            none
        """

        g_sim.org_flow.clear()

        # 导入的流量
        input_flow_num = 0
        # 基于tunnel创建的流量
        base_tun_creat_num = 0

        # 先创建各以时间为key的字典
        for time_info in g_sim.time_sim_info:
            s_time = time_info["start_time"]
            g_sim.org_flow[s_time] = []

        # 如果选择的用户创建的流量，则把用户创建的流量按时间进行保存
        if g_sim.object_input_flow:
            for value in g_allFlows.values(): 
                if value.start_time <= g_sim.time_end and  value.end_time >= g_sim.time_start and value.start_time != value.end_time:  # 用户导入的流的起始和结束时间
                    input_flow_num += 1                

            for time_info in g_sim.time_sim_info:    # 按时间片遍历 
                s_time = time_info["start_time"]    # 切片的时间段
                e_time = time_info["end_time"]

                if time_info["has_flow"] == "true":     # 如果这段时间，有流量信息，才需要遍历
                    for flow_id, value in g_allFlows.items():    # 遍历所有的用户导入的流量
                        start_time = value.start_time    # 用户导入的流的起始和结束时间
                        end_time = value.end_time
                        # 流量时间覆盖仿真的时间段，则把这个流量数据保存起来
                        if start_time <= s_time and end_time >= e_time:  # sprint 4 仅需要判断流量的时间包含最后一个时刻即可
                            if g_allFlows[flow_id].tun_name == '':  # 获取underlay的流路径
                                if flow_id not in g_sim.flow_info.keys():
                                    ret, data = get_underlay_flow_path('orgin', flow_id, s_time) #这里是start_time还是e_time呢？
                                    if ret != ErrCode.SUCCESS:
                                        print("get_underlay_flow_path failed==================")
                                        info_logger.error("get_underlay_flow_path failed==================")
                                else:
                                    g_sim.org_flow[s_time].append(flow_id)
                                    continue
                            else:  
                               # 获取tunnel的流路径
                                ret, data = get_tunnel_flow_path('orgin', flow_id, s_time)
                                if ret != ErrCode.SUCCESS:
                                    print("get_tunnel_flow_path failed==================")
                                    info_logger.error("get_tunnel_flow_path failed==================")
                            
                            # 当且仅当异常时,或某时刻无tunel信息时,会返回失败,失败时不用保存
                            if ret == ErrCode.SUCCESS:
                                # 如果flow_id不存在，则先把流信息直接COPY过来
                                if flow_id not in g_sim.flow_info.keys():
                                    if g_allFlows[flow_id].tun_name == '':    # 普通的打入的underlay flow，所有时间的路径一样、跳数一样、带宽一样
                                        g_allFlows[flow_id].org_path["all"] = copy.deepcopy(data["path"])
                                        g_sim.flow_info[flow_id] = copy.deepcopy(g_allFlows[flow_id])
                                        if g_sim.type_flow != True:
                                            g_sim.flow_info[flow_id].b4_jump["all"] = data["jump"]
                                            g_sim.flow_info[flow_id].b4_path["all"] = copy.deepcopy(data["path"])
                                            g_sim.flow_info[flow_id].b4_delay["all"] = data["delay"]    # 延时，暂时设置为0 
                                        else:
                                            g_sim.flow_info[flow_id].b4_jump["all"] = 0
                                            g_sim.flow_info[flow_id].b4_path["all"] = []
                                            g_sim.flow_info[flow_id].b4_delay["all"] = 0   
                                    else:
                                        g_sim.flow_info[flow_id] = copy.deepcopy(g_allFlows[flow_id])
                                        g_sim.flow_info[flow_id].org_path.clear()
                                        g_sim.flow_info[flow_id].bandwidth.clear()
                                        g_sim.flow_info[flow_id].org_path[s_time] = copy.deepcopy(data["path"])
                                        g_sim.flow_info[flow_id].bandwidth[s_time] = g_allFlows[flow_id].bandwidth["all"]
                                        if g_sim.type_flow != True:
                                            g_sim.flow_info[flow_id].b4_path[s_time] = copy.deepcopy(data["path"])
                                            g_sim.flow_info[flow_id].b4_jump[s_time] = data["jump"]
                                            g_sim.flow_info[flow_id].b4_delay[s_time] = data["delay"]    # 延时，暂时设置为0 
                                        else:
                                            g_sim.flow_info[flow_id].b4_path[s_time] = []
                                            g_sim.flow_info[flow_id].b4_jump[s_time] = 0
                                            g_sim.flow_info[flow_id].b4_delay[s_time] = 0 
                                else:
                                    if g_allFlows[flow_id].tun_name != '':
                                        g_sim.flow_info[flow_id].org_path[s_time] = copy.deepcopy(data["path"])
                                        g_sim.flow_info[flow_id].bandwidth[s_time] = g_allFlows[flow_id].bandwidth["all"]
                                        if g_sim.type_flow != True:
                                            g_sim.flow_info[flow_id].b4_path[s_time] = copy.deepcopy(data["path"])
                                            g_sim.flow_info[flow_id].b4_jump[s_time] = data["jump"]
                                            g_sim.flow_info[flow_id].b4_delay[s_time] = data["delay"]    # 延时，暂时设置为0
                                        else:
                                            g_sim.flow_info[flow_id].b4_path[s_time] = []
                                            g_sim.flow_info[flow_id].b4_jump[s_time] = 0
                                            g_sim.flow_info[flow_id].b4_delay[s_time] = 0

                                g_sim.org_flow[s_time].append(flow_id)
                  
                    if s_time in g_sim.flow_info[flow_id].b4_jump.keys():
                        info_logger.error("============ org flow info [%d]:%d = %s"%(s_time,g_sim.flow_info[flow_id].b4_jump[s_time], g_sim.flow_info[flow_id].b4_path[s_time]))
                    else:
                        info_logger.error("=========not in keys:%s"%(g_sim.flow_info[flow_id].b4_jump.keys()))
        
        if g_sim.object_tunnel_flow:
            base_tun_creat_num = len(g_tunrec.org_tuns)
            for tun_time, value in g_tunrec.sim_orgtuns.items():
                for tun_key, tun_value in value.items():
                    g_sim.org_flow[tun_time].append(tun_key)
                    if tun_key not in g_sim.flow_info.keys():
                        g_sim.flow_info[tun_key] = FlowObj()
                        flow = g_sim.flow_info[tun_key] 
                        #flow = g_sim.org_flow[key][tun_key]
                        # 如果是基于tunnel创建的流量,就把tunnel_id直接作为flowid进行保存即可
                        flow.id = tun_key
                        flow.src_name = g_sim.topo.nodes[tun_value.src_id].name
                        flow.des_name = g_sim.topo.nodes[tun_value.des_id].name
                        flow.flow_name = tun_value.name + '_' + flow.src_name + '_' + flow.des_name
                        flow.src_ip = tun_value.src_ip
                        flow.des_ip = tun_value.des_ip
                        flow.src_id = tun_value.src_id
                        flow.des_id = tun_value.des_id
                        # 默认基于tunnel创建的流量的起始时间，先填一个初值,最终给的是整个tunnel存续时间的最开始时间
                        flow.start_time = tun_time 
                        flow.end_time = ''
                        flow.flow_type = 'tunnel_flow'
                        flow.orgin = 'tunnel_build'
                        flow.tun_name = tun_value.name
                        flow.bandwidth[tun_time] = tun_value.throughput 
                        if tun_value.primary_path.path_status == 'UP':
                            flow.org_path[tun_time] = copy.deepcopy(tun_value.primary_path.path) 
                            if g_sim.type_flow != True:
                                if len(tun_value.primary_path.path) > 0: # 如果是正常状态则跳数加一，中断跳数则为0
                                    flow.b4_jump[tun_time] = len(tun_value.primary_path.path) + 1
                                else:
                                    flow.b4_jump[tun_time] = len(tun_value.primary_path.path)
                                flow.b4_path[tun_time] = copy.deepcopy(tun_value.primary_path.path)
                                flow.b4_delay[tun_time] =tun_value.primary_path.delay 
                            else:
                                flow.b4_jump[tun_time] = 0
                                flow.b4_delay[tun_time] = 0
                                if tun_time in flow.b4_path.keys():
                                    flow.b4_path[tun_time].clear()
                                else:
                                    flow.b4_path[tun_time] = []
                        else:
                            flow.org_path[tun_time] = copy.deepcopy(tun_value.standby_path.path) 
                            if g_sim.type_flow != True:
                                if len(tun_value.standby_path.path) > 0:
                                    flow.b4_jump[tun_time] = len(tun_value.standby_path.path) + 1
                                else:
                                    flow.b4_jump[tun_time] = len(tun_value.standby_path.path)
                                flow.b4_path[tun_time] = copy.deepcopy(tun_value.standby_path.path)
                                flow.b4_delay[tun_time] =tun_value.standby_path.delay 
                            else:
                                flow.b4_jump[tun_time] = 0
                                flow.b4_delay[tun_time] = 0
                                if tun_time in flow.b4_path.keys():
                                    flow.b4_path[tun_time].clear()
                                else:
                                    flow.b4_path[tun_time] = []       
                    else:
                        if tun_value.primary_path.path_status == 'UP':
                            g_sim.flow_info[tun_key].org_path[tun_time] = copy.deepcopy(tun_value.primary_path.path)
                            if g_sim.type_flow != True:
                                g_sim.flow_info[tun_key].b4_path[tun_time] = copy.deepcopy(tun_value.primary_path.path)
                                if len(tun_value.primary_path.path) > 0:
                                    g_sim.flow_info[tun_key].b4_jump[tun_time] = len(tun_value.primary_path.path) + 1
                                else:
                                    g_sim.flow_info[tun_key].b4_jump[tun_time] = len(tun_value.primary_path.path)
                                g_sim.flow_info[tun_key].b4_delay[tun_time] = tun_value.primary_path.delay 
                            else:
                                g_sim.flow_info[tun_key].b4_path[tun_time] = []
                                g_sim.flow_info[tun_key].b4_jump[tun_time] = 0
                                g_sim.flow_info[tun_key].b4_delay[tun_time] = 0
                        else:
                            g_sim.flow_info[tun_key].org_path[tun_time] = copy.deepcopy(tun_value.standby_path.path)
                            if g_sim.type_flow != True: 
                                g_sim.flow_info[tun_key].b4_path[tun_time] = copy.deepcopy(tun_value.standby_path.path)
                                if len(tun_value.standby_path.path) > 0:
                                    g_sim.flow_info[tun_key].b4_jump[tun_time] = len(tun_value.standby_path.path) + 1
                                else:
                                    g_sim.flow_info[tun_key].b4_jump[tun_time] = len(tun_value.standby_path.path)
                                g_sim.flow_info[tun_key].b4_delay[tun_time] = tun_value.standby_path.delay
                            else:
                                g_sim.flow_info[tun_key].b4_path[tun_time] = []
                                g_sim.flow_info[tun_key].b4_jump[tun_time] = 0
                                g_sim.flow_info[tun_key].b4_delay[tun_time] = 0

                        g_sim.flow_info[tun_key].bandwidth[tun_time] = tun_value.throughput
                        # 默认基于tunnel创建的流量,是贯穿于整个tunnel存续时间的,所以一旦发现某次的tunnel时间小,则把start_time赋予这个小的值  
                        if tun_time < g_sim.flow_info[tun_key].start_time:
                            g_sim.flow_info[tun_key].start_time = tun_time

        info_logger.error("===========see see g_sim.flow_info keys:%s"%(g_sim.flow_info.keys()))
                
        all_flow_num = base_tun_creat_num + input_flow_num
        print("aaaa===all flow num:",all_flow_num)
        
        info_logger.error("all_flow_num:%d"%(all_flow_num))
        return all_flow_num
    except Exception as e:
        print("load_flow Exception:", e)
        info_logger.error(e)
        error_logger.error(e) 
        return 0 

def save_tunnel_occupy_current_bandwidth(): 
    try:
        """保存tunnel流的变化情况
        
        Args:
            none
        Returns:
            none
        Raise:
            none
        """
        
        if g_sim.object_tunnel_flow:
            for tun_time, value in g_tunrec.sim_orgtuns.items():
                g_tunrec.occupy_cur[tun_time] = {}
                temp = g_tunrec.occupy_cur[tun_time]
                for tunnid in value.keys():
                    temp[tunnid] = [value[tunnid].throughput, 2 * (value[tunnid].throughput)]
        else:
            for tun_time, value in g_tunrec.sim_orgtuns.items():
                g_tunrec.occupy_cur[tun_time] = {}
                temp = g_tunrec.occupy_cur[tun_time]
                for tunnid in value.keys():
                    temp[tunnid] = [value[tunnid].throughput, value[tunnid].throughput]
        
        if g_sim.object_input_flow:
            for _, value in g_sim.flow_info.items():
                if value.tun_name != '' and value.orgin == 'model':
                    tunnid = value.src_id + value.tun_name
                    for s_time in value.bandwidth.keys():
                        if s_time in g_tunrec.occupy_cur.keys():
                            if tunnid in g_tunrec.occupy_cur[s_time].keys():
                                g_tunrec.occupy_cur[s_time][tunnid][1] += value.bandwidth[s_time]
    except Exception as e:
        print("save_tunnel_occupy_current_bandwidth Exception:", e)
        info_logger.error(e)
        error_logger.error(e) 

#sprint 3 add
def copy_inherit_topo():
    try:
        """继承仿真时，左右两侧的flows采用最后添加的所有的flows;
        左侧的TOPO跟上次仿真的TOPO右侧的TOPO一样;右侧的topo采用仿真定义的topo
        
        Args:
            none
        Returns:
            none
        Raise:
            none
        """
        # 如果flow和TOPO信息都没有，则返回错误
        if not g_dt.phy_topo:
            return ErrCode.FAILED
    
        # sprint3 modify,继承仿真，仿真分析左页面呈现的TOPO是继承的上一次仿真的右侧页面的TOPO
        g_sim.topo.node_num = g_sim.af_topo.node_num
        g_sim.topo.link_num = g_sim.af_topo.link_num
        g_sim.topo.fault_num = g_sim.af_topo.fault_num
        g_sim.topo.nodes.clear() # 清除上次保存的数据
        g_sim.topo.nodes = copy.deepcopy(g_sim.af_topo.nodes)
        g_sim.topo.links.clear()
        g_sim.topo.links = copy.deepcopy(g_sim.af_topo.links)

        # sprint3 modify,继承仿真，仿真分析左页面呈现的TOPO是继承的上一次仿真的右侧页面的TOPO
        g_sim.l3_topo.node_num = g_sim.af_l3_topo.node_num
        g_sim.l3_topo.link_num = g_sim.af_l3_topo.link_num
        g_sim.l3_topo.nodes.clear() 
        g_sim.l3_topo.nodes = copy.deepcopy(g_sim.af_l3_topo.nodes)
        g_sim.l3_topo.links.clear()
        g_sim.l3_topo.links = copy.deepcopy(g_sim.af_l3_topo.links)

        # sprint3 modify,继承仿真，仿真分析的右页面的TOPO，用的是故障定义后最新的TOPO
        g_sim.af_topo.node_num = g_dt.phy_topo.node_num
        g_sim.af_topo.link_num = g_dt.phy_topo.link_num
        g_sim.af_topo.fault_num = g_dt.phy_topo.fault_num
        g_sim.af_topo.nodes.clear()
        g_sim.af_topo.nodes = copy.deepcopy(g_dt.phy_topo.nodes)
        g_sim.af_topo.links.clear()
        g_sim.af_topo.links = copy.deepcopy(g_dt.phy_topo.links)

        # sprint3 modify,故障后的三层topo，保存跟设置时的一样
        g_sim.af_l3_topo.node_num = g_dt.l3_topo.node_num
        g_sim.af_l3_topo.link_num = g_dt.l3_topo.link_num
        g_sim.af_l3_topo.nodes.clear()
        g_sim.af_l3_topo.nodes = copy.deepcopy(g_dt.l3_topo.nodes)
        g_sim.af_l3_topo.links.clear()
        g_sim.af_l3_topo.links = copy.deepcopy(g_dt.l3_topo.links)

        return ErrCode.SUCCESS
    except Exception as e:
        print("copy_inherit_topo Exception:", e)
        info_logger.error(e)
        error_logger.error(e) 
        return ErrCode.FAILED

def copy_inherit_topo_and_flow():
    try:
        """继承仿真时，左右两侧的flows采用最后添加的所有的flows;
        左侧的TOPO跟上次仿真的TOPO右侧的TOPO一样;右侧的topo采用仿真定义的topo
        
        Args:
            none
        Returns:
            none
        Raise:
            none
        """
        # 如果flow和TOPO信息都没有，则返回错误
        if not g_allFlows and not g_dt.phy_topo:
            return ErrCode.FAILED

        if not g_allFlows:
            sim_rate.sim_org_flow_num = 0
            print("! Flows is None !")
        else:
            if g_sim.object_input_flow:
                sim_rate.sim_org_flow_num = len(g_allFlows)
                for key, value in g_allFlows.items():
                    start_time = value.start_time
                    end_time = value.end_time
                    # 流量时间不在仿真时间范围内，不添加仿真
                    if start_time >= g_sim.time_end or end_time <= g_sim.time_start:
                        continue
                    g_sim.flow_info[key] = copy.deepcopy(value)
            else:
                sim_rate.sim_org_flow_num = 0
        
        # sprint3 modify,继承仿真，仿真分析左页面呈现的TOPO是继承的上一次仿真的右侧页面的TOPO
        g_sim.topo.node_num = g_sim.af_topo.node_num
        g_sim.topo.link_num = g_sim.af_topo.link_num
        g_sim.topo.fault_num = g_sim.af_topo.fault_num
        g_sim.topo.nodes.clear() # 清除上次保存的数据
        g_sim.topo.nodes = copy.deepcopy(g_sim.af_topo.nodes)
        g_sim.topo.links.clear()
        g_sim.topo.links = copy.deepcopy(g_sim.af_topo.links)

        # sprint3 modify,继承仿真，仿真分析左页面呈现的TOPO是继承的上一次仿真的右侧页面的TOPO
        g_sim.l3_topo.node_num = g_sim.af_l3_topo.node_num
        g_sim.l3_topo.link_num = g_sim.af_l3_topo.link_num
        g_sim.l3_topo.nodes.clear() 
        g_sim.l3_topo.nodes = copy.deepcopy(g_sim.af_l3_topo.nodes)
        g_sim.l3_topo.links.clear()
        g_sim.l3_topo.links = copy.deepcopy(g_sim.af_l3_topo.links)

        # sprint3 modify,继承仿真，仿真分析的右页面的TOPO，用的是故障定义后最新的TOPO
        g_sim.af_topo.node_num = g_dt.phy_topo.node_num
        g_sim.af_topo.link_num = g_dt.phy_topo.link_num
        g_sim.af_topo.fault_num = g_dt.phy_topo.fault_num
        g_sim.af_topo.nodes.clear()
        g_sim.af_topo.nodes = copy.deepcopy(g_dt.phy_topo.nodes)
        g_sim.af_topo.links.clear()
        g_sim.af_topo.links = copy.deepcopy(g_dt.phy_topo.links)

        # sprint3 modify,故障后的三层topo，保存跟设置时的一样
        g_sim.af_l3_topo.node_num = g_dt.l3_topo.node_num
        g_sim.af_l3_topo.link_num = g_dt.l3_topo.link_num
        g_sim.af_l3_topo.nodes.clear()
        g_sim.af_l3_topo.nodes = copy.deepcopy(g_dt.l3_topo.nodes)
        g_sim.af_l3_topo.links.clear()
        g_sim.af_l3_topo.links = copy.deepcopy(g_dt.l3_topo.links)

        return ErrCode.SUCCESS
    except Exception as e:
        print("copy_inherit_topo_and_flow Exception:", e)
        info_logger.error(e)
        error_logger.error(e) 
        return ErrCode.FAILED

def calc_link_static_info():
    try:
        """获得故障前、后，链路的最大利用率级链路的带宽利用率超过100%的链路个数
        
        Args:
            none
        Returns:
            none
        Raise:
            none
        """
        more_than_100_list = [] # 记录故障前带宽利用率超过100的链路ID
        before_hun = 0 # 故障前，带宽利用率的超过100的链路个数统计
        before_max = 0 # 故障前，带宽利用率的最大值

        after_more_than_100_list = [] # 记录故障后带宽利用率超过100的链路ID
        after_hun = 0 # 故障后，带宽利用率的超过100的链路个数统计
        after_max = 0 # 故障后，带宽利用率的最大值

        for _, value in g_sim.before_fault_link_info.items():
            all_link_info = value.link_info
            # 轮询各个时刻下的所有的链路
            for key in all_link_info:
                one_link_info = all_link_info[key]
                one_Link_a_b = one_link_info.a_to_b
                one_Link_b_a = one_link_info.b_to_a

                # 如果带宽利用率超过原来记录的最大的带宽利用率，则把这个值进行保存
                if one_Link_a_b.out_use_ratio > before_max:
                    before_max = one_Link_a_b.out_use_ratio
                if one_Link_b_a.out_use_ratio > before_max:
                    before_max = one_Link_b_a.out_use_ratio
                
                # 带宽利用率大于100,且这个链路从来未曾被统计过，则把带宽利用率大于100的统计进行加一的操作
                if one_Link_a_b.out_use_ratio >= 100 or one_Link_b_a.out_use_ratio >= 100:
                    if key not in more_than_100_list:
                        more_than_100_list.append(key) 
                        before_hun +=1   

        for _, value in g_sim.after_fault_link_info.items():
            all_link_info = value.link_info

            for key in all_link_info:
                one_link_info = all_link_info[key]
                one_Link_a_b = one_link_info.a_to_b
                one_Link_b_a = one_link_info.b_to_a
                if one_Link_a_b.out_use_ratio > after_max:
                    after_max = one_Link_a_b.out_use_ratio
                if one_Link_b_a.out_use_ratio > after_max:
                    after_max = one_Link_b_a.out_use_ratio
                
                if one_Link_a_b.out_use_ratio >= 100 or one_Link_b_a.out_use_ratio >= 100:
                    if key not in after_more_than_100_list:
                        after_more_than_100_list.append(key) 
                        after_hun +=1  

        if 'before' in g_sim.sim_step_statis.keys():
            g_sim.sim_step_statis['before'].overload_100_link_num = before_hun 
            g_sim.sim_step_statis['before'].link_max_used_ratio = before_max 

        if 'after' in g_sim.sim_step_statis.keys():        
            g_sim.sim_step_statis['after'].overload_100_link_num = after_hun 
            g_sim.sim_step_statis['after'].link_max_used_ratio = after_max  
    except Exception as e:
        print("calc_link_static_info Exception:", e)
        info_logger.error(e)
        error_logger.error(e) 


def simulate_clear():
    try:
        g_sim.statis_flow.clear()
        # g_sim.flow_info.clear() # sprint 4 这里不清除流量
        g_sim.all_fault.clear()
        g_sim.flow_list_before_fault.clear()
        g_sim.flow_list_after_fault.clear()
    except Exception as e:
        print("simulate_clear Exception:", e)
        info_logger.error(e)
        error_logger.error(e) 
    
def record_sim_static_start_time():
    try:
        """保存仿真的统计信息中的时间信息
        
        Args:
            none
        Returns:
            none
        Raise:
            none
        """
        
        simulate_time = datetime.now() 
        g_sim.sim_step_statis['before'] = SimStepStatisAll('before')
        g_sim.sim_step_statis['before'].sim_creat_time = datetime.strftime(simulate_time,'%Y-%m-%d %H:%M:%S')
        g_sim.sim_step_statis['after'] = SimStepStatisAll('after')
        g_sim.sim_step_statis['after'].sim_creat_time = g_sim.sim_step_statis['before'].sim_creat_time

    except Exception as e:
        print("record_sim_static_start_time Exception:", e)
        info_logger.error(e)
        error_logger.error(e) 

def save_sim_static_start_time():
    try:
        """保存仿真的统计信息中的时间信息
        
        Args:
            none
        Returns:
            none
        Raise:
            none
        """
        timeStamp = float(g_sim.time_sim_info[-1]["end_time"]/1000) 
        timeArray = time.localtime(timeStamp) 
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

        if 'before' in g_sim.sim_step_statis.keys():
            g_sim.sim_step_statis['before'].sim_net_start_time = otherStyleTime
        if 'after' in g_sim.sim_step_statis.keys():
            g_sim.sim_step_statis['after'].sim_net_start_time = otherStyleTime

    except Exception as e:
        print("save_sim_static_start_time Exception:", e)
        info_logger.error(e)
        error_logger.error(e) 


def record_sim_static_info():
    try:
        """保存仿真的统计信息中的除了仿真开始时间之外的其他信息   
        Args:
            none
        Returns:
            none
        Raise:
            none
        """  
        # 避免多人操作,数据同步时清空了却还来使用
        if 'before' not in g_sim.sim_step_statis.keys() or 'after' not in g_sim.sim_step_statis.keys():
            return

        g_sim.sim_step_statis['before'].cycle_num = g_sim.time_section
        g_sim.sim_step_statis['after'].cycle_num = g_sim.time_section
        if g_sim.time_cycle == 3600000:
            g_sim.sim_step_statis['before'].cycle = '1hour'
            g_sim.sim_step_statis['after'].cycle = '1hour'
        elif g_sim.time_cycle == 1800000:
            g_sim.sim_step_statis['before'].cycle = '30min'
            g_sim.sim_step_statis['after'].cycle = '30min'
        elif g_sim.time_cycle == 86400000:
            g_sim.sim_step_statis['before'].cycle = '1day'
            g_sim.sim_step_statis['after'].cycle = '1day'
        else:
            second = str(int(g_sim.time_cycle / 1000))+'second'
            g_sim.sim_step_statis['before'].cycle = second
            g_sim.sim_step_statis['after'].cycle = second
        
        #sim_rate.sim_b4_flow_num = cal_before_fault_flow_num()
        #g_sim.sim_step_statis['before'].flow_num = sim_rate.sim_b4_flow_num 

        sim_rate.sim_after_flow_num = cal_after_fault_flow_num()
        g_sim.sim_step_statis['after'].flow_num = sim_rate.sim_after_flow_num  

        # tunnel 条数
        be_tun_num = 0
        af_tun_num = 0
        last_st_time = g_sim.time_sim_info[-1]['start_time']
        if last_st_time in g_tunrec.sim_b4tuns.keys():
            b4_tuninfo = g_tunrec.sim_b4tuns[last_st_time]
            for tunid in b4_tuninfo.keys():
                if b4_tuninfo[tunid].status == 'UP':
                    be_tun_num += 1
        else:
            error_logger.error("sim_orgtuns keys:%s"%(g_tunrec.sim_orgtuns.keys()))
            error_logger.error("keys:%s"%(g_tunrec.sim_b4tuns.keys()))
            error_logger.error("time %d not in b4_tun keys"%(last_st_time))
        
        if last_st_time in g_tunrec.sim_aftuns.keys():
            af_tuninfo = g_tunrec.sim_aftuns[last_st_time]
            for tunid in af_tuninfo.keys():
                if af_tuninfo[tunid].status == 'UP':
                    af_tun_num += 1
        else:
            error_logger.error("keys:%s"%(g_tunrec.sim_aftuns.keys()))
            error_logger.error("time %d not in b4_tun keys"%(last_st_time))

        g_sim.sim_step_statis['before'].tunnel_num = be_tun_num
        g_sim.sim_step_statis['after'].tunnel_num  = af_tun_num
    except Exception as e:
        print("record_sim_static_info Exception:", e)
        info_logger.error(e)
        error_logger.error(e) 

####################################################
# 仿真主流程
####################################################
def simulate_processing(input_data):
    try:
        """仿真主流程
        
        Args:
            none
        Returns:
            none
        Raise:
            none
        """
        if g_sim.stop_simulate_flag != 1:
            # 仿真的流程,最开始是数据加载阶段
            sim_rate.sim_step = 'dataLoad'

            # 获得仿真开始的系统时间
            sim_rate.init_simulate_status()

            # 保存操作时的时间信息,便于在统计信息里展示
            record_sim_static_start_time()

            # 开始清除数据 
            assemb_data_sim_message(SimDataSyncCode.SIM_CLEAR_DATA_BEGIN)
            delay_s(0.1)

        if g_sim.stop_simulate_flag != 1:
            # 清除数据
            simulate_clear()
            assemb_data_sim_message(SimDataSyncCode.SIM_CLERA_DATA_SUCCESS)
            delay_s(0.1)

            # 保存参数
            save_sim_parm(input_data)  
            delay_s(0.1)

            # 添加“保存TOPO”这个message
            assemb_data_sim_message(SimDataSyncCode.SIM_SAVE_TOPO_BEGIN)
            delay_s(0.1)

        if g_sim.stop_simulate_flag != 1:
            # 重新仿真或首次仿真时，保留两份topo
            if g_sim.inherit_flag == False:
            
                ret = copy_topo() 
                if ret != ErrCode.SUCCESS:
                    SIMLATAE_STATE_LOCK.acquire()
                    g_sim.status = 2
                    g_thd_ident.clear()
                    SIMLATAE_STATE_LOCK.release()
                    sim_rate.sim_step = 'stop'
                    return   
            else:
                ret = copy_inherit_topo()
                if ret != ErrCode.SUCCESS:
                    SIMLATAE_STATE_LOCK.acquire()
                    g_sim.status = 2
                    g_thd_ident.clear()
                    SIMLATAE_STATE_LOCK.release()
                    sim_rate.sim_step = 'stop'
                    return    

        # 创建定义前后的dijkstra图
        if g_sim.stop_simulate_flag != 1:
            built_before_dijkstra_network()
            built_after_fault_dijkstra_network()

        # sprint 4 open
        if g_sim.inherit_flag == False and g_sim.stop_simulate_flag != 1:
            ret = split_time_flow()
            #ret = split_time_flow_sprint3()

        if g_sim.stop_simulate_flag != 1:
            assemb_data_sim_message(SimDataSyncCode.SIM_SAVE_TOPO_SUCCESS)
            delay_s(0.5)

        if g_sim.stop_simulate_flag != 1:
            assemb_data_sim_message(SimDataSyncCode.SIM_SYNC_DATA_BEGIN)
            delay_s(0.5)

        if g_sim.stop_simulate_flag != 1 and g_sim.inherit_flag == False: 
            # 进行数据加载记录
            load_data()

            #仿真分析链路质量接口
            get_link_availabilities()
            # 这两个函数在下一阶段，按时间段获取的时候，还是需要使用的，勿删
            separ_tunnel()
            save_all_tunnel_standby_path()
            save_one_time_org_tunnel()
            sim_rate.sim_org_flow_num = load_flow()
            save_tunnel_occupy_current_bandwidth()

        if g_sim.stop_simulate_flag != 1:
            assemb_data_sim_message(SimDataSyncCode.SIM_SYNC_DATA_FINISH)
            #加载完数据调到故障前放置的速度太快了，加载完100%，需要做停留
            delay_s(1)
            sim_rate.sim_step = 'beforeFault'

        if g_sim.stop_simulate_flag != 1:    
            sim_rate.sim_b4_flow_sim_progress = 5
            delay_s(1)
            ret = before_fault_simulate()       
            delay_s(0.5)
            sim_rate.sim_b4_flow_sim_progress = 100
            sim_rate.sim_b4_data_pre_progress = 100
            sim_rate.sim_b4_route_sim_progress = 100
        
            # 完成100%的时候，需要停顿一下，否则前台界面收不到100%的信息
            delay_s(1)

        if g_sim.stop_simulate_flag != 1:
            sim_rate.sim_step = 'afterFault'
            sim_rate.sim_after_flow_sim_progress = 0        

        if g_sim.stop_simulate_flag != 1:    
            #  注，这个函数里有累加sim_after_flow_sim_progress的值
            ret = after_fault_simulate()

        if g_sim.stop_simulate_flag != 1:    
            sim_rate.sim_after_flow_sim_progress = 90
            delay_s(0.5)

        if g_sim.stop_simulate_flag != 1:
            save_flow_info_to_sim_flow_list()  
            sim_rate.sim_after_flow_sim_progress = 91

        if g_sim.stop_simulate_flag != 1: 
            # 统计带宽利用率等信息
            calc_link_static_info()
            sim_rate.sim_after_flow_sim_progress = 92
            delay_s(0.5)

        if g_sim.stop_simulate_flag != 1: 
            # 计算tunnel状态变化信息
            cmp_before_after_tunnel()
            sim_rate.sim_after_flow_sim_progress = 95
            
        if g_sim.stop_simulate_flag != 1 and (g_sim.object_input_flow == True or g_sim.object_tunnel_flow == True):
            # 计算流量仿真统计信息
            count_flows_diff_info()

        if g_sim.stop_simulate_flag != 1:
            #记录仿真统计信息的时间  
            save_sim_static_start_time()

        if g_sim.stop_simulate_flag != 1: 
            # leijuyan 阈值由前台下发初始的默认的阈值范围，或者前后台写死
            g_ana.analyse_time = g_sim.time_sim_info[0]['start_time']
            g_ana.analyse_start_time = g_sim.time_sim_info[0]['start_time'] 
            g_ana.analyse_end_time = g_sim.time_sim_info[0]['end_time']
            g_ana.analyse_firstStepEnd = 25
            g_ana.analyse_secondStepEnd = 75
            g_ana.analyse_thirdStepEnd = 90

            cal_load_info_by_threshold(g_sim.time_sim_info[0]['start_time'], g_ana.analyse_thirdStepEnd)

        if g_sim.stop_simulate_flag != 1:
            record_sim_static_info()

        if g_sim.stop_simulate_flag != 1:
            # 提前生成好报表的部分文件
            report_xls_in_advance()

            SIMLATAE_STATE_LOCK.acquire()
            if g_sim.status != 2: 
                g_sim.status = 1
                g_thd_ident.clear()
            SIMLATAE_STATE_LOCK.release()

        if g_sim.stop_simulate_flag == 1: 
            SIMLATAE_STATE_LOCK.acquire()
            g_sim.status = 2
            sim_rate.sim_step = 'stop'
            g_thd_ident.clear()
            SIMLATAE_STATE_LOCK.release()

        if g_sim.stop_simulate_flag != 1: 
            sim_rate.sim_after_data_pre_progress = 100
            sim_rate.sim_after_route_sim_progress = 100
            sim_rate.sim_after_flow_sim_progress = 100 
        
            # 完成100%的时候，需要停顿一下，否则前台界面收不到100%的信息
            delay_s(1)
            sim_rate.sim_step = 'finish'
        
        if debug_postman:
            print('\nSimulate finshed ! \n')

        return ErrCode.SUCCESS
    except Exception as e:
        print("simulate_processing Exception:", e)
        info_logger.error(e)
        error_logger.error(e) 
        return ErrCode.FAILED

def start_simulate(input_data):
    try:
        """开始仿真
        
        Args:
            input_data:仿真的参数
        Returns:
            none
        Raise:
            none
        """ 
        SIMLATAE_STATE_LOCK.acquire()
        other_in_sim = False
        if g_sim.status == 3:
            other_in_sim = True
        else:
            g_sim.status = 3 
            g_sim.stop_simulate_flag = 0
        SIMLATAE_STATE_LOCK.release()
        
        if other_in_sim == True:
            return ErrCode.OTHERS_IN_SIMILATING

        SIMLATAE_STATE_LOCK.acquire()
        simulate_thd = threading.Thread(target = simulate_processing, args = (input_data,))
        simulate_thd.start()
        g_thd_ident.append(simulate_thd.ident)
        SIMLATAE_STATE_LOCK.release()

        return ErrCode.SUCCESS
    except Exception as e:
        print("start_simulate Exception:", e)
        info_logger.error(e)
        error_logger.error(e) 
        return ErrCode.FAILED

def stop_thread(ident, exctype = SystemExit):
    try:
        tid = ctypes.c_long(ident)

        if not inspect.isclass(exctype):
            exctype = type(SystemExit)

        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
        return res
    except Exception as e:
        print("stop_thread Exception:", e)
        info_logger.error(e)
        error_logger.error(e) 
        return None   

def stop_simulate():
    try:
        SIMLATAE_STATE_LOCK.acquire()
        if g_sim.status == 3:      
            sim_rate.sim_step = 'stop'
            res = 1
            for i in g_thd_ident:
                res = stop_thread(i, SystemExit)
    
            g_sim.status = 2 
            g_sim.stop_simulate_flag = 1
            g_thd_ident.clear()
            g_sim.clear_info()
            SIMLATAE_STATE_LOCK.release()
            if res == 1:
                return ErrCode.SUCCESS
            else:
                return ErrCode.FAILED
        # 多人操作时候，返回前台success 以便于回到故障仿真主界面
        else:
            SIMLATAE_STATE_LOCK.release()
            return ErrCode.SUCCESS
    except Exception as e:
        print("stop_simulate Exception:", e)
        info_logger.error(e)
        error_logger.error(e) 
        return ErrCode.FAILED

def set_re_sim(reSimType):
    try:
        if reSimType == "inheritSim":
            # 继承仿真
            g_sim.inherit_flag = True
            sim_rate.sim_step = 0
        else:
            # 清除数据状态
            g_dt.init_data_status()
            
            g_allFlows.clear()
            
            # 清除仿真信息,并且把继承仿真的标志设置为False
            g_sim.clear_info()
            sim_rate.sim_step = 0
        return ErrCode.SUCCESS
    except Exception as e:
        info_logger.error(e)
        error_logger.error(e)
        print("set_re_sim Exception:", e)
        return ErrCode.FAILED

def cal_tunnel_paths_delay(flag, paths,startTime):
    """计算从仿真控制器回来的所有tunnel 链路的时延
    
    Args:
        flag：
        paths：["linkid1", "linkid2","linkid3"]
    Returns:
        none
    Raise:
        none
    """
    try: 
        delay = 0
        
        if flag == "after_fault":
            for one_link in paths:
                print("input:", startTime)
                print("keys1",g_sim.af_l3_topo.links[one_link].delay.keys())
                delay += g_sim.af_l3_topo.links[one_link].delay[startTime]
        else:
            for one_link in paths:
                print("input:", startTime)
                print("keys1",g_sim.l3_topo.links[one_link].delay.keys())
                delay += g_sim.l3_topo.links[one_link].delay[startTime] # 判断key是否存在。
        return delay
    except Exception as e:
        delay = 0
        info_logger.error(e)
        error_logger.error(e)
        print("cal_tunnel_paths_delay:", e)
        return delay


def get_link_availabilities():
    """查询链路质量信息,轮询时间段，解析数据，存储到g_sim.l3_topo.links[key].jittery等里

    Args:
        none
    Returns:
        none
    Raise:
        ErrCode.SUCCESS
    """
    try:
        start_time = g_sim.time_start
        end_time = g_sim.time_end
        cycle = g_sim.time_cycle
        cycle_num = int(g_sim.time_cycle_num)

        one_cycle_start = start_time
        one_cycle_end_time = min(start_time + cycle, end_time)
        linkList = []
       
        for linkid in g_sim.topo.links:  # 物理链路id
            linkList.append(linkid)
        # 前面n-1次均取一整个周期的数据
        for _ in range(cycle_num):
            data = get_link_availability(one_cycle_start, one_cycle_end_time, linkList)
            print("从zhangzhenwei处取回的链路质量信息为：")
            print(data)
            if data != None:
                parse_link_availabilty(one_cycle_start, data)
                
            else:
                print("the result of link availablity from big data is None,make up dafault value.")
                default_link_availabilty(one_cycle_start,linkList)

            # 把这一时间段的链路质量信息按时间切片的方式保存
            sim_end_time = get_end_time(one_cycle_start)
            if one_cycle_end_time != sim_end_time:
                copy_all_linkd_aviliablities(one_cycle_start, sim_end_time, one_cycle_end_time)
            one_cycle_start = one_cycle_end_time
            one_cycle_end_time = min(one_cycle_start + cycle, end_time)

        # 这是一个很恶心的问题，测到有时候，发下去10条链路，但是大数据只回复了8条链路，所以为了避免，再遍历一下所有的链路
        for time_info in g_sim.time_sim_info:
            sim_start_time = time_info["start_time"]
            for key in g_sim.l3_topo.links:
                if sim_start_time not in g_sim.l3_topo.links[key].delay.keys():
                    info_logger.error("%d not linkid:%s in delay keys:%s"%(sim_start_time, key, g_sim.l3_topo.links[key].delay.keys()))
                    g_sim.l3_topo.links[key].delay[sim_start_time] = 0
                    g_sim.af_l3_topo.links[key].delay[sim_start_time] = 0
                if sim_start_time not in g_sim.l3_topo.links[key].jittery.keys():
                    info_logger.error("%d not linkid:%s in jittery keys:%s"%(sim_start_time, key, g_sim.l3_topo.links[key].jittery.keys()))

                    g_sim.l3_topo.links[key].jittery[sim_start_time] = 0
                    g_sim.af_l3_topo.links[key].jittery[sim_start_time] = 0
                if sim_start_time not in g_sim.l3_topo.links[key].loss_rate.keys():
                    info_logger.error("%d not linkid:%s in loss_rate keys:%s"%(sim_start_time, key, g_sim.l3_topo.links[key].loss_rate.keys()))
                    g_sim.l3_topo.links[key].loss_rate[sim_start_time] = 0
                    g_sim.af_l3_topo.links[key].loss_rate[sim_start_time] = 0

        return ErrCode.SUCCESS
    except Exception as e:
        print("load_data Exception:", e)
        error_logger.error(e)
        info_logger.error(e)
        return ErrCode.FAILED


def default_link_availabilty(start_time, linkList):
    try:
        for linkId in linkList:
            l3_link_pos_id = g_sim.topo.links[linkId].l3_link_id[0]
            l3_link_neg_id = g_sim.topo.links[linkId].l3_link_id[1]
            if l3_link_pos_id in g_sim.l3_topo.links.keys() and l3_link_neg_id in g_sim.l3_topo.links.keys():
                g_sim.l3_topo.links[l3_link_pos_id].jittery[start_time] =0 # 选择时间段内平均 源到目的 方向抖动 正方向
                g_sim.l3_topo.links[l3_link_neg_id].jittery[start_time] = 0 # 选择时间段内平均 目的到源 方向抖动 负方向
                g_sim.af_l3_topo.links[l3_link_pos_id].jittery[start_time] = 0 # 选择时间段内平均 源到目的 方向抖动 正方向
                g_sim.af_l3_topo.links[l3_link_neg_id].jittery[start_time] = 0 # 选择时间段内平均 目的到源 方向抖动 负方向

                g_sim.l3_topo.links[l3_link_pos_id].delay[start_time] = 0 # 选择时间段内平均时延
                g_sim.l3_topo.links[l3_link_neg_id].delay[start_time] = 0 # 选择时间段内平均时延
                g_sim.af_l3_topo.links[l3_link_pos_id].delay[start_time] = 0 # 选择时间段内平均时延
                g_sim.af_l3_topo.links[l3_link_neg_id].delay[start_time] = 0 # 选择时间段内平均时延

                g_sim.l3_topo.links[l3_link_pos_id].loss_rate[start_time] = 0 # 选择时间段内平均丢包率
                g_sim.l3_topo.links[l3_link_neg_id].loss_rate[start_time] = 0 # 选择时间段内平均丢包率
                g_sim.af_l3_topo.links[l3_link_pos_id].loss_rate[start_time] = 0 # 选择时间段内平均时延
                g_sim.af_l3_topo.links[l3_link_neg_id].loss_rate[start_time] = 0 # 选择时间段内平均时延
    except Exception as e:
        print("default_link_availabilty Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.FAILED


def parse_link_availabilty(start_time, data):
    """
    解析从大数据返回的数据，获取抖动、时延、丢包率的平均值。
    Args:
        data: 从大数据返回的数据

    Returns:
        是否解析成功
        self.delay = -1  # ms,时延
        self.loss_rate = -1  # %，丢包率
        self.jitter = -1  # ms，抖动
        self.priority = 1  # 1-5，优先级
    """
    try:
        for linkId in data:
            l3_link_pos_id = g_sim.topo.links[linkId].l3_link_id[0]
            l3_link_neg_id = g_sim.topo.links[linkId].l3_link_id[1]
            if l3_link_pos_id in g_sim.l3_topo.links.keys() and l3_link_neg_id in g_sim.l3_topo.links.keys():
                if len(data[linkId]) > 0:
                    msg = data[linkId][0]
                    info_logger.error("msg:%s"%(msg))
                    if "negAvgSD" in msg.keys():
                        g_sim.l3_topo.links[l3_link_neg_id].jittery[start_time] = msg['negAvgSD'] # 选择时间段内平均 目的到源 方向抖动 负方向
                        g_sim.af_l3_topo.links[l3_link_neg_id].jittery[start_time] = msg['negAvgSD'] # 选择时间段内平均 目的到源 方向抖动 负方向
                    else:
                        g_sim.l3_topo.links[l3_link_neg_id].jittery[start_time] = 0 # 选择时间段内平均 目的到源 方向抖动 负方向
                        g_sim.af_l3_topo.links[l3_link_neg_id].jittery[start_time] = 0 # 选择时间段内平均 目的到源 方向抖动 负方向

                    if "posAvgSD" in msg.keys():
                        g_sim.l3_topo.links[l3_link_pos_id].jittery[start_time] = msg['posAvgSD'] # 选择时间段内平均 源到目的 方向抖动 正方向
                        g_sim.af_l3_topo.links[l3_link_pos_id].jittery[start_time] = msg['posAvgSD'] # 选择时间段内平均 源到目的 方向抖动 正方向
                    else:
                        g_sim.l3_topo.links[l3_link_pos_id].jittery[start_time] = 0 # 选择时间段内平均 源到目的 方向抖动 正方向
                        g_sim.af_l3_topo.links[l3_link_pos_id].jittery[start_time] = 0 # 选择时间段内平均 源到目的 方向抖动 正方向
                    
                    if "avgRtt" in msg.keys():
                        g_sim.l3_topo.links[l3_link_pos_id].delay[start_time] = msg['avgRtt'] # 选择时间段内平均时延
                        g_sim.l3_topo.links[l3_link_neg_id].delay[start_time] = msg['avgRtt'] # 选择时间段内平均时延
                        g_sim.af_l3_topo.links[l3_link_pos_id].delay[start_time] = msg['avgRtt'] # 选择时间段内平均时延
                        g_sim.af_l3_topo.links[l3_link_neg_id].delay[start_time] = msg['avgRtt'] # 选择时间段内平均时延
                    else:
                        g_sim.l3_topo.links[l3_link_pos_id].delay[start_time] = 0  
                        g_sim.l3_topo.links[l3_link_neg_id].delay[start_time] = 0 
                        g_sim.af_l3_topo.links[l3_link_pos_id].delay[start_time] = 0 
                        g_sim.af_l3_topo.links[l3_link_neg_id].delay[start_time] = 0 

                    if "lossRatio" in msg.keys():
                        g_sim.l3_topo.links[l3_link_pos_id].loss_rate[start_time] = msg['lossRatio'] # 选择时间段内平均丢包率
                        g_sim.l3_topo.links[l3_link_neg_id].loss_rate[start_time] = msg['lossRatio'] # 选择时间段内平均丢包率
                        g_sim.af_l3_topo.links[l3_link_pos_id].loss_rate[start_time] = msg['lossRatio'] # 选择时间段内平均时延
                        g_sim.af_l3_topo.links[l3_link_neg_id].loss_rate[start_time] = msg['lossRatio'] # 选择时间段内平均时延
                    else:
                        g_sim.l3_topo.links[l3_link_pos_id].loss_rate[start_time] = 0 # 选择时间段内平均丢包率
                        g_sim.l3_topo.links[l3_link_neg_id].loss_rate[start_time] = 0 # 选择时间段内平均丢包率
                        g_sim.af_l3_topo.links[l3_link_pos_id].loss_rate[start_time] = 0 # 选择时间段内平均时延
                        g_sim.af_l3_topo.links[l3_link_neg_id].loss_rate[start_time] = 0 # 选择时间段内平均时延
                else:
                    # 无数据时填充成默认值
                    info_logger.error("time:%d, data:%s"%(start_time,data))
                    g_sim.l3_topo.links[l3_link_neg_id].jittery[start_time] = 0 
                    g_sim.af_l3_topo.links[l3_link_neg_id].jittery[start_time] = 0

                    g_sim.l3_topo.links[l3_link_pos_id].jittery[start_time] = 0
                    g_sim.af_l3_topo.links[l3_link_pos_id].jittery[start_time] = 0

                    g_sim.l3_topo.links[l3_link_pos_id].delay[start_time] = 0  
                    g_sim.l3_topo.links[l3_link_neg_id].delay[start_time] = 0 

                    g_sim.af_l3_topo.links[l3_link_pos_id].delay[start_time] = 0 
                    g_sim.af_l3_topo.links[l3_link_neg_id].delay[start_time] = 0 

                    g_sim.l3_topo.links[l3_link_pos_id].loss_rate[start_time] = 0 
                    g_sim.l3_topo.links[l3_link_neg_id].loss_rate[start_time] = 0

                    g_sim.af_l3_topo.links[l3_link_pos_id].loss_rate[start_time] = 0 
                    g_sim.af_l3_topo.links[l3_link_neg_id].loss_rate[start_time] = 0 
                    
    except Exception as e:
        print("parse_link_availabilty Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.FAILED

    return ErrCode.SUCCESS
