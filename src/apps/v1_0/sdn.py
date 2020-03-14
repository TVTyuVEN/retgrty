# -*- encoding: utf-8 -*-
"""
@File    : sdn.py
@Time    : 2019/09/21 18:30:45
@Author  : 
@License : Copyright (c) 2004-2019 New H3C Tech. Co., Ltd. All rights reserved.
@Desc    : sdn
"""

import requests
import json
from apps.errcode import ErrCode
from apps.util import info_logger, error_logger
from apps.util import get_current_time

from apps.v1_0.bginterface import *
from apps.v1_0.test import *
from param import *

if debug_postman:
    SDN_URL = 'http://10.99.211.188:10080'
    headers = {"content-type": "application/json", "iam-role": "admin", "X-Auth-Token": token}
else:
    SDN_URL = "http://adwan-north-service.adwan-system:8181"
    headers = {'content-type': "application/json", "iam-role": "admin"}

SDN_TOPO_CONTROL_URL = SDN_URL + '/restconf/operations/topology-modelV2:get-topology'
# SDN_TOPO_NODE_CONTROL_URL = SDN_URL + '/restconf/operations/topology-modelV2:get-topo-node'
SDN_TOPO_LINK_CONTROL_URL = SDN_URL + '/restconf/operations/topology-modelV2:get-link'
SDN_LINK_INFO_CONTROL_URL = SDN_URL + '/restconf/operations/device-manager:get-terminal-point'
SDN_TOPO_LINK_QUALITY_CONTROL_URL = SDN_URL + '/restconf/operations/oam-manager:get-link-quality'
SDN_TUNNEL_INFO_URL = SDN_URL + '/restconf/operations/tunnel:get-tunnel'  # 后面加 %(phy_src_id,phy_des_id)
SDN_RES_PERCENT = SDN_URL + '/restconf/operations/traffic-global:get-reservedBandwidthPercent'
SDN_GLOBAL_TRAFFIC = SDN_URL + '/restconf/operations/traffic-global:get-advanceSchedule'


def get_all_tunnels():
    """获取所有的tunnels
    
    Args:
        none
    Returns:
        所有隧道信息
    Raise:
        none
    """

    data_templet = {}
    data_templet["input"] = {}

    try:

        if test_debug:
            data = sna_tunnel_info_data
            return data["output"]["totalSize"], data["output"]

        resp = requests.post(SDN_TUNNEL_INFO_URL, data=json.dumps(data_templet), headers=headers)

        if resp.status_code == 200:
            response = resp.json()
            return response["output"]["totalSize"], response["output"]
        else:
            error_logger.error("get_all_tunnels none")
            error_logger.error(resp.status_code)
            return 0, None
    except Exception as e:
        print("get_all_tunnels Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return 0, None


# sprint3 add
# 代码需要根据接口重新写
def get_topo_control_from_sdn():
    """从SDN获取拓扑控制信息
    
    Args:
        none
    Returns:
        none
    Raise:
        none
    """
    try:
        data_templet = {"input": {}}
        if test_debug:
            data = sna_topology_data
            return ErrCode.SUCCESS, data
        response = requests.post(SDN_TOPO_CONTROL_URL, data=json.dumps(data_templet), headers=headers)

        if response.status_code == 200:
            data = response.json()

            return ErrCode.SUCCESS, data
        elif response.status_code == 404:
            info_logger.error('e RESOURCE_NOT_FOUND')
            return ErrCode.RESOURCE_NOT_FOUND, None
        else:
            return ErrCode.FAILED, None

    except Exception as e:
        print("get_topo_control_from_sdn Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.INTERNAL_ERROR, None


def get_resver_percent_from_sdn():
    try:
        if test_debug:
            data = 80
            return ErrCode.SUCCESS, data
        percent = 100
        response = requests.post(SDN_RES_PERCENT, headers=headers)
        if response.status_code == 200:
            resp = response.json()
            if "reservedBandwidthPercent" in resp["output"].keys():
                percent = resp["output"]["reservedBandwidthPercent"]
            return ErrCode.SUCCESS, percent
        return ErrCode.FAILED, percent
    except Exception as e:
        percent = 100
        print("get_resver_percent_from_sdn Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.FAILED, percent


def get_traffic_global_from_sdn():
    try:
        if test_debug:
            data = sdn_global_data
            return ErrCode.SUCCESS, data

        response = requests.post(SDN_GLOBAL_TRAFFIC, headers=headers)
        if response.status_code == 200:
            resp = response.json()
            return ErrCode.SUCCESS, resp["output"]
        return ErrCode.FAILED, {}
    except Exception as e:
        print("get_resver_percent_from_sdn Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.FAILED, {}


# sprint3 add
# 代码需要根据接口重新写
def get_topo_link_control_from_sdn(topo_id):
    """从SDN获取拓扑链路控制信息
    
    Args:
        none
    Returns:
        none
    Raise:
        none
    """

    try:
        data_templet = {"input": {}}
        data_templet["input"]["topoId"] = topo_id
        if test_debug:
            data = sna_link_data
            return ErrCode.SUCCESS, data
        response = requests.post(SDN_TOPO_LINK_CONTROL_URL, data=json.dumps(data_templet), headers=headers)

        if response.status_code == 200:
            data = response.json()

            return ErrCode.SUCCESS, data
        elif response.status_code == 404:
            return ErrCode.RESOURCE_NOT_FOUND, None
        else:
            return ErrCode.FAILED, None

    except Exception as e:
        print("get_topo_link_control_from_sdn Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.INTERNAL_ERROR, None


def get_link_info_control_from_sdn(node_id, tp_id):
    """从SDN获取拓扑链路控制信息
    
    Args:
        none
    Returns:
        none
    Raise:
        none
    """

    try:
        data_templet = {"input": {}}
        data_templet["input"]["deviceId"] = node_id
        data_templet["input"]["tpId"] = tp_id

        if test_debug:
            data = sna_terminal_point_data[tp_id]
            return ErrCode.SUCCESS, data
        response = requests.post(SDN_LINK_INFO_CONTROL_URL, data=json.dumps(data_templet), headers=headers)

        if response.status_code == 200:
            data = response.json()

            return ErrCode.SUCCESS, data
        elif response.status_code == 404:
            return ErrCode.RESOURCE_NOT_FOUND, None
        else:
            return ErrCode.FAILED, None

    except Exception as e:
        print("get_link_info_control_from_sdn Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.INTERNAL_ERROR, None


def get_topo_link_quality_control_from_sdn(link_id):
    """从SDN获取拓扑链路控制信息
    
    Args:
        none
    Returns:
        none
    Raise:
        none
    """
    try:
        data_templet = {"input": {}}
        data_templet["input"]["linkId"] = link_id

        if test_debug:
            data = sna_link_quality_data[link_id]
            return ErrCode.SUCCESS, data
        response = requests.post(SDN_TOPO_LINK_QUALITY_CONTROL_URL, data=json.dumps(data_templet), headers=headers)

        if response.status_code == 200:
            data = response.json()

            return ErrCode.SUCCESS, data
        elif response.status_code == 404:
            return ErrCode.RESOURCE_NOT_FOUND, None
        else:
            return ErrCode.FAILED, None

    except Exception as e:
        print("get_topo_link_quality_control_from_sdn Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.INTERNAL_ERROR, None
