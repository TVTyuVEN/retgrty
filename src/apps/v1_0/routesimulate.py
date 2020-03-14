# -*- encoding: utf-8 -*-
"""
@File    : routesimulate.py
@Time    : 2019/05/29 14:04:36
@Author  : 
@License : Copyright (c) 2004-2019 New H3C Tech. Co., Ltd. All rights reserved.
@Desc    : 路由仿真
"""
import copy
import requests
import time
import networkx as nx
from functools import reduce

from apps.util import g_sim
from apps.util import get_start_end_time, get_end_time
from apps.util import error_logger,info_logger

from apps.errcode import ErrCode

from apps.v1_0.bginterface import get_quinte_from_bigdata, get_quient_path_from_bigdata

gl_digkstra_graph = nx.DiGraph()
gl_after_faulte_graph = nx.DiGraph()

def judge_kafaka_node_in_fault_list(node_ip,node_port):
    try:
        for info in g_sim.all_fault:
            if info['host'] == node_ip and  info['port'] == node_port:
                # 成功代表节点在故障节点列表里
                return ErrCode.SUCCESS
        return ErrCode.FAILED
    except Exception as e:
        info_logger.error(e)
        error_logger.error(e)
        print("judge_kafaka_node_in_fault_list Exception:", e)
        return ErrCode.FAILED

def get_cycle_time(ts):
    try:
        start_time = int(g_sim.time_start)
        cycle = int(g_sim.time_cycle)
        num = int((ts - start_time) / cycle)
        cyc_time = start_time + num * cycle
        return cyc_time
    except Exception as e:
        info_logger.error(e)
        error_logger.error(e)
        print("get_cycle_time Exception:", e)
        return 0

def get_all_fault_node_quintet_info():
    try:
        """ 获得所有故障节点对的五元组等信息，把其填入sim.fault_backgrond_info
        
        Args:
            none
        Returns:
            none
        Raise:
            none
        """
        # 如果没有设置故障,则没必要获取故障节点的背景流
        if len(g_sim.all_fault) == 0:
            return

        start_time = g_sim.time_sim_info[0]['start_time']
        end_time = g_sim.time_sim_info[0]['start_time'] + g_sim.time_cycle

        etime = g_sim.time_sim_info[-1]['end_time']
        ts = start_time

        # 遍历所有的时间节点
        while ts < etime:
            # 遍历所有的故障信息
            quintet_list = []
            for info in g_sim.all_fault:
                fault_node_ip = info['host']
                fault_node_port = info['port']
                respdata = get_quinte_from_bigdata(ts, end_time,fault_node_ip, fault_node_port)
                # 注：得用extend，这样最后的quintet_list格式为[{},{},{},....]
                # {
                # "srcIp" : "10.121.44.12",
                # "destIp" : "10.121.44.13",
                # "srcPort" : 3456,
                # "destPort" ： 6543，
                # "protocol" : 1
                # "totalBytes": 123
                # }
                
                # 因为环境很有可能出现无数据返回的情况，测试过程中经常出现环境未配号，返回值out:[]
                if respdata != None:
                    quintet_list.extend(respdata)

            length = len(quintet_list) 
            g_sim.fault_backgrond_info[ts] = []
            for i in range(length):
                has_flag = 0

                # 速率为0的五元组，不添加
                if quintet_list[i]['speed'] == 0:
                    continue
                # 协议不是UDP和TCP，不添加
                if quintet_list[i]['protocol'] != 17 and quintet_list[i]['protocol'] != 6:
                    continue

                for oldquint in g_sim.fault_backgrond_info[ts]:
                    if (quintet_list[i]['srcPort'] == oldquint['srcPort'] and 
                        quintet_list[i]['destPort'] == oldquint['destPort'] and
                        quintet_list[i]['protocol'] == oldquint['protocol'] and
                        quintet_list[i]['srcIp'] == oldquint['srcIp'] and
                        quintet_list[i]['destIp'] == oldquint['destIp']):
                        has_flag = 1
                        break
                if has_flag == 0:
                    g_sim.fault_backgrond_info[ts].append(quintet_list[i])
                    
            #error_logger.error('add quint')
            #error_logger.error("%d"%(len(g_sim.fault_backgrond_info[start_time])))

            #if len(quintet_list):
                # 把quintet去重，保存到sim.fault_backgrond_info里
                #run_function = lambda x, y: x if y in x else x + [y]
                #g_sim.fault_backgrond_info[start_time] = reduce(run_function, [[], ] + quintet_list)

            ts += g_sim.time_cycle
            end_time += g_sim.time_cycle
            if end_time > etime:
                end_time = etime
    except Exception as e:
        info_logger.error(e)
        error_logger.error(e)
        print("get_all_fault_node_quintet_info Exception:", e)
 
