# -*- encoding: utf-8 -*-
"""
@File    : sdnsimctrl.py
@Time    : 2019/10/08 17:13:00
@License : Copyright (c) 2004-2019 New H3C Tech. Co., Ltd. All rights reserved.
@Desc    : sdn 仿真控制器的接口
"""
import requests
import json
import operator

from apps.util import g_dt, g_sim, g_tunrec, g_sdnply
from apps.util import info_logger, error_logger

from apps.errcode import ErrCode
from apps.v1_0.application import get_slainfo_by_groupid, get_bandwidth_by_groupid
from apps.v1_0.test import *

if debug_postman:
    headers={"content-type":"application/json","iam-role":"admin","X-Auth-Token":token} 
    SDN_CONTROLLER_URI = 'http://10.99.211.108:8383'
else:
    SDN_CONTROLLER_URI = 'http://localhost:8383'

SDN_CTR_B4_TOPO_URL = SDN_CONTROLLER_URI +'/rest/createTopoBf'
SDN_CTR_AF_TOPO_URL = SDN_CONTROLLER_URI +'/rest/createTopoAf'
SDN_CTR_B4_FLOW_URL = SDN_CONTROLLER_URI +'/rest/addFlowBf'
SDN_CTR_AF_FLOW_URL = SDN_CONTROLLER_URI +'/rest/addFlowAf'
SDN_CTR_B4_GET_PATH_URL = SDN_CONTROLLER_URI +'/rest/getFlowPathBf?id='
SDN_CTR_AF_GET_PATH_URL = SDN_CONTROLLER_URI +'/rest/getFlowPathAf?id='

# 1.1 创建topo
SDN_CTR_TOPO_URL = SDN_CONTROLLER_URI +'/rest/createTopo'
# 1.2 添加SLA策略
SDN_CTR_GET_SLAPOLICY_URL = SDN_CONTROLLER_URI +'/rest/addSlaPolicy'
# 1.3 添加流组
SDN_CTR_GET_FLOWGROUP_URL = SDN_CONTROLLER_URI +'/rest/addFlowGroup'
# 1.4 添加流组实例
SDN_CTR_GET_FLOWGROUP_INSTANCE_URL = SDN_CONTROLLER_URI +'/rest/addFlowGroupInstance'
# 1.5 添加流组实例（隧道）路径
SDN_CTR_GET_FLOWGROUP_INSTANCE_TUNNEL_URL = SDN_CONTROLLER_URI +'/rest/addTunnelAndPath'
# 1.6 流组实例路径计算
SDN_CTR_CAL_TUNNEL_PATH_URL = SDN_CONTROLLER_URI +'/rest/calcPathByTunnelId'
# 1.7 通知链路故障
SDN_CTR_NOTIFY_LINK_FAULT_URL = SDN_CONTROLLER_URI +'/rest/linkFault'
# 1.8 通知节点故障 
SDN_CTR_NOTIFY_NODE_FAULT_URL = SDN_CONTROLLER_URI +'/rest/nodeFault'
# 1.9 通知链路故障恢复
SDN_CTR_RECOVER_LINK_FAULT_URL = SDN_CONTROLLER_URI +'/rest/linkRecover'
# 1.10 通知节点故障恢复 （1125修改）
SDN_CTR_RECOVER_NODE_FAULT_URL = SDN_CONTROLLER_URI +'/rest/nodeRecover'
# 1.11 通知路径流量变化
SDN_CTR_NOTIFY_FLOW_CHANGE_URL = SDN_CONTROLLER_URI +'/rest/changeTunnelBandwidth'
# 1.12 通知链路质量变化 (取消)
SDN_CTR_NOTIFY_QUALITY_CHANGE_URL = SDN_CONTROLLER_URI +'/rest/changeLinkQuality'
# 1.14 主备同路重计算
SDN_CTR_AF_CAL_SAME_PATH_URL = SDN_CONTROLLER_URI +'/rest/sameLinkDispatch'
# 1.15 通知链路流量超载
SDN_CTR_NOTIFY_LINK_OVERLOAD_URL = SDN_CONTROLLER_URI +'/rest/linkOverFlowDispatch'
# 1.16 获取流组实例（隧道）路径
SDN_CTR_AF_GET_TUNNEL_PATH_URL = SDN_CONTROLLER_URI +'/rest/getTunnelAndPaths'
# 1.17 全局变量保存
SDN_GLOABL_TRAFFIC_URL = SDN_CONTROLLER_URI +'/rest/saveGlobalConfig'

def add_af_fault_te_flow_speed(flowid, st_time, throughput, path):
    try:
        all_link_info = g_sim.after_fault_link_info[st_time].link_info

        for step_path in path:
            start_id = step_path['start_node_id']
            link_id = step_path['linkid']

            # 由linkid直接取链路信息,把flow加到这条链路上
            one_link_info = all_link_info[link_id]
            if one_link_info.asset_a == start_id:
                one_link_info.a_to_b.flow_tun_speed += throughput
                one_link_info.a_to_b.add_flow_id.append(flowid)
                one_link_info.a_to_b.add_flow_num += 1
            else:
                one_link_info.b_to_a.flow_tun_speed += throughput
                one_link_info.b_to_a.add_flow_id.append(flowid)
                one_link_info.b_to_a.add_flow_num += 1
    except Exception as e:
        print("add_af_fault_te_flow_speed Exception:", e)
        info_logger.error(e)
        error_logger.error(e)

def add_af_fault_te_speed(tunnel_id, st_time, throughput, path):
    try:
        all_link_info = g_sim.after_fault_link_info[st_time].link_info

        for step_path in path:
            start_id = step_path['start_node_id']
            link_id = step_path['linkid']

            # 由linkid直接取链路信息,把flow加到这条链路上
            one_link_info = all_link_info[link_id]
            if one_link_info.asset_a == start_id:
                one_link_info.a_to_b.te_speed += throughput
                one_link_info.a_to_b.te_id.append(tunnel_id)
            else:
                one_link_info.b_to_a.te_speed += throughput
                one_link_info.b_to_a.te_id.append(tunnel_id)
    except Exception as e:
        print("add_af_fault_te_speed Exception:", e)
        info_logger.error(e)
        error_logger.error(e)

def add_af_fault_input_flow_speed(flow_id, st_time, throughput, path):
    try:
        if st_time in g_sim.after_fault_link_info:
            all_link_info = g_sim.after_fault_link_info[st_time].link_info

            for step_path in path:
                start_id = step_path['start_node_id']
                link_id = step_path['linkid']

                # 由linkid直接取链路信息,把flow加到这条链路上
                one_link_info = all_link_info[link_id]
                if one_link_info.asset_a == start_id:
                    one_link_info.a_to_b.flow_speed += throughput
                    one_link_info.a_to_b.add_flow_id.append(flow_id)
                    one_link_info.a_to_b.add_flow_num += 1
                else:
                    one_link_info.b_to_a.flow_speed += throughput
                    one_link_info.b_to_a.add_flow_id.append(flow_id)
                    one_link_info.b_to_a.add_flow_num += 1

    except Exception as e:
        print("add_af_fault_input_flow_speed Exception:", e)
        info_logger.error(e)
        error_logger.error(e)

