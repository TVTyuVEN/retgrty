# -*- encoding: utf-8 -*-
"""
@File    : bgpls.py
@Time    : 2019/08/05 09:59:01
@Author  : chengbofeng
@License : Copyright (c) 2004-2019 New H3C Tech. Co., Ltd. All rights reserved.
@Desc    : bgpls相关配置信息
"""

import time
import requests
import json

from apps.util import info_logger, error_logger
from apps.util import get_current_time
from apps.util import g_dt

from apps.errcode import ErrCode
from apps.datacode import SyncModCode, SyncLogStatusCode, SyncStatusCode

from apps.v1_0.language import get_sync_lang_str
from apps.v1_0.topo import Topo, TopoLink, TopoNode
from apps.v1_0.test import *
from param import *

BGP_INSTANCE_NAME = "global-bgp"
BGP_PROTOCOL_NAME = "bgp-example"
BGP_TOPOLOGY_NAME = "bgp-example-topology"
BGP_PEER_ACCEPTOR_NAME = "default"
BGP_PEER_LOCAL_PORT = 179
BGP_REST_HTTP = "http://localhost:8181"
#BGP_REST_HTTP = "http://10.99.211.109:8181"
BGP_CONF_CHECK_URL = BGP_REST_HTTP+"/restconf/config/openconfig-network-instance:network-instances/network-instance/"\
                    +BGP_INSTANCE_NAME+"/openconfig-network-instance:protocols/protocol/openconfig-policy-types:BGP/"\
                    +BGP_PROTOCOL_NAME
BGP_STATE_URL = BGP_REST_HTTP+"/restconf/operational/openconfig-network-instance:network-instances/network-instance/"\
                    +BGP_INSTANCE_NAME+"/openconfig-network-instance:protocols/protocol/openconfig-policy-types:BGP/"\
                    +BGP_PROTOCOL_NAME
BGP_PROTOCOL_CONF_URL = BGP_REST_HTTP+"/restconf/config/openconfig-network-instance:network-instances/network-instance/"\
                    +BGP_INSTANCE_NAME+"/openconfig-network-instance:protocols"
BGP_PEER_CONF_URL = BGP_REST_HTTP+"/restconf/config/openconfig-network-instance:network-instances/network-instance/"\
                    +BGP_INSTANCE_NAME+"/openconfig-network-instance:protocols/protocol/openconfig-policy-types:BGP/"\
                    +BGP_PROTOCOL_NAME+"/bgp/neighbors"
BGP_PROTOCOL_DEL_URL = BGP_REST_HTTP+"/restconf/config/openconfig-network-instance:network-instances/network-instance/"\
                    +BGP_INSTANCE_NAME+"/openconfig-network-instance:protocols/protocol/openconfig-policy-types:BGP/"\
                    +BGP_PROTOCOL_NAME
BGP_TOPOLOGY_CHECK_URL = BGP_REST_HTTP+"/restconf/config/network-topology:network-topology/topology/"\
                    +BGP_TOPOLOGY_NAME
BGP_TOPOLOGY_GET_URL = BGP_REST_HTTP+"/restconf/operational/network-topology:network-topology/topology/"\
                    +BGP_TOPOLOGY_NAME
BGP_TOPOLOGY_DEL_URL = BGP_REST_HTTP+"/restconf/config/network-topology:network-topology/topology/"\
                    +BGP_TOPOLOGY_NAME
BGP_TOPOLOGY_CONF_URL = BGP_REST_HTTP+"/restconf/config/network-topology:network-topology"
BGP_PEER_ACCEPTOR_URL = BGP_REST_HTTP+"/restconf/config/odl-bgp-peer-acceptor-config:bgp-peer-acceptor-config/"\
                    +BGP_PEER_ACCEPTOR_NAME