def get_background_route_before_fault():
    try:
        """获得故障点及故障链路上，所有的背景流，在故障前的具体路径
        
        Args:
            none
        Returns:
            none
        Raise:
            none
        """
        length = len(g_sim.fault_backgrond_info)
        if length != 0:
            add_progress = 40 / length
            progress = 15
        else:
            return

        for key, value in g_sim.fault_backgrond_info.items():
            start_time = key
            end_time = start_time + g_sim.time_cycle
            for one_back_flow in value:
            # 正式时，打开
                if one_back_flow['protocol'] == 17:
                    protocol = 'UDP'
                elif one_back_flow['protocol'] == 6:
                    protocol = 'TCP'
                else:
                    continue

                
                data = get_quient_path_from_bigdata(protocol,
                                                    start_time,
                                                    end_time,
                                                    one_back_flow['srcIp'],
                                                    one_back_flow['srcPort'],
                                                    one_back_flow['destIp'],
                                                    one_back_flow['destPort'])

                if data != None:
                    link_num = data['linkNum']
                    index = 0
                    path = []

                    if link_num == 1:
                        link_info = data['links'][0]
                        temp = {'start_node_id':link_info['assetId1'],
                                    'end_node_id':link_info['assetId2'],
                                    'linkid':link_info['linkId']}

                        path.append(temp)

                        one_back_flow['before_route'] = path  
                
                    elif link_num != 0:
                        start_point = []
                        end_point = []
                        link_point = []
                        for index in range(link_num):    
                            link_info = data['links'][index]
                            start_point.append(link_info['assetId1'])
                            end_point.append(link_info['assetId2'])
                            link_point.append(link_info['linkId'])

                        # 对于当前而言，仅需要链路的第一个节点和最后一个节点，在故障后仿真时，即可得到路由，所以这里不重新排列所有的路径了
                        first_index = [start_index for start_index in range(len(start_point)) if start_point[start_index] not in end_point][0]
                        #for index in range(len(start_point)):
                        #    if start_point[index] not in end_point:
                        #        first_index = index
                        #        break
                        
                        # 找准路径的起始节点
                        if first_index != 0: 
                            first = start_point.pop(first_index)
                            start_point.insert(0, first)
                            first = end_point.pop(first_index)
                            end_point.insert(0, first)
                            first = link_point.pop(first_index)
                            link_point.insert(0,first)
                        

                        end_index = [end_index for end_index in range(len(end_point)) if end_point[end_index] not in start_point][0]
                        #for index in range(len(end_point)):
                        #    if end_point[index] not in start_point:
                        #        end_index = index
                        #        break
                        if end_index != (link_num - 1):
                            end_pop = start_point.pop(end_index)
                            start_point.append(end_pop)
                            end_pop = end_point.pop(end_index)
                            end_point.append(end_pop)
                            end_pop = link_point.pop(end_index)
                            link_point.append(end_pop)

                        for i in range(link_num):
                            temp = {'start_node_id':start_point[i],
                                    'end_node_id':end_point[i],
                                    'linkid':link_point[i]}
                            path.append(temp)

                        one_back_flow['before_route'] = path     
            
    except Exception as e:# 正式时，打开
        print("get_background_route_before_fault Exception:", e)
        info_logger.error(e)
        error_logger.error(e)

def print_sim_link_info():
    try:
        for value in g_sim.time_sim_info:
            start_time = value['start_time']
            # 获取start_time 
            period_link_before = g_sim.before_fault_link_info[start_time]
            period_link_after = g_sim.after_fault_link_info[start_time]

            # 获取链路信息
            for key, value in period_link_before.link_info.items():
                linkInfo_before = value

                linkInfo_after = period_link_after.link_info[key]   
                # 获取带宽利用率 
                rate1to2_before = linkInfo_before.a_to_b.out_use_ratio 
                rate1to2_before_speed = linkInfo_before.a_to_b.speed

                rate1to2_after = linkInfo_after.a_to_b.out_use_ratio 
                rate1to2_after_speed = linkInfo_after.a_to_b.speed

                rate2to1_before = linkInfo_before.b_to_a.out_use_ratio 
                rate2to1_before_speed = linkInfo_before.b_to_a.speed

                rate2to1_after = linkInfo_after.b_to_a.out_use_ratio
                rate2to1_after_speed = linkInfo_after.b_to_a.speed           
    except Exception as e:# 正式时，打开
        print("print_sim_link_info Exception:", e)
        info_logger.error(e)
        error_logger.error(e)


