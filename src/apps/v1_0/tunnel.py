# -*- encoding: utf-8 -*-
"""
@File    : tunnel.py
@Time    : 2019/09/21 14:45:04
@Author  : 
@License : Copyright (c) 2004-2019 New H3C Tech. Co., Ltd. All rights reserved.
@Desc    : Tunnel数据结构与实现
"""
import requests
import copy
import operator
from flask import request

from apps.errcode import ErrCode
from apps.util import g_tunrec, g_sim, g_dt, g_allFlows
from apps.util import error_logger, info_logger
from apps.util import get_end_time, get_start_end_time

from apps.v1_0.bginterface import *
from apps.v1_0.topo import L3TopoNode, TopoNode
from apps.v1_0.application import tunnel_flowgroup_storing, parse_flowgroup_path
from apps.v1_0.sdn import get_all_tunnels
from apps.v1_0.test import *
from apps.v1_0.sdnsimctrl import *
from param import *

class TunnelHop(object):
    """Class for hop of tunnel.
    
    Attributes:
        none
    """

    def __init__(self):
        self.node_id = ''         # 二层TOPO的ID
        self.node_name = 'N/A'    # 节点名称，没有
        self.out_interface = ''   # 端口名称g1/0/24, 大数据没有名称有IP
        self.cost = 1             # 大数据没有,从链路里去取


class TunnelPath(object):
    """Class for path of tunnel.
    
    Attributes:
        none
    """

    def __init__(self):
        self.path_status = 'DOWN'  # 这个根据路径，根据路径和当时的TOPO来计算。DOWN/UP,UP是工作状态，如果状态是Down，则说明路径挂掉了,其他的参数就无意义了
        self.hop_num = 0 # 根据路径来计算
        self.delay = 0  # 大数据没有，SDN也没有。都根据走过的路径来计算
        self.hops = {}  # TunnelHop，SDN是LINKID，大数据是端口IP {node_id:TunnelHop()}
        self.label_stack = []  # 暂时不存
        self.path = [] # {'start_node_id':phy_sourcid,'end_node_id':phy_desid,'linkid':linkid}
        self.strict_result = 0 # 选路状态的结果。0：勉强选路1：严格选路2：路径不可用3：未选路 

class Tunnel(object):
    """Class for tunnel.
    
    Attributes:
        none
    """
    
    def __init__(self):
        self.bguuid = ''       # tunnel在bigdata大数据里的uuid
        self.sdnuuid = ''      # tunnel在sdn的uuid
        self.name = 'N/A'      # sdn 有，大数据没有
        self.node_name = 'N/A' # 起始节点名称，sdn没有 , 大数据没有
        self.src_ip = 'N/A'    # sdn 有， 大数据有
        self.des_ip = 'N/A'   # sdn 有， 大数据有
        self.src_id = ''  # 对应二层topo的节点ID，自己对应
        self.des_id = ''  # 对应二层topo的节点ID，自己对应
        self.tunnel_type = 'N/A' # sdn 有， 大数据有 
        self.business_name = 'N/A' # sdn 没有， 大数据没有
        self.status = 'DOWN'  # DOWN/UP/NONE SDN返回值是这样的，Uint16类型，无默认值，范围0-3（0: none，1：Up，2：Down，3：AdminDown。），进行转换一下

        self.path_num = 0                # path的条数，如果主路径primary_path和备路径standby_path都存在，则path_num = 2
        self.active_path = "primary"     # 当前有效的tunnel，如果是“primary”，则代表主路径有效；如果是“standby”，则代表备路径有效
        self.primary_path = TunnelPath() # sdn 有，需要根据tunnelpath下的status转换一下; 大数据有
        self.standby_path = TunnelPath() # sdn 有，需要根据tunnelpath下的status转换一下， 大数据有

        self.throughput = 0    # sdn 没有，大数据有,默认修改为-1，用于删除有误的隧道信息
        self.max_throughput = 0
        self.min_throughput = 0
        self.bandwidth = 0
        self.flowgroup_id = 'N/A'  #隧道对应的应用组流组信息

