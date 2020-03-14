# -*- encoding: utf-8 -*-
"""
@File    : datasync.py
@Time    : 2019/05/29 13:56:26
@Author  : 
@License : Copyright (c) 2004-2019 New H3C Tech. Co., Ltd. All rights reserved.
@Desc    : 数据同步
"""
import re
import time
import requests

from apps.util import info_logger, error_logger
from apps.util import g_dt, g_allFlows, g_sim, g_tunrec, g_sdnply
from apps.util import parse_flow_to_kbps
from apps.util import get_current_time

from apps.errcode import ErrCode
from apps.datacode import SyncModCode, SyncLogStatusCode, SyncStatusCode

from apps.v1_0.language import get_sync_lang_str

from apps.v1_0.topo import Topo, L3Topo, TopoLink, TopoNode, Interface
from apps.v1_0.sdn import get_topo_control_from_sdn, get_topo_link_control_from_sdn
from apps.v1_0.sdn import get_link_info_control_from_sdn, get_topo_link_quality_control_from_sdn
from apps.v1_0.sdn import get_resver_percent_from_sdn, get_traffic_global_from_sdn
from apps.v1_0.bginterface import *
from apps.v1_0.tunnel import *
from apps.v1_0.bginterface import get_topo_from_bigdata, get_port_ip_from_bigdata
from apps.v1_0.application import parse_all_flowgroup, parse_all_policy, parse_all_sla_level
from apps.v1_0.test import *
from apps.v1_0.simulate import sim_rate
from param import *


def prase_bgpls_single_ospf_area():
    """解析单域OSPF的BGP LS信息，来得到三层协议topo
    
    Args:
        none
    Returns:
        none
    Raise:
        none
    """
    pass