def check_bgp_acceptor():
    """检查BGP连接监听的端口号"""
    try:
        response = requests.get(BGP_PEER_ACCEPTOR_URL, auth=("admin", "admin"))
        #print("check bgp listen port")
        #print(response.content)
        if response.status_code == 200:
            config = response.json()["bgp-peer-acceptor-config"][0]
            if config["binding-port"] == BGP_PEER_LOCAL_PORT:
                return ErrCode.SUCCESS
            else:
                return ErrCode.FAILED
        elif response.status_code == 404:
            return ErrCode.RESOURCE_NOT_FOUND
        else:
            info_logger.error("check_bgp_acceptor fail: response code: %d, content: %s"%(response.status_code, response.content))
            error_logger.error("check_bgp_acceptor fail: response code: %d, content: %s"%(response.status_code, response.content))
            return ErrCode.FAILED
    except Exception as e:
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.INTERNAL_ERROR


def check_bgpls_topo():
    """检查BGP LS的topo配置情况"""
    try:
        response = requests.get(BGP_TOPOLOGY_CHECK_URL, auth=("admin", "admin"))
        #print("check topo")
        #print(response.content)
        if response.status_code == 200:
            return ErrCode.SUCCESS
        elif response.status_code == 404:
            return ErrCode.RESOURCE_NOT_FOUND
        else:
            info_logger.error("check_bgpls_topo fail: response code: %d, content: %s"%(response.status_code, response.content))
            error_logger.error("check_bgpls_topo fail: response code: %d, content: %s"%(response.status_code, response.content))
            return ErrCode.FAILED
    except Exception as e:
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.INTERNAL_ERROR


def check_bgpls_config(as_number, local_ip, peer_ip):
    """检查bgpls的配置情况"""
 
    try:
        for i in range(3):
            response = requests.get(BGP_CONF_CHECK_URL, auth=("admin", "admin"))
            #print("check bgp")
            #print(response.content)
            if response.status_code == 200:
                protocol = response.json()["protocol"][0]
                bgp_info = protocol["bgp-openconfig-extensions:bgp"]
                peer = bgp_info["neighbors"]["neighbor"][0]

                if bgp_info["global"]["config"]["as"] == as_number and bgp_info["global"]["config"]["router-id"] == local_ip and peer["neighbor-address"] == peer_ip:
                    return ErrCode.SUCCESS
                else:
                    return ErrCode.FAILED
            elif response.status_code == 404:
                return ErrCode.RESOURCE_NOT_FOUND
            elif response.status_code == 401:
                if i == 2:
                    return ErrCode.UNAUTHORIZED
                else:
                    continue
            else:
                info_logger.error("check_bgpls_config fail: response code: %d, content: %s"%(response.status_code, response.content))
                error_logger.error("check_bgpls_config fail: response code: %d, content: %s"%(response.status_code, response.content))
                return ErrCode.FAILED
    except Exception as e:
        #print(e)
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.INTERNAL_ERROR

def odl_add_bgpls(as_number, local_ip):
    """在ODL中添加BPG LS配置"""

    # 请求模板
    data_templet = {
        "openconfig-network-instance:protocol": [
        {
            "openconfig-network-instance:identifier": "openconfig-policy-types:BGP",
            "openconfig-network-instance:name": "bgp-example",
            "openconfig-network-instance:bgp-openconfig-extensions:bgp": {
                "openconfig-network-instance:bgp-openconfig-extensions:global": {
                    "openconfig-network-instance:bgp-openconfig-extensions:config": {
                        "openconfig-network-instance:bgp-openconfig-extensions:as": "300",
                        "openconfig-network-instance:bgp-openconfig-extensions:router-id": "192.60.60.3"
                    },
                    "openconfig-network-instance:bgp-openconfig-extensions:afi-safis": {
                        "openconfig-network-instance:bgp-openconfig-extensions:afi-safi": [
                        {
                            "openconfig-network-instance:bgp-openconfig-extensions:afi-safi-name": "openconfig-bgp-types:IPV4-UNICAST"
                        },
                        {
                            "openconfig-network-instance:bgp-openconfig-extensions:afi-safi-name": "bgp-openconfig-extensions:LINKSTATE"
                        }]
                    }
                }        
            }
        }]
    }

    # 修改参数
    data_templet["openconfig-network-instance:protocol"][0]["openconfig-network-instance:name"] = BGP_PROTOCOL_NAME
    data_templet["openconfig-network-instance:protocol"][0]["openconfig-network-instance:bgp-openconfig-extensions:bgp"]\
        ["openconfig-network-instance:bgp-openconfig-extensions:global"]["openconfig-network-instance:bgp-openconfig-extensions:config"]\
        ["openconfig-network-instance:bgp-openconfig-extensions:as"] = str(as_number)
    data_templet["openconfig-network-instance:protocol"][0]["openconfig-network-instance:bgp-openconfig-extensions:bgp"]\
        ["openconfig-network-instance:bgp-openconfig-extensions:global"]["openconfig-network-instance:bgp-openconfig-extensions:config"]\
        ["openconfig-network-instance:bgp-openconfig-extensions:router-id"] = local_ip
    
    try:
        headers = {'content-type': "application/json"}
        response = requests.post(BGP_PROTOCOL_CONF_URL, data=json.dumps(data_templet), auth=("admin", "admin"), headers=headers)
        #print("bgp")
        #print(response.content)
        if response.status_code == 204:
            return ErrCode.SUCCESS
        elif response.status_code == 409:
            return ErrCode.RESOURCE_ALREADY_EXIST
        else:
            info_logger.error("odl_add_bgpls fail: response code: %d, content: %s"%(response.status_code, response.content))
            error_logger.error("odl_add_bgpls fail: response code: %d, content: %s"%(response.status_code, response.content))
            return ErrCode.FAILED
    except Exception as e:
        #print(e)
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.INTERNAL_ERROR