# sprint 3 modify
def built_before_dijkstra_network(): 
    try: 
        """建立故障前的迪克斯特拉图
        
        Args:
            none
        Returns:
            none
        Raise:
            none
        """
        # 先清理之前的信息
        gl_digkstra_graph.clear() 

        # 添加节点
        for key in g_sim.l3_topo.nodes:
            if g_sim.l3_topo.nodes[key].fault != 'yes':
                gl_digkstra_graph.add_node(key)
        
        # 添加链路
        for key in g_sim.l3_topo.links:
            if g_sim.l3_topo.links[key].fault != 'yes':
                src_id = g_sim.l3_topo.links[key].src_id
                des_id = g_sim.l3_topo.links[key].des_id
                if g_sim.l3_topo.nodes[src_id].fault != 'yes' and g_sim.l3_topo.nodes[des_id].fault != 'yes':
                    gl_digkstra_graph.add_edges_from([(src_id, des_id)], weight=g_sim.l3_topo.links[key].cost)
    except Exception as e:# 正式时，打开
        print("built_before_dijkstra_network Exception:", e)
        info_logger.error(e)
        error_logger.error(e)

# sprint 3 modify       
def built_after_fault_dijkstra_network():  
    try:
        """建立故障后的迪克斯特拉图
        
        Args:
            none
        Returns:
            none
        Raise:
            none
        """
        # 先清理gl_after_faulte_graph
        gl_after_faulte_graph.clear() 

        # 遍历所有的节点，如果节点已经被设置为故障节点了，则不添加
        for key in g_sim.af_l3_topo.nodes:
            if g_sim.af_l3_topo.nodes[key].fault != 'yes':
                gl_after_faulte_graph.add_node(key)
        
        # 遍历所有的链路，如果链路没有设置为故障链路，并且链路两端的节点没有设置为故障节点，才添加此链路
        for key in g_sim.af_l3_topo.links:
            if g_sim.af_l3_topo.links[key].fault != 'yes':
                src_id = g_sim.af_l3_topo.links[key].src_id
                des_id = g_sim.af_l3_topo.links[key].des_id
                if g_sim.af_l3_topo.nodes[src_id].fault != 'yes' and g_sim.af_l3_topo.nodes[des_id].fault != 'yes':
                    gl_after_faulte_graph.add_edges_from([(src_id, des_id)], weight=g_sim.af_l3_topo.links[key].cost)
    except Exception as e:# 正式时，打开
        print("built_after_fault_dijkstra_network Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        
def get_dijkstra_path(phy_src_id, phy_des_id,flag,startTime):
    """用迪克斯特拉图计算故障前的路径
    
    Args:
        phy_src_id:物理层源节点id
        phy_des_id:物理层源目的点id
        flag:'before_fault'(获取故障前路由),'after_fault'(获取故障后路由)
    Returns:
        none
    Raise:
        none
    """ 
    try:
        if flag == 'before_fault':
            phy_topo = g_sim.topo
            l3_topo = g_sim.l3_topo
        else:
            phy_topo = g_sim.af_topo
            l3_topo = g_sim.af_l3_topo
        # 因为传入的参数是物理层的ID，先转换为三层ID
        layer3_src_id = phy_topo.nodes[phy_src_id].l3_node_id
        layer3_des_id = phy_topo.nodes[phy_des_id].l3_node_id

        if flag == 'before_fault':
            # 获取路径,路径的格式:[a,b,c,c]，代表这条流的路径是a-->b-->c-->d
            path = nx.dijkstra_path(gl_digkstra_graph, source = layer3_src_id, target = layer3_des_id, weight='weight')
        else:
            # 获取路径,路径的格式:[a,b,c,c]，代表这条流的路径是a-->b-->c-->d
            path = nx.dijkstra_path(gl_after_faulte_graph, source = layer3_src_id, target = layer3_des_id, weight='weight')

        data = {}
        path_list = []
        jump = len(path)
        cyc_len = jump - 1
        if cyc_len > 0:
            for i in range(cyc_len):
                if path[i] in l3_topo.nodes and path[(i+1)] in l3_topo.nodes:
                    # 把三层节点转换为二层节点
                    phy_sourcid = l3_topo.nodes[path[i]].phy_id 
                    phy_desid = l3_topo.nodes[path[(i+1)]].phy_id

                    # 通过节点ID，取得其对应的二层链路ID
                    if phy_sourcid in phy_topo.nodes:
                        linkid = phy_topo.nodes[phy_sourcid].neighbour[phy_desid]

                        # 记录一条链路信息
                        one_link_path = {'start_node_id':phy_sourcid,'end_node_id':phy_desid,'linkid':linkid}
                        path_list.append(one_link_path)
        
        # 把所有的链路信息输出，格式未{'path':[{'start_node_id':phy_sourcid,'end_node_id':phy_desid,'linkid':linkid}]}
        data['path'] = path_list

        data['jump'] = jump

        # sprint 3 add
        # 计算时延
        data['delay'] = calc_dijstra_path_delay(path,startTime)

        return ErrCode.SUCCESS,data
    except Exception as e:
        print("get_dijkstra_path Exception:", e)
        error_logger.error(e)
        info_logger.error(e)
        return ErrCode.BGP_ROUTE_UNREACH,None

def get_background_route_after_fault():             
    """获得故障点及故障链路上，所有的背景流，在故障后的具体路径

        具体实现待调整
    Args:
        none
    Returns:
        none
    Raise:
        none
    """
    try:
        for key, value in g_sim.fault_backgrond_info.items():
            for one_back_flow in value:
                if 'before_route' in one_back_flow.keys():
                    if len(one_back_flow['before_route']) > 0:
                        before_fault_path = one_back_flow['before_route']
                        phy_begin_node = before_fault_path[0]['start_node_id']
                        phy_end_node = before_fault_path[-1]['end_node_id']
                        # 如果起始节点或结束节点为故障点，则链路不可达
                        if phy_begin_node not in g_sim.topo.nodes or phy_end_node not in g_sim.topo.nodes:
                            one_back_flow['after_route'] = [] 
                            one_back_flow['after_status'] = 'interrupt'

                        elif g_sim.topo.nodes[phy_begin_node].fault == 'yes' or g_sim.topo.nodes[phy_end_node].fault == 'yes':
                            one_back_flow['after_route'] = [] 
                            one_back_flow['after_status'] = 'interrupt'
                        else:
                            # 获取路径
                            ret, data = get_dijkstra_path(phy_begin_node, phy_end_node,'after_fault', key)
                            if ret == ErrCode.SUCCESS:
                                one_back_flow['after_route'] = data['path']
                                one_back_flow['after_status'] = 'normal'
                            else:
                                # 如果路径不可达，则状态为interrupt
                                one_back_flow['after_route'] = [] 
                                one_back_flow['after_status'] = 'interrupt'
    except Exception as e:
        print("get_background_route_after_fault Exception:", e)
        error_logger.error(e)
        info_logger.error(e)
                
# sprint3 add
def calc_dijstra_path_delay(path,startTime):
    """计算dijstra路径的总时延;path = [a,b,c,d],其中a,b,c,d为各个三层链路的节点
    
    Args:
        path
    Returns:
        时延的大小
    Raise:
        none
    """
    delay = 0
    if len(path) <= 1:
        return delay
    
    cyc_len = len(path) - 1
    for i in range(cyc_len):
        # 把三层节点转换为二层节点
        l3_srcid = path[i]
        l3_desid = path[(i+1)]

        for linkid in g_sim.l3_topo.links.keys():
            if l3_desid == g_sim.l3_topo.links[linkid].des_id and l3_srcid == g_sim.l3_topo.links[linkid].src_id:
                if startTime in g_sim.l3_topo.links[linkid].delay.keys():
                    delay += g_sim.l3_topo.links[linkid].delay[startTime] #
                else:
                    print("shit startTime not in delay keys", startTime, g_sim.l3_topo.links[linkid].delay.keys())
                break
  
    return delay
    