# sprint 3 add待补充
def get_tunnel_path(phy_src_id, phy_des_id):
    """获取从源节点到目的节点的，基于现网的tunnel路由
    
    Args:
        none
    Returns:
        none
    Raise:
        none
    """
    try:
        #url = TUNNEL_PATH_URL%(phy_src_id, phy_des_id)
        #response = requests.get(url, headers={"authen":"DataCore"})
        data = []
        return ErrCode.SUCCESS, data
    except Exception as e:
        print("get_tunnel_path Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.FAILED,[]

# sprint 3 add待补充
def parse_one_tunnel(id, data):
    """解析新获得的tunnel,这是基于之前已经获取过网络的tunnel，这次是基于新的环境再获取之前的tunnelid对应的tunnel
       如果data返回的值为不可达，也需要记录，只是path_num需记录为0而已
    
    Args:
        id:tunnel的id
        data:tunnel数据
    Returns:
        none
    Raise:
        none
    """
    try:
        for time_step in g_tunrec.sim_aftuns.keys(): # 按时间段遍历
            tun_step = g_tunrec.sim_aftuns[time_step]
            if id not in tun_step.keys():
                tun_step[id] = Tunnel()
            temp = tun_step[id]
            temp.name = data['name']
        
    except Exception as e:
        print("parse_one_tunnel Exception:", e)
        info_logger.error(e)
        error_logger.error(e)

def sdn_status_trans(status):
    """转换路径状态
    """
    try:
        if status == 0:
            return "none"
        elif status == 1:
            return "Up"
        elif status == 2 or status == 3:
            return "Down"
    except Exception as e:
        print("sdn_status_trans Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.FAILED,[]

def path_storing(links):
    """Tunnel主备信息的存储
    
    Args:
        links：linkid为键的字典列表
    Returns:
        None
    Raise:
        none
    """ 
    try: 
        path = TunnelPath() 
        start_point = []
        end_point = []
        link_point = []

                                        
        path.hop_num = len(links) + 1
        if len(links) == 0:  #判断是否存在
            path.path_status = "DOWN"
            return path

        link_num = len(links)

        for num in range(link_num):
            
            l3_link_id = links[num]["linkId"]
            if l3_link_id not in g_dt.l3_topo.links.keys():
                error_logger.warning("path_storing hop1 failed")
                path.path_status = "DOWN"
                path.hop_num = 0
                path.hops.clear()
                path.path.clear()
                return path
            
            # 根据三层链路，找到二层链路和节点信息
            l3_src_nodeId = g_dt.l3_topo.links[l3_link_id].src_id
            l3_des_nodeId = g_dt.l3_topo.links[l3_link_id].des_id
            phy_src_nodeid = g_dt.l3_topo.nodes[l3_src_nodeId].phy_id
            phy_des_nodeid = g_dt.l3_topo.nodes[l3_des_nodeId].phy_id

            phy_linkid = g_dt.l3_topo.links[l3_link_id].phy_id
          
            start_point.append(phy_src_nodeid)
            end_point.append(phy_des_nodeid)
            link_point.append(phy_linkid)
            path.delay += 0 # 一开始无链路时延信息

        path.path_status = "UP"

        # 实测三楼环境，SDN返回的数据，没有按链路连接顺序给出，所以这里重新组织路径
        if link_num == 1:
            temp = {'start_node_id':start_point[0],
                    'end_node_id':end_point[0],
                    'linkid':link_point[0]}
            path.path.append(temp)
        else:
            # 对于当前而言，仅需要链路的第一个节点和最后一个节点，在故障后仿真时，即可得到路由，所以这里不重新排列所有的路径了
            first_index = [start_index for start_index in range(len(start_point)) if start_point[start_index] not in end_point][0]
            # 找准路径的起始节点
            if first_index != 0: 
                first = start_point.pop(first_index)
                start_point.insert(0, first)
                first = end_point.pop(first_index)
                end_point.insert(0, first)
                first = link_point.pop(first_index)
                link_point.insert(0,first)

            end_index = [end_index for end_index in range(len(end_point)) if end_point[end_index] not in start_point][0]
            if end_index != (link_num - 1):
                end_pop = start_point.pop(end_index)
                start_point.append(end_pop)
                end_pop = end_point.pop(end_index)
                end_point.append(end_pop)
                end_pop = link_point.pop(end_index)
                link_point.append(end_pop)
            
            # 对中间进行排序
            for i in range(link_num + 1):
                if i == 0:
                    temp = {'start_node_id':start_point[i], 
                            'end_node_id':end_point[i],
                            'linkid':link_point[i]}
                    path.path.append(temp)
                else:
                    for j in range(len(start_point)):
                        if path.path[i-1]["end_node_id"] == start_point[j]:
                            temp = {'start_node_id':start_point[j],
                                    'end_node_id':end_point[j],
                                    'linkid':link_point[j]}  
                            path.path.append(temp)
                            break      

        # 存储hops结构，为什么不能在前面存HOPS，因为一旦路径没有按序给出的话，则会有中间节点多存，尾节点没有存储的问题。
        for i in range(link_num):
            one_hop = TunnelHop()
            one_hop.node_id = start_point[i]
            one_hop.node_name = g_dt.phy_topo.nodes[one_hop.node_id].name
            phy_linkid = link_point[i]
            if g_dt.phy_topo.links[phy_linkid].nodeid1 == start_point[i]:
                one_hop.out_interface = g_dt.phy_topo.links[phy_linkid].ifdesc1 
            else:
                one_hop.out_interface = g_dt.phy_topo.links[phy_linkid].ifdesc2 
            path.hops[one_hop.node_id]=one_hop 

        one_hop = TunnelHop()
        one_hop.node_id = end_point[-1]
        one_hop.node_name = g_dt.phy_topo.nodes[one_hop.node_id].name
        one_hop.out_interface = 'N/A'
        path.hops[one_hop.node_id]=one_hop 
        
        return path

    except Exception as e:
        print("path_storing Exception:", e)
        path.hops.clear()
        path.path.clear()
        info_logger.error(e)
        error_logger.error(e)
        return path      

def parse_all_tunnels():
    """解析所有的tunnels信息，并保存在Tunnle实例化后的unrec.sim_orgtuns[uuid]结构中，uuid为二层node_id+tunnel_id
    
    Args:
        none
    Returns:
        none
    Raise:
        none
    """
    try:
        tunnel_num, data = get_all_tunnels()
        path_info = parse_flowgroup_path()
        if path_info == None:
            error_logger.warning("no_configure_message")
            return ErrCode.SUCCESS
        if data == None:
            error_logger.error("parse_all_tunnels failed")
            return ErrCode.FAILED
        if "tunnel" not in data:
            return ErrCode.SUCCESS
        data = data["tunnel"]
        #print("tunnel_num", tunnel_num)
        for i in range(tunnel_num): 
            if data[i]["mode"] == 0 and data[i]["status"] == 1:  #只取MPLSTE类型隧道
                for paths in path_info:
                    if data[i]["tunnelId"] == paths["tunnelid"]:
                        tunnel_temp = Tunnel()
                        tunnel_temp.sdnuuid = data[i]["tunnelId"]
                        tunnel_temp.name = data[i]["name"]

                        tunnel_temp.tunnel_type = data[i]["tunnelType"]  #True表示用户导入隧道，不允许改变设备上的配置，False表示用户添加隧道，需要配置设备。      
                        # tunnel_temp.status = sdn_status_trans(data[i]["status"])
                    

                        tunnel_temp.path_num = len(paths["paths"])
                        if tunnel_temp.path_num == 0:   #主备路径都不存在直接跳过
                            continue
                        
                        pri_status = 3 # 初始化，未选路
                        sta_status = 3 #
                        for one_path in paths["paths"]:          #主备路径的存储
                            if one_path["pathNumber"] == 0:
                                tunnel_temp.primary_path = path_storing(one_path["linkList"])
                                pri_status = one_path["strictStatus"]

                            elif one_path["pathNumber"] == 1:
                                tunnel_temp.standby_path = path_storing(one_path["linkList"]) 
                                sta_status = one_path["strictStatus"]

                        if tunnel_temp.primary_path.path_status == "UP":    #当前运行路径判断
                            tunnel_temp.active_path = "primary"
                            phy_src_id = tunnel_temp.primary_path.path[0]["start_node_id"]
                            phy_des_id = tunnel_temp.primary_path.path[-1]["end_node_id"]
                        elif tunnel_temp.primary_path.path_status == "DOWN" and tunnel_temp.standby_path.path_status == "UP":
                            tunnel_temp.active_path = "standby"
                            phy_src_id = tunnel_temp.standby_path.path[0]["start_node_id"]
                            phy_des_id = tunnel_temp.standby_path.path[-1]["end_node_id"]
                        else:
                            tunnel_temp.status = "DOWN"
                            continue

                        l3_src_id = g_dt.phy_topo.nodes[phy_src_id].l3_node_id
                        tunnel_temp.node_name = g_dt.phy_topo.nodes[phy_src_id].name
                        tunnel_temp.src_id = phy_src_id
                        tunnel_temp.src_ip = g_dt.phy_topo.nodes[phy_src_id].mgrip

                        tunnel_temp.des_id = phy_des_id
                        tunnel_temp.des_ip = g_dt.phy_topo.nodes[phy_des_id].mgrip

                        if (pri_status == 2 and sta_status == 2) or (pri_status == 2 and sta_status == 3) or (pri_status == 3 and sta_status == 2):
                            tunnel_temp.status = "DOWN"
                        else:
                            tunnel_temp.status = "UP"

                        uuid = phy_src_id + data[i]["name"]                        #存储的uuid为二层节点id加上隧道id
                
                        g_tunrec.sdntunnelid_to_tunneluuid[tunnel_temp.sdnuuid] = uuid  #tunnel_id到uuid的字典
                        g_tunrec.org_tuns[uuid] = tunnel_temp

                        # 把tunnel  name存储在各个起始节点上，方便显示
                        g_dt.phy_topo.nodes[phy_src_id].tun_id[data[i]["name"]] = uuid
                        g_dt.l3_topo.nodes[l3_src_id].tun_id[data[i]["name"]] = uuid

                        # 气泡显示，用于提供用户查看当前Tunnel是走向哪个网元的
                        des_node_name = g_dt.phy_topo.nodes[phy_des_id].name
                        name_l2 = data[i]["name"] + '(目的:' + des_node_name + ')'
                        g_dt.phy_topo.nodes[phy_src_id].tun_name.append(name_l2)
                        g_dt.l3_topo.nodes[l3_src_id].tun_name.append(name_l2)
        
        ret = tunnel_flowgroup_storing()  #存储流组信息
        if ret != ErrCode.SUCCESS:
            return ErrCode.FAILED

        return ErrCode.SUCCESS

    except Exception as e:
        print("parse_all_tunnels Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.FAILED

def copy_all_base_tunnel_flow(source_start_time, des_start_time,des_end_time):
    """把tunnel，直接存多份
        例如仿真的时间周期为1小时，而这1小时由于有flow导入被切分成5段了,在其他函数已经存了g_tunrec.sim_orgtuns[t1]了,
        这里把g_tunrec.sim_orgtuns[t2]到g_tunrec.sim_orgtuns[t5]都存成g_tunrec.sim_orgtuns[t1]一样的数据值    
    Args:
        source_start_time:第一段数据的时间
        des_start_time：第二段数据的时间
        des_end_time：结束的时间
    Returns:
        none
    Raise:
        none
    """   
    try:
        start_time_new = des_start_time
        sim_end_time = des_start_time
        while sim_end_time != des_end_time:
            g_tunrec.sim_orgtuns[start_time_new] = copy.deepcopy(g_tunrec.sim_orgtuns[source_start_time])
            sim_end_time = get_end_time(start_time_new)
            start_time_new = sim_end_time
    except Exception as e:
        print("copy_all_base_tunnel_flow Exception:", e)
        info_logger.error(e)
        error_logger.error(e)

def separ_tunnel():
    """从背景流量中分离tunnel流量,仅在首次仿真或重新仿真时才需要
    
    Args:
        none
    Returns:
        none
    Raise:
        none
    """
    try:
        start_time = g_sim.time_start
        end_time = g_sim.time_end
        cycle = g_sim.time_cycle
        cycle_num = int(g_sim.time_cycle_num)

        one_cycle_start = start_time
        one_cycle_end_time = min(start_time + cycle, end_time)
        info_logger.error("cycle_num:%d"%(cycle_num))
        info_logger.error("time_sim_info:%s"%(g_sim.time_sim_info))

        # 前面n-1次均取一整个周期的数据
        info_logger.error("rang_num:%d time:%d-%d"%(cycle_num, one_cycle_start, one_cycle_end_time))
        for _ in range(cycle_num):
            # if g_sim.object_load or g_sim.object_tunnel_flow:
            info_logger.error("first time%d-%d"%(one_cycle_start, one_cycle_end_time))
            save_org_tunnel_info(one_cycle_start, one_cycle_end_time)
        
            # 把这一时间段的tunnel信息按时间切片的方式保存    
            sim_end_time = get_end_time(one_cycle_start)
            if one_cycle_end_time != sim_end_time:
                copy_all_base_tunnel_flow(one_cycle_start, sim_end_time, one_cycle_end_time)

            one_cycle_start = one_cycle_end_time
            one_cycle_end_time = min(one_cycle_start + cycle, end_time)
        
        # 最后一个周期的隧道信息，取数据同步时的隧道信息。因为数据同步时的隧道信息是从应用组里获取的，跟仿真控制器计算的结果更接近。
        # 不能这么玩，这样会把获取备路径的流程搞得特别奇怪
        # if g_sim.object_load or g_sim.object_tunnel_flow:
        #     # 2020-02-05 如果最后一个周期的时间为数据同步的时候或者是跟最后一个周期的最后的时间在数据同步时间前10分支范围内，那么就用数据同步时的从仿真控制器获取的隧道路径
        #     if end_time == g_dt.sync_data_finish_time or (end_time > (g_dt.sync_data_finish_time - 600000)): 
        #         info_logger.error("third time%d-%d-%d"%(one_cycle_start, one_cycle_end_time, end_time))
        #         if one_cycle_start in g_tunrec.sim_orgtuns.keys():
        #             g_tunrec.sim_orgtuns[one_cycle_start].clear()     
        #         g_tunrec.sim_orgtuns[one_cycle_start] = copy.deepcopy(g_tunrec.org_tuns)
        #         sim_end_time = get_end_time(one_cycle_start)
        #         info_logger.error("www third time%d-%d-%d"%(one_cycle_start, sim_end_time, end_time))
        #         if end_time != sim_end_time:
        #             copy_all_base_tunnel_flow(one_cycle_start, sim_end_time, end_time)
        #     else:
        #         # 2020-02-05 如果时间跟同步时间相差太远，则从历史时间获取
        #         info_logger.error("second time%d-%d-%d"%(one_cycle_start, one_cycle_end_time, end_time))
        #         save_org_tunnel_info(one_cycle_start, end_time)
        #         sim_end_time = get_end_time(one_cycle_start)
        #         if end_time != sim_end_time:
        #             copy_all_base_tunnel_flow(one_cycle_start, sim_end_time, end_time)

        # 遍历所有的时间段的tunnel信息,把相应的背景流量减掉此tunnel的大小，把te值加上次tunnel值的大小
        for s_time, tunnel_dict in g_tunrec.sim_orgtuns.items():
            period_link = g_sim.all_link_payload[s_time]

            if len(g_tunrec.sim_orgtuns[s_time]) == 0:
                info_logger.error("len(g_tunrec.sim_orgtuns[%d]) == 0"%(s_time))
                continue

            for key in tunnel_dict.keys():
                tunInfo = tunnel_dict[key]

                # 历史时刻的主路径的选路策略，默认跟当前时刻的流组里带的值一样
                flowgroup_id = tunInfo.flowgroup_id
                flowGroupId_info = g_sdnply.flowgroup[flowgroup_id]
                tunInfo.primary_path.strict_result = flowGroupId_info.pri_strictStatus

                throughput = tunInfo.throughput

                if tunInfo.path_num == 0 or throughput == 0:
                    continue

                if tunInfo.active_path == "primary":
                    path = tunInfo.primary_path.path   
                else:
                    path = tunInfo.standby_path.path
                            
                #找到对应的链路，把back_speed减去这个tunnel流量的大小,把tunnel流量加上这个流量的大小
                for one_path in path: 
                    linkid = one_path["linkid"]
                    linkInfo = period_link.link_info[linkid]
                    if one_path["start_node_id"] == linkInfo.asset_a and one_path["end_node_id"] == linkInfo.asset_b:
                        one_Link = linkInfo.a_to_b
                    else:
                        one_Link = linkInfo.b_to_a

                    if one_Link.back_speed > throughput:
                        one_Link.back_speed -= throughput
                    else:
                        one_Link.back_speed = 0

                    if g_sim.object_load == True:
                        one_Link.te_speed += throughput

            # print('after seper tunnel,link info is:', s_time)
            # for key in period_link.link_info.keys():
            #     linkInfo = period_link.link_info[key]
            #     print(key,':', linkInfo.a_to_b.back_speed, linkInfo.b_to_a.back_speed,linkInfo.a_to_b.te_speed, linkInfo.b_to_a.te_speed)
    except Exception as e:
        print("separ_tunnel Exception:", e)
        info_logger.error(e)
        error_logger.error(e)

def save_one_time_org_tunnel():
    """从背景流量中分离tunnel流量,仅在首次仿真或重新仿真时才需要
    
    Args:
        none
    Returns:
        none
    Raise:
        none
    """

    try:
        start_time = g_sim.time_start
        end_time = g_sim.time_end
        cycle = g_sim.time_cycle
        cycle_num = int(g_sim.time_cycle_num)

        one_cycle_start = start_time
        one_cycle_end_time = min(start_time + cycle, end_time)

        if cycle_num == 1 or ((end_time - start_time) < 3600000):
            g_tunrec.sim_orgtuns[start_time] = copy.deepcopy(g_tunrec.org_tuns)
            
        # 遍历所有的时间段的tunnel信息,把相应的背景流量减掉此tunnel的大小，把te值加上次tunnel值的大小
        for s_time, tunnel_dict in g_tunrec.sim_orgtuns.items():
            period_link = g_sim.all_link_payload[s_time]

            if len(g_tunrec.sim_orgtuns[s_time]) == 0:
                continue

            for key in tunnel_dict.keys():
                tunInfo = tunnel_dict[key]
                throughput = tunInfo.throughput

                if tunInfo.path_num == 0 or throughput == 0:
                    continue

                if tunInfo.active_path == "primary":
                    path = tunInfo.primary_path.path   
                else:
                    path = tunInfo.standby_path.path
                            
                #找到对应的链路，把back_speed减去这个tunnel流量的大小,把tunnel流量加上这个流量的大小
                for one_path in path: 
                    linkid = one_path["linkid"]
                    linkInfo = period_link.link_info[linkid]
                    if one_path["start_node_id"] == linkInfo.asset_a and one_path["end_node_id"] == linkInfo.asset_b:
                        one_Link = linkInfo.a_to_b
                    else:
                        one_Link = linkInfo.b_to_a

                    if one_Link.back_speed > throughput:
                        one_Link.back_speed -= throughput
                    else:
                        one_Link.back_speed = 0
                    # idms:202001021304
                    if g_sim.object_load == True:    
                        one_Link.te_speed += throughput

        for s_time, tunnel_dict in g_tunrec.sim_orgtuns.items():
            info_logger.error("g_tunrec.sim_orgtuns[%s],tunnid:%s"%(s_time, tunnel_dict.keys()))

    except Exception as e:
        print("separ_tunnel Exception:", e)
        info_logger.error(e)
        error_logger.error(e)

def judge_path(flag, path):
    try:
        # 判断tunnel路径是否可达,如果路径中有一个节点故障或者链路故障，则不可达
        if flag == 'before_fault':
            for one_path in path:
                if (g_sim.topo.nodes[one_path["start_node_id"]].fault == 'yes' or
                    g_sim.topo.nodes[one_path["end_node_id"]].fault == 'yes' or
                    g_sim.topo.links[one_path["linkid"]].fault == 'yes'
                    ):
                    return ErrCode.FAILED
        else: 
            for one_path in path:
                if (g_sim.af_topo.nodes[one_path["start_node_id"]].fault == 'yes' or
                    g_sim.af_topo.nodes[one_path["end_node_id"]].fault == 'yes' or
                    g_sim.af_topo.links[one_path["linkid"]].fault == 'yes'
                    ):
                    return ErrCode.FAILED
        return ErrCode.SUCCESS
    except Exception as e:
        print("judge_path Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.FAILED

def tunflow_get_path(flag, tun_name, src_id):
    """导入的tunnel 类型的flow,获取其tunnel流量路径
    
    Args:
        key:tunnel的id信息
    Returns:
        path  or None
    Raise:
        none
    """
    try:
        key = src_id + tun_name
        if flag == 'before_fault':
            for time_step in g_tunrec.sim_b4tuns.keys(): # 按时间段遍历
                tun_step = g_tunrec.sim_b4tuns[time_step]
                if key in tun_step.keys():
                    tun = tun_step[key]        
                    if g_sim.topo.nodes[tun.src_id].fault == 'yes' or g_sim.topo.nodes[tun.des_id].fault == 'yes':
                        return ErrCode.FAILED, None
                else:
                    error_logger.error("not in af_tun.keys: src_id %d, tun_name: %s"%(src_id, tun_name))
                    return ErrCode.FAILED, None
        else: 
            for time_step in g_tunrec.sim_aftuns.keys(): # 按时间段遍历
                tun_step = g_tunrec.sim_aftuns[time_step]
                if key in tun_step.keys():
                    tun = tun_step[key]        
                    if g_sim.af_topo.nodes[tun.src_id].fault == 'yes' or g_sim.af_topo.nodes[tun.des_id].fault == 'yes':
                        return ErrCode.FAILED, None
                else:
                    error_logger.error("not in af_tun.keys: src_id %d, tun_name: %s"%(src_id, tun_name))
                    return ErrCode.FAILED, None

        error_logger.info("tun.primary_path.path_status %s, stat: %s"%(tun.primary_path.path_status, tun.standby_path.path_status))

        # 如果原始的主备路径可达，则记录原始的路径
        if tun.primary_path.path_status == 'UP':   # 用隧道路径的状态来看
            data = {}
            data['jump'] = len(tun.primary_path.path) + 1
            data['path'] = tun.primary_path.path
            data['delay'] = tun.primary_path.delay
            return ErrCode.SUCCESS, data
        elif tun.standby_path.path_status == 'UP':
            data = {}
            data['jump'] = len(tun.standby_path.path) + 1
            data['path'] = tun.standby_path.path
            data['delay'] = tun.standby_path.delay
            return ErrCode.SUCCESS, data
                
        return ErrCode.FAILED, None
    except Exception as e:
        print("tunflow_get_path Exception:", e)
        error_logger.error(e)
        return ErrCode.FAILED, None


def fill_one_tunnel_path(s_time, sim_flag, pri_flag, uuid, paths):
    """
    Args:
        sim_flag:before_fault, after_fault
        pri_flag:standby, primary
        key:tunnel的UUID
    Returns:
        none
    Raise:
        none
    """
    try:
        if sim_flag == "after_fault":
            if s_time in g_tunrec.sim_aftuns.keys(): # 按时间段遍历
                tun_step = g_tunrec.sim_aftuns[s_time]
                if pri_flag == "standby":
                    tunnel_path = tun_step[uuid].standby_path
                else:
                    tunnel_path = tun_step[uuid].primary_path
            else:
                return    
        elif sim_flag == 'orgin':
            if s_time in g_tunrec.sim_orgtuns.keys(): # 按时间段遍历
                tun_step = g_tunrec.sim_orgtuns[s_time]
                if pri_flag == "standby":
                    tunnel_path = tun_step[uuid].standby_path
                else:
                    tunnel_path = tun_step[uuid].primary_path 
            else:
                return
        else:
            if s_time in g_tunrec.sim_b4tuns.keys(): # 按时间段遍历
                tun_step = g_tunrec.sim_b4tuns[s_time]
                if pri_flag == "standby":
                    tunnel_path = tun_step[uuid].standby_path
                else:
                    tunnel_path = tun_step[uuid].primary_path 
            else:
                return        
    
        tunnel_path.path_status = 'UP'
        tunnel_path.path = copy.deepcopy(paths)
        
        tunnel_path.hop_num = len(paths) + 1
        for one_path in paths:
            one_hop = TunnelHop()
            one_hop.node_id = one_path["start_node_id"] 
            one_hop.node_name = g_dt.phy_topo.nodes[one_hop.node_id].name
            linkid = one_path["linkid"]
            if g_dt.phy_topo.links[linkid].nodeid1 == one_hop.node_id:
                one_hop.out_interface = g_dt.phy_topo.links[linkid].ifdesc1 # ifindex1
            elif g_dt.phy_topo.links[linkid].nodeid2 == one_hop.node_id:
                one_hop.out_interface = g_dt.phy_topo.links[linkid].ifdesc2 #ifindex2

            tunnel_path.hops[one_hop.node_id]=one_hop
        
        # 记录最后一个节点
        one_hop = TunnelHop()
        one_hop.node_id = tunnel_path.path[-1]["end_node_id"] 
        one_hop.node_name = g_dt.phy_topo.nodes[one_hop.node_id].name
        one_hop.out_interface = "N/A"
        tunnel_path.hops[one_hop.node_id]=one_hop
        print("out:",one_hop.node_name)
    except Exception as e:
        print("fill_one_tunnel_path Exception:", e)
        error_logger.error(e)
        return ErrCode.FAILED, None

def af_get_tunnel_path():
    """故障后，获取所有的基于tunnel创建的背景流的路径
    
    Args:
        none
    Returns:
        none
    Raise:
        none
    """
    try:
        for time_step in g_tunrec.sim_aftuns.keys(): # 按时间段遍历
            tun_step = g_tunrec.sim_aftuns[time_step]
            for key in tun_step.keys():
                tun = tun_step[key]
                active_path_num = 0
                if g_sim.af_topo.nodes[tun.src_id].fault == 'yes' or g_sim.af_topo.nodes[tun.des_id].fault == 'yes':
                    tun.status = 'DOWN'
                    tun.primary_path.path_status = "DOWN"  # 源或目的故障时，把主被路径干掉
                    tun.primary_path.path.clear()
                    tun.primary_path.hop_num = 0
                    tun.primary_path.delay = 0
                    tun.primary_path.hops.clear()

                    tun.standby_path.path_status = "DOWN"
                    tun.standby_path.path.clear()
                    tun.standby_path.hop_num = 0
                    tun.standby_path.hops.clear()
                    tun.standby_path.delay = 0
                    continue
                
                # 如果原始的主备路径可达，则记录原始的路径
                if len(tun.primary_path.path):
                    ret = judge_path('after_fault', tun.primary_path.path)
                    if ret == ErrCode.SUCCESS:
                        tun.status = 'UP'
                        tun.active_path = "primary"
                        tun.primary_path.path_status = 'UP'
                        active_path_num += 1
                    else:
                        tun.status = 'DOWN'
                        tun.primary_path.path_status = 'DOWN'
                        tun.primary_path.path.clear()
                        tun.primary_path.hop_num = 0
                        tun.primary_path.delay = 0
                        tun.primary_path.hops.clear()
                
                if len(tun.standby_path.path):
                    ret = judge_path("after_fault", tun.standby_path.path)
                    if ret == ErrCode.SUCCESS:
                        tun.status = 'UP'
                        tun.standby_path.path_status = 'UP'
                        active_path_num += 1
                    else:
                        tun.standby_path.path_status = 'DOWN'
                        tun.standby_path.hop_num = 0
                        tun.standby_path.path.clear()
                        tun.standby_path.hops.clear()

                # 当只有备路径是UP的时候，把备路径COPY到主路径上
                if active_path_num == 1 and tun.primary_path.path_status == 'DOWN' and tun.standby_path.path_status == 'UP': 
                    tun.active_path = "primary"
                    tun.primary_path.path_status = 'UP'
                    tun.primary_path.hop_num = tun.standby_path.hop_num
                    tun.primary_path.delay = tun.standby_path.delay
                    tun.primary_path.hops = copy.deepcopy(tun.standby_path.hops)
                    tun.primary_path.label_stack = copy.deepcopy(tun.standby_path.label_stack)
                    tun.primary_path.path = copy.deepcopy(tun.standby_path.path)

                    tun.standby_path.path_status = 'DOWN'
                    tun.standby_path.hop_num = 0
                    tun.standby_path.delay = 0
                    tun.standby_path.path.clear()
                    tun.standby_path.hops.clear()

                # 如果原始的主备路径均不可达,从仿真控制器获得新的tunnel 路径
                if active_path_num < 2:
                    error_logger.error("af_get_tpath_from_sdn_simctrl  begin")
                    resp = af_get_tpath_from_sdn_simctrl(key)
                    if resp == None:
                        error_logger.error("af_get_tpath_from_sdn_simctrl none")
                    else:
                        if tun.primary_path.path_status == 'UP': # 如果原来主路径是OK的
                            if "standby_path" in resp and operator.eq(tun.primary_path.path, resp["standby_path"]) == False:
                                active_path_num += 1
                                fill_one_tunnel_path(time_step, "after_fault", "standby", key, resp["standby_path"])
                            else:
                                if "primary_path" in resp and operator.eq(tun.primary_path.path, resp["primary_path"]) == False:
                                    fill_one_tunnel_path(time_step, "after_fault", "standby", key, resp["primary_path"])
                                    active_path_num += 1
                                else:
                                    continue
                        else:
                            if "primary_path" in resp and "standby_path" in resp:
                                tun.status = 'UP'
                                if operator.eq(resp["primary_path"], resp["standby_path"]) == False:
                                    active_path_num += 2
                                    fill_one_tunnel_path(time_step, "after_fault", "primary", key, resp["primary_path"])
                                    fill_one_tunnel_path(time_step, "after_fault", "standby", key, resp["standby_path"])
                                else:
                                    active_path_num += 1
                                    fill_one_tunnel_path(time_step, "after_fault", "primary", key, resp["primary_path"])

                            elif "primary_path" in resp and "standby_path" not in resp:
                                tun.status = 'UP'
                                fill_one_tunnel_path(time_step, "after_fault", "primary", key, resp["primary_path"])
                                active_path_num += 1

                            elif "primary_path" not in resp and "standby_path" in resp:
                                tun.status = 'UP'
                                fill_one_tunnel_path(time_step, "after_fault", "primary", key, resp["standby_path"])
                                active_path_num += 1
                
                if active_path_num == 2 and tun.path_num == 1:
                    tun.path_num = 2
    except Exception as e:
        print("af_get_tunnel_path Exception:", e)
        error_logger.error(e)

def parse_tunnels_from_bigdata(s_time, e_time):
    """从大数据获取隧道信息后进行解析,先判断是否在SDN中，再判断大数据的路径与SDN的路径是否一致
    
    Args:
        none
    Returns:
        none
    Raise:
        none
    """
    try:
        ret, all_tunnels_inf_from_bd = process_tunnels_inf_from_bigdata(s_time, e_time)
        if ret == ErrCode.SUCCESS:
            if all_tunnels_inf_from_bd == None:
                print("parse_tunnels_from_bigdata() FAILED")
                info_logger.error("parse_tunnels_from_bigdata() FAILED")
                return ErrCode.FAILED
            all_tunnels_uid_from_bd = [uid for uid in all_tunnels_inf_from_bd.keys()]

            for uid in all_tunnels_uid_from_bd:
                device_id =  get_id_by_ip(all_tunnels_inf_from_bd[uid]["ingressLsrIp"])
                if device_id == None:
                    continue
                tunnel_id = all_tunnels_inf_from_bd[uid]["tunnelId"]
                tunnel_uuid = device_id + 'Tunnel' + str(tunnel_id)

                if tunnel_uuid in g_tunrec.org_tuns.keys():
                    tunnel_main_path = all_tunnels_inf_from_bd[uid]["path"]["mainNodes"] 

                    if len(g_tunrec.org_tuns[tunnel_uuid].primary_path.path):
                        main_hops = [p['start_node_id'] for p in g_tunrec.org_tuns[tunnel_uuid].primary_path.path]
                        main_hops.append(g_tunrec.org_tuns[tunnel_uuid].primary_path.path[-1]["end_node_id"])      
                        ret = judge_two_paths(tunnel_main_path,main_hops,'primary')
                        
                    g_tunrec.org_tuns[tunnel_uuid].bguuid = uid
                    g_tunrec.org_tuns[tunnel_uuid].throughput = all_tunnels_inf_from_bd[uid]["throughput"]
        
        return ErrCode.SUCCESS

    except Exception as e:
        print("parse_tunnels_from_bigdata Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.PARSE_TUNNEL_FROM_BG

def judge_two_paths(path_from_bg,path_from_sdn,path_type):
    """
    
    Args:
        path_from_bg：从大数据获取的路径，为IP列表形式；
        path_from_sdn：从sdn获取的路径，为ID列表形式
        path_type：str，路径类型，"主"或"备份"
    Returns:
        路径相同时，返回True
        路径不同时，返回False,同时打印信息
    Raise:
        none
    """
    try:
        temp = 0
        if len(path_from_bg) != len(path_from_sdn):
            print("从大数据获取的隧道"+path_type+"路径信息和SDN的信息不一致")
            info_logger.warning("从大数据获取的隧道"+path_type+"路径信息和SDN的信息不一致")
            return False
        for i,path_ip in enumerate(path_from_bg):
            path_id = get_id_by_ip(path_ip)
            if path_id != path_from_sdn[i]:
                break
            temp += 1
        if temp != len(path_from_bg):
            print("从大数据获取的隧道"+path_type+"主路径信息和SDN的信息不一致")
            info_logger.warning("从大数据获取的隧道"+path_type+"主路径信息和SDN的信息不一致")
            return False
        return True

    except Exception as e:
        print("judge_two_paths Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return False

def get_id_by_ip(ip):
    try:
        if ip in g_dt.phy_topo.mgrip_nodeid.keys():
            return g_dt.phy_topo.mgrip_nodeid[ip]
        else:
            return None
    except Exception as e:
        print("get_id_by_ip Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
  
def process_tunnels_inf_from_bigdata(s_time, e_time):
    """"从大数据获取隧道信息后进行处理，每一个隧道UID对应一个隧道的信息
    
    Args:
        none
    Returns:
        none
    Raise:
        none
    """
    try:
        data = get_tunnels_from_bigdata(s_time, e_time)
        if data == None:
            error_logger.error("get_tunnels_from_bigdata ret none")
            return ErrCode.TUNNEL_INF_FROM_BG, None

        tunnels_data = {}
        uuid_list = []

        for i in range(len(data)):
            if data[i]["type"] == "SR-TE.ILM":
                temp = {}
                uuid = data[i]["tunnelUid"] 
                temp["tunnelId"] = data[i]["tunnelId"]
                temp["ingressLsrIp"] = data[i]["ingressLsrIp"]
                temp["egressLsrIp"] = data[i]["egressLsrIp"]
                uuid_list.append(uuid)   
                tunnels_data[uuid] = temp

        uuid_len = len(uuid_list)
        for tendata in [uuid_list[i:i + 10] for i in range(0, uuid_len, 10)]:
            ret, thrput = process_tunnels_flow_from_bigdata(tendata, s_time, e_time)
            if ret == ErrCode.SUCCESS:
                for key,value in thrput.items():
                    tunnels_data[key]["throughput"] = value
        
        for tendata in [uuid_list[i:i + 10] for i in range(0, uuid_len, 10)]:
            ret, pathdata = process_tunnels_path_from_bigdata(tendata)
            if ret == ErrCode.SUCCESS:
                for key,value in pathdata.items():
                    tunnels_data[key]["path"] = value
                
        del_key = []
        for key,value in tunnels_data.items():
            if "throughput" not in value or "path" not in value:
                del_key.append(key)
        
        if len(del_key) != 0:
            for key in del_key:
                del tunnels_data[key]
    
        return ErrCode.SUCCESS, tunnels_data

    except Exception as e:
        print("process_tunnels_inf_from_bigdata Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.TUNNEL_INF_FROM_BG, None

def process_tunnels_flow_from_bigdata(tunnelUid, s_time, e_time):
    """从大数据获取隧道流量信息后进行处理，每一个隧道UID对应一个吞吐量
    
    Args:
        none
    Returns:
        none
    Raise:
        none
    """
    try:
        data = get_tunnel_flow_from_bigdata(tunnelUid, s_time, e_time)
        if data == None:
            error_logger.error("get_tunnel_flow_from_bigdata return None")
            return ErrCode.TUNNEL_FLOW_FROM_BG, None
        # 从大数据获得的单位是Mbps，直接乘以1000转换成kbps
        tunnels_flow_inf = {data[i]["tunnelUid"]:data[i]["throughput"]*1000 for i in range(len(data))}
        return ErrCode.SUCCESS, tunnels_flow_inf
    except Exception as e:
        print("process_tunnels_flow_from_bigdata Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.TUNNEL_FLOW_FROM_BG, None

     
def process_tunnels_path_from_bigdata(tunnelUid):
    """从大数据获取隧道路径信息后进行解析，每一个隧道UID对应一个主路径和备份路径
    
    Args:
        none
    Returns:
        none
    Raise:
        none
    """
    try:
        data = get_tunnel_path_from_bigdata(tunnelUid)
        if data == None:
            error_logger.error("get_tunnel_path_from_bigdata None")
            return ErrCode.TUNNEL_PATH_FROM_BG, None
        tunnels_path_inf = {}
        for i in range(len(data)):
            mark_1 = False
            mark_2 = False
            temp = {}
            if test_debug:
                if data[i]["mainNodes"] != 'null':
                    mark_1 = True
                if data[i]["backupNodes"] != 'null':
                    mark_2 = True
            else:
                if data[i]["mainNodes"]:
                    mark_1 = True
                if data[i]["backupNodes"]:
                    mark_2 = True                

            main_ip = []
            backup_ip = []
            if mark_1 and mark_2:
                # mainNodes
                temp_mainNodes = data[i]["mainNodes"]
                if temp_mainNodes:
                    main_ip = [temp_mainNodes[j]["nodeLsrIp"] for j in range(len(temp_mainNodes))]

                # backupNodes
                temp_backupNodes = data[i]["backupNodes"]
                if temp_backupNodes:
                    backup_ip = [temp_backupNodes[j]["nodeLsrIp"] for j in range(len(temp_backupNodes))]
            
                temp = {
                    "path_type":0, # 取0表示两条路径都有
                    "mainNodes":main_ip,
                    "backupNodes":backup_ip
                }      
            elif mark_1 and not mark_2:
                # mainNodes
                temp_mainNodes = data[i]["mainNodes"]
                if temp_mainNodes:
                    main_ip = [temp_mainNodes[j]["nodeLsrIp"] for j in range(len(temp_mainNodes))]            
                temp = {
                    "path_type":1,  # 取1表示只有主路径
                    "mainNodes":main_ip,
                    "backupNodes":[]
                }
            else:
                continue      
            tunnels_path_inf[data[i]["tunnelUid"]] = temp

        return ErrCode.SUCCESS, tunnels_path_inf

    except Exception as e:
        print("process_tunnels_path_from_bigdata Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.TUNNEL_PATH_FROM_BG, None

def check_tunnel_state(tun_b4_info, tun_af_info):
    try:
        # return 1 代表是中断的类型，否则为其他类型
        if tun_af_info.primary_path.path_status == 'DOWN' and tun_af_info.standby_path.path_status == 'DOWN':
            if tun_b4_info.primary_path.path_status == 'UP' or tun_b4_info.standby_path.path_status == 'UP':
                return 1
        return 0
    except Exception as e:
        print("check_tunnel_state Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return 0

# 仿真前后隧道路径对比统计 
def cmp_before_after_tunnel():
    try:
        if g_tunrec:
            # 统计前需要先清除上次仿真的统计信息
            g_tunrec.unchange_tuns.clear()
            g_tunrec.change_tuns.clear()
            g_tunrec.interrupt_tuns.clear()

            tunnel_befor = g_tunrec.sim_b4tuns    # {t1: {tunnel_id:Tunnel类}, t2: {tunnel_id:Tunnel类}}
            tunnel_after = g_tunrec.sim_aftuns
            # 通过故障前后的状态、path_num、active_path、primary_path、standby_path判断前后是否一致
            
            for time_step in tunnel_befor.keys(): # 按时间段遍历
                tun_step = g_tunrec.sim_b4tuns[time_step]
                for tun_id, tun_b4_info in tun_step.items():                
                    if tun_id in tunnel_after[time_step]:
                        # 先检查Tunnel状态
                        
                        tun_af_info = tunnel_after[time_step][tun_id]

                        #if tun_b4_info.status == "UP" and tun_af_info.status == "DOWN":
                        if check_tunnel_state(tun_b4_info, tun_af_info) == 1:
                            if time_step in g_tunrec.interrupt_tuns.keys():
                                g_tunrec.interrupt_tuns[time_step].append(tun_id)
                            else:
                                g_tunrec.interrupt_tuns[time_step] = []
                                g_tunrec.interrupt_tuns[time_step].append(tun_id)
                        else:
                            #路径全部down了，就不关系具体的路径方向了
                            if (tun_b4_info.status == 'DOWN' and tun_af_info.status == 'DOWN' and 
                                tun_b4_info.primary_path.path_status == 'DOWN' and tun_b4_info.standby_path.path_status == 'DOWN' and
                                tun_af_info.primary_path.path_status == 'DOWN' and tun_af_info.standby_path.path_status == 'DOWN'):
                                if time_step in g_tunrec.unchange_tuns.keys():
                                    g_tunrec.unchange_tuns[time_step].append(tun_id)
                                else:
                                    g_tunrec.unchange_tuns[time_step] = []
                                    g_tunrec.unchange_tuns[time_step].append(tun_id)
                            elif (tun_b4_info.status == tun_af_info.status and tun_b4_info.path_num == tun_af_info.path_num
                                and tun_b4_info.primary_path.path_status == tun_af_info.primary_path.path_status and tun_b4_info.standby_path.path_status == tun_af_info.standby_path.path_status
                                and operator.eq(tun_b4_info.primary_path.path, tun_af_info.primary_path.path) == True
                                and operator.eq(tun_b4_info.standby_path.path, tun_af_info.standby_path.path) == True):
                                # 上述4个条件满足，说明未变化 
                                if time_step in g_tunrec.unchange_tuns.keys():
                                    g_tunrec.unchange_tuns[time_step].append(tun_id)
                                else:
                                    g_tunrec.unchange_tuns[time_step] = []
                                    g_tunrec.unchange_tuns[time_step].append(tun_id)                               
                            else:
                                # 其他状态说明
                                if time_step in g_tunrec.change_tuns.keys():
                                    g_tunrec.change_tuns[time_step].append(tun_id)
                                else:
                                    g_tunrec.change_tuns[time_step] = []
                                    g_tunrec.change_tuns[time_step].append(tun_id)                                
                    else:
                        if time_step in g_tunrec.interrupt_tuns.keys():
                            g_tunrec.interrupt_tuns[time_step].append(tun_id)
                        else:
                            g_tunrec.interrupt_tuns[time_step] = []
                            g_tunrec.interrupt_tuns[time_step].append(tun_id) 
            return ErrCode.SUCCESS

    except Exception as e:
        print("cmp_before_after_tunnel Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.FAILED

def check_tunnel_info_after_bigdata():
    """如果大数据比对后throughput为-1，说明该tunnel信息有误，删除该tunnel信息
    
    Args:
        none
    Returns:
        none
    Raise:
        none
    """
    try:
        for time_step in g_tunrec.sim_orgtuns.keys(): # 按时间段遍历
            tun_step = g_tunrec.sim_orgtuns[time_step]
            for key in tun_step:
                if tun_step[key].throughput == -1:
                    error_logger.error("tunnel information from sdn and bigdata are diffrent")
        return ErrCode.SUCCESS

    except Exception as e:
        print("check_tunnel_info_after_bigdata Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.FAILED


def get_and_check_tunnels_inf(s_time, e_time):
    """"从大数据获取隧道信息后进行处理，每一个隧道UID对应一个隧道的信息
    
    Args:
        none
    Returns:
        none
    Raise:
        none
    """
    try:
        info_logger.error("================time %d"%(s_time))
        data = get_tunnels_from_bigdata(s_time, e_time)
        if data == None:
            error_logger.error("get_tunnels_from_bigdata ret none %d -%d"%(s_time, e_time))
            return ErrCode.TUNNEL_INF_FROM_BG, None

        tunnels_data = {}
        uuid_list = []

        for i in range(len(data)):
            if data[i]["type"] == "SR-TE.ILM":
                temp = {}
                start_node = get_id_by_ip(data[i]["ingressLsrIp"])
                end_node = get_id_by_ip( data[i]["egressLsrIp"])

                if start_node == None or end_node == None:
                    continue

                uuid = data[i]["tunnelUid"] 
                temp["tunnelId"] = data[i]["tunnelId"]
                temp["ingressLsrIp"] = data[i]["ingressLsrIp"]
                temp["egressLsrIp"] = data[i]["egressLsrIp"]
                temp["start_node"] = start_node
                temp["end_node"] = end_node
                temp['tun_type'] = data[i]["type"]
                temp["org_uuid"] = uuid
                temp["createTime"]= data[i]["createTime"]

                same_flag = False

                # 如果对于某一个隧道,tunnel6,从a->b，如果在某段时间内假设10：00-11点间，在10：20的时候修改了器必经或算路约束，路径改变后，大数据保存的是两个UUID
                # 但是对于我们而言，在这段时间tunnel6的只显示一个主备路径。我们取11：20改变后的那个隧道UUID
                for tun_value in tunnels_data.values():
                    if temp["tunnelId"] == tun_value["tunnelId"] and temp["ingressLsrIp"] == tun_value["ingressLsrIp"] and temp["egressLsrIp"] == tun_value["egressLsrIp"]:                        
                        # 保留隧道创建时间新的那个隧道UUID
                        if temp["createTime"] > tun_value["createTime"]:
                            uuid_list.remove(tun_value["org_uuid"]) 
                            uuid_list.append(temp["org_uuid"]) 
                            tun_value["createTime"] = temp["createTime"]
                            tun_value["org_uuid"] = temp["org_uuid"]

                        # 只要tunnelid和源及目的相同，则认为找到相同的，找到即可break for循环
                        same_flag = True
                        break

                if same_flag == False:               
                    info_logger.error("add uuid %s"%(uuid))
                    uuid_list.append(uuid)   
                    tunnels_data[uuid] = temp

        uuid_len = len(uuid_list)
        if uuid_len == 0:
            return ErrCode.TUNNEL_INF_FROM_BG, None

        for tendata in [uuid_list[i:i + 10] for i in range(0, uuid_len, 10)]:
            ret, thrput = process_tunnels_flow_from_bigdata(tendata, s_time, e_time)
            if ret == ErrCode.SUCCESS:
                for key,value in thrput.items():
                    if key in tunnels_data.keys():
                        tunnels_data[key]["throughput"] = value
                    else:
                        error_logger.error("tunid %s not in tunnels_data.keys():%s"%(key, tunnels_data.keys()))
        
        for tendata in [uuid_list[i:i + 10] for i in range(0, uuid_len, 10)]:
            ret, pathdata = process_tunnels_path_from_bigdata(tendata)
            if ret == ErrCode.SUCCESS:
                for key,value in pathdata.items():
                    if key in tunnels_data.keys():
                        tunnels_data[key]["path"] = value
                    else:
                        error_logger.error("tunid %s not in tunnels_data.keys():%s"%(key, tunnels_data.keys()))
                
        del_key = []
        for key,value in tunnels_data.items():
            if "throughput" not in value or "path" not in value:
                del_key.append(key)
        
        if len(del_key) != 0:
            for key in del_key:
                del tunnels_data[key]

        if len(tunnels_data) == 0:
            return ErrCode.TUNNEL_INF_FROM_BG, None
    
        return ErrCode.SUCCESS, tunnels_data

    except Exception as e:
        info_logger.error(e)
        error_logger.error(e)
        print("get_and_check_tunnels_inf Exception:", e)
        return ErrCode.TUNNEL_INF_FROM_BG, None

def save_org_tunnel_info(s_time, e_time):
    """从大数据获取隧道信息后进行解析,先判断是否在SDN中，再判断大数据的路径与SDN的路径是否一致
    
    Args:
        none
    Returns:
        none
    Raise:
        none
    """
    try:
        g_tunrec.sim_orgtuns[s_time] = {}

        ret, all_tunnels = get_and_check_tunnels_inf(s_time, e_time)
        if ret == ErrCode.SUCCESS:
            for value in all_tunnels.values():
                device_id =  value["start_node"]
                tunnel_id = value["tunnelId"]
                tunnel_uuid = device_id + 'Tunnel' + str(tunnel_id)

                # A时刻获取的tunnid 不存在数据同步的tunid 中，则A时刻的tunid信息不保存
                if tunnel_uuid not in g_tunrec.org_tuns.keys():
                    info_logger.error("tunnel_uuid %s not in orgkeys:%s,orguuid:%s"%(tunnel_uuid, g_tunrec.org_tuns.keys(),value["org_uuid"]))
                    continue

                flow_group_id = g_tunrec.org_tuns[tunnel_uuid].flowgroup_id
                flowgroup_info = g_sdnply.flowgroup[flow_group_id]

                phy_st_node = value['start_node']
                if phy_st_node in g_sim.topo.nodes.keys():
                    layer3_st_node = g_sim.topo.nodes[phy_st_node].l3_node_id
                    
                phy_end_node = value['end_node']
                if phy_end_node in g_sim.topo.nodes.keys():
                    layer3_end_node = g_sim.topo.nodes[phy_end_node].l3_node_id

                if flowgroup_info.srcNodeid != layer3_st_node or flowgroup_info.dstNodeid != layer3_end_node:
                    info_logger.error("bg data tunnel start not eq flow start tid:%s, ouguuid:%s"%(tunnel_uuid, value["org_uuid"]))
                    st_id = flowgroup_info.srcNodeid
                    st_id2 = layer3_st_node
                    end_id = flowgroup_info.dstNodeid
                    end_id2 = layer3_end_node
                    if st_id in g_sim.l3_topo.nodes.keys() and st_id2 in  g_sim.l3_topo.nodes.keys():
                        info_logger.error("srcnode:%s,%s, %s,%s"%(st_id,st_id2, g_sim.l3_topo.nodes[st_id].name,  g_sim.topo.nodes[st_id2].name))
                    else:
                        info_logger.error("%s,%s not in "%(st_id,st_id2))
                    if end_id in  g_sim.l3_topo.nodes.keys() and end_id2 in  g_sim.l3_topo.nodes.keys():
                        info_logger.error("srcnode:%s,%s, %s,%s"%(end_id, end_id2,  g_sim.l3_topo.nodes[end_id].name,  g_sim.l3_topo.nodes[end_id2].name))
                    else:  
                        info_logger.error("end %s,%s not in "%(end_id,end_id2))
                    continue
                
                info_logger.error("add :%d, uuid:%s, orgid:%s"%(s_time, tunnel_uuid, value["org_uuid"]))
                
                g_tunrec.sim_orgtuns[s_time][tunnel_uuid] = Tunnel()
                temp = g_tunrec.sim_orgtuns[s_time][tunnel_uuid]

                tunnel_main_path = value["path"]["mainNodes"]  
                temp.name = 'Tunnel' + str(tunnel_id)             
                temp.bguuid = value["tunnelId"]
                temp.throughput = value["throughput"]
                
                temp.src_id = value['start_node']
                temp.des_id = value['end_node']
                temp.node_name = g_sim.topo.nodes[temp.src_id].name
                temp.src_ip = g_sim.topo.nodes[temp.src_id].mgrip
                temp.des_ip = g_sim.topo.nodes[temp.des_id].mgrip
                temp.tunnel_type = value['tun_type']
                temp.status = 'UP'
                temp.path_num = 1
                temp.active_path = 'primary'
                temp.flowgroup_id = g_tunrec.org_tuns[tunnel_uuid].flowgroup_id

                temp.primary_path.path_status = 'UP'
                jump = len(tunnel_main_path)
                temp.primary_path.hop_num = jump
                cyc_len = jump - 1
                i = 0
                temp.primary_path.delay = 0    # 时延先初始化为0

                for i in range(cyc_len):
                    # 把三层节点转换为二层节点
                    phy_sourcid = get_id_by_ip(tunnel_main_path[i])
                    phy_desid = get_id_by_ip(tunnel_main_path[(i + 1)])
                    # 通过节点ID，取得其对应的二层链路ID
                    linkid = g_sim.topo.nodes[phy_sourcid].neighbour[phy_desid]

                    if phy_sourcid == g_sim.topo.links[linkid].nodeid1:
                        l3_linkid = g_sim.topo.links[linkid].l3_link_id[0]
                    else:
                        l3_linkid = g_sim.topo.links[linkid].l3_link_id[1]
                    if g_sim.l3_topo.links[l3_linkid].delay[s_time]:
                        temp.primary_path.delay += g_sim.l3_topo.links[l3_linkid].delay[s_time] #这里取真实值

                    # 记录一条链路信息
                    one_link_path = {'start_node_id':phy_sourcid,'end_node_id':phy_desid,'linkid':linkid}
                    temp.primary_path.path.append(one_link_path)

                    one_hop = TunnelHop()
                    one_hop.node_id = phy_sourcid
                    one_hop.node_name = g_sim.topo.nodes[phy_sourcid].name

                    if g_sim.topo.links[linkid].nodeid1 == one_hop.node_id:
                        one_hop.out_interface = g_sim.topo.links[linkid].ifdesc1 
                    elif g_sim.topo.links[linkid].nodeid2 == one_hop.node_id:
                        one_hop.out_interface = g_dt.phy_topo.links[linkid].ifdesc2 

                    temp.primary_path.hops[one_hop.node_id]=one_hop
                
                # 记录最后一个节点
                one_hop = TunnelHop()
                one_hop.node_id = phy_desid
                one_hop.node_name = g_dt.phy_topo.nodes[one_hop.node_id].name
                one_hop.out_interface = "N/A"
                temp.primary_path.hops[one_hop.node_id]=one_hop

        info_logger.error("g_tunrec.sim_orgtuns[%d],keys:%s"%(s_time, g_tunrec.sim_orgtuns[s_time].keys()))
        return ErrCode.SUCCESS

    except Exception as e:
        print("save_org_tunnel_info execption:",e)
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.PARSE_TUNNEL_FROM_BG

def get_tunnel_flow_path(flag, flowid, s_time):
    try:
        data = {}
        if flag == "orgin":
            flow = g_allFlows[flowid]
            src_id = flow.src_id  # 这里
            tun_name = flow.tun_name
            tun_id = src_id + tun_name
            # print("tunid:", tun_id, s_time)
            if s_time in g_tunrec.sim_orgtuns.keys():
                # print("s_time in", tun_id)
                if tun_id in g_tunrec.sim_orgtuns[s_time].keys():
                    if g_tunrec.sim_orgtuns[s_time][tun_id].primary_path.path_status == 'UP':
                        data["path"] = g_tunrec.sim_orgtuns[s_time][tun_id].primary_path.path 
                        data["jump"] = g_tunrec.sim_orgtuns[s_time][tun_id].primary_path.hop_num
                        data["delay"] = g_tunrec.sim_orgtuns[s_time][tun_id].primary_path.delay
                        return ErrCode.SUCCESS, data
                    elif g_tunrec.sim_orgtuns[s_time][tun_id].standby_path.path_status == 'UP':
                        data["path"] = g_tunrec.sim_orgtuns[s_time][tun_id].standby_path.path 
                        data["jump"] = g_tunrec.sim_orgtuns[s_time][tun_id].standby_path.hop_num
                        data["delay"] = g_tunrec.sim_orgtuns[s_time][tun_id].standby_path.delay 
                        return ErrCode.SUCCESS, data
                    else:
                        return ErrCode.FAILED, data
                else:
                    return ErrCode.FAILED, data
            else:
                return ErrCode.FAILED, data
        elif flag == 'before_fault':
            flow = g_sim.flow_info[flowid]
            src_id = flow.src_id  # 这里
            tun_name = flow.tun_name
            tun_id = src_id + tun_name

            if s_time in g_tunrec.sim_b4tuns.keys():
                if tun_id in g_tunrec.sim_b4tuns[s_time].keys():
                    data["path"] = g_tunrec.sim_b4tuns[s_time][tun_id].primary_path.path 
                    data["jump"] = g_tunrec.sim_b4tuns[s_time][tun_id].primary_path.hop_num
                    data["delay"] = g_tunrec.sim_b4tuns[s_time][tun_id].primary_path.delay
                    return data
                else:
                    return ErrCode.FAILED, data
            else:
                return ErrCode.FAILED, data
        else:
            flow = g_sim.flow_info[flowid]
            src_id = flow.src_id
            tun_name = flow.tun_name
            tun_id = src_id + tun_name

            if s_time in g_tunrec.sim_aftuns.keys():
                if tun_id in g_tunrec.sim_aftuns[s_time].keys():
                    data["path"] = g_tunrec.sim_aftuns[s_time][tun_id].primary_path.path 
                    data["jump"] = g_tunrec.sim_aftuns[s_time][tun_id].primary_path.hop_num
                    data["delay"] = g_tunrec.sim_aftuns[s_time][tun_id].primary_path.delay
                    return data
                else:
                    return ErrCode.FAILED, data
            else:
                return ErrCode.FAILED, data

    except Exception as e:
        print("get_tunnel_flow_path Exception:", e)
        data = {}
        data["path"] = []
        data["jump"] = 0
        data["delay"] = 0
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.FAILED, data

def save_all_tunnel_standby_path():
    """从SDN仿真控制器获取备路径，并保存
    
    Args:
        none
    Returns:
        none
    Raise:
        none
    """   
    try:
        flag = 'before_fault'
        ret = send_affinityEnable_to_sdn_simctrl()
        if ret != ErrCode.SUCCESS:
            error_logger.error("send_affinityEnable_to_sdn_simctrl Failed %d"%(ret))
            info_logger.error("send_affinityEnable_to_sdn_simctrl Failed %d"%(ret))

        # ret = send_topo_to_sdn_simctrl()  # 传入时间
        # if ret != ErrCode.SUCCESS:
        #     error_logger.error("send_topo_to_sdn_simctrl Failed %d"%(ret))
                
        for s_time, tunnel_dict in g_tunrec.sim_orgtuns.items():

            ret = send_topo_to_sdn_simctrl(s_time)  # 传入时间
            if ret != ErrCode.SUCCESS:
                error_logger.error("send_topo_to_sdn_simctrl Failed %d" % (ret))

            ret = send_slapolicy_to_sdn_simctrl()
            if ret != ErrCode.SUCCESS:
                error_logger.error("send_slapolicy_to_sdn_simctrl Failed %d"%(ret))
                info_logger.error("send_slapolicy_to_sdn_simctrl Failed %d"%(ret))

            info_logger.error("=============send_flowgroup====================")
            send_flowgroup_to_sdn_simctrl(flag, s_time) 
            info_logger.error("=============send_flowgroup_instance====================")          
            send_flowgroup_instance_to_sdn_simctrl(flag, s_time)
            info_logger.error("=============send_flowgroup_instance_tunnel====================")   
            send_flowgroup_instance_tunnel_to_sdn_simctrl(flag, s_time)
            
            ret = calc_flowgroup_instance_tunnel_path(flag, s_time, mode = 2)
            if ret != ErrCode.SUCCESS:
                info_logger.error("=============calc_org_flowgroup_instance_tunnel_path failed====================")   
                error_logger.error("calc_org_flowgroup_instance_tunnel_path Failed")
                info_logger.error("calc_org_flowgroup_instance_tunnel_path Failed")
            
            if ret == ErrCode.SUCCESS:
                info_logger.error("=============calc_org_flowgroup_instance_tunnel_path success====================")
                ret, data = get_flowgroup_instance_tunnel_path(flag, s_time)
                if ret != ErrCode.SUCCESS:
                    info_logger.error("mode = 2 nONE")
                    ret = calc_flowgroup_instance_tunnel_path(flag, s_time, mode = 0)
                    if ret != ErrCode.SUCCESS:
                        info_logger.error("calc_org_flowgroup_instance_tunnel_path failied")

                    ret, data = get_flowgroup_instance_tunnel_path(flag, s_time)
                    if ret != ErrCode.SUCCESS:
                        info_logger.error("MODE 0:%s"%(data))
                        info_logger.error("get_org_tunnel_path:%s"%(data))

                if ret == ErrCode.SUCCESS:
                    for tun_info in data:
                        tun_id = tun_info["tunnelId"]
                        info_logger.info("leijy s_time:%d, tunnel_dict[tun_id].path_num:%d, tunid:%s"%(s_time, tunnel_dict[tun_id].path_num,tun_id))
                        if tun_id in tunnel_dict.keys():
                            
                            if "strictStatus" in tun_info["standby"].keys():
                                tunnel_dict[tun_id].standby_path.strict_result = tun_info["standby"]["strictStatus"]
                            else:
                                tunnel_dict[tun_id].standby_path.strict_result = 3 # 未选路

                            path = tun_info["standby"]["linkList"]
                            if len(path) > 0:
                                path_list = []
                                for l3_linkid in path:
                                    # 把三层节点转换为二层节点
                                    if l3_linkid in g_sim.l3_topo.links.keys():
                                        l3_st_node = g_sim.l3_topo.links[l3_linkid].src_id
                                        l3_des_node = g_sim.l3_topo.links[l3_linkid].des_id
                                        phy_sourcid = g_sim.l3_topo.nodes[l3_st_node].phy_id 

                                        phy_desid = g_sim.l3_topo.nodes[l3_des_node].phy_id

                                        # 通过节点ID，取得其对应的二层链路ID
                                        linkid = g_sim.topo.nodes[phy_sourcid].neighbour[phy_desid]

                                        # 记录一条链路信息
                                        one_link_path = {'start_node_id':phy_sourcid,'end_node_id':phy_desid,'linkid':linkid}
                                        path_list.append(one_link_path)

                                if  operator.eq(tunnel_dict[tun_id].primary_path.path, path_list) == False:
                                    tunnel_dict[tun_id].path_num += 1
                                    fill_one_tunnel_path(s_time, "orgin", "standby", tun_id, path_list)
                                    info_logger.info("2=== leijy tunnel_dict[tun_id].path_num:%d, tunid:%s"%(tunnel_dict[tun_id].path_num,tun_id))
    except Exception as e:
        print("save_all_tunnel_standby_path Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.FAILED