def odl_add_bgpls_peer(as_number, peer_ip):
    """在ODL中添加BGP LS对等体配置"""

    # 请求参数模板
    data_templet = {
        "openconfig-network-instance:bgp-openconfig-extensions:neighbor": [
        {
            "openconfig-network-instance:bgp-openconfig-extensions:neighbor-address": "192.60.60.2",
            "openconfig-network-instance:bgp-openconfig-extensions:config": {
                "openconfig-network-instance:bgp-openconfig-extensions:peer-as": "300",
                "openconfig-network-instance:bgp-openconfig-extensions:peer-type": "INTERNAL"
            },
            "openconfig-network-instance:bgp-openconfig-extensions:timers": {
                "openconfig-network-instance:bgp-openconfig-extensions:config": {
                "openconfig-network-instance:bgp-openconfig-extensions:connect-retry": "10",
                "openconfig-network-instance:bgp-openconfig-extensions:hold-time": "180"
                }
            },
            "openconfig-network-instance:bgp-openconfig-extensions:transport": {
                "openconfig-network-instance:bgp-openconfig-extensions:config": {
                "openconfig-network-instance:bgp-openconfig-extensions:passive-mode": "false",
                "openconfig-network-instance:bgp-openconfig-extensions:remote-port": "179"
                }
            },
            "openconfig-network-instance:bgp-openconfig-extensions:afi-safis": {
                "openconfig-network-instance:bgp-openconfig-extensions:afi-safi": [
                {
                    "openconfig-network-instance:bgp-openconfig-extensions:afi-safi-name": "openconfig-bgp-types:IPV4-UNICAST"
                },
                {
                    "openconfig-network-instance:bgp-openconfig-extensions:afi-safi-name": "bgp-openconfig-extensions:LINKSTATE"
                }]
            }
        }]
    }

    # 参数设置
    data_templet["openconfig-network-instance:bgp-openconfig-extensions:neighbor"][0]\
        ["openconfig-network-instance:bgp-openconfig-extensions:neighbor-address"] = peer_ip
    data_templet["openconfig-network-instance:bgp-openconfig-extensions:neighbor"][0]\
        ["openconfig-network-instance:bgp-openconfig-extensions:config"]\
        ["openconfig-network-instance:bgp-openconfig-extensions:peer-as"] = str(as_number)

    try:
        headers = {'content-type': "application/json"}
        response = requests.post(BGP_PEER_CONF_URL, data=json.dumps(data_templet), auth=("admin", "admin"), headers=headers)
        #print("peer")
        #print(response.content)
        if response.status_code == 204:
            return ErrCode.SUCCESS
        elif response.status_code == 409:
            return ErrCode.RESOURCE_ALREADY_EXIST
        else:
            info_logger.error("odl_add_bgpls_peer fail: response code: %d, content: %s"%(response.status_code, response.content))
            error_logger.error("odl_add_bgpls_peer fail: response code: %d, content: %s"%(response.status_code, response.content))
            return ErrCode.FAILED
    except Exception as e:
        #print(e)
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.INTERNAL_ERROR    