def notify_link_overload_to_sdn_simctrl(time_start):
    try:
        overloadList = []
        
        # 先清除链路上,上次计算所得的跟隧道相关的流量te_speed，flow_te_speed
        all_link_info = g_sim.after_fault_link_info[time_start].link_info
        for key in all_link_info.keys():
            all_link_info[key].a_to_b.flow_tun_speed = 0
            all_link_info[key].a_to_b.te_speed = 0

        # 计算隧道原始流
        if time_start in g_tunrec.sim_aftuns.keys():
            tunnels = g_tunrec.sim_aftuns[time_start]
            for tunid, value in tunnels.items():
                path = value.primary_path.path
                speed = value.throughput
                if speed != 0:
                    add_af_fault_te_speed(tunid, time_start, speed, path)
        
        # 计算隧道导入的flow
        for flow_id, value in g_sim.flow_info.items():
            if value.tun_name != '':
                if value.orgin == "model":
                    throughput = value.bandwidth[time_start]
                    tunid = value.src_id + value.tun_name
                    if tunid in g_tunrec.sim_aftuns[time_start].keys():
                        path = g_tunrec.sim_aftuns[time_start][tunid].primary_path.path
                        add_af_fault_input_flow_speed(flow_id, time_start, throughput, path)
                elif value.orgin == "tunnel_build":     # 基于tunnel创建的流量
                    if time_start in value.bandwidth.keys():
                        throughput = value.bandwidth[time_start]
                         # 基于tunnel创建的流量的flow id就是隧道id
                        if flow_id in g_tunrec.sim_aftuns[time_start].keys():
                            path = g_tunrec.sim_aftuns[time_start][flow_id].primary_path.path
                            add_af_fault_te_flow_speed(flow_id, time_start, throughput, path)

        for link_id in g_sim.af_topo.links.keys():
            one_link_info = all_link_info[link_id]
            # 把隧道原来的隧道流，加上隧道flow，再加上导入的普通流
            curBandwidth1 = one_link_info.a_to_b.flow_tun_speed + one_link_info.a_to_b.te_speed + one_link_info.a_to_b.flow_speed + one_link_info.a_to_b.back_speed
            curBandwidth2 = one_link_info.b_to_a.flow_tun_speed + one_link_info.b_to_a.te_speed + one_link_info.b_to_a.flow_speed + one_link_info.b_to_a.back_speed

            if curBandwidth1 > g_sim.af_topo.links[link_id].resBandWidth1:
                data = {
                    "id": g_sim.af_topo.links[link_id].l3_link_id[0],
                    "curBandwidth": curBandwidth1,
                    "reservedBandwidth": g_sim.af_topo.links[link_id].resBandWidth1
                }
                overloadList.append(data)

            if curBandwidth2 > g_sim.af_topo.links[link_id].resBandWidth2:
                data = {
                    "id" : g_sim.af_topo.links[link_id].l3_link_id[1],
                    "curBandwidth" : curBandwidth2,
                    "reservedBandwidth" : g_sim.af_topo.links[link_id].resBandWidth2
                }
                overloadList.append(data)

        data_templet = {
            'linkList':overloadList
        }
        headers = {'content-type' : "application/json"}
        if len(overloadList) == 0:
            return ErrCode.SUCCESS

        if test_debug:
            return ErrCode.SUCCESS
        response = requests.post(SDN_CTR_NOTIFY_LINK_OVERLOAD_URL, data=json.dumps(data_templet), headers=headers)
        if response.status_code == 200:
            resp = response.json()
            if resp["code"] != 0:
                info_logger.error("1.15 failed %d, msg %s, post:%s"%(resp["code"], resp["msg"], json.dumps(data_templet)))
                return ErrCode.FAILED
            else:  
                print_in_log("1.15 SDN_CTR_NOTIFY_LINK_OVERLOAD_URL success")
                return ErrCode.SUCCESS
        else:
            info_logger.error("failed %d"%(response.status_code))
            return ErrCode.FAILED      

    except Exception as e:
        print("notify_link_overload_to_sdn_simctrl Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.FAILED 

def notify_te_flow_change_to_sdn_simctrl(time_start):

    try:
        changeList = []
        if time_start in g_tunrec.occupy_cur.keys(): # 按时间段遍历
            tunnels = g_tunrec.occupy_cur[time_start]
            for tunId, value in tunnels.items(): 
                occupyBandwidth = value[0]
                currentBandwidth = value[1]
                if occupyBandwidth != currentBandwidth:
                    data = {
                        "tunnelId" : tunId,
                        "occupyBandwidth" : occupyBandwidth,
                        "currentBandwidth" : currentBandwidth
                    }
                    changeList.append(data)

        data_templet = {
            'tunnelList':changeList
        }

        headers = {'content-type' : "application/json"}
        if test_debug:
            return ErrCode.SUCCESS
        response = requests.post(SDN_CTR_NOTIFY_FLOW_CHANGE_URL, data=json.dumps(data_templet), headers=headers)
        if response.status_code == 200:
            resp = response.json()
            if resp["code"] != 0:
                info_logger.error("1.11 failed %d, msg %s, post:%s"%(resp["code"], resp["msg"], json.dumps(data_templet)))
                return ErrCode.FAILED  
            else:  
                print_in_log("1.11 SDN_CTR_NOTIFY_FLOW_CHANGE_URL success")
                return ErrCode.SUCCESS

        else:
            info_logger.error("failed %d"%(response.status_code))
            return ErrCode.FAILED      

    except Exception as e:
        print("notify_te_flow_change_to_sdn_simctrl Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.FAILED 

def recover_link_fault_to_sdn_simctrl(startTime):
    try:
        recoverNodes = []
        recoverLinks = []
        # 第1种情况：节点原先故障，后来恢复
        for key in g_sim.l3_topo.nodes:
            if g_sim.l3_topo.nodes[key].fault == 'yes' and g_sim.af_l3_topo.nodes[key].fault == 'no':
                # 记录下该节点ID 
                recoverNodes.append(key)

        # 第2种情况：链路原先故障，后来恢复
        for key in g_sim.l3_topo.links:
            srcNodeId = g_sim.l3_topo.links[key].src_id
            dstNodeId = g_sim.l3_topo.links[key].des_id
            if g_sim.af_l3_topo.links[key].fault == 'no':
                # 如果原链路故障,定义后链路无故障,链路两端节点无故障,则进行链路恢复
                if g_sim.l3_topo.links[key].fault == 'yes' and g_sim.af_l3_topo.nodes[srcNodeId].fault == 'no' and g_sim.af_l3_topo.nodes[dstNodeId].fault == 'no':
                    data = {
                        'id':key,
                        "srcNodeId":g_sim.l3_topo.links[key].src_id,
                        "dstNodeId":g_sim.l3_topo.links[key].des_id,
                        "cost": g_sim.l3_topo.links[key].cost,
                        "bandwidth":g_sim.l3_topo.links[key].bandwidth, 
                        "reserved":g_sim.l3_topo.links[key].reservableBandWidth,
                        "delay":g_sim.l3_topo.links[key].delay[startTime],
                        "jitter":g_sim.l3_topo.links[key].jittery[startTime],
                        "loss":g_sim.l3_topo.links[key].loss_rate[startTime],
                        "attributeFlags":g_sim.l3_topo.links[key].attributeFlags
                    }
                    recoverLinks.append(data)       
                # 如果链路的某个节点在节点恢复列表,且另一节点无故障,且链路无故障,则进行链路恢复
                elif srcNodeId in recoverNodes and g_sim.af_l3_topo.nodes[dstNodeId].fault == 'no':  
                    data = {
                        'id':key,
                        "srcNodeId":g_sim.l3_topo.links[key].src_id,
                        "dstNodeId":g_sim.l3_topo.links[key].des_id,
                        "cost": g_sim.l3_topo.links[key].cost,
                        "bandwidth":g_sim.l3_topo.links[key].bandwidth, 
                        "reserved":g_sim.l3_topo.links[key].reservableBandWidth,
                        "delay":g_sim.l3_topo.links[key].delay,
                        "jitter":g_sim.l3_topo.links[key].jittery,
                        "loss":g_sim.l3_topo.links[key].loss_rate,
                        "attributeFlags":g_sim.l3_topo.links[key].attributeFlags
                    }
                    recoverLinks.append(data)
                elif dstNodeId in recoverNodes and g_sim.af_l3_topo.nodes[srcNodeId].fault == 'no':  
                    data = {
                        'id':key,
                        "srcNodeId":g_sim.l3_topo.links[key].src_id,
                        "dstNodeId":g_sim.l3_topo.links[key].des_id,
                        "cost": g_sim.l3_topo.links[key].cost,
                        "bandwidth":g_sim.l3_topo.links[key].bandwidth, 
                        "reserved":g_sim.l3_topo.links[key].reservableBandWidth,
                        "delay":g_sim.l3_topo.links[key].delay,
                        "jitter":g_sim.l3_topo.links[key].jittery,
                        "loss":g_sim.l3_topo.links[key].loss_rate,
                        "attributeFlags":g_sim.l3_topo.links[key].attributeFlags
                    }
                    recoverLinks.append(data)

        recoLinkNum = len(recoverLinks)       
        data_templet = {
            'linkNum':recoLinkNum,
            'links':recoverLinks
        }

        headers = {'content-type' : "application/json"}
        if test_debug:
            return ErrCode.SUCCESS

        response = requests.post(SDN_CTR_RECOVER_LINK_FAULT_URL, data=json.dumps(data_templet), headers=headers)
        if response.status_code == 200:
            resp = response.json()
            if resp["code"] != 0:
                info_logger.error("1.9 failed %d, msg %s"%(resp["code"], resp["msg"]))
                return ErrCode.FAILED 
            else:
                info_logger.error("1.9 SDN_CTR_RECOVER_LINK_FAULT_URL success")
                return ErrCode.SUCCESS 
        else:
            info_logger.error("1.9 SDN_CTR_RECOVER_LINK_FAULT_URL failed %d,%s"%(response.status_code, response))
            return ErrCode.FAILED      

    except Exception as e:
        print("recover_link_fault_to_sdn_simctrl Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.FAILED 

def recover_node_fault_to_sdn_simctrl():
    try:
        recoverNodes = []
        # 节点原先故障，后来恢复
        for node_key in g_sim.l3_topo.nodes:
            if g_sim.l3_topo.nodes[node_key].fault == 'yes' and g_sim.af_l3_topo.nodes[node_key].fault == 'no':
                linklist = []
                # 需要显示每个节点恢复后，与之相邻的所有链路恢复信息（不同node id 直接，恢复的link会有重复）
                recoverLinkIds = []
                for link_key in g_sim.l3_topo.links:

                    srcNodeId = g_sim.l3_topo.links[link_key].src_id
                    dstNodeId = g_sim.l3_topo.links[link_key].des_id
                
                    # 如果有节点在上述列表中 
                    if srcNodeId == node_key or dstNodeId == node_key:
                        # 防止重复加 
                        if link_key not in recoverLinkIds:
                            temp = {
                                'id':link_key,
                                "srcNodeId":g_sim.l3_topo.links[link_key].src_id,
                                "dstNodeId":g_sim.l3_topo.links[link_key].des_id,
                                "cost": g_sim.l3_topo.links[link_key].cost,
                                "bandwidth":g_sim.l3_topo.links[link_key].bandwidth, 
                                "reserved":g_sim.l3_topo.links[link_key].reservableBandWidth,
                                "delay":g_sim.l3_topo.links[link_key].delay,
                                "jitter":g_sim.l3_topo.links[link_key].jittery,
                                "loss":g_sim.l3_topo.links[link_key].loss_rate,
                                "attributeFlags":g_sim.l3_topo.links[link_key].attributeFlags
                            }
                            linklist.append(temp)
                            recoverLinkIds.append(link_key)
                data = {
                    'id':node_key,  # 记录下该节点ID 
                    'links':linklist  # 再记录下与之相关的链路信息
                }
                recoverNodes.append(data)

        recoNodeNum = len(recoverNodes)       
        data_templet = {
            'nodeNum':recoNodeNum,
            'nodeAndLinks':recoverNodes
        }

        headers = {'content-type' : "application/json"}
        if test_debug:
            return ErrCode.SUCCESS
        response = requests.post(SDN_CTR_RECOVER_NODE_FAULT_URL, data=json.dumps(data_templet), headers=headers)
        if response.status_code == 200:
            resp = response.json()
            if resp["code"] != 0:
                info_logger.error("1.10 failed %d, msg %s, post:%s"%(resp["code"], resp["msg"], json.dumps(data_templet)))
                return ErrCode.FAILED  
            else:
                print_in_log("1.10 SDN_CTR_RECOVER_LINK_FAULT_URL success")
                return ErrCode.SUCCESS
        else:
            info_logger.error("failed %d"%(response.status_code))
            return ErrCode.FAILED      

    except Exception as e:
        print("recover_link_fault_to_sdn_simctrl Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.FAILED 


def notify_node_fault_to_sdn_simctrl():
    """把定义前为不故障，定义后为故障 的node信息，通告给SDN仿真控制器
    
    Args:
        none
    Returns:
        none
    Raise:
        none
    """
    try:
        nodeNum = 0
        faultNodes = []

        # 首先遍历一次node节点，有故障的话与之相连的链路都置为故障 
        for key in g_sim.l3_topo.nodes:
            if g_sim.l3_topo.nodes[key].fault == 'no' and g_sim.af_l3_topo.nodes[key].fault == 'yes':
                data = {
                    "id":key,
                }
                faultNodes.append(data)

        nodeNum = len(faultNodes)       
        data_templet = {
            'nodeNum':nodeNum,
            'nodes':faultNodes
        }

        headers = {'content-type' : "application/json"}
        if test_debug:
            return ErrCode.SUCCESS
        response = requests.post(SDN_CTR_NOTIFY_NODE_FAULT_URL, data=json.dumps(data_templet), headers=headers)
        if response.status_code == 200:
            resp = response.json()
            if resp["code"] != 0:
                info_logger.error("failed %d, msg %s, post:%s"%(resp["code"], resp["msg"], json.dumps(data_templet)))
                return ErrCode.FAILED 
            else:
                print_in_log("1.9 SDN_CTR_NOTIFY_NODE_FAULT_URL success")
                return ErrCode.SUCCESS 
        else:
            info_logger.error("failed %d"%(response.status_code))
            return ErrCode.FAILED        

    except Exception as e:
        print("notify_node_fault_to_sdn_simctrl Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.FAILED 


def notify_link_fault_to_sdn_simctrl():
    """把定义前为不故障，定义后为故障 的link信息，通告给SDN仿真控制器
    
    Args:
        none
    Returns:
        none
    Raise:
        none
    """
    try:
        linkNum = 0
        linkList = []
        # 定义前为不故障，定义后为故障
        for key in g_sim.af_l3_topo.links:           
            srcNodeId = g_sim.af_l3_topo.links[key].src_id
            dstNodeId = g_sim.af_l3_topo.links[key].des_id
            # 如果检测到是链路设置了故障，且定义前链路无故障且链路两端节点也无故障,则通知链路故障
            if (g_sim.l3_topo.links[key].fault == 'no' and 
                g_sim.l3_topo.nodes[srcNodeId].fault == 'no' and 
                g_sim.l3_topo.nodes[dstNodeId].fault == 'no' and
                g_sim.af_l3_topo.links[key].fault == 'yes'):
                link_info = {
                    'id':key,
                    'srcNodeId':srcNodeId,
                    'dstNodeId':dstNodeId
                }
                info_logger.error("linkid %s"%(key))
                linkList.append(link_info)
                
            elif (g_sim.af_l3_topo.nodes[srcNodeId].fault == 'yes' and 
                g_sim.l3_topo.links[key].fault == 'no' and 
                g_sim.l3_topo.nodes[srcNodeId].fault == 'no' and
                g_sim.l3_topo.nodes[dstNodeId].fault == 'no'):
                link_info = {
                    'id':key,
                    'srcNodeId':srcNodeId,
                    'dstNodeId':dstNodeId
                }
                linkList.append(link_info)
            elif (g_sim.af_l3_topo.nodes[dstNodeId].fault == 'yes' and 
                g_sim.l3_topo.links[key].fault == 'no' and 
                g_sim.l3_topo.nodes[srcNodeId].fault == 'no' and
                g_sim.l3_topo.nodes[dstNodeId].fault == 'no'):
                link_info = {
                    'id':key,
                    'srcNodeId':srcNodeId,
                    'dstNodeId':dstNodeId
                }
                linkList.append(link_info)
            
        linkNum = len(linkList)       
        data_templet = {
            'linkNum':linkNum,
            'links':linkList
        }

        headers = {'content-type' : "application/json"}
        if test_debug:
            return ErrCode.SUCCESS
        response = requests.post(SDN_CTR_NOTIFY_LINK_FAULT_URL, data=json.dumps(data_templet), headers=headers)
        if response.status_code == 200:
            resp = response.json()
            if resp["code"] != 0:
                info_logger.error("1.7 failed %d, msg %s, post:%s"%(resp["code"], resp["msg"], json.dumps(data_templet)))
                return ErrCode.FAILED  
            else:
                print_in_log("1.7 SDN_CTR_NOTIFY_LINK_FAULT_URL success")
                return ErrCode.SUCCESS 
        else:
            info_logger.error("failed %d"%(response.status_code))
            return ErrCode.FAILED        

    except Exception as e:
        print("notify_link_fault_to_sdn_simctrl Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.FAILED 

def send_affinityEnable_to_sdn_simctrl():
    try:
        headers = {'content-type' : "application/json"}
        data_templet = {
            "affinityEnable": g_sdnply.affinityEnable,
            "reservedBandwidthPercent": g_sdnply.reservedBandwidthPercent,
            "calcLimit": g_sdnply.calcLimit
        }
        if test_debug:
            return ErrCode.SUCCESS
        response = requests.post(SDN_GLOABL_TRAFFIC_URL, data=json.dumps(data_templet), headers=headers)
        if response.status_code == 200:
            resp = response.json()
            if resp["code"] != 0:
                info_logger.error("1.17 failed %d, msg %s, post:%s"%(resp["code"], resp["msg"], json.dumps(data_templet)))
                return ErrCode.FAILED
            else:  
                print_in_log("1.17 SDN_GLOABL_TRAFFIC_URL success:%s"%(json.dumps(data_templet)))
                return ErrCode.SUCCESS
        else:
            error_logger.error("failed %d"%(response.status_code))
            return ErrCode.FAILED        
    except Exception as e:
        print("send_affinityEnable_to_sdn_simctrl Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.FAILED 

def send_topo_to_sdn_simctrl(startTime):
    try:
        """把故障前的topo信息，通告给SDN仿真控制器
            为什么定义后仿真也发送的是定义前的拓扑呢？是由于故障链路恢复和故障链路设置
            都是对比着定义前的拓扑来的，所以这里发送的是定义前的拓扑
        
        Args:
            none
        Returns:
            none
        Raise:
            none
        """
        nodelist = []
        linklist = []
        # 添加节点
        for key in g_sim.l3_topo.nodes:
            # 有无故障均加上node ID
            temp = {'id':key}
            nodelist.append(temp)
        
        # 添加链路
        for key in g_sim.l3_topo.links:
            if g_sim.l3_topo.links[key].fault != 'yes': #非故障
                src_id = g_sim.l3_topo.links[key].src_id
                des_id = g_sim.l3_topo.links[key].des_id
                # 若link两端的节点有故障，则丢弃当前链路 
                if g_sim.l3_topo.nodes[src_id].fault != 'yes' and g_sim.l3_topo.nodes[des_id].fault != 'yes':
                    if startTime not in g_sim.l3_topo.links[key].delay.keys() or startTime not in g_sim.l3_topo.links[key].jittery.keys() or startTime not in g_sim.l3_topo.links[key].loss_rate.keys():
                        info_logger.error("delay keys:%s"%(g_sim.l3_topo.links[key].delay.keys()))
                        info_logger.error("jittery keys:%s"%(g_sim.l3_topo.links[key].jittery.keys()))
                        info_logger.error("loss_rate keys:%s"%(g_sim.l3_topo.links[key].loss_rate.keys()))
                        delay = 0
                        jittery = 0
                        loss = 0
                    else:
                        delay = g_sim.l3_topo.links[key].delay[startTime]
                        jittery = g_sim.l3_topo.links[key].jittery[startTime]
                        loss = g_sim.l3_topo.links[key].loss_rate[startTime]
                    reserved = g_sim.l3_topo.links[key].reservableBandWidth
                    attributeFlags = g_sim.l3_topo.links[key].attributeFlags
                    if delay == -1:
                        delay = 0
                    if jittery == -1:
                        jittery = 0
                    if loss == -1:
                        loss = 0  

                    temp = {"id":key,
                            "srcNodeId":src_id,
                            "dstNodeId":des_id,
                            "cost":g_sim.l3_topo.links[key].cost,
                            "bandwidth":g_sim.l3_topo.links[key].bandwidth,
                            "reserved": reserved,
                            "delay":delay,
                            "jitter":jittery,
                            "loss":loss,
                            "attributeFlags":attributeFlags
                            }
                    linklist.append(temp)
        data_templet = {}
        data_templet["linkNum"] = len(linklist)
        data_templet["links"] = linklist
        data_templet["nodeNum"] = len(nodelist)
        data_templet["nodes"] = nodelist

        headers = {'content-type' : "application/json"}
        if test_debug:
            return ErrCode.SUCCESS

        response = requests.post(SDN_CTR_TOPO_URL, data=json.dumps(data_templet), headers=headers)
        if response.status_code == 200:
            resp = response.json()
            print_in_log("1.1 ### data_templet:%s  resp:%s "%(json.dumps(data_templet), json.dumps(resp)))
            if resp["code"] != 0:
                info_logger.error("1.1 failed %d, msg %s, post:%s"%(resp["code"], resp["msg"], json.dumps(data_templet)))
                return ErrCode.FAILED 
            else: 
                return ErrCode.SUCCESS 
        elif response.status_code == 409:
            info_logger.error("409")
            return ErrCode.RESOURCE_ALREADY_EXIST
        else:
            info_logger.error("failed %d"%(response.status_code))
            return ErrCode.FAILED
    except Exception as e:
        print("send_topo_to_sdn_simctrl Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.INTERNAL_ERROR

# 发送SLA策略给仿真控制器
def send_slapolicy_to_sdn_simctrl():
    """把仿真定义前后的SLA策略，通告给SDN仿真控制器件
    
    Args:
        none
    Returns:
        none
    Raise:
        none
    """    
    try:
        ret = ErrCode.SUCCESS
        for policy_id in g_sdnply.policy.keys():
            policy_info = g_sdnply.policy[policy_id]
            policyName = policy_info.name
            policyId = policy_info.policy_id
            slaLevelId = policy_info.sla_id
            minBandwidth = policy_info.min_bandwidth
            maxBandwidth = policy_info.max_bandwidth
            maxHop = policy_info.max_hop
            enableRateLimit = policy_info.enableRateLimit
            preferColor = policy_info.preferColor
            affinity = policy_info.affinity
            if policy_info.sla_id in g_sdnply.sla_level.keys(): 
                sla_info = g_sdnply.sla_level[policy_info.sla_id]
                priority = sla_info.priority
                maxDelay = sla_info.delay
                maxJitter = sla_info.jitter
                maxPacketLossRate = sla_info.loss_rate
            else:
                priority = 0
                maxDelay = 0
                maxJitter = 50
                maxPacketLossRate = 5

            data_templet = {
                "policyName": policyName,
                "policyId": policyId,
                "slaLevelId": slaLevelId,
                "minBandwidth": minBandwidth,
                "maxBandwidth": maxBandwidth,
                "maxHop": maxHop,
                "enableRateLimit": enableRateLimit,
                "priority": priority,
                "maxDelay": maxDelay,
                "maxJitter": maxJitter,
                "maxPacketLossRate": maxPacketLossRate,
                "affinity":affinity,  # 可选
                "preferColor":preferColor # 可选
            }        
            
            headers ={'content-type':"application/json"}        
            if test_debug:
                return ErrCode.SUCCESS  
            
            response = requests.post(SDN_CTR_GET_SLAPOLICY_URL, data=json.dumps(data_templet), headers=headers)
            if response.status_code == 200:
                resp = response.json()
                print_in_log("1.2 ### data_templet:%s  resp:%s "%(json.dumps(data_templet), json.dumps(resp)))
                if resp["code"] != 0:
                    info_logger.error("failed %d, %s"%(resp["code"], resp["msg"]))
                    ret = ErrCode.INTERNAL_ERROR
                else:
                    print_in_log("1.2 SDN_CTR_GET_SLAPOLICY_URL success,%s"%(json.dumps(data_templet)))
            else:
                error_logger.error("failed %d"%(response.status_code))
                ret = ErrCode.INTERNAL_ERROR
        # 只有全部成功的时候，才会返回成功        
        return ret        
    except Exception as e:
        print("af_send_slapolicy_to_sdn_simctrl Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.INTERNAL_ERROR

# 发送流组信息给仿真控制器
def send_flowgroup_to_sdn_simctrl(flag, start_time):
    """把仿真定义后的流组信息，通告给SDN仿真控制器件
    
    Args:
        none
    Returns:
        none
    Raise:
        none
    """
    try:
        if flag == 'before_fault':
            if start_time in g_tunrec.sim_orgtuns.keys(): 
                tun_step = g_tunrec.sim_orgtuns[start_time]
            else:
                info_logger.error("start_time not in af_tunnels")
                return ErrCode.FAILED
        else:
            if start_time in g_tunrec.sim_aftuns.keys(): 
                tun_step = g_tunrec.sim_aftuns[start_time]
            else:
                info_logger.error("start_time not in af_tunnels")
                return ErrCode.FAILED

        ret = ErrCode.SUCCESS

        for key in tun_step.keys():
            tun = tun_step[key]               
            flowgroup_info = g_sdnply.flowgroup[tun.flowgroup_id]
            flowGroupName = flowgroup_info.name
            flowGroupId = flowgroup_info.flowgroup_id
            pathNum = flowgroup_info.pathNum
            pathMode = flowgroup_info.pathMode
            scheduleId = flowgroup_info.scheduleId
            slaPolicyIds = []
            
            for policeids in flowgroup_info.policies:
                policyid = {"policyId": policeids} 
                slaPolicyIds.append(policyid)

            data_templet = {
                "flowGroupName": flowGroupName,
                "flowGroupId": flowGroupId,
                "pathNum": pathNum,
                "pathMode": pathMode,
                "scheduleId": scheduleId,
                "slaPolicyIds": slaPolicyIds
            }

            headers ={'content-type':"application/json"}
            if test_debug:
                return ErrCode.SUCCESS
            
            response = requests.post(SDN_CTR_GET_FLOWGROUP_URL, data=json.dumps(data_templet), headers=headers)
            if response.status_code == 200:
                resp = response.json()
                print_in_log("1.3 ### data_templet:%s  resp:%s "%(json.dumps(data_templet), json.dumps(resp)))
                if resp["code"] != 0:
                    info_logger.error("1.3 failed %d, %s"%(resp["code"], resp["msg"]))
                    ret = ErrCode.FAILED
            else:
                info_logger.error("failed %d"%(response.status_code))
                ret = ErrCode.FAILED
        return ret

    except Exception as e:
        print("af_send_flowgroup_to_sdn_simctrl Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.INTERNAL_ERROR

# 发送流组实例给仿真控制器
def send_flowgroup_instance_to_sdn_simctrl(flag, start_time):
    """把仿真定义后的流组实例，通告给SDN仿真控制器件
    
    Args:
        none
    Returns:
        none
    Raise:
        none
    """
    try:
        if flag == 'before_fault':
            if start_time in g_tunrec.sim_orgtuns.keys(): 
                tun_step = g_tunrec.sim_orgtuns[start_time]
            else:
                info_logger.error("start_time not in af_tunnels")
                return ErrCode.FAILED
        else:
            if start_time in g_tunrec.sim_aftuns.keys(): 
                tun_step = g_tunrec.sim_aftuns[start_time]
            else:
                info_logger.error("start_time not in af_tunnels")
                return ErrCode.FAILED
        
        ret = ErrCode.SUCCESS

        for key in tun_step.keys():
            tun = tun_step[key]  
            flowgroup_info = g_sdnply.flowgroup[tun.flowgroup_id]
            srcNodeId = flowgroup_info.srcNodeid
            dstNodeId = flowgroup_info.dstNodeid
            flowGroupId = flowgroup_info.flowgroup_id
            flowGroupInstanceId = flowgroup_info.flowgroupinstanceid
            includeNodeAndLink = flowgroup_info.includeNodeAndLink
            excludeNodeAndLink = flowgroup_info.excludeNodeAndLink

            data_templet = {
                "srcNodeId": srcNodeId,
                "dstNodeId": dstNodeId,
                "flowGroupId": flowGroupId,
                "flowGroupInstanceId": flowGroupInstanceId,
                "includeNodeAndLink": includeNodeAndLink,
                "excludeNodeAndLink": excludeNodeAndLink
            }

            headers ={'content-type':"application/json"}
            if test_debug:
                return ErrCode.SUCCESS
            
            response = requests.post(SDN_CTR_GET_FLOWGROUP_INSTANCE_URL, data=json.dumps(data_templet), headers=headers)
            if response.status_code == 200:
                resp = response.json()
                print_in_log("1.4 ### data_templet:%s  resp:%s "%(json.dumps(data_templet), json.dumps(resp)))
                if resp["code"] != 0:
                    info_logger.error("1.4 failed %d, %s"%(resp["code"], resp["msg"]))
                    ret = ErrCode.FAILED
                else:
                    print_in_log("1.4 SDN_CTR_GET_FLOWGROUP_INSTANCE_URL success")
            else:
                info_logger.error("failed %d"%(response.status_code))
                ret = ErrCode.FAILED
        return ret

    except Exception as e:
        print("af_send_flowgroup_instance_to_sdn_simctrl Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.INTERNAL_ERROR

# 发送流组实例隧道给仿真控制器
def send_flowgroup_instance_tunnel_to_sdn_simctrl(flag, start_time):
    """把仿真定义后的流组实例隧道，通告给SDN仿真控制器件
    
    Args:
        none
    Returns:
        none
    Raise:
        none
    """
    try:
        if flag == 'before_fault':
            if start_time in g_tunrec.sim_orgtuns.keys(): 
                tun_step = g_tunrec.sim_orgtuns[start_time]
                phy_topo = g_sim.af_topo
            else:
                info_logger.error("start_time not in af_tunnels")
                return ErrCode.INTERNAL_ERROR
        else:
            if start_time in g_tunrec.sim_aftuns.keys(): 
                tun_step = g_tunrec.sim_aftuns[start_time]
                phy_topo = g_sim.af_topo
            else:
                info_logger.error("start_time not in af_tunnels")
                return ErrCode.INTERNAL_ERROR

        ret = ErrCode.SUCCESS
        for key in tun_step.keys():
            #primary = {"linkList":[], "strictStatus":0, "pathNumber":0}
            #standby = {"linkList":[], "strictStatus":0, "pathNumber":1} # 备路径不存在直接赋值  
            primary = {}
            standby = {}              
            bindTunnel = key
            tun = tun_step[key]
            bandwidth = tun.throughput
            flowGroupId = tun.flowgroup_id
            flowGroupInstanceId = g_sdnply.flowgroup[flowGroupId].flowgroupinstanceid

            primary["strictStatus"] = g_sdnply.flowgroup[flowGroupId].pri_strictStatus
            standby["strictStatus"] = g_sdnply.flowgroup[flowGroupId].sta_strictStatus 
            primary["pathNumber"] = g_sdnply.flowgroup[flowGroupId].pri_pathNumber
            standby["pathNumber"] = g_sdnply.flowgroup[flowGroupId].sta_pathNumber
            primary["linkList"] = []
            standby["linkList"] = []

            for path_step in tun.primary_path.path:
                phy_linkid = path_step["linkid"]
                if path_step["start_node_id"] == phy_topo.links[phy_linkid].nodeid1 and \
                    path_step["end_node_id"] == phy_topo.links[phy_linkid].nodeid2:
                    linkid = phy_topo.links[phy_linkid].l3_link_id[0]
                    primary["linkList"].append(linkid)
                else:
                    linkid = phy_topo.links[phy_linkid].l3_link_id[1]
                    primary["linkList"].append(linkid)
                    
            for path_step in tun.standby_path.path:
                phy_linkid = path_step["linkid"]
                if path_step["start_node_id"] == phy_topo.links[phy_linkid].nodeid1 and \
                    path_step["end_node_id"] == phy_topo.links[phy_linkid].nodeid2:
                    linkid = phy_topo.links[phy_linkid].l3_link_id[0]
                    standby["linkList"].append(linkid)
                else:
                    linkid = phy_topo.links[phy_linkid].l3_link_id[1]
                    standby["linkList"].append(linkid)

            data_templet = {
                "flowGroupInstanceId": flowGroupInstanceId,
                "flowGroupId": flowGroupId,
                "primary": primary,
                "standby": standby,
                "bindTunnel": bindTunnel,
                "bandwidth": bandwidth               
            }

            headers ={'content-type':"application/json"}
            if test_debug:
                return ErrCode.SUCCESS
            
            response = requests.post(SDN_CTR_GET_FLOWGROUP_INSTANCE_TUNNEL_URL, data=json.dumps(data_templet), headers=headers)
            
            if response.status_code == 200:
                resp = response.json()
                print_in_log("1.5 ### data_templet:%s  resp:%s "%(json.dumps(data_templet), json.dumps(resp)))
                if resp["code"] != 0:
                    info_logger.error("1.5 failed %d, %s"%(resp["code"], resp["msg"]))
                    ret = ErrCode.FAILED
                else:
                    print_in_log("1.5 SDN_CTR_GET_FLOWGROUP_INSTANCE_TUNNEL_URL success")
            else:
                info_logger.error("1.5 failed %d"%(response.status_code))  
                ret = ErrCode.FAILED  
        return ret

    except Exception as e:
        print("af_send_flowgroup_instance_tunnel_to_sdn_simctrl Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.INTERNAL_ERROR

# 流组实例路径计算
def calc_flowgroup_instance_tunnel_path(flag, start_time, mode): # 传入mode参数，0表示算主备，1表示只算主，2表示只算备
    try:
        if flag == 'before_fault':
            if start_time in g_tunrec.sim_orgtuns.keys(): 
                tun_step = g_tunrec.sim_orgtuns[start_time]
            else:
                info_logger.error("start_time not in af_tunnels")
                return ErrCode.INTERNAL_ERROR
        else:
            if start_time in g_tunrec.sim_aftuns.keys(): 
                tun_step = g_tunrec.sim_aftuns[start_time]
            else:
                info_logger.error("start_time not in af_tunnels")
                return ErrCode.INTERNAL_ERROR

        ret = ErrCode.SUCCESS

        tunnelList = []
        for tunnel_id in tun_step.keys():
            flowgroup_info = g_sdnply.flowgroup[tun_step[tunnel_id].flowgroup_id]
            pathNum = flowgroup_info.pathNum
            if pathNum == 1:
                if mode == 0 or mode == 1:
                    cal_mode = 1
                else:
                    continue 
            else:
                cal_mode = mode

            tunnels = {
                    "tunnelId": tunnel_id,
                    "mode": cal_mode
                }
            tunnelList.append(tunnels)
        
        data_templet = {
                "tunnelList": tunnelList             
            }

        headers ={'content-type':"application/json"}
        if test_debug:
            return ErrCode.SUCCESS
        response = requests.post(SDN_CTR_CAL_TUNNEL_PATH_URL, data=json.dumps(data_templet), headers=headers)
        if response.status_code == 200:
            resp = response.json()
            if resp["code"] != 0:
                info_logger.error("1.6 failed %d, %s"%(resp["code"], resp["msg"]))
                ret = ErrCode.FAILED
            else:
                info_logger.error("1.6 af_calc_all_flowgroup_instance_tunnel_path success")
        else:
            error_logger.error("1.6 failed %d"%(response.status_code))
            ret = ErrCode.FAILED

        return ret

    except Exception as e:
        print("af_calc_all_flowgroup_instance_tunnel_path Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.INTERNAL_ERROR

# 获取流组实例隧道路径
def get_flowgroup_instance_tunnel_path(flag, start_time): 
    """根据隧道id获得流组实例对象，进行路径计算
    
    Args:
        none
    Returns:
        none
    Raise:
        none
    """
    try:
        if flag == 'before_fault':
            if start_time in g_tunrec.sim_orgtuns.keys(): 
                tun_step = g_tunrec.sim_orgtuns[start_time]
            else:
                info_logger.error("start_time not in af_tunnels")
                return ErrCode.INTERNAL_ERROR, None
        else:
            if start_time in g_tunrec.sim_aftuns.keys(): 
                tun_step = g_tunrec.sim_aftuns[start_time]
            else:
                info_logger.error("start_time not in af_tunnels")
                return ErrCode.INTERNAL_ERROR, None

        tunnelList = []
        for tunnel_id in tun_step.keys():
            tunnels = {
                "tunnelId": tunnel_id
            }
            tunnelList.append(tunnels)
        
        data_templet = {
            "tunnelList": tunnelList        
        }
        if test_debug:
            resp = test_sdn_resp_data
            return ErrCode.SUCCESS, resp["data"]
        headers ={'content-type':"application/json"}
        response = requests.post(SDN_CTR_AF_GET_TUNNEL_PATH_URL, data=json.dumps(data_templet), headers=headers)
        if response.status_code == 200:
            resp = response.json()
            print_in_log("1.16 ### data_templet:%s  resp:%s "%(json.dumps(data_templet), json.dumps(resp)))
            if resp["code"] != 0:
                info_logger.error("1.16 failed %d, %s"%(resp["code"], resp["msg"]))
                return ErrCode.FAILED, None
            else:
                return ErrCode.SUCCESS, resp["data"]
        else:
            info_logger.error("failed %d"%(response.status_code))
            return ErrCode.FAILED, None


    except Exception as e:
        print("af_get_flowgroup_instance_tunnel_path Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.INTERNAL_ERROR, None

# 隧道的主备路径同路，需要调整隧道路径
def af_calc_same_path(path_data):
    """如果隧道的主备路径同路，则需要调整隧道路径
    
    Args:
        none
    Returns:
        none
    Raise:
        none
    """
    try:
        tunnelList = []
        for path_info in path_data:
            # 首先保障主备路径都不为空
            if path_info["primary"] and path_info["standby"] and path_info["primary"]['linkList'] and path_info["standby"]['linkList']:
                # 判断链路列表中的内容是否相同
                if path_info["primary"]['linkList'] == path_info["standby"]['linkList']:
                    tunnels = {
                                "tunnelId": path_info["tunnelId"]
                            }
                    tunnelList.append(tunnels)

        if len(tunnelList) != 0:
            data_templet = {
                "tunnelList": tunnelList        
            }

            headers ={'content-type':"application/json"}
            if test_debug:
                return ErrCode.SUCCESS
            response = requests.post(SDN_CTR_AF_CAL_SAME_PATH_URL, data=json.dumps(data_templet), headers=headers)
            if response.status_code == 200:
                resp = response.json()
                print_in_log("1.14 ### data_templet:%s  resp:%s "%(json.dumps(data_templet), json.dumps(resp)))
                if resp["code"] != 0:
                    info_logger.error("1.14 failed %d, %s"%(resp["code"], resp["msg"]))
                    return ErrCode.FAILED
                else:
                    print_in_log("1.14 SDN_CTR_AF_CAL_SAME_PATH_URL success")
                    return ErrCode.SUCCESS
            else:
                info_logger.error("failed %d"%(response.status_code))
                return ErrCode.FAILED
        else:
            return ErrCode.CAL_DIFFERENT_PATH
    except Exception as e:
        print("af_calc_same_path Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.INTERNAL_ERROR
                
####################################
# 把流信息给到仿真控制器
####################################
def af_send_flows_to_sdn_simctrl(time_start):
    """把故障后的tunnel信息，通告给SDN仿真控制器件
    
    Args:
        none
    Returns:
        none
    Raise:
        none
    """
    try:
        if time_start in g_tunrec.sim_aftuns.keys(): # 按时间段遍历
            tun_step = g_tunrec.sim_aftuns[time_start]
            for key in tun_step.keys():
                tun = tun_step[key]
                group_id = tun.flowgroup_id
                if tun.flowgroup_id == 'N/A':
                    info_logger.error("tun.flowgroup_id == N/A")
                
                ret, bandwidth = get_bandwidth_by_groupid(group_id)

                ret, info = get_slainfo_by_groupid(group_id)
                if ret == ErrCode.SUCCESS:
                    delay = info.delay
                    jitter = info.jitter
                    loss = info.loss_rate
                    
                    if delay == -1:
                        delay = 10000
                    if jitter == -1:
                        jitter = 10000
                    if loss == -1:
                        loss == 10000

                    data_templet = {
                        "id":key,
                        "bandwidth":bandwidth,
                        "startNodeId":g_dt.phy_topo.nodes[tun.src_id].l3_node_id,
                        "endNodeId":g_dt.phy_topo.nodes[tun.des_id].l3_node_id,
                        "delay":delay,      
                        "jitter":jitter,     
                        "loss":loss,       
                        "priority":info.priority,     
                        "preempt":True,    # 填的假数据
                        "standby":True    # True 代表计算主备路径, False代表只计算备路径 
                    }
                else:
                    data_templet = {
                        "id":key,
                        "bandwidth":bandwidth,
                        "startNodeId":g_dt.phy_topo.nodes[tun.src_id].l3_node_id,
                        "endNodeId":g_dt.phy_topo.nodes[tun.des_id].l3_node_id,
                        "delay":10000,      # 填的假数据
                        "jitter":10000,      # 填的假数据
                        "loss":10000,        # 填的假数据
                        "priority":0,     # 填的假数据
                        "preempt":True,    # 填的假数据
                        "standby":True    # True 代表计算主备路径, False代表只计算备路径 
                    }
            
                headers = {'content-type' : "application/json"}
                if test_debug:
                    return ErrCode.SUCCESS
                response = requests.post(SDN_CTR_AF_FLOW_URL, data=json.dumps(data_templet), headers=headers)
                if response.status_code == 200:
                    resp = response.json()
                    print_in_log("SDN_CTR_AF_FLOW_URL ### data_templet:%s  resp:%s "%(json.dumps(data_templet), json.dumps(resp)))
                    if resp["code"] != 0:
                        info_logger.error("failed %d, %s, %s"%(resp["code"], resp['msg'],json.dumps(data_templet)))
                elif response.status_code == 409:
                    info_logger.error("failed %d"%(response.status_code))
                else:
                    info_logger.error("failed %d"%(response.status_code))
        else:
            info_logger.error("time not in g_sim_af")
        return ErrCode.SUCCESS
    except Exception as e:
        print("af_send_flows_to_sdn_simctrl Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.INTERNAL_ERROR

####################################
# 获取流路径 
####################################
def af_get_tpath_from_sdn_simctrl(tunnel_id):
    """从仿真控制器获得tunnel路径"""
    try:
        headers = {'content-type' : "application/json"}
        if test_debug:
            return ErrCode.SUCCESS
        response = requests.get(SDN_CTR_AF_GET_PATH_URL + tunnel_id, headers=headers)
        if response.status_code == 200:
            resp = response.json()
            if resp["code"] != 0:
                info_logger.error("resp[code] %d,msg:%s"%(resp["code"], resp['msg']))
                return None
        else:
            info_logger.error("failed %d"%(response.status_code))
            return None

        resp_data = resp["data"]

        data = {}
        data["path_num"] = resp_data["pathNum"]
        if data["path_num"] == 0:
            info_logger.error("[path_num] %d, tunnel_id:%s"%(data["path_num"], tunnel_id))
            return None

        path_list = []
        path = resp_data["primary"]
        jump = len(path)
        cyc_len = jump - 1
        i = 0
        for i in range(cyc_len):
            # 把三层节点转换为二层节点
            phy_sourcid = g_sim.af_l3_topo.nodes[path[i]].phy_id 
            phy_desid = g_sim.af_l3_topo.nodes[path[(i+1)]].phy_id

            # 通过节点ID，取得其对应的二层链路ID
            linkid = g_sim.topo.nodes[phy_sourcid].neighbour[phy_desid]

            # 记录一条链路信息
            one_link_path = {'start_node_id':phy_sourcid,'end_node_id':phy_desid,'linkid':linkid}
            path_list.append(one_link_path)
        
        data['primary_path'] = path_list
        
        if data["path_num"] == 2:
            stand_list = []
            path = resp_data["standby"]
            jump = len(path)
            cyc_len = jump - 1
            i = 0
            for i in range(cyc_len):
                # 把三层节点转换为二层节点
                phy_sourcid = g_sim.af_l3_topo.nodes[path[i]].phy_id 
                phy_desid = g_sim.af_l3_topo.nodes[path[(i+1)]].phy_id

                # 通过节点ID，取得其对应的二层链路ID
                linkid = g_sim.af_topo.nodes[phy_sourcid].neighbour[phy_desid]

                # 记录一条链路信息
                one_link_path = {'start_node_id':phy_sourcid,'end_node_id':phy_desid,'linkid':linkid}
                stand_list.append(one_link_path)
            
            data['standby_path'] = stand_list

        return data
    except Exception as e:
        print("af_get_tpath_from_sdn_simctrl Exception:", e)
        error_logger.error('SDN_CTR_AF_GET_PATH_URL error')
        info_logger.error(e)
        error_logger.error(e)
        return None  

