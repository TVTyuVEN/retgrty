# -*- encoding: utf-8 -*-
"""
@File    : application_group.py
@Time    : 2019/09/21 18:30:45
@Author  : 
@License : Copyright (c) 2004-2019 New H3C Tech. Co., Ltd. All rights reserved.
@Desc    : 应用组配置
"""
import requests
import json

from apps.util import error_logger,info_logger
from apps.util import g_tunrec, g_sdnply, g_dt
from apps.errcode import ErrCode
from apps.v1_0.bginterface import *
from apps.v1_0.test import *
from param import *

from apps.v1_0.sdn import headers

if debug_postman:
    FLOWGROUP_HTTP = 'http://10.99.211.188:10080'
else:
    FLOWGROUP_HTTP = "http://adwan-north-service.adwan-system:8181"

FLOWGROUP_INFO_URL = FLOWGROUP_HTTP + "/restconf/operations/flow-group-avc:get-flow-group"
SLA_POLICY_INFO_URL = FLOWGROUP_HTTP + "/restconf/operations/sla-policy-avc:get-slaPolicy"
FLOWGROUP_INSTANCE = FLOWGROUP_HTTP + "/restconf/operations/flow-group-avc:get-flow-group-instance"
FLOWGROUP_INSTANCE_WITH_TUNNEL_INFO = FLOWGROUP_HTTP + "/restconf/operations/flow-group-avc:get-flow-group-instance-view"
GET_SLA_LEVEL_INFO_URL = FLOWGROUP_HTTP + "/restconf/operations/sla-level-avc:get-slaLevel"

class Sla(object):
    """Class for service level agreement
    
    Attributes:
        none
    """
    
    def __init__(self, name='default'):
        self.name = name
        self.delay = -1  # ms,时延
        self.loss_rate = -1  # %，丢包率
        self.jitter = -1  # ms，抖动
        self.priority = 1  # 1-5，优先级


class AclRule(object):
    """Class for ACL rule
    
    Attributes:
        none
    """
    pass


class Policy(object):
    """Class for application

    
    Attributes:
        none
    """
    
    def __init__(self, name='default'):
	
        self.policy_id = ''
        self.name = name
        self.sla_id = ''
        self.max_bandwidth = 2000  # kbps
        self.min_bandwidth = 0  # kbps
        self.max_hop = 64
        self.enableRateLimit = False
        self.preferColor = None
        self.affinity = []
        #self.acl = '' #暂时不存
 
class AplyTunnelpath(object):
    """Class for application
    
    Attributes:
        none
    """


    def __init__(self, name='default'):
        self.primary = []
        self.standby = []
        self.tunnelid = ''


class AppGroup(object):
    """Class for application
    
    Attributes:
        none
    """
    
    def __init__(self, name='default'):
        self.flowgroup_id = ''
        self.name = name
        self.policies = [] # [policyid]
        self.srcNodeid = ''
        self.dstNodeid = ''
        self.flowgroupinstanceid = ''
        self.pri_strictStatus = 0    # 0:严格选路 1:勉强选路
        self.sta_strictStatus = 0
        self.pri_pathNumber = 0 # 0:主路径 1：备路径
        self.sta_pathNumber = 1
        # self.tunnelpath = {} # {tunnelid:TunnelPath(),tunnelid:TunnelPath()}
        self.bandwidth = -1
        self.pathNum = 0
        self.pathMode = 0
        self.scheduleId = ''
        self.includeNodeAndLink = {"primary": [], "standby": []}
        self.excludeNodeAndLink = {"primary": [], "standby": []}
        self.phyIncludeNodeAndLink =  {"primary": [], "standby": []}  #为了实现在物理链路上的显示
        self.phyExcludeNodeAndLink =  {"primary": [], "standby": []}  #为了实现在物理链路上的显示



