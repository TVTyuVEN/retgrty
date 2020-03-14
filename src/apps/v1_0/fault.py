# -*- encoding: utf-8 -*-
"""
@File    : fault.py
@Time    : 2019/05/29 13:56:42
@Author  : 
@License : Copyright (c) 2004-2019 New H3C Tech. Co., Ltd. All rights reserved.
@Desc    : 故障管理
"""
from flask import request, json
from flask_restful import Resource

from apps.util import g_dt
from apps.util import info_logger, error_logger
from apps.util import  get_current_time
from apps.errcode import ErrCode

#网元/链路 设置/清除独个故障      
def set_fault(data):
    try: 
        data_type = data["type"]
        fault_id = data["id"]
        fault = data["fault"]

        #输入的type为节点类型
        if data_type == "node" :
            g_dt.phy_topo.nodes[fault_id].fault = fault
            # 设置3层topo的node故障
            layer3_node_id = g_dt.phy_topo.nodes[fault_id].l3_node_id
            g_dt.l3_topo.nodes[layer3_node_id].fault = fault
            if fault == 'yes':
                # 故障数量加增加      
                g_dt.phy_topo.fault_num += 1
            else:
                # 故障数量加增加      
                g_dt.phy_topo.fault_num -= 1

        #输入的type为链路类型 
        if data_type == "link" :
            g_dt.phy_topo.links[fault_id].fault = fault
            # 设置3层topo的link故障

            for layer3_link_id in g_dt.phy_topo.links[fault_id].l3_link_id:

                if layer3_link_id:
                    g_dt.l3_topo.links[layer3_link_id].fault = fault
        
            if fault == 'yes':
                # 故障数量加增加      
                g_dt.phy_topo.fault_num += 1
            else:
                # 故障数量加增加      
                g_dt.phy_topo.fault_num -= 1

        return ErrCode.SUCCESS

    except Exception as e:
        print("set_fault exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return  ErrCode.FAILED 

# 获取故障列表
def get_fault_list():
    try:
        linksFaultNum = 0
        nodesFaultNum = 0
        dicAll = []

        #遍历字典 寻找错误的nodes
        for key in g_dt.phy_topo.nodes:
            if g_dt.phy_topo.nodes[key].fault == "yes":
                dic = {}
                dic["name"] = g_dt.phy_topo.nodes[key].name
                dic["type"] = "node"
                dic["id"] = g_dt.phy_topo.nodes[key].id
                #dic["description"] = g_dt.phy_topo.nodes[key].description
                # 将dic字典加入集合
                dicAll.insert(0, dic) 
                # 统计的数量加 1
                nodesFaultNum = nodesFaultNum + 1 
                
        for key in g_dt.phy_topo.links:
            if g_dt.phy_topo.links[key].fault == "yes":
                dic = {}
                dic["name"] = g_dt.phy_topo.links[key].name
                dic["type"] = "link"
                dic["id"] = g_dt.phy_topo.links[key].id
                #dic["description"] = g_dt.phy_topo.links[key].description
                # 将dic字典加入集合
                dicAll.insert(0, dic)
                # 统计的数量加 1
                linksFaultNum = linksFaultNum + 1 

        data = { 
                    "faultNodeNum": nodesFaultNum,
                    "faultLinkNum": linksFaultNum,
                    "faulInfo": dicAll
                }

        return ErrCode.SUCCESS, data
    except Exception as e:
        print("get_fault_list exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        data = { 
                    "faultNodeNum": 0,
                    "faultLinkNum": 0,
                    "faulInfo": []
                }
        return ErrCode.FAILED, data

def judge_fault():
    """判断是否设置了故障
    
    Args:
        none
    Returns:
        none
    Raise:
        none
    """
    
    try:
        # 一旦找到一个节点故障，则认为设置了故障
        for key in g_dt.phy_topo.nodes:
            if g_dt.phy_topo.nodes[key].fault == "yes":
                return True
               
        # 一旦找到一个链路故障，则认为设置了故障
        for key in g_dt.phy_topo.links:
            if g_dt.phy_topo.links[key].fault == "yes":
                return True

        return False
    except Exception as e:
        print("judge_fault exception:", e)
        info_logger.error(e)
        error_logger.error(e)

        return False

# 清除故障 
def clear_fault(data):
    try:
        nodeNum = data["nodeNum"]
        linkNum = data["linkNum"]

        # node故障清除 
        if nodeNum > 0 :
            for i in range(nodeNum):
                id = data["faultNode"][i]["assetId"]
                for key in g_dt.phy_topo.nodes:
                    if id == key:
                        # 找到对应的id后，将错误标志位置为 no
                        g_dt.phy_topo.nodes[key].fault = "no"
                        g_dt.phy_topo.fault_num -= 1

        # link故障清除 
        if linkNum > 0:
            for i in range(linkNum):
                id = data["faultLink"][i]["linkId"]
                for key in g_dt.phy_topo.links:
                    if id == key:
                        # 找到对应的id后，将错误标志位置为 no
                        g_dt.phy_topo.links[key].fault = "no"
                        g_dt.phy_topo.fault_num -= 1
        
        return ErrCode.SUCCESS
    except Exception as e:
        print("clear_fault exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.FAILED