def odl_del_bgpls():
    """在ODL中删除BGP LS的配置"""
    
    try:
        response = requests.delete(BGP_PROTOCOL_DEL_URL, auth=("admin", "admin"))
        #print("del")
        #print(response.content)
        if response.status_code == 200:
            return ErrCode.SUCCESS
        elif response.status_code == 404:
            return ErrCode.RESOURCE_NOT_FOUND
        else:
            info_logger.error("odl_del_bgpls fail: response code: %d, content: %s"%(response.status_code, response.content))
            error_logger.error("odl_del_bgpls fail: response code: %d, content: %s"%(response.status_code, response.content))
            return ErrCode.FAILED
    except Exception as e:
        #print(e)
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.INTERNAL_ERROR

def odl_add_topology():
    """在ODL中添加BPG LS的网络topo配置"""
    
    data_templet = {
        "network-topology:topology": [
        {
            "network-topology:topology-id": "bgp-example-topology",
            "network-topology:topology-types": {
                "network-topology:odl-bgp-topology-types:bgp-linkstate-topology": {}
            },
            "network-topology:odl-bgp-topology-config:rib-id": "bgp-example"
        }]
    }
    data_templet["network-topology:topology"][0]["network-topology:topology-id"] = BGP_TOPOLOGY_NAME
    data_templet["network-topology:topology"][0]["network-topology:odl-bgp-topology-config:rib-id"] = BGP_PROTOCOL_NAME

    try:
        headers = {'content-type': "application/json"}
        response = requests.post(BGP_TOPOLOGY_CONF_URL, data=json.dumps(data_templet), auth=("admin", "admin"), headers=headers)
        #print("add topo")
        #print(response.content)
        if response.status_code == 204:
            return ErrCode.SUCCESS
        elif response.status_code == 409:
            return ErrCode.RESOURCE_ALREADY_EXIST
        else:
            info_logger.error("odl_add_topology fail: response code: %d, content: %s"%(response.status_code, response.content))
            error_logger.error("odl_add_topology fail: response code: %d, content: %s"%(response.status_code, response.content))
            return ErrCode.FAILED
    except Exception as e:
        #print(e)
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.INTERNAL_ERROR

def odl_del_topology():
    """在ODL中删除BGP LS的网络topo配置"""
    
    try:
        response = requests.delete(BGP_TOPOLOGY_DEL_URL, auth=("admin", "admin"))
        #print("del topo")
        #print(response.content)
        if response.status_code == 200:
            return ErrCode.SUCCESS
        elif response.status_code == 404:
            return ErrCode.RESOURCE_NOT_FOUND
        else:
            info_logger.error("odl_del_topology fail: response code: %d, content: %s"%(response.status_code, response.content))
            error_logger.error("odl_del_topology fail: response code: %d, content: %s"%(response.status_code, response.content))
            return ErrCode.FAILED
    except Exception as e:
        #print(e)
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.INTERNAL_ERROR

def odl_put_bpg_acceptor():
    """添加或修改BGP连接端口配置"""
    
    data_templet = {
        "odl-bgp-peer-acceptor-config:bgp-peer-acceptor-config": [
        {
            "odl-bgp-peer-acceptor-config:config-name": "default",
            "odl-bgp-peer-acceptor-config:binding-address": "0.0.0.0",
            "odl-bgp-peer-acceptor-config:binding-port": "179"
        }]
    }
    data_templet["odl-bgp-peer-acceptor-config:bgp-peer-acceptor-config"][0]["odl-bgp-peer-acceptor-config:binding-port"] = str(BGP_PEER_LOCAL_PORT)

    try:
        headers = {'content-type': "application/json"}
        response = requests.put(BGP_PEER_ACCEPTOR_URL, data=json.dumps(data_templet), auth=("admin", "admin"), headers=headers)
        #print("put bgp port")
        #print(response.content)
        if response.status_code == 200 or response.status_code == 201:
            return ErrCode.SUCCESS
        else:
            info_logger.error("odl_put_bpg_acceptor fail: response code: %d, content: %s"%(response.status_code, response.content))
            error_logger.error("odl_put_bpg_acceptor fail: response code: %d, content: %s"%(response.status_code, response.content))
            return ErrCode.FAILED
    except Exception as e:
        #print(e)
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.INTERNAL_ERROR