def get_flowgroup_instance_with_tunnel_info():
    """获取所有的flowGroup信息
    
    Args:
        none
    Returns:
        所有flowGroup信息或者None
    Raise:
        none
    """

    data_templet = {
        "input":{}
    }

    if test_debug:
        response = ins_with_tun_data
        return ErrCode.SUCCESS, response["output"]["flowGroupInstanceInfoView"]

    try:
        resp = requests.post(FLOWGROUP_INSTANCE_WITH_TUNNEL_INFO, data=json.dumps(data_templet), headers=headers) 
        
        if resp.status_code == 200:
            response = resp.json()
            if "flowGroupInstanceInfoView" in response["output"].keys():
                return ErrCode.SUCCESS, response["output"]["flowGroupInstanceInfoView"]
            else:
                return ErrCode.NO_CONF_MESSAGE, None
        else: 
            return ErrCode.FAILED, None

    except Exception as e:
        print("get_flowgroup_instance_with_tunnel_info Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.FAILED, None    

def get_sla_level():
    """获取一条或者所有sla级别信息，用于获取最大时延、最大丢包率和最大抖动信息
    
    Args:
        SlaLevelId
    Returns:
        data或者None
    Raise:
        none
    """

    data_templet = {
        "input":{}
    }
    if test_debug:
        data = sla_level_data
        return ErrCode.SUCCESS, data["output"]["slaLevelInfo"]

    try:
        resp = requests.post(GET_SLA_LEVEL_INFO_URL, data=json.dumps(data_templet), headers=headers) 
        if resp.status_code == 200:
            response = resp.json()
            if "slaLevelInfo" in response["output"].keys():
                return ErrCode.SUCCESS, response["output"]["slaLevelInfo"]
            else:
                return ErrCode.NO_CONF_MESSAGE, None
        else:
            return ErrCode.FAILED, None

    except Exception as e:
        print("get_sla_level Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.FAILED, None    

def get_all_flowgroup():
    """获取所有的flowGroup信息
    
    Args:
        none
    Returns:
        所有flowGroup信息或者None
    Raise:
        none
    """

    data_templet = {
        "input":{}
    }
    if test_debug:
        data = group_info_data
        return ErrCode.SUCCESS, data["output"]["flowGroupsInfo"]
    try:
        resp = requests.post(FLOWGROUP_INFO_URL, data=json.dumps(data_templet), headers=headers)    
        if resp.status_code == 200:
            response = resp.json()
            if "flowGroupsInfo" in response["output"].keys():
                if len(response["output"]["flowGroupsInfo"]) > 0:
                    return ErrCode.SUCCESS, response["output"]["flowGroupsInfo"]
            else:
                return ErrCode.NO_CONF_MESSAGE, None

        return ErrCode.FAILED, None

    except Exception as e:
        print("get_all_flowgroup Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.FAILED, None

def get_all_flowgroup_with_instance():
    """获取所有的带实例的flowGroup信息
    
    Args:
        none
    Returns:
        所有flowGroup信息或者None
    Raise:
        none
    """

    data_templet = {
        "input":{}
    }
    if test_debug:
        data = all_group_info_data
        return ErrCode.SUCCESS, data["output"]["flowGroupInstanceInfo"]
    try:
        resp = requests.post(FLOWGROUP_INSTANCE, data=json.dumps(data_templet), headers=headers)    
        if resp.status_code == 200:
            response = resp.json()
            if "flowGroupInstanceInfo" in response["output"].keys():
                return ErrCode.SUCCESS, response["output"]["flowGroupInstanceInfo"]
            else:
                return ErrCode.NO_CONF_MESSAGE, None
        else: 
            return ErrCode.FAILED, None

    except Exception as e:
        print("get_all_flowgroup_with_instance Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.FAILED, None

def get_policy_info():
    """根据policyId获取信息
    
    Args:
        policyId
    Returns:
        policyId的所有信息,不填获取所有policy信息
    Raise:
        none
    """

    data_templet = {"input":{}}
 
    if test_debug:
        data = sla_policy_data
        return ErrCode.SUCCESS, data["output"]["slaPolicyInfo"]

    try:
        resp = requests.post(SLA_POLICY_INFO_URL, data=json.dumps(data_templet), headers=headers)
        
        if resp.status_code == 200:
            response = resp.json() 
            if "slaPolicyInfo" in response["output"].keys():
                return ErrCode.SUCCESS, response["output"]["slaPolicyInfo"]
            else:
                return ErrCode.NO_CONF_MESSAGE, None
        else: 
            return ErrCode.FAILED, None

    except Exception as e:
        print("get_policy_info Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.FAILED, None

def parse_flowgroup_path():
    try:
        # 取隧道的流组实例的信息
        ret, flow_tun_ins_data = get_flowgroup_instance_with_tunnel_info()
        if ret == ErrCode.NO_CONF_MESSAGE:
            error_logger.warning("no_configure_message")
            return flow_tun_ins_data
        if ret != ErrCode.SUCCESS:
            error_logger.warning("parse_flowgroup_path failed")
            return ErrCode.FAILED
        
        all_path_info = []
        # 解析隧道的流组实例的信息
        for tun_ins in flow_tun_ins_data:
            srcNodeid = tun_ins["srcNode"]
            if srcNodeid not in g_dt.l3_topo.nodes.keys():
                error_logger.error("srcNodeid :%s not in keys, all keys:%s"%(srcNodeid, g_dt.l3_topo.nodes.keys()))

            phy_src_id = g_dt.l3_topo.nodes[srcNodeid].phy_id
            uuid = phy_src_id + tun_ins["tunnelInfo"][0]["tunnelName"]


            if "flowPaths" in tun_ins.keys():
                all_path = tun_ins["flowPaths"] 
                for one_path in all_path:  
                    if "paths" in one_path:        
                        paths = one_path["paths"]
                        tunnelid = one_path["tunnelId"]

                        one_path_info = {
                                            "uuid": uuid,
                                            "tunnelid": tunnelid,
                                            "paths": paths                                    
                                        }  
                        all_path_info.append(one_path_info)                                
                                                         
        return all_path_info
           
    except Exception as e:
        print("parse_all_flowgroup Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        data = []
        return data


def parse_all_flowgroup():
    """解析流组信息并保存,存储在flowgroup全局变量，键为flowgroup_id，值为AppGroup()类
    
    Args:
        none
    Returns:
        none
    Raise:
        none
    """

    try:
        # 先取flowgroup的信息
        ret, flow_data = get_all_flowgroup()
        if ret == ErrCode.NO_CONF_MESSAGE:
            error_logger.error("no_configure_message")
            return ErrCode.SUCCESS
        if ret != ErrCode.SUCCESS:
            error_logger.error("parse_all_flowgroup1 failed")
            return ErrCode.FAILED
        
        # 取流组实例的信息
        ret, flow_inst_data = get_all_flowgroup_with_instance()
        if ret == ErrCode.NO_CONF_MESSAGE:
            error_logger.error("no_configure_message")
            return ErrCode.SUCCESS
        if ret != ErrCode.SUCCESS:
            error_logger.warning("parse_all_flowgroup_instance failed")
            return ErrCode.FAILED

        # 取隧道的流组实例的信息
        ret, flow_tun_ins_data = get_flowgroup_instance_with_tunnel_info()
        if ret == ErrCode.NO_CONF_MESSAGE:
            error_logger.error("no_configure_message")
            return ErrCode.SUCCESS
        if ret != ErrCode.SUCCESS:
            error_logger.warning("parse_all_flowgroup2 failed")
            return ErrCode.FAILED
        
        # 如果前面三项有一项取数据失败，则直接退出

        # 解析flowgroup的信息
        for group_info in flow_data:
            flowgroup_temp = AppGroup()  
            flowgroup_id = group_info["flowGroupId"] 
            flowgroup_temp.name = group_info["flowGroupName"]
            flowgroup_temp.pathNum = group_info["pathNum"]
            flowgroup_temp.pathMode = group_info["pathMode"]
            flowgroup_temp.flowgroup_id = flowgroup_id
            if "schedulePolicyIds" in group_info.keys():   
                for policy_info in group_info["schedulePolicyIds"]:
                    flowgroup_temp.scheduleId = policy_info["scheduleId"]
                    for one_policy in policy_info["slaPolicyIds"]:
                        flowgroup_temp.policies.append(one_policy["policyId"])
            
            g_sdnply.flowgroup[flowgroup_id] = flowgroup_temp

        # 解析流组实例的信息
        for flow_ins in flow_inst_data:
            flowGroupId = flow_ins["flowGroupId"]
            flowGroupId_info = g_sdnply.flowgroup[flowGroupId]
            flowGroupId_info.srcNodeid = flow_ins["srcNode"]
            flowGroupId_info.dstNodeid = flow_ins["dstNode"]
            flowGroupId_info.flowgroupinstanceid = flow_ins["flowGroupInstanceId"]
            if "instancePaths" in flow_ins.keys():
                for control_info in flow_ins["instancePaths"]:
                    if control_info["constraintType"] == "INCLUDE": # 保存必经链路和节点
                        if control_info["pathNum"] == "MAIN": # 保存主路径
                            if control_info["pathType"] == 'NODE':
                                pri_info = {
                                    "id": control_info["pathId"],
                                    "type": 0,
                                    "sortNum": control_info["sortNum"]
                                }
                                flowGroupId_info.includeNodeAndLink["primary"].append(pri_info)
                                try:
                                    phyid = g_dt.l3_topo.nodes[control_info["pathId"]].phy_id
                                    phy_pri_info = {
                                        "id": phyid,
                                        "type": 0,
                                        "sortNum": control_info["sortNum"],
                                        "name":g_dt.phy_topo.nodes[phyid].name
                                    }
                                    flowGroupId_info.phyIncludeNodeAndLink["primary"].append(phy_pri_info)
                                except Exception as e:
                                    info_logger.error("l3 nodeid:%s"%(g_dt.l3_topo.nodes.keys()))
                                    info_logger.error("phy nodeid:%s"%(g_dt.phy_topo.nodes.keys()))
                                    info_logger.error(e)
                            else:
                                pri_info = {
                                    "id": control_info["pathId"],
                                    "type": 1,
                                    "sortNum": control_info["sortNum"]
                                }
                                flowGroupId_info.includeNodeAndLink["primary"].append(pri_info)
                                try:
                                    phyid = g_dt.l3_topo.links[control_info["pathId"]].phy_id
                                    l3_srcid = g_dt.l3_topo.links[control_info["pathId"]].src_id
                                    l3_desid = g_dt.l3_topo.links[control_info["pathId"]].des_id 
                                    phy_srcid = g_dt.l3_topo.nodes[l3_srcid].phy_id
                                    phy_dstid = g_dt.l3_topo.nodes[l3_desid].phy_id
                                    phy_src_name = g_dt.phy_topo.nodes[phy_srcid].name
                                    phy_dst_name = g_dt.phy_topo.nodes[phy_dstid].name

                                    phy_pri_info = {
                                        "id": phyid,
                                        "type": 1,
                                        "sortNum": control_info["sortNum"],
                                        "name":phy_src_name + '->' + phy_dst_name
                                    }
                                    flowGroupId_info.phyIncludeNodeAndLink["primary"].append(phy_pri_info)
                                except Exception as e:
                                    info_logger.error("l3 links:%s"%(g_dt.l3_topo.links.keys()))
                                    info_logger.error("phy links:%s"%(g_dt.phy_topo.links.keys()))
                                    info_logger.error(e)
                        else: 
                            if control_info["pathType"] == 'NODE':                    
                                pri_info = {
                                    "id": control_info["pathId"],
                                    "type": 0,
                                    "sortNum": control_info["sortNum"]
                                }
                                flowGroupId_info.includeNodeAndLink["standby"].append(pri_info)
                                try:
                                    phyid = g_dt.l3_topo.nodes[control_info["pathId"]].phy_id
                                    phy_std_info = {
                                        "id": phyid,
                                        "type": 0,
                                        "sortNum": control_info["sortNum"],
                                        "name":g_dt.phy_topo.nodes[phyid].name
                                    }
                                    flowGroupId_info.phyIncludeNodeAndLink["standby"].append(phy_std_info)
                                except Exception as e:
                                    info_logger.error(e)
                            else:
                                pri_info = {
                                    "id": control_info["pathId"],
                                    "type": 1,
                                    "sortNum": control_info["sortNum"]
                                }
                                flowGroupId_info.includeNodeAndLink["standby"].append(pri_info)

                                try:
                                    phyid = g_dt.l3_topo.links[control_info["pathId"]].phy_id
                                    l3_srcid = g_dt.l3_topo.links[control_info["pathId"]].src_id
                                    l3_desid = g_dt.l3_topo.links[control_info["pathId"]].des_id 
                                    phy_srcid = g_dt.l3_topo.nodes[l3_srcid].phy_id
                                    phy_dstid = g_dt.l3_topo.nodes[l3_desid].phy_id
                                    phy_src_name = g_dt.phy_topo.nodes[phy_srcid].name
                                    phy_dst_name = g_dt.phy_topo.nodes[phy_dstid].name
                                    phy_std_info = {
                                        "id": phyid,
                                        "type": 1,
                                        "sortNum": control_info["sortNum"],
                                        "name":phy_src_name + '->' + phy_dst_name
                                    }
                                    flowGroupId_info.phyIncludeNodeAndLink["standby"].append(phy_std_info)
                                except Exception as e:
                                    info_logger.error(e)
                    else:
                        if control_info["pathNum"] == "MAIN": # 保存排除节点和链路
                            if control_info["pathType"] == 'NODE':
                                pri_info = {
                                    "id": control_info["pathId"],
                                    "type": 0,
                                    "sortNum": control_info["sortNum"]
                                }
                                flowGroupId_info.excludeNodeAndLink["primary"].append(pri_info)
                                try:
                                    phyid = g_dt.l3_topo.nodes[control_info["pathId"]].phy_id
                                    phy_pri_info = {
                                        "id": phyid,
                                        "type": 0,
                                        "sortNum": control_info["sortNum"],
                                        "name":g_dt.phy_topo.nodes[phyid].name
                                    }
                                    flowGroupId_info.phyExcludeNodeAndLink["primary"].append(phy_pri_info)
                                except Exception as e:
                                    info_logger.error(e)
                            else:
                                pri_info = {
                                    "id": control_info["pathId"],
                                    "type": 1,
                                    "sortNum": control_info["sortNum"]
                                }
                                flowGroupId_info.excludeNodeAndLink["primary"].append(pri_info)
                                try:
                                    phyid = g_dt.l3_topo.links[control_info["pathId"]].phy_id
                                    l3_srcid = g_dt.l3_topo.links[control_info["pathId"]].src_id
                                    l3_desid = g_dt.l3_topo.links[control_info["pathId"]].des_id 
                                    phy_srcid = g_dt.l3_topo.nodes[l3_srcid].phy_id
                                    phy_dstid = g_dt.l3_topo.nodes[l3_desid].phy_id
                                    phy_src_name = g_dt.phy_topo.nodes[phy_srcid].name
                                    phy_dst_name = g_dt.phy_topo.nodes[phy_dstid].name
                                    phy_pri_info = {
                                        "id": phyid,
                                        "type": 1,
                                        "sortNum": control_info["sortNum"],
                                        "name":phy_src_name + '->' + phy_dst_name
                                    }
                                    flowGroupId_info.phyExcludeNodeAndLink["primary"].append(phy_pri_info)
                                except Exception as e:
                                    info_logger.error(e)
                        else:   
                            if control_info["pathType"] == 'NODE':                     
                                pri_info = {
                                    "id": control_info["pathId"],
                                    "type": 0,
                                    "sortNum": control_info["sortNum"]
                                }
                                flowGroupId_info.excludeNodeAndLink["standby"].append(pri_info)
                                try: 
                                    phyid = g_dt.l3_topo.nodes[control_info["pathId"]].phy_id
                                    phy_std_info = {
                                        "id": phyid,
                                        "type": 0,
                                        "sortNum": control_info["sortNum"],
                                        "name":g_dt.phy_topo.nodes[phyid].name
                                    }
                                    flowGroupId_info.phyExcludeNodeAndLink["standby"].append(phy_std_info)
                                except Exception as e:
                                    info_logger.error(e)
                            else:
                                pri_info = {
                                    "id": control_info["pathId"],
                                    "type": 1,
                                    "sortNum": control_info["sortNum"]
                                }
                                flowGroupId_info.excludeNodeAndLink["standby"].append(pri_info) 
                                try:
                                    phyid = g_dt.l3_topo.links[control_info["pathId"]].phy_id
                                    l3_srcid = g_dt.l3_topo.links[control_info["pathId"]].src_id
                                    l3_desid = g_dt.l3_topo.links[control_info["pathId"]].des_id 
                                    phy_srcid = g_dt.l3_topo.nodes[l3_srcid].phy_id
                                    phy_dstid = g_dt.l3_topo.nodes[l3_desid].phy_id
                                    phy_src_name = g_dt.phy_topo.nodes[phy_srcid].name
                                    phy_dst_name = g_dt.phy_topo.nodes[phy_dstid].name
                                    phy_std_info = {
                                        "id": phyid,
                                        "type": 1,
                                        "sortNum": control_info["sortNum"],
                                        "name":phy_src_name + '->' + phy_dst_name
                                    }
                                    flowGroupId_info.phyExcludeNodeAndLink["standby"].append(phy_std_info) 
                                except Exception as e:
                                    info_logger.error(e)

        # 解析隧道的流组实例的信息
        for tun_ins in flow_tun_ins_data:
            flowGroupId = tun_ins["flowGroupId"]
            flowGroupId_info = g_sdnply.flowgroup[flowGroupId]
            flowGroupId_info.bandwidth = tun_ins["bandwidth"]
            if "flowPaths" in tun_ins.keys():
                all_path = tun_ins["flowPaths"] 
                for one_path in all_path:  
                    if "paths" in one_path:        
                        paths = one_path["paths"]
                        for path_detail in paths:
                            if path_detail["pathNumber"] == 0:
                                flowGroupId_info.pri_strictStatus = path_detail["strictStatus"]  # 保存主路径的strictStatus
                                flowGroupId_info.pri_pathNumber = path_detail["pathNumber"]
                            else:
                                flowGroupId_info.sta_strictStatus = path_detail["strictStatus"]  # 保存备路径的strictStatus
                                flowGroupId_info.sta_pathNumber = path_detail["pathNumber"]
                    else:
                        flowGroupId_info.pri_strictStatus = 3
                        flowGroupId_info.pri_pathNumber = 0
                        flowGroupId_info.sta_strictStatus = 3
                        flowGroupId_info.sta_pathNumber = 1
  
        return ErrCode.SUCCESS
           
    except Exception as e:
        print("parse_all_flowgroup Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.FAILED

def parse_all_policy():
    """解析所有隧道policy，存储policy全局变量信息，键为policy_id，值为Policy()类
    
    Args:
        none
    Returns:
        none
    Raise:
        none
    """

    try:
        ret, data = get_policy_info()
        if ret == ErrCode.NO_CONF_MESSAGE:
            error_logger.error("no_configure_message")
            return ErrCode.SUCCESS
        if ret != ErrCode.SUCCESS:
            info_logger.error("parse_all_policy failed")
            error_logger.error("parse_all_policy failed")
            return ErrCode.FAILED

        for policy_info in data: 
            policy_temp = Policy()
            policy_temp.policy_id = policy_info["policyId"]
            policy_temp.name = policy_info["policyName"]
            policy_temp.sla_id = policy_info["slaLevelId"]
            policy_temp.max_bandwidth = policy_info["maxBandwidth"]
            policy_temp.min_bandwidth = policy_info["minBandwidth"]
            policy_temp.max_hop = policy_info["maxHop"]
            policy_temp.enableRateLimit = policy_info["enableRateLimit"]
            if "preferColor" in policy_info:
                policy_temp.preferColor = policy_info["preferColor"][0]            
            if "affinity" in  policy_info:
                policy_temp.affinity = policy_info["affinity"]
            

            g_sdnply.policy[policy_temp.policy_id] = policy_temp

        return ErrCode.SUCCESS
            
    except Exception as e:
        print("parse_all_policy Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.FAILED

def tunnel_flowgroup_storing():
    """为每个隧道填入对应的应用组信息
    
    Args:
        none
    Returns:
        none
    Raise:
        none
    """

    try:
        ret, data = get_flowgroup_instance_with_tunnel_info()
        if ret == ErrCode.NO_CONF_MESSAGE:
            error_logger.error("no_configure_message")
            return ErrCode.SUCCESS
        if ret != ErrCode.SUCCESS:
            info_logger.error("tunnel_flowgroup_storing failed")
            error_logger.error("tunnel_flowgroup_storing failed")
            return ErrCode.FAILED

        for instan in data: 
            flowgroup_id = instan["flowGroupId"]
            if "tunnelInfo" in instan.keys():
                data1 = instan["tunnelInfo"]
                for detail in data1:
                    if "tunnelId" in detail:
                        if detail["tunnelId"] in g_tunrec.sdntunnelid_to_tunneluuid:
                            tunnel_uuid = g_tunrec.sdntunnelid_to_tunneluuid[detail["tunnelId"]]
                            g_tunrec.org_tuns[tunnel_uuid].flowgroup_id = flowgroup_id

        return ErrCode.SUCCESS
          
    except Exception as e:
        print("tunnel_flowgroup_storing Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.FAILED
   

def parse_all_sla_level():
    """解析所有sla_level信息，存储在sla_level全局变量里，键为sla_level_id，值为Sla()类
    
    Args:
        none
    Returns:
        none
    Raise:
        none
    """

    try:
        ret, data = get_sla_level()
        if ret == ErrCode.NO_CONF_MESSAGE:
            error_logger.error("no_configure_message")
            return ErrCode.SUCCESS
        if ret != ErrCode.SUCCESS:
            info_logger.error("parse_all_sla_level")
            error_logger.error("parse_all_sla_level")
            return ErrCode.FAILED
        
        for sla_info in data: 
            sla_level_temp = Sla()
            sla_level_temp.name = sla_info["slaLevelName"]
            sla_level_temp.delay = sla_info["maxDelay"]
            sla_level_temp.loss_rate = sla_info["maxPacketLossRate"]
            sla_level_temp.jitter = sla_info["maxJitter"]
            sla_level_temp.priority = sla_info["priority"]
            g_sdnply.sla_level[sla_info["slaLevelId"]] = sla_level_temp

        return ErrCode.SUCCESS
            
    except Exception as e:
        print("parse_all_sla_level Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.FAILED


def get_slainfo_by_groupid(groupid):
    try:
        if groupid in g_sdnply.flowgroup.keys():
            flow_group_info = g_sdnply.flowgroup[groupid]
            # 现在策略取第一个策略
            for i in range(len(flow_group_info.policies)):
                policy_id = flow_group_info.policies[i]
                policy_info = g_sdnply.policy[policy_id]
                sla_id = policy_info.sla_id
                sla_info = g_sdnply.sla_level[sla_id]
                return ErrCode.SUCCESS, sla_info
    except Exception as e:
        print("get_slainfo_by_groupid Exception:", e)
        sla_info = Sla()
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.FAILED, sla_info

    sla_info = Sla()
    return ErrCode.FAILED, sla_info

def get_bandwidth_by_groupid(groupid):
    try:
        if groupid in g_sdnply.flowgroup.keys():
            flow_group_info = g_sdnply.flowgroup[groupid]
            # 现在策略取第一个策略
            for i in range(len(flow_group_info.policies)):
                policy_id = flow_group_info.policies[i]
                policy_info = g_sdnply.policy[policy_id]
                bandwith = policy_info.min_bandwidth 
                return ErrCode.SUCCESS, bandwith
    except Exception as e:
        print("get_bandwidth_by_groupid Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        # 默认的最小值是10K，所以返回10
        return ErrCode.FAILED, 10
    return ErrCode.FAILED, 10
   
