# -*- encoding: utf-8 -*-
"""
@File    : bginterface.py
@Time    : 2019/06/26 17:06:36
@Author  : 
@License : Copyright (c) 2004-2019 New H3C Tech. Co., Ltd. All rights reserved.
@Desc    : bigdata 接口文件
"""
import requests
import json
import sys, os
from apps.errcode import ErrCode
from apps.util import g_dt, g_sim
from apps.util import error_logger, info_logger
from apps.util import get_current_time
from apps.v1_0.test import *
from param import *

if debug_postman:
    BIGDATA_URI = 'http://10.99.211.188:8882'
else:
    BIGDATA_URI = 'http://itoa-datacore.itoa:8080'  # 本地调试环境使用该url无法获取数据

BIGDATA_TOPO_URL = BIGDATA_URI + '/DataCore/NDPBusiness/netTopo/getTopoInfo?topoId=globalTopo'
BIGDATA_PORT_IP_URL = BIGDATA_URI + '/DataCore/healthAnalysis/netTopo/getAssetDeviceIps?deviceId='
BIGDATA_BACKGRAND_DATA_URL = BIGDATA_URI + '/DataCore/NDPBusiness/netTopo/linkIndicatorChangeTrend?from=%d&linkId=%s&selectType=advanced&to=%d'  # 后面加 %(start_time,link_id,end_time)
BIGDATA_QUINTET_INFO_URL = BIGDATA_URI + '/DataCore/NDPBusiness/netLink/linkFlowInfoTopN?startTime=%d&endTime=%d&hostIp=%s&ifIndex=%d&topN=%d'  # 后面加毫秒级时间、想要获得的设备的管理IP和端口
BIGDATA_B4FAULT_PATH_URL = BIGDATA_URI + '/DataCore/INTBusiness/appHealth/getAppRoadPath?protocol=%s&startTime=%d&endTime=%d&srcIp=%s&srcPort=%d&destIp=%s&destPort=%d'  # 后面加 %(协议号,开始时间，结束时间，源IP，源端口,目的ip,目的端口)
TOP_N = 100

BIGDATA_TUNNEL_INFO_URL = BIGDATA_URI + "/DataCore/NDPBusiness/flowAnalysis/getTunnelSummary"  # leijy 调试发现需要加上DataCore
BIGDATA_TUNNEL_FLOW_URL = BIGDATA_URI + "/DataCore/NDPBusiness/flowAnalysis/getTunnelTraffic"
BIGDATA_TUNNEL_PATH_URL = BIGDATA_URI + "/DataCore/NDPBusiness/flowAnalysis/getTunnelPath"

BIGDATA_LINK_AVAILABILITY_URL = BIGDATA_URI + "/DataCore/healthAnalysis/netTopo/getTopoLinkAvailability"