def enable_bgpls(as_number, local_ip, peer_ip):
    """使能bgp ls配置

    Args:
        as_number:as域号
        local_ip:本地BGP端口IP
        peer_ip:BGP对等体IP
    Returns:
        none
    Raise:
        none
    """
    
    # 主动建立BGP连线，无需再修改监听端口
    # 检查BGP连接端口配置
    #ret = check_bgp_acceptor()
    #if ret == ErrCode.SUCCESS:
    #    # 说明已经配置完成，do nothing
    #    pass
    #else:
    #    # 修改配置
    #    ret_ret = odl_put_bpg_acceptor()
    #    if ret_ret != ErrCode.SUCCESS:
    #       return ErrCode.BGP_PORT_MOD_ERROR

    # 检查BGP LS配置
    ret = check_bgpls_config(as_number, local_ip, peer_ip)
    if ret == ErrCode.SUCCESS:
        # 说明已经配置完成，do nothing
        pass
    elif ret == ErrCode.RESOURCE_NOT_FOUND:
        # 添加配置
        ret_ret = odl_add_bgpls(as_number, local_ip)
        if ret_ret != ErrCode.SUCCESS and ret_ret != ErrCode.RESOURCE_ALREADY_EXIST:
            return ErrCode.BGP_ADD_ERROR
        ret_ret = odl_add_bgpls_peer(as_number, peer_ip)
        if ret_ret != ErrCode.SUCCESS and ret_ret != ErrCode.RESOURCE_ALREADY_EXIST:
            return ErrCode.BGP_PEER_ADD_ERROR
    else:
        # 先删除之前的配置
        ret_ret = odl_del_bgpls()
        if ret_ret != ErrCode.SUCCESS and ret_ret != ErrCode.RESOURCE_NOT_FOUND:
            return ErrCode.BGP_DEL_ERROR
        # 添加新的配置
        odl_add_bgpls(as_number, local_ip)
        if ret_ret != ErrCode.SUCCESS and ret_ret != ErrCode.RESOURCE_ALREADY_EXIST:
            return ErrCode.BGP_ADD_ERROR
        odl_add_bgpls_peer(as_number, peer_ip)
        if ret_ret != ErrCode.SUCCESS and ret_ret != ErrCode.RESOURCE_ALREADY_EXIST:
            return ErrCode.BGP_PEER_ADD_ERROR

    # 检查topology配置
    ret = check_bgpls_topo()
    if ret == ErrCode.SUCCESS:
        pass
    elif ret == ErrCode.RESOURCE_NOT_FOUND:
        # 添加配置
        ret_ret = odl_add_topology()
        if ret_ret != ErrCode.SUCCESS and ret_ret != ErrCode.RESOURCE_ALREADY_EXIST:
            return ErrCode.BGP_TOPO_ADD_ERROR
    else:
        # 先删除之前的配置
        ret_ret = odl_del_topology()
        if ret_ret != ErrCode.SUCCESS and ret_ret != ErrCode.RESOURCE_NOT_FOUND:
            return ErrCode.BGP_TOPO_DEL_ERROR
        # 添加新的配置
        ret_ret = odl_add_topology()
        if ret_ret != ErrCode.SUCCESS and ret_ret != ErrCode.RESOURCE_ALREADY_EXIST:
            return ErrCode.BGP_TOPO_ADD_ERROR

    return ErrCode.SUCCESS