def parse_l3_topo_info(data):
    """解析l3 topo信息
    
    Args:
        data:从BGP-LS取到的三层TOPO信息
    Returns:
        none
    Raise:
        none
    Notes:当前的解析,三层TOPO上的节点和链路,一定能在phy上找到对应的节点和链路的
    """
    # 3层topo解析
    if g_dt.l3_topo == None:
        g_dt.l3_topo = L3Topo()
    else:
        g_dt.l3_topo.clear_topo()

    # print(' data = ', data )
    # IP 对应 id
    phy_node_port_ips = []
    phy_node_ids = []
    for key, value in g_dt.phy_topo.nodes.items():
        for value2 in value.port.values():
            phy_node_port_ips.append(value2.ip)
            # 同时记录下二层topo中的 node id ，放到数组中，与上面的ip对应 
            phy_node_ids.append(key)

    # print('## phy_node_port_ips = ', phy_node_port_ips)
    # print('## phy_node_ids = ', phy_node_ids)
    # print('########### g_dt.phy_topo.nodes = ', g_dt.phy_topo.nodes)
    # print('!!!!!!!## parse_l3_topo_info begin ')

    try:
        # 解析节点 
        topologys = data["topology"]
        node_num = 0
        l3_to_phy_node_id = {}

        # print('nodes = ', topologys)
        for topology in topologys:
            if "node" not in topology:
                continue

            nodes = topology['node']

            for node in nodes:
                # print('node-id:',node["node-id"])
                # 最后一个冒号是防止有些有前后两个id 的情况 
                node_id = node["node-id"].split('&')[-1].split('=')[-1].split(':')[0]
                # print('# split node_id = ', node_id)
                # id已存在的还不需要再添加
                if node_id in g_dt.l3_topo.nodes.keys():
                    continue

                # 如果无termination-point字段，不添加 
                if 'termination-point' not in node:
                    continue

                for tp in node['termination-point']:
                    # print('tp-id:', node['termination-point'])
                    # phy_ip = tp['tp-id'].split('&')[-1].split('=')[-1]
                    if 'l3-unicast-igp-topology:igp-termination-point-attributes' not in tp:
                        continue

                    if 'ip-address' not in tp['l3-unicast-igp-topology:igp-termination-point-attributes']:
                        continue

                    phy_ip_list = tp['l3-unicast-igp-topology:igp-termination-point-attributes']['ip-address']

                    # 暂时取列表中的第一个 
                    if len(phy_ip_list) > 0:
                        phy_ip = phy_ip_list[0]
                    else:
                        continue
                    # print('# split phy_ip = ', phy_ip)

                    # layer3上添加的节点，在phy层上一定是存在对应节点的
                    if phy_ip in phy_node_port_ips:
                        idx = phy_node_port_ips.index(phy_ip)
                        phy_id = phy_node_ids[idx]
                        # leijuyan 把原来的参数phy_ip改成phy_id，存二层的ID
                        g_dt.l3_topo.add_node(phy_id, node_id)

                        temp = g_dt.l3_topo.nodes[node_id]
                        # 记录三层TOPO的位置
                        temp.x = g_dt.phy_topo.nodes[phy_id].x
                        temp.y = g_dt.phy_topo.nodes[phy_id].y
                        # temp 后续有内容需要在此处添加

                        # 获取其下标，找到对应的二层node id 

                        g_dt.phy_topo.nodes[phy_node_ids[idx]].l3_node_id = node_id
                        # 添加到对应字典中 通过三层topo的node id找到二层的node id
                        l3_to_phy_node_id[node_id] = phy_node_ids[idx]
                        node_num += 1
                        break

        g_dt.l3_topo.node_num = node_num

        # 解析链路 
        link_num = 0
        for topology in topologys:
            if "link" not in topology:
                continue

            links = topology['link']

            matr_temp = {}
            for link in links:
                src_router_id = link['source']["source-node"].split('&')[-1].split('=')[-1]
                des_router_id = link['destination']["dest-node"].split('&')[-1].split('=')[-1]
                l3_src_node_id = link['source']["source-node"].split('&')[-1].split('=')[-1].split(':')[0]
                l3_des_node_id = link['destination']["dest-node"].split('&')[-1].split('=')[-1].split(':')[0]
                if l3_src_node_id == l3_des_node_id:
                    matr_temp[src_router_id + "-" + des_router_id] = \
                    link['l3-unicast-igp-topology:igp-link-attributes']["metric"]

            for link in links:
                # print('link = ', link)
                l3_link_id = link["link-id"]  # 先用原id，有点长，但是唯一 
                if l3_link_id in g_dt.l3_topo.links.keys():
                    continue

                src_ip = link['source']["source-tp"].split('=')[-1]
                des_ip = link['destination']["dest-tp"].split('=')[-1]

                src_router_id = link['source']["source-node"].split('&')[-1].split('=')[-1]
                des_router_id = link['destination']["dest-node"].split('&')[-1].split('=')[-1]
                l3_src_node_id = link['source']["source-node"].split('&')[-1].split('=')[-1].split(':')[0]
                l3_des_node_id = link['destination']["dest-node"].split('&')[-1].split('=')[-1].split(':')[0]

                if l3_src_node_id not in l3_to_phy_node_id or l3_des_node_id not in l3_to_phy_node_id:
                    continue

                # 首先要两端的ip不相等 
                # if src_ip != des_ip:
                if l3_src_node_id != l3_des_node_id:

                    # 通过3层的node id 找到 2层的 node id
                    phy_src_node_id = l3_to_phy_node_id[l3_src_node_id]
                    phy_des_node_id = l3_to_phy_node_id[l3_des_node_id]

                    for phy_key, phy_value in g_dt.phy_topo.links.items():
                        # 找相应的link
                        if (phy_value.nodeid1 == phy_src_node_id and phy_value.nodeid2 == phy_des_node_id) \
                                or (phy_value.nodeid1 == phy_des_node_id and phy_value.nodeid2 == phy_src_node_id):
                            phy_id = phy_key

                            # 给2层topo的l3_link_id赋值 
                            if l3_link_id not in phy_value.l3_link_id:
                                phy_value.l3_link_id.append(l3_link_id)

                            g_dt.l3_topo.add_link(phy_id, l3_link_id)

                            temp = g_dt.l3_topo.links[l3_link_id]
                            temp.src_ip = src_ip
                            temp.des_ip = des_ip
                            temp.src_id = l3_src_node_id
                            temp.des_id = l3_des_node_id

                            cost_t = link['l3-unicast-igp-topology:igp-link-attributes']["metric"]
                            if ":" in src_router_id and ":" not in des_router_id:
                                id_m = l3_src_node_id + "-" + src_router_id
                                if id_m in matr_temp:
                                    temp.cost = cost_t + matr_temp[id_m]
                                else:
                                    temp.cost = cost_t
                            elif ":" not in src_router_id and ":" in des_router_id:
                                id_m = des_router_id + "-" + l3_des_node_id
                                if id_m in matr_temp:
                                    temp.cost = cost_t + matr_temp[id_m]
                                else:
                                    temp.cost = cost_t
                            elif ":" not in src_router_id and ":" not in des_router_id:
                                temp.cost = cost_t
                            else:
                                if l3_src_node_id + "-" + src_router_id in matr_temp and des_router_id + "-" + l3_des_node_id in matr_temp:
                                    temp.cost = cost_t + matr_temp[l3_src_node_id + "-" + src_router_id] + matr_temp[
                                        des_router_id + "-" + l3_des_node_id]
                                elif l3_src_node_id + "-" + src_router_id in matr_temp:
                                    temp.cost = cost_t + matr_temp[l3_src_node_id + "-" + src_router_id]
                                elif des_router_id + "-" + l3_des_node_id in matr_temp:
                                    temp.cost = cost_t + matr_temp[des_router_id + "-" + l3_des_node_id]
                                else:
                                    temp.cost = cost_t

                            if phy_value.nodeid1 == phy_src_node_id and phy_value.nodeid2 == phy_des_node_id:
                                phy_value.ifdesc1cost = temp.cost
                            else:
                                phy_value.ifdesc2cost = temp.cost

                            # print("add link %s  %s " % (src_ip,des_ip))
                            link_num += 1
                            break

        g_dt.l3_topo.link_num = link_num

    except Exception as e:
        print("parse_l3_topo_info Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.FAILED

    return ErrCode.SUCCESS


def parse_topo_info(topo):
    """解析topo信息"""

    if g_dt.phy_topo == None:
        g_dt.phy_topo = Topo()
    else:
        g_dt.phy_topo.clear_topo()

    try:
        # 解析节点 
        g_dt.phy_topo.node_num = topo["result"]["nodeNum"]
        # print('topo result:',topo["result"])

        # idms:202001080041 不要显示控制器
        # max_x = 0
        # max_y = 0

        if g_dt.phy_topo.node_num != 0:
            nodes = topo["result"]["nodes"]
            for node in nodes:
                # print(node["assetId"])
                # print('get_assetid:',node["assetId"])
                g_dt.phy_topo.add_node(node["assetId"])

                temp = g_dt.phy_topo.nodes[node["assetId"]]
                temp.name = node["assetName"]
                temp.mgrip = node["assetNetAddress"]
                temp.nettypeid = node["netElementType"]
                temp.nettypedesc = node["secondTypeIdValue"]
                temp.x = node["locationX"]
                temp.y = node["locationY"]

                # idms:202001080041 不要显示控制器
                # if temp.x > max_x:
                #     max_x = temp.x
                # if temp.y > max_y:
                #     max_y = temp.y                   

            # idms:202001080041 不要显示控制器
            # 增加一个控制器的node信息
            # g_dt.phy_topo.add_node('controller')   
            # temp = g_dt.phy_topo.nodes['controller'] 
            # temp.name = '控制器'
            # temp.mgrip = ''
            # temp.nettypeid = ''
            # temp.nettypedesc = '控制器'
            # temp.x =  max_x + 200
            # temp.y =  max_y
            # g_dt.phy_topo.node_num += 1

        # 解析链路信息
        g_dt.phy_topo.link_num = topo["result"]["linkNum"]

        if g_dt.phy_topo.link_num != 0:
            links = topo["result"]["links"]
            # print(topo["result"]["linkNum"])
            for link in links:
                if "ifOperStatus" in link.keys():
                    if link["ifOperStatus"] == "down":
                        g_dt.phy_topo.link_num -= 1
                        error_logger.error("linkid %s is down,link_num:%d" % (link["linkId"], g_dt.phy_topo.link_num))
                        continue
                # print(link["linkId"])
                g_dt.phy_topo.add_link(link["linkId"])

                temp = g_dt.phy_topo.links[link["linkId"]]
                temp.name = link["name"]
                temp.nodeid1 = link["assetId1"]
                temp.nodeid2 = link["assetId2"]
                temp.nodename1 = link["assetName1"]
                temp.nodename2 = link["assetName2"]
                temp.ifindex1 = link["ifIndex1"]
                temp.ifindex2 = link["ifIndex2"]
                temp.ifflowindex1 = link["ifFlowIndex1"]
                temp.ifflowindex2 = link["ifFlowIndex2"]
                temp.ifdesc1 = link["ifDescr1"]
                temp.ifdesc2 = link["ifDescr2"]
                snmpIfHighSpeed = link['snmpIfHighSpeed']

                extract_num = re.findall(r"\d+\.?\d*", snmpIfHighSpeed)[0]
                unit = ''.join(re.findall(r'[A-Za-z]', snmpIfHighSpeed))

                # 带宽,单位是kbps
                temp.snmpIfHighSpeed = parse_flow_to_kbps(unit, float(extract_num))
                if temp.snmpIfHighSpeed == 0:
                    temp.snmpIfHighSpeed = 1000000  # 默认带宽100M

                # 把ifindex记录到node节点上,因为故障仿真的时候,kafka需要用到
                value = g_dt.phy_topo.nodes[temp.nodeid1]
                value.port[temp.ifindex1] = Interface(temp.ifindex1)
                value.neighbour[temp.nodeid2] = link["linkId"]  # 把链路信息记录到节点里，方便根据节点ID和邻居节点ID直接找到链路ID

                value = g_dt.phy_topo.nodes[temp.nodeid2]
                value.port[temp.ifindex2] = Interface(temp.ifindex1)
                value.neighbour[temp.nodeid1] = link["linkId"]

    except Exception as e:
        print("parse_topo_info Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.FAILED

    if g_dt.phy_topo.node_num == 0:
        return ErrCode.NO_NODES_IN_TOPO

    return ErrCode.SUCCESS


def parse_l3_topo_control_info(data):
    """解析l3 topo信息
    
    Args:
        data:从SDN取到的三层TOPO信息
    Returns:
        none
    Raise:
        none
    Notes:当前的解析,三层TOPO上的节点和链路,一定能在phy上找到对应的节点和链路的
    """
    # 3层topo解析
    if g_dt.l3_topo == None:
        g_dt.l3_topo = L3Topo()
    else:
        g_dt.l3_topo.clear_topo()

    try:
        # 解析拓扑
        topologys = data["output"]["topos"]
        for topo in topologys:
            if "topoLinks" in topo:
                sdn_topo_id = topo["topoId"]  # 获取拓扑id之后，利用该id获取指定拓扑的所有链路信息（SDN）
                break

        l3_to_phy_node_id = {}

        # 传入sdn_topo_id获得所有的链路信息
        ret, sdn_resp = get_topo_link_control_from_sdn(sdn_topo_id)
        if ret != ErrCode.SUCCESS:
            info_logger.error("get_topo_link_control_from_sdn FAILED")
            error_logger.error("get_topo_link_control_from_sdn FAILED")
            return ErrCode.FAILED
        link_info = sdn_resp["output"]["links"]  # 三层拓扑中的链路信息
        link_len = len(link_info)

        # print("link_info:", link_info)
        g_dt.topo_sync_progress = 28

        # 获取调度可分配带宽阈值（SDN)
        ret, percent = get_resver_percent_from_sdn()

        g_dt.topo_sync_progress = 30
        step_begin = 30

        # 函数占用整个进度25--90， 25-30为前面部分， 30-60为中间部分， 60-90 为后面部分
        step_progress = float(30 / link_len)
        count = 0
        # 解析每条链路
        for link in link_info:
            if sync_stop_check() == 1:
                return ErrCode.USER_STOP
            g_dt.topo_sync_progress = int(count * step_progress + step_begin)  # 同步进度更新
            count += 1
            l3_src_node_id = link["srcNodeId"]
            l3_des_node_id = link["dstNodeId"]
            src_id = link["srcTpId"]  # 链路源接口名称
            des_id = link["dstTpId"]

            # 传入node_id和tp_id获得此链路的接口信息
            ret, sdn_inter_resp = get_link_info_control_from_sdn(l3_src_node_id, src_id)
            if ret != ErrCode.SUCCESS:
                info_logger.error("get_link_info_control_from_sdn FAILED")
                error_logger.error("get_link_info_control_from_sdn FAILED")
                continue

            inter_info = sdn_inter_resp["output"]["terminalPoints"][0]  # 调试运行有错误，增加了[0]
            src_index = inter_info["ifIndex"]
            src_inter = inter_info["tpIp"]

            add_flag = 0
            # 通过遍历二层topo的节点找到port中的ifindex，与src_index进行比较，然后判断src_inter与tp_ip是否相等，找到对应的node_id
            for node in g_dt.phy_topo.nodes.values():
                for _, value in node.port.items():
                    if value.ifindex == src_index and value.ip == src_inter:
                        phy_id = node.id

                        g_dt.l3_topo.add_node(phy_id, l3_src_node_id)
                        temp = g_dt.l3_topo.nodes[l3_src_node_id]
                        # 记录三层TOPO的位置
                        temp.x = g_dt.phy_topo.nodes[phy_id].x
                        temp.y = g_dt.phy_topo.nodes[phy_id].y
                        temp.name = g_dt.phy_topo.nodes[phy_id].name
                        # temp 后续有内容需要在此处添加

                        # 获取其下标，找到对应的二层node id                
                        g_dt.phy_topo.nodes[phy_id].l3_node_id = l3_src_node_id
                        # print_in_log('Add l3 node 1 !!! l2_id = %s  l3_id  ===  %s, name = %s '%(phy_id,l3_src_node_id,temp.name))
                        # 添加到对应字典中 通过三层topo的node id找到二层的node id
                        l3_to_phy_node_id[l3_src_node_id] = phy_id
                        add_flag = 1
                        break
                if add_flag == 1:
                    break

                    # 传入 node_id 和 des_id 获得此链路的接口信息, 重新获取一遍数据,防止有些节点只有进没有出会丢失
            ret, sdn_inter_resp = get_link_info_control_from_sdn(l3_des_node_id, des_id)
            if ret != ErrCode.SUCCESS:
                info_logger.error("get_link_info_control_from_sdn FAILED")
                error_logger.error("get_link_info_control_from_sdn FAILED")
                continue

            inter_info = sdn_inter_resp["output"]["terminalPoints"][0]  # 调试运行有错误，增加了[0]
            src_index = inter_info["ifIndex"]
            src_inter = inter_info["tpIp"]
            # print_in_log('# get_link_info_control_from_sdn,  src_index = %s  src_inter = %s  '%(src_index, src_inter))
            # 同上 遍历
            for node in g_dt.phy_topo.nodes.values():
                for _, value in node.port.items():
                    if value.ifindex == src_index and value.ip == src_inter:
                        phy_id = node.id

                        g_dt.l3_topo.add_node(phy_id, l3_des_node_id)
                        temp = g_dt.l3_topo.nodes[l3_des_node_id]
                        # 记录三层TOPO的位置
                        temp.x = g_dt.phy_topo.nodes[phy_id].x
                        temp.y = g_dt.phy_topo.nodes[phy_id].y
                        temp.name = g_dt.phy_topo.nodes[phy_id].name
                        # temp 后续有内容需要在此处添加

                        # 获取其下标，找到对应的二层node id                
                        g_dt.phy_topo.nodes[phy_id].l3_node_id = l3_des_node_id
                        # print_in_log('Add  l3 node 2 !!! l2_id = %s  l3_id  ===  %s, name = %s '%(phy_id,l3_src_node_id,temp.name))
                        # 添加到对应字典中 通过三层topo的node id找到二层的node id
                        l3_to_phy_node_id[l3_des_node_id] = phy_id
                        break
        # print_in_log('###### Get topo  g_dt.phy_topo.nodes num ==', len(g_dt.phy_topo.nodes))
        # print_in_log('###### Get topo  g_dt.l3_topo.nodes num ==', len(g_dt.l3_topo.nodes))

        g_dt.topo_sync_progress = 60
        step_begin = g_dt.topo_sync_progress
        count = 0

        for link in link_info:
            if sync_stop_check() == 1:
                return ErrCode.USER_STOP
            g_dt.topo_sync_progress = int(count * step_progress + step_begin)
            count += 1
            l3_link_id = link["linkId"]
            l3_src_node_id = link["srcNodeId"]
            l3_des_node_id = link["dstNodeId"]
            src_id = link["srcTpId"]
            des_id = link["dstTpId"]
            cost = link["metric"]
            bandwidth = link["bandwidth"]
            reservableBandWidth = (link["reservableBandWidth"] * percent) / 100
            attributeFlags = link["attributeFlags"]

            # 传入link_id获得每条链路的质量信息
            ret, topo_link_quality_one = get_topo_link_quality_control_from_sdn(l3_link_id)
            if ret != ErrCode.SUCCESS:
                info_logger.error("get_topo_link_quality_control_from_sdn FAILED")
                error_logger.error("get_topo_link_quality_control_from_sdn FAILED")
            else:
                topo_link_quality = topo_link_quality_one["output"]

                # 首先要两端的ip不相等
            if l3_src_node_id != l3_des_node_id:
                # 通过3层的node id 找到 2层的 node id
                if l3_src_node_id in l3_to_phy_node_id.keys() and l3_des_node_id in l3_to_phy_node_id.keys():
                    phy_src_node_id = l3_to_phy_node_id[l3_src_node_id]
                    phy_des_node_id = l3_to_phy_node_id[l3_des_node_id]
                    for phy_key, phy_value in g_dt.phy_topo.links.items():
                        # 找相应的link
                        if (phy_value.nodeid1 == phy_src_node_id and phy_value.nodeid2 == phy_des_node_id) \
                                or (phy_value.nodeid1 == phy_des_node_id and phy_value.nodeid2 == phy_src_node_id):
                            phy_id = phy_key
                            # 给2层topo的l3_link_id赋值 
                            if l3_link_id not in phy_value.l3_link_id:
                                if phy_src_node_id == phy_value.nodeid1:
                                    phy_value.l3_link_id[0] = l3_link_id
                                else:
                                    phy_value.l3_link_id[1] = l3_link_id

                            g_dt.l3_topo.add_link(phy_id, l3_link_id)
                            temp = g_dt.l3_topo.links[l3_link_id]
                            temp.src_ip = src_id
                            temp.des_ip = des_id
                            temp.src_id = l3_src_node_id
                            temp.des_id = l3_des_node_id
                            temp.cost = cost
                            temp.bandwidth = bandwidth
                            temp.reservableBandWidth = reservableBandWidth
                            temp.attributeFlags = attributeFlags

                            # 给二层topo的cost赋值
                            if phy_value.nodeid1 == phy_src_node_id and phy_value.nodeid2 == phy_des_node_id:
                                phy_value.ifdesc1cost = temp.cost
                                phy_value.resBandWidth1 = temp.reservableBandWidth
                            else:
                                phy_value.ifdesc2cost = temp.cost
                                phy_value.resBandWidth2 = temp.reservableBandWidth

                            break
        g_dt.l3_topo.link_num = len(g_dt.l3_topo.links)
        g_dt.l3_topo.node_num = len(g_dt.l3_topo.nodes)

        if (g_dt.l3_topo.link_num == 0 and g_dt.l3_topo.node_num == 0):
            info_logger.error(
                ' g_dt.l3_topo.link_num ==%d, node_num:%d' % (g_dt.l3_topo.link_num, g_dt.l3_topo.node_num))
            error_logger.error(
                '  g_dt.l3_topo.node_num ==%d, node_num:%d' % (g_dt.l3_topo.link_num, g_dt.l3_topo.node_num))
            return ErrCode.FAILED

    except Exception as e:
        print("parse_l3_topo_control_info Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.FAILED

    return ErrCode.SUCCESS


def compare_phy_l3_topo():
    """对比二层和三层的TOPO
       由于在三层TOPO解析的时候，如果不存在其对应的二层节点和链路则不进行添加。
       所以这里仅需要把在二层里有，而在三层里没有的节点进行删除即可
    
    Args:
        none
    Returns:
        none
    Raise:
        none
    """
    try:
        # 遍历字典 寻找没有三层TOPO节点的nodes
        need_remove_nodes = []
        for key in g_dt.phy_topo.nodes.keys():
            # idms:202001080041 不要显示控制器  
            # if key == 'controller':
            #     continue
            if g_dt.phy_topo.nodes[key].l3_node_id == '':  # 某节点没有对应的三层节点
                # 注意：不能直接在这里用dt.phy_topo.remove_node(node_id)删除节点，因为删除会影响外层的for循环,故而只是记录节点
                need_remove_nodes.append(key)
                for nei_node_id, nei_linkid in g_dt.phy_topo.nodes[key].neighbour.items():  # 取出这个节点相连的邻居节点
                    # 把邻居节点记录的与这个节点的关系删除
                    nei_node_info = g_dt.phy_topo.nodes[nei_node_id].neighbour
                    del nei_node_info[key]
                    g_dt.phy_topo.remove_link(nei_linkid)
                    g_dt.phy_topo.link_num -= 1

        for node_id in need_remove_nodes:
            g_dt.phy_topo.remove_node(node_id)
            g_dt.phy_topo.node_num -= 1

        need_remove_links = []
        for key in g_dt.phy_topo.links.keys():
            if len(g_dt.phy_topo.links[key].l3_link_id) == 0:  # 某链路没有对应的三层链路
                # 注意：不能直接在这里用dt.phy_topo.remove_limk(link_id)删除链路，因为删除会影响外层的for循环,故而只是记录节点
                need_remove_links.append(key)

                temp = g_dt.phy_topo.links[key]

                value = g_dt.phy_topo.nodes[temp.nodeid1]
                value.port.pop(temp.ifindex1)
                value.neighbour.pop(temp.nodeid2)

                value = g_dt.phy_topo.nodes[temp.nodeid2]
                value.port.pop(temp.ifindex2)
                value.neighbour.pop(temp.nodeid1)

        for link_id in need_remove_links:
            g_dt.phy_topo.remove_link(link_id)
            g_dt.phy_topo.link_num -= 1

        return ErrCode.SUCCESS

    except Exception as e:
        print("compare_phy_l3_topo Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.FAILED


def prase_port_ip_info(node_id, data):
    """解析从大数据获取设备的端口IP和mask信息"""
    # 解析的信息存储在topo的节点port字典中，key为ifindex，value为Interface对象，IP写入对象中
    try:
        value = g_dt.phy_topo.nodes[node_id]
        data_list = data['data']

        for info in data_list:
            # ip为空则不添加
            if info['ip'].strip() != '':
                ifindex = info['ifIndex']
                if ifindex in value.port.keys():
                    value.port[ifindex].ifindex = ifindex
                    value.port[ifindex].ip = info['ip']

        return ErrCode.SUCCESS
    except Exception as e:
        print("prase_port_ip_info Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.FAILED


def set_topo_sync_detail(status_code, reason_code):
    g_dt.topo_sync_detail["time"] = get_current_time()
    g_dt.topo_sync_detail["status"] = status_code
    g_dt.topo_sync_detail["reason"] = reason_code


def set_conf_sync_detail(status_code, reason_code):
    g_dt.conf_sync_detail["time"] = get_current_time()
    g_dt.conf_sync_detail["status"] = status_code
    g_dt.conf_sync_detail["reason"] = reason_code


def set_link_control_sync_detail(status_code, reason_code):
    g_dt.link_control_sync_detail["time"] = get_current_time()
    g_dt.link_control_sync_detail["status"] = status_code
    g_dt.link_control_sync_detail["reason"] = reason_code


def sync_stop_check():
    # 是否有停止操作
    try:
        if g_dt.stop_sync_flag == 1:
            if g_dt.topo_sync_progress != 100:
                g_dt.topo_sync_status = SyncStatusCode.SYNC_FAIL  # "同步失败"
                set_topo_sync_detail(SyncLogStatusCode.SYNC_LOG_FAIL, SyncModCode.SYNC_LOG_USER_STOP)
                set_link_control_sync_detail(SyncLogStatusCode.SYNC_LOG_FAIL, SyncModCode.SYNC_LOG_USER_STOP)
            else:
                set_link_control_sync_detail(SyncLogStatusCode.SYNC_LOG_FAIL, SyncModCode.SYNC_LOG_USER_STOP)
            return 1
        else:
            return 0
    except Exception as e:
        print("sync_stop_check Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return 0


def sync_topo_data():
    """同步topo数据。"""
    try:
        g_dt.topo_sync_status = SyncStatusCode.SYNC_SYNCING  # "同步中"

        # 获取二层topo信息
        resp = get_topo_from_bigdata()
        # resp = bigdata_topo
        if resp == None:
            info_logger.warning("get topo info form bigdata failed!")
            g_dt.topo_sync_status = SyncStatusCode.SYNC_FAIL  # "同步失败"
            set_topo_sync_detail(SyncLogStatusCode.SYNC_LOG_FAIL, SyncModCode.SYNC_LOG_TOPO_GET_FAIL)
            return ErrCode.FAILED

        if sync_stop_check() == 1:
            return ErrCode.USER_STOP

        g_dt.topo_sync_progress = 5
        # print('sync_topo_data before parse_topo_info ---')

        # 解析获取到的二层topo信息
        ret = parse_topo_info(resp)  # 二层拓扑数据记录至g_dt.phy_topo数据结构
        if ret != ErrCode.SUCCESS:
            if ret == ErrCode.NO_NODES_IN_TOPO:
                info_logger.warning("parse topo info failed!")
                g_dt.topo_sync_status = SyncStatusCode.SYNC_FAIL  # "同步失败"
                set_topo_sync_detail(SyncLogStatusCode.SYNC_LOG_FAIL, SyncModCode.SYNC_LOG_TOPO_NO_NODES)
            else:
                info_logger.warning("parse topo info failed!")
                g_dt.topo_sync_status = SyncStatusCode.SYNC_FAIL  # "同步失败"
                set_topo_sync_detail(SyncLogStatusCode.SYNC_LOG_FAIL, SyncModCode.SYNC_LOG_TOPO_PARSE_FAIL)
            return ErrCode.FAILED

        delay_s(0.2)
        g_dt.topo_sync_progress = 10

        if sync_stop_check() == 1:
            return ErrCode.USER_STOP

        # print('sync_topo_data before get_port_ip_from_bigdata ---')
        step_begin = g_dt.topo_sync_progress
        step_progress = float(10 / g_dt.phy_topo.node_num)
        count_num = 0

        # 获取网络设备有连接的接口的IP信息,遍历设备
        for key in g_dt.phy_topo.nodes.keys():
            g_dt.topo_sync_progress = int(step_begin + count_num * step_progress)
            count_num += 1
            # idms:202001080041 不要显示控制器
            # if key == 'controller':
            #     continue

            ip = g_dt.phy_topo.nodes[key].mgrip  # 节点网络ip地址
            g_dt.phy_topo.mgrip_nodeid[ip] = key  # ip地址与节点id的映射数据结构

            resp = get_port_ip_from_bigdata(key)

            if resp == None:
                info_logger.warning("get port ip info from bigdata failed!")
                g_dt.topo_sync_status = SyncStatusCode.SYNC_FAIL  # "同步失败"
                set_topo_sync_detail(SyncLogStatusCode.SYNC_LOG_FAIL, SyncModCode.SYNC_LOG_PORT_IP_GET_FAIL)
                return ErrCode.FAILED

            ret = prase_port_ip_info(key, resp)
            if ret != ErrCode.SUCCESS:
                info_logger.warning("parse port ip info failed!")
                g_dt.topo_sync_status = SyncStatusCode.SYNC_FAIL  # "同步失败"
                set_topo_sync_detail(SyncLogStatusCode.SYNC_LOG_FAIL, SyncModCode.SYNC_LOG_PORT_IP_PARSE_FAIL)
                return ErrCode.FAILED

            if sync_stop_check() == 1:
                return ErrCode.USER_STOP

        g_dt.topo_sync_progress = 20

        # 获取三层topo
        ret, resp_data = get_topo_control_from_sdn()

        if ret != ErrCode.SUCCESS:
            g_dt.topo_sync_status = SyncStatusCode.SYNC_FAIL  # "同步失败"
            set_topo_sync_detail(SyncLogStatusCode.SYNC_LOG_FAIL, SyncModCode.SYNC_LOG_GET_LAYER3_PORT_FAIL)
            # print('get_bgpls_from_odl failed')
            return ErrCode.FAILED

        g_dt.topo_sync_progress = 25
        if sync_stop_check() == 1:
            return ErrCode.USER_STOP

        # 解析三层topo ，目前占用总进度的65
        ret = parse_l3_topo_control_info(resp_data)
        if ret == ErrCode.FAILED:
            g_dt.topo_sync_status = SyncStatusCode.SYNC_FAIL  # "同步失败"
            set_topo_sync_detail(SyncLogStatusCode.SYNC_LOG_FAIL, SyncModCode.SYNC_LOG_PARSER_LAYER3_FAIL)
            # print('parse_l3_topo_info failed')
            return ErrCode.FAILED
        elif ret == ErrCode.USER_STOP:
            return ErrCode.FAILED

        g_dt.topo_sync_progress = 90
        delay_s(0.2)

        if sync_stop_check() == 1:
            return ErrCode.USER_STOP

        ret = compare_phy_l3_topo()

        if ret != ErrCode.SUCCESS:
            return ErrCode.FAILED

        g_dt.topo_sync_progress = 95
        delay_s(0.2)
        if sync_stop_check() == 1:
            return ErrCode.USER_STOP

        g_dt.topo_sync_status = SyncStatusCode.SYNC_FINISH  # "同步完成"
        g_dt.topo_sync_progress = 100
        set_topo_sync_detail(SyncLogStatusCode.SYNC_LOG_SUCCESS, SyncModCode.SYNC_LOG_SYNC_SUCCESS)

        return ErrCode.SUCCESS
    except Exception as e:
        print("sync_topo_data Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.FAILED


def compare_sna_bg_tunnel():
    """比较tunnel信息
    
    Args:
        none
    Returns:
        none
    Raise:
        none
    """
    try:
        need_del_tunid = []
        for tunid in g_tunrec.org_tuns.keys():

            flow_groupid = g_tunrec.org_tuns[tunid].flowgroup_id
            flowGroupId_info = g_sdnply.flowgroup[flow_groupid]

            # 如果从应用组获取到路径不可用，则把路径清除
            if flowGroupId_info.pri_strictStatus == 2:
                g_tunrec.org_tuns[tunid].primary_path.path_status = 'DOWN'
                g_tunrec.org_tuns[tunid].primary_path.delay = 0
                g_tunrec.org_tuns[tunid].primary_path.hops.clear()
                g_tunrec.org_tuns[tunid].primary_path.label_stack.clear()
                g_tunrec.org_tuns[tunid].primary_path.path.clear()
            if flowGroupId_info.sta_strictStatus == 2:
                g_tunrec.org_tuns[tunid].standby_path.path_status = 'DOWN'
                g_tunrec.org_tuns[tunid].standby_path.delay = 0
                g_tunrec.org_tuns[tunid].standby_path.hops.clear()
                g_tunrec.org_tuns[tunid].standby_path.label_stack.clear()
                g_tunrec.org_tuns[tunid].standby_path.path.clear()

            # 如果从应用组获取到主备路径均不可用，且从大数据获取tunnel信息失败，直接把这个tunnel信息删除
            if (flowGroupId_info.pri_strictStatus == 2 and
                    flowGroupId_info.sta_strictStatus == 2 and
                    g_tunrec.org_tuns[tunid].bguuid == ''):
                need_del_tunid.append(tunid)

        if len(need_del_tunid):
            for tun_id in need_del_tunid:
                del g_tunrec.org_tuns[tun_id]
    except Exception as e:
        info_logger.error(e)
        error_logger.error(e)


def sync_link_control_data():
    """同步链路约束
    
    Args:
        none
    Returns:
        none
    Raise:
        none
    """

    try:
        g_dt.link_control_sync_status = SyncStatusCode.SYNC_SYNCING  # "同步中"
        # 从SDN控制器获取隧道基本信息
        g_dt.link_control_sync_progress = 18
        if sync_stop_check() == 1:
            return ErrCode.USER_STOP
        ret = parse_all_tunnels()

        if ret != ErrCode.SUCCESS:
            g_dt.link_control_sync_status = SyncStatusCode.SYNC_FAIL  # "同步失败"
            set_link_control_sync_detail(SyncLogStatusCode.SYNC_LOG_FAIL, SyncModCode.SYNC_LOG_PARSER_SNA_TUNNEL_FAIL)
            return ErrCode.FAILED

        g_dt.link_control_sync_progress = 28

        start_time = g_dt.sync_data_finish_time - 600000  # 从同步时间往前推10分钟，当起始时间
        end_time = g_dt.sync_data_finish_time
        g_dt.link_control_sync_progress = 29

        # 从大数据获取隧道基本、路径、流量信息
        ret = parse_tunnels_from_bigdata(start_time, end_time)
        if ret != ErrCode.SUCCESS:
            g_dt.link_control_sync_status = SyncStatusCode.SYNC_FAIL  # "同步失败"
            set_link_control_sync_detail(SyncLogStatusCode.SYNC_LOG_FAIL, SyncModCode.SYNC_LOG_PARSER_BIG_TUNNEL_FAIL)
            return ErrCode.FAILED
        g_dt.link_control_sync_progress = 31

        if sync_stop_check() == 1:
            return ErrCode.USER_STOP

        g_dt.link_control_sync_progress = 40
        # 没有更新吞吐量删除这条隧道
        # ret = check_tunnel_info_after_bigdata()
        # if ret != ErrCode.SUCCESS:
        #     return ErrCode.FAILED	
        g_dt.link_control_sync_progress = 45

        if sync_stop_check() == 1:
            return ErrCode.USER_STOP

        g_dt.link_control_sync_progress = 50
        if sync_stop_check() == 1:
            return ErrCode.USER_STOP

        g_dt.link_control_sync_progress = 60
        if sync_stop_check() == 1:
            return ErrCode.USER_STOP

        g_dt.link_control_sync_progress = 80

        # 获取全局配置
        ret = parse_traffic_global()

        ret = parse_flowgroup_info()
        if ret != ErrCode.SUCCESS:
            g_dt.link_control_sync_status = SyncStatusCode.SYNC_FAIL  # "同步失败"
            set_link_control_sync_detail(SyncLogStatusCode.SYNC_LOG_FAIL, SyncModCode.SYNC_LOG_PARSER_FLOWGROUP_FAIL)
            return ErrCode.FAILED
        if sync_stop_check() == 1:
            return ErrCode.USER_STOP

        if sync_stop_check() != 1:
            compare_sna_bg_tunnel()

        g_dt.link_control_sync_status = SyncStatusCode.SYNC_FINISH  # "同步完成"
        g_dt.link_control_sync_progress = 100
        set_link_control_sync_detail(SyncLogStatusCode.SYNC_LOG_SUCCESS, SyncModCode.SYNC_LOG_SYNC_SUCCESS)

        return ErrCode.SUCCESS
    except Exception as e:
        print("sync_link_control_data Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.FAILED


def parse_traffic_global():
    try:
        ret, data = get_traffic_global_from_sdn()
        if ret == ErrCode.SUCCESS:
            if "affinityEnable" in data.keys():
                g_sdnply.affinityEnable = data["affinityEnable"]
            if "calcLimit" in data.keys():
                g_sdnply.calcLimit = data["calcLimit"]
            if "reservedBandwidthPercent" in data.keys():
                g_sdnply.reservedBandwidthPercent = data["reservedBandwidthPercent"]
            return ErrCode.SUCCESS
        else:
            return ErrCode.FAILED

    except Exception as e:
        print("parse_traffic_global Exception:", e)
        info_logger.error(e)
        error_logger.error(e)


def parse_flowgroup_info():
    """同步应用组数据。"""

    try:
        ret = parse_all_flowgroup()
        if ret != ErrCode.SUCCESS:
            return ErrCode.FAILED

        ret = parse_all_policy()
        if ret != ErrCode.SUCCESS:
            return ErrCode.FAILED

        ret = parse_all_sla_level()
        if ret != ErrCode.SUCCESS:
            return ErrCode.FAILED

        return ErrCode.SUCCESS

    except Exception as e:
        print("parse_flowgroup_info exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.FAILED


def sync_config_data():
    """同步config数据。"""
    try:
        g_dt.conf_sync_status = SyncStatusCode.SYNC_SYNCING  # "同步中"

        delay_s(0.5)

        if sync_stop_check() == 1:
            return ErrCode.USER_STOP

        g_dt.conf_sync_progress = 50

        delay_s(0.5)

        if sync_stop_check() == 1:
            return ErrCode.USER_STOP

        g_dt.conf_sync_status = SyncStatusCode.SYNC_FINISH  # "同步完成"
        g_dt.conf_sync_progress = 100
        set_conf_sync_detail(SyncLogStatusCode.SYNC_LOG_SUCCESS, SyncModCode.SYNC_LOG_SYNC_SUCCESS)

        return ErrCode.SUCCESS
    except Exception as e:
        print("sync_config_data exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.FAILED


def sync_data(sim_end_time):
    """同步数据。"""
    try:
        # 清除数据状态（不清除g_dt的全局同步状态，只清除三类同步的状态）
        g_dt.init_data_status()
        g_dt.topo_sync_status = SyncStatusCode.SYNC_SYNCING

        # 同步topo数据
        ret = sync_topo_data()
        if ret != ErrCode.SUCCESS:
            g_dt.topo_sync_status = SyncStatusCode.SYNC_FAIL  # 拓扑同步失败，则全局数据同步失败
            g_dt.data_sync_status = SyncStatusCode.SYNC_FAIL
            return

        # 同步配置数据
        ret = sync_config_data()
        if ret != ErrCode.SUCCESS:
            g_dt.conf_sync_status = SyncStatusCode.SYNC_FAIL  # 配置同步失败，则全局数据同步失败
            g_dt.data_sync_status = SyncStatusCode.SYNC_FAIL
            return
        sim_rate.sim_step = 0
        g_allFlows.clear()
        g_sim.clear_info()  # sprint 3 add,数据同步时，把之前的仿真信息进行删除

        # 清除tunnel信息
        g_tunrec.clear_info()

        # 保存同步时间，这个时间获取tunnel信息时，需要用到，所以在这里获取时间
        g_dt.sync_data_finish_time = sim_end_time

        # 同步链路约束数据
        # sprint3 add, 从大数据和SDN控制器获取隧道信息
        ret = sync_link_control_data()
        if ret != ErrCode.SUCCESS:
            g_dt.link_control_sync_status = SyncStatusCode.SYNC_FAIL
            g_dt.data_sync_status = SyncStatusCode.SYNC_FAIL
            return

        g_dt.data_sync_status = SyncStatusCode.SYNC_FINISH
        if debug_postman:
            print('\n Sync data finshed ! \n ')

        return
    except Exception as e:
        print("sync_data exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return


def stop_sync_data():
    """停止数据同步。"""

    # 设置stop状态
    g_dt.stop_sync_flag = 1

    while g_dt.data_sync_status == 1:
        delay_s(0.1)

    # 设置数据同步状态
    if g_dt.topo_sync_status == SyncStatusCode.SYNC_SYNCING:
        g_dt.topo_sync_status = SyncStatusCode.SYNC_FAIL
        g_dt.topo_sync_detail["time"] = get_current_time()
        g_dt.topo_sync_detail["status"] = SyncLogStatusCode.SYNC_LOG_FAIL
        g_dt.topo_sync_detail["reason"] = SyncModCode.SYNC_LOG_USER_STOP

    if g_dt.conf_sync_status == SyncStatusCode.SYNC_SYNCING:
        g_dt.conf_sync_status = SyncStatusCode.SYNC_FAIL
        g_dt.conf_sync_detail["time"] = get_current_time()
        g_dt.conf_sync_detail["status"] = SyncLogStatusCode.SYNC_LOG_FAIL
        g_dt.conf_sync_detail["reason"] = SyncModCode.SYNC_LOG_USER_STOP

    if g_dt.link_control_sync_status == SyncStatusCode.SYNC_SYNCING:
        g_dt.link_control_sync_status = SyncStatusCode.SYNC_FAIL
        g_dt.link_control_sync_detail["time"] = get_current_time()
        g_dt.link_control_sync_detail["status"] = SyncLogStatusCode.SYNC_LOG_FAIL
        g_dt.link_control_sync_detail["reason"] = SyncModCode.SYNC_LOG_USER_STOP

    g_dt.stop_sync_flag = 0

    return ErrCode.SUCCESS


def get_sync_status():
    """获取数据同步状态"""

    data = {
        "syncButStatus": g_dt.data_sync_status,
        "topo": {
            "progress": g_dt.topo_sync_progress,
            "status": g_dt.topo_sync_status
        },
        "config": {
            "progress": g_dt.conf_sync_progress,
            "status": g_dt.conf_sync_status
        },
        "linkControl": {
            "progress": g_dt.link_control_sync_progress,
            "status": g_dt.link_control_sync_status,
        },
        "syncTime": g_dt.sync_data_finish_time  # sprint3新增，用于配置同步界面最下方显示
    }

    return ErrCode.SUCCESS, data