def get_topo_from_bigdata():
    """从大数据获取topo信息"""
    try:
        if test_debug:  # 进行本地调试时，获取的是代码存放的静态拓扑数据，而非网络同步所得数据
            resp = debug_topo_data
            return resp

        response = requests.get(BIGDATA_TOPO_URL, headers={"authen": "DataCore"})
        resp = response.json()

        if resp["success"] != True:
            return None
        return resp

    except Exception as e:
        print("get_topo_from_bigdata Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return None


def get_port_ip_from_bigdata(node_id):
    """从大数据获取设备的端口IP和mask信息"""
    # BIGDATA_PORT_IP_URL与大数据的需求文档中的接口6，将获取的信息返回字典格式，获取失败返回None
    try:
        if test_debug:
            data = big_assetDeviceIp_data[node_id]
            return data
        response = requests.get(BIGDATA_PORT_IP_URL + node_id, headers={"authen": "DataCore"})
        resp = response.json()
        # port_ip_node_id[node_id] = resp
        # print('@@resp = ',resp)

        # 暂时设置的假数据  
        if resp["errorCode"] != 0:
            return None
        return resp
    except Exception as e:
        print("get_port_ip_from_bigdata Exception:", e)
        error_logger.error('BIGDATA_PORT_IP_URL error')
        info_logger.error(e)
        error_logger.error(e)
        return None

    return None


def get_link_load_data_from_bigdata(start_time, end_time, link_id):
    """获取某段时间某链路负载数据
    
    Args:
        none
    Returns:
        none
    Raise:
        none
    """

    try:
        if test_debug:
            # data = data_b46131aecfa6()
            data = big_data_linkIndicatorChangeTrend['data']
            return data

        url = BIGDATA_BACKGRAND_DATA_URL % (start_time, link_id, end_time)
        response = requests.get(url, headers={"authen": "DataCore"})
        # 如果返回的状态不为0，则返回失败
        if response.json()['errorInfo'] != 'OK':
            # print('get_link_load_data_from_bigdata response.json()[errorCode and info]:',response.json()['status'],response.json()['errorCode'],response.json()['errorInfo'])
            return None
        else:
            # print('get_link_load_data_from_bigdata:', response.json())
            data = response.json()['data']
            if 'linkBandWidth' not in data:
                error_logger.error('BIGDATA_BACKGRAND_DATA_URL linkBandWidth not in data')
                return None
            else:
                return data
    except Exception as e:
        print("get_link_load_data_from_bigdata Exception:", e)
        error_logger.error('BIGDATA_BACKGRAND_DATA_URL exception')
        error_logger.error(e)
        info_logger.error(e)

        # print('Exception get_link_load_data_from_bigdata:',e)
        return None


def get_quinte_from_bigdata(stime, etime, ip, port):
    url = BIGDATA_QUINTET_INFO_URL % (stime, etime, ip, port, TOP_N)
    try:
        # 获取一定时间范围内，某条链路的流量信息
        response = requests.get(url, headers={"authen": "DataCore"})
        # 如果返回的状态不为0，则返回失败
        if response.json()['success'] != True:
            error_logger.error('BIGDATA_QUINTET_INFO_URL response.json()[success] != True')
            return None
        else:
            data = response.json()['result']['out']
            if len(data) == 0:
                return None
            return data

    except Exception as e:
        print("get_quinte_from_bigdata Exception:", e)
        error_logger.error('QUINTET_INFO_URL exception')
        error_logger.error(e)
        return None


def get_quient_path_from_bigdata(protocol, stime, etime, src_ip, src_port, des_ip, des_port):
    url = BIGDATA_B4FAULT_PATH_URL % (protocol, stime, etime, src_ip, src_port, des_ip, des_port)
    try:
        response = requests.get(url, headers={"authen": "DataCore"})
        status = response.json()['success']
        if status == True:
            data = response.json()['data']  # 正式时，打开 leijy 把['data']去掉
            return data
        else:
            return None

    except Exception as e:
        print("get_quient_path_from_bigdata Exception:", e)
        error_logger.error('get_quient_path_from_bigdata exception')
        error_logger.error(e)
        return None


def get_tunnels_from_bigdata(start_time, end_time):
    """从大数据获取所有隧道信息
    
    Args:
        none
    Returns:
        none
    Raise:
        none
    """

    headers = {"content-type": "application/json", "authen": "DataCore"}
    # 参数设置
    data_templet = {
        "startTime": start_time,
        "endTime": end_time,
        "pageNum": 1,  # 当前页码，从1开始
        "pageSize": -1  # 每页多少条，如果不分页，传入-1
    }
    try:
        if test_debug:
            data = big_tunnel_info_list
            return data

        response = requests.post(BIGDATA_TUNNEL_INFO_URL, data=json.dumps(data_templet), headers=headers)
        response = response.json()
        if response["status"] == True and response["code"] == 100000:
            data = response["data"]["list"]
            return data
        else:
            return None

    except Exception as e:
        print("get_tunnels_from_bigdata Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return None


def get_tunnel_flow_from_bigdata(tunnelUid, start_time, end_time):
    """从大数据获取隧道流量信息
    
    Args:
        none
    Returns:
        none
    Raise:
        none
    """

    headers = {"content-type": "application/json", "authen": "DataCore"}
    # 参数设置
    data_templet = {
        "tunnelUid": tunnelUid,  # 最多输入10项
        "startTime": start_time,
        "endTime": end_time,
    }

    try:
        if test_debug:
            data = big_tunnelTraffic_list
            return data

        response = requests.post(BIGDATA_TUNNEL_FLOW_URL, data=json.dumps(data_templet), headers=headers)
        response = response.json()

        if response["status"] == True and response["code"] == 100000:
            data = response["data"]["list"]
            return data
        else:
            return None

    except Exception as e:
        print("get_tunnel_flow_from_bigdata Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return None


def get_tunnel_path_from_bigdata(tunnelUid):
    """从大数据获取隧道路径信息
    
    Args:
        none
    Returns:
        none
    Raise:
        none
    """

    headers = {"content-type": "application/json", "authen": "DataCore"}
    # 参数设置
    data_templet = {
        "tunnelUid": tunnelUid  # 最多输入10项
    }

    try:
        if test_debug:
            data = big_tunnelPath_list
            return data
        response = requests.post(BIGDATA_TUNNEL_PATH_URL, data=json.dumps(data_templet), headers=headers)
        response = response.json()
        if response["status"] == True and response["code"] == 100000:
            data = response["data"]["list"]
            return data
        else:
            return None

    except Exception as e:
        print("get_tunnel_path_from_bigdata Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return None


def get_link_availability(startTime, endTime, linkList):
    """
    从大数据处查询物理链路基本信息
    基本信息： 抖动、时延、丢包率等。
    Returns:none

    """
    print("get_link_availability in")
    headers = {"content-type": "application/json", "authen": "DataCore"}
    print(headers)
    # 参数设置
    data_templet = {
        "start": startTime,  # 周期开始
        "end": endTime,  # 周期结束
        "linkList": linkList
    }
    print("data_templet:", data_templet)

    try:
        if test_debug:
            data = big_tunnelPath_list
            return data
        info_logger.error("get_link_availability in==================")

        info_logger.error("data_templet:%s" % (json.dumps(data_templet)))
        info_logger.error("url:%s" % (BIGDATA_LINK_AVAILABILITY_URL))
        resp = requests.post(BIGDATA_LINK_AVAILABILITY_URL, data=json.dumps(data_templet), headers=headers)
        print("resp:", resp)
        info_logger.error("get_link_availability resp:%s" % (resp))
        response = resp.json()

        info_logger.error("get_link_availability,resp:%s" % (response))
        if response["status"] == True and response["code"] == 1000:
            data = response["data"]
            return data
        else:
            return None

    except Exception as e:
        print("get_link_availability Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return None
    return None