def disable_bgpls():    
    """去使能BGP LS"""

    # 只需删除bgpls配置，topo配置保留
    ret = odl_del_bgpls()
    if ret != ErrCode.SUCCESS and ret != ErrCode.RESOURCE_NOT_FOUND:
        return ErrCode.BGP_DEL_ERROR

    return ErrCode.SUCCESS

def config_bgpls(data):
    """设置BGP LS信息
    
    Args:
        data：{
            "enable":0 or 1,
            "asNumber":300,
            "localIp":"192.60.60.3",
            "peerIp":"192.60.60.2"
        }
    Returns:
        none
    Raise:
        none
    """
    if test_debug:
        g_dt.bgp_enable = data["enable"]
        g_dt.bgp_as = data["asNumber"]
        g_dt.bgp_port_ip = data["localIp"]
        g_dt.bgp_peer_ip = data["peerIp"]
        g_dt.bgp_state = "Unknown"
        return ErrCode.SUCCESS

    if data["enable"] == 0:
        # 去使能BGP LS
        ret = disable_bgpls()
        if ret == ErrCode.SUCCESS:
            g_dt.bgp_enable = 0
            g_dt.bgp_state = "N/A"

        return ret
    else:
        # 使能BGP LS
        if  isinstance(data["asNumber"], str):
            as_number = int(data["asNumber"])
        elif isinstance(data["asNumber"], int):
            as_number = data["asNumber"]
        ret = enable_bgpls(as_number, data["localIp"], data["peerIp"])
        if ret == ErrCode.SUCCESS:
            g_dt.bgp_enable = 1
            g_dt.bgp_as = data["asNumber"]
            g_dt.bgp_port_ip = data["localIp"]
            g_dt.bgp_peer_ip = data["peerIp"]
            g_dt.bgp_state = "Unknown"
            return ErrCode.SUCCESS
        else:
            return ErrCode.BGP_ADD_ERROR

def get_bgpls_state():
    """更新BGP LS的状态"""
    
    try:
        response = requests.get(BGP_STATE_URL, auth=("admin", "admin"))
        #print("bgp state")
        #print(response.content)
        if response.status_code == 200:
            protocol = response.json()["protocol"][0]
            peer = protocol["bgp-openconfig-extensions:bgp"]["neighbors"]["neighbor"][0]
            if "session-state" not in peer["state"]:
                state = "Unknown"
            else:
                state = peer["state"]["session-state"]

            return  ErrCode.SUCCESS, state
        elif response.status_code == 404:
            return ErrCode.RESOURCE_NOT_FOUND, "Unknown"
        else:
            return ErrCode.FAILED, "Unknown"
    except Exception as e:
        #print(e)
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.INTERNAL_ERROR, "Unknown"

def get_bgpls_config():
    """获取BGP LS的配置"""

    if g_dt.bgp_enable == 1:
        _, state = get_bgpls_state()
        g_dt.bgp_state = state

    data = {
        "enable": g_dt.bgp_enable,
        "asNumber": g_dt.bgp_as,
        "localIp": g_dt.bgp_port_ip,
        "peerIp": g_dt.bgp_peer_ip,
        "state": g_dt.bgp_state
    }

    return ErrCode.SUCCESS, data


def get_bgpls_from_odl():
    """从BGP邻居获取BGP LS信息
    
    Args:
        none
    Returns:
        none
    Raise:
        none
    """
    
    # url: 10.99.211.109:8181/restconf/operational/network-topology:network-topology/topology/bgp-example-topology 
    try:
        if test_debug:
            #print("####get_bgpls_from_odl:",odl_test_data)
            #print("####get_bgpls_from_odl end ")
            return  0
        
        response = requests.get(BGP_TOPOLOGY_GET_URL, auth=("admin", "admin"))

        if response.status_code == 200:
            data = response.json()
            #print("####get_bgpls_from_odl:",data)
            #print("####get_bgpls_from_odl end ")
            return  ErrCode.SUCCESS, data
        elif response.status_code == 404:
            return ErrCode.RESOURCE_NOT_FOUND, None
        else:
            return ErrCode.FAILED, None
			
    except Exception as e:
        #print('get_bgpls_from_odl',e)
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.INTERNAL_ERROR, None
