# -*- encoding: utf-8 -*-
"""
@File    : flowsimulate.py
@Time    : 2019/05/29 14:04:21
@Author  : leijuyan
@License : Copyright (c) 2004-2019 New H3C Tech. Co., Ltd. All rights reserved.
@Desc    : 流量仿真
"""
import re
import copy
import operator

from apps.errcode import ErrCode

from apps.util import g_sim, g_allFlows
from apps.util import get_end_time, get_start_end_time
from apps.util import info_logger, error_logger
from apps.util import parse_flow_to_kbps

from apps.v1_0.routesimulate import get_dijkstra_path
from apps.v1_0.tunnel import get_tunnel_path, tunflow_get_path

# PeriodLinkInfo, OneLinkInfo, OneDirectLink是为了sim.before_fault_link_info和sim.after_fault_link_info 设计的
class OneDirectLink():
    """ 记录某条链路上的A->B或B->A的链路信息
    
    Attributes:
        none
    """
    
    def __init__(self,id):
        self.asset_Id = id       # 出端口的设备节点的ID
        self.asset_net_name = '' # 网元名称
        self.asset_port = ''     # 出端口设备的出端口名称
        self.interface_type = '' # 接口类型
        self.back_speed = 0      # 所有背景流量大小,单位是bps 
        self.te_speed = 0        # tunnel的流量大小 #sprint 3 add
        self.flow_speed = 0      # 导入的flow的流量大小(普通的非隧道的flow) #sprint 3 add
        self.flow_tun_speed = 0  # 基于tunnel创建的流，流量模板导入的隧道流 # sprint 4 add
        self.speed = 0           # 总流量的大小，在计算带宽利用率的时候，进行加和 speed = back_speed + te_speed + flow_speed + flow_tun_speed
        self.out_use_ratio = 0   # 带宽利用率
        self.backgrond_flow_num = 0   # 背景流的个数
        self.add_flow_num = 0         # 添加了多少条flow信息
        self.background_flow_id = []  # 背景流的流量ID列表
        self.add_flow_id = []         # 添加的flow的ID列表
        self.te_id = []               # 添加的tunnel 流量ID  #sprint3 add
        self.band_width = 0           # 带宽    

class OneLinkInfo():
    """记录链路AB上,A->B和B->A的链路信息
    
    Attributes:
        none
    """
    
    def __init__(self,id):
        self.linkid = id
        self.asset_a = 0 # A 设备的AssetID
        self.asset_b = 0 # B 设备的AssetID     
        self.a_to_b = None # 加OneDirectLink的字典,
        self.b_to_a = None # 加OneDirectLink的字典                                             

class PeriodLinkInfo():
    def __init__(self, start_time):
        self.start_time = start_time
        self.end_time = 0
        self.link_id_list = []
        self.link_info = {} # 加OneLinkInfo的字典

# 故障前后flow的对比的统计信息
class FlowDiff():
    def __init__(self, id):
       
        self.id = id  # 流量的ID
        self.name = '' # 流量名称
        self.size = 0 # 流量大小
        self.status = ''  #'change'.'interrupt'.'unchange'
        self.b4_fault_jump = 0 # 故障前的跳数 
        self.after_fault_jump = 0   # 故障后的跳数
        self.b4_fault_delay = ''   # 故障后的延时
        self.after_fault_delay= '' # 故障后的延时
        self.b4_fault_path = []    # 故障前的路径,如['a','b','c']所写，代表从a->b->c的流量路径
        self.after_fault_path = [] # 故障后的路径

class PeriodFlowInfo():
    """某一时间段内故障前故障后的流量统计信息
    
    Attributes:
        none
    """
    
    def __init__(self, start_time):
        self.start_time = 0 # 这个值应该跟key start_time的值 相等
        self.end_time = 0 

        self.b4_fault_flow_num = 0  # 当前时间段故障前有多少条打入的流量
        self.after_fault_flow_num = 0 # 当前时间段故障后有多少条打入的流量

        self.changed_flow_num = 0 # 故障前与故障后相比较，有改变的流量个数
        self.unchanged_flow_num = 0 # 故障前与故障后相比较，没有改变的流量个数
        self.interrupt_flow_num = 0 # 故障前与故障后相比较，中断的流量个数

        self.b4_fault_flow_list = [] # 当前时间段,故障前的流量ID列表
        self.after_fault_flow_list = [] # 当前时间段，故障后的流量ID列表

        self.flow_interrupt_info = {}
        self.flow_changed_info = {}
        self.flow_unchanged_info = {}

        # add : 5.2.1 点击某条链路展示flow信息的需求
        # self.link_to_flow = {'linkid1':['flow1_id','flow2_id'],'linkid2':['flow3_id','flow2_id']}
        self.b4_link_to_flow = {}
        self.after_link_to_flow = {}
    



############################################3
# 接口函数
##############################################
# jinqi
def get_nity_five_max_value(data):
    """获得95%峰值
    
    Args:
        data:某端口的负载数据
    Returns:
        none
    Raise:
        none
    """
    if len(data) == 0:
        return ErrCode.NO_DATA_CAN_NOT_CALCULATE
    elif len(data) == 1:
        return  data[0]
    else:
        data.sort(key=lambda k: (k.get('outUseRatioList')), reverse=False)
        new_data = data
        num = len(new_data)
        index_peak = int(num * 0.95)
        # 注意：如果取的是50%以上的峰值，这里不用判断index_peak>1的情况。如果后续改成小于50%了，这里需要判断是否大于1
        peak_95 = new_data[index_peak - 1]
        return peak_95

def get_coincidence_time(start_time, end_time):
    """获得重叠的时间
    
    Args:
        none
    Returns:
        none
    Raise:
        none
    """
    
    time_list = g_sim.time_sim_info
    first_time = time_list[0]['start_time']
    last_time = time_list[-1]['end_time']

    if start_time >= last_time or end_time <= first_time:
        return ErrCode.FAILED,start_time, end_time
    
    if start_time < first_time:
        start_time = first_time

    if end_time > last_time:
        end_time = last_time

    return ErrCode.SUCCESS,start_time, end_time


def get_flow_flag(start_time):
    """通过start_time获取sim.time_sim_info下，start_time对应的这一段时间是否有打入的flow
    
    Args:
        none
    Returns:
        none
    Raise:
        none
    """
    
    ret = ErrCode.FAILED
    flow_flag = 'false'
    time_list = g_sim.time_sim_info
    for it  in time_list:
        if it['start_time'] == start_time:
            flow_flag = it['has_flow']
            ret = ErrCode.SUCCESS
            break 
    return ret, flow_flag


def get_underlay_flow_path(in_flag, flowid,startTime):
    
    try:
        if in_flag == "orgin":    # 最开始的时候，还没有填充g_sim.flow_info,这个时候，得从g_allFlows里去取flow信息
            flow = g_allFlows[flowid]
            flag = 'before_fault' 
        else:
            flow = g_sim.flow_info[flowid]
            flag = in_flag

        src_id = flow.src_id
        des_id = flow.des_id
        if flag == 'before_fault':
            if g_sim.topo.nodes[src_id].fault == 'yes' or g_sim.topo.nodes[des_id].fault == 'yes':
                data = {"path":[], "delay":0, "jump":0}
                return ErrCode.SUCCESS, data
        else:
            if g_sim.af_topo.nodes[src_id].fault == 'yes' or g_sim.af_topo.nodes[des_id].fault == 'yes':
                data = {"path":[], "delay":0, "jump":0}
                return ErrCode.SUCCESS, data
        
        ret, data = get_dijkstra_path(src_id, des_id, flag,startTime)
        if ret == ErrCode.SUCCESS:
            return ErrCode.SUCCESS, data
        else:
            return ErrCode.FAILED, data
    except Exception as e:
        data = {"path":[], "delay":0, "jump":0}
        print("get_underlay_flow_path Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return  ErrCode.FAILED, data

def add_b4_flows_to_links():
    """把定义前的流添加到定义前的链路信息上
    
    Args:
        none
    Returns:
        none
    Raise:
        none
    """
    try:
        # 遍历取所有的flow
        for time_flag, flows in g_sim.b4_flow.items():
            for flowid in flows:
                if flowid in g_sim.flow_info:
                    tun_name = g_sim.flow_info[flowid].tun_name

                    # underlay flow
                    if tun_name == "":
                        flow_size = g_sim.flow_info[flowid].bandwidth["all"]
                        path = g_sim.flow_info[flowid].b4_path["all"]

                        back_ground = g_sim.before_fault_link_info[time_flag]

                        all_link_info = back_ground.link_info
                        
                        # 把某条流的流经的所有路径，加上打入的流大小
                        for step_path in path:
                            node_start_id = step_path['start_node_id']
                            link_id = step_path['linkid']

                            # 由linkid直接取链路信息,把flow加到这条链路上
                            one_link_info = all_link_info[link_id]
                            if one_link_info.asset_a == node_start_id:
                                one_Link = one_link_info.a_to_b
                            else:
                                one_Link = one_link_info.b_to_a

                            # one_Link 对应OneDirectLink    
                            one_Link.flow_speed += flow_size  
                            one_Link.add_flow_num += 1
                            one_Link.add_flow_id.append(flowid)

                    # 基于tunnel创建的流或者从流量模板导入的隧道流
                    else:
                        flow_size = g_sim.flow_info[flowid].bandwidth[time_flag]
                        path = g_sim.flow_info[flowid].b4_path[time_flag]

                        back_ground = g_sim.before_fault_link_info[time_flag]

                        all_link_info = back_ground.link_info
                        
                        # 把某条流的流经的所有路径的链路上，加上打入的流大小
                        for step_path in path:
                            node_start_id = step_path['start_node_id']
                            link_id = step_path['linkid']

                            # 由linkid直接取链路信息,把flow加到这条链路上
                            one_link_info = all_link_info[link_id]
                            if one_link_info.asset_a == node_start_id:
                                one_Link = one_link_info.a_to_b
                            else:
                                one_Link = one_link_info.b_to_a

                            # one_Link 对应OneDirectLink    
                            one_Link.flow_tun_speed += flow_size  
                            one_Link.add_flow_num += 1
                            one_Link.add_flow_id.append(flowid)
    
        return ErrCode.SUCCESS                 
    except Exception as e:
        print("add_b4_flows_to_links Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.FAILED 

def save_flow_info_to_sim_flow_list():
    # 遍历取所有的flow
    try:
        b4_flow_list = g_sim.flow_list_before_fault
        after_flow_list = g_sim.flow_list_after_fault
        for s_time, flowid_list in g_sim.af_flow.items():
            if len(flowid_list):
                for flowid in flowid_list:
                    if flowid in g_sim.flow_info:
                        one_flow = {'flowId':g_sim.flow_info[flowid].id, 
                                    'flow_name':g_sim.flow_info[flowid].flow_name, 
                                    'source_node_name':g_sim.flow_info[flowid].src_name, 
                                    'des_node_name':g_sim.flow_info[flowid].des_name,
                                    'source_node_id':g_sim.flow_info[flowid].src_id, 
                                    'des_node_id':g_sim.flow_info[flowid].des_id, 
                                    'flow_type':g_sim.flow_info[flowid].flow_type}

                        if s_time in b4_flow_list:
                            time_flow_info = b4_flow_list[s_time]
                            time_flow_info['num'] += 1
                            time_flow_info['flowinfo'].append(one_flow)
                        else:
                            b4_flow_list[s_time] = {'num':1,'flowinfo':[one_flow]}

                        if s_time in after_flow_list:
                            time_flow_info = after_flow_list[s_time]
                            time_flow_info['num'] += 1
                            time_flow_info['flowinfo'].append(one_flow)
                        else:
                            after_flow_list[s_time] = {'num':1,'flowinfo':[one_flow]}
                
                if g_sim.type_flow == True:
                    if s_time in b4_flow_list:
                        b4_flow_list[s_time]['num'] = 0
                        b4_flow_list[s_time]['flowinfo'].clear()

    except Exception as e:
        print("save_flow_info_to_sim_flow_list exception:", e)
        info_logger.error(e)
        error_logger.error(e)

def count_flows_diff_info():
    """故障前后的流量对比统计信息
    
    Args:
        none
    Returns:
        none
    Raise:
        none
    """
    #{'start_time的值':{''num':2,'flowinfo':[{'flowId': '', 'flow_name': '', 'source_node_name': '', 'des_node_name': ''
    # 'source_node_id':"", 'des_node_id':"", 'flow_type':""}]}}
    try:
        for key, value in g_sim.flow_list_after_fault.items():
            start_time = key
            flow_info = value['flowinfo']
            g_sim.statis_flow[start_time] = PeriodFlowInfo(start_time)
            cences_info = g_sim.statis_flow[start_time]
            cences_info.start_time = start_time

            cences_info.after_fault_flow_num = value['num']
            
            # 先判断sim.flow_list_after_fault是否存在这个key值，因为如果故障后的路径均不可达，则故障后的流量个数统计为0
            if key in g_sim.flow_list_before_fault.keys():
                before_fault_flow = g_sim.flow_list_before_fault[key]
                cences_info.b4_fault_flow_num = before_fault_flow['num']
            else:
                cences_info.b4_fault_flow_num = 0

            for flow_detail in flow_info:
                flow_id = flow_detail['flowId']
                # 根据flow_id，找到流量信息
                flow_dict = g_sim.flow_info[flow_id]
                cences_info.after_fault_flow_list.append(flow_id)
                temp_flow_diff = FlowDiff(flow_id)

                if flow_dict.tun_name == "":
                    # 如果故障后，流量跳数为0，那么这条流量就是不可达的
                    temp_flow_diff.size = flow_dict.bandwidth["all"]
                    temp_flow_diff.b4_fault_jump = flow_dict.b4_jump['all'] # 故障前的跳数 
                    temp_flow_diff.after_fault_jump = flow_dict.af_jump['all']   # 故障后的跳数
                    temp_flow_diff.b4_fault_delay = 0  # 故障前的延时
                    temp_flow_diff.after_fault_delay= 0 # 故障后的延时
                    if flow_dict.af_jump["all"] == 0:
                        status = 'interrupt'
                        cences_info.interrupt_flow_num += 1
                        cences_info.flow_interrupt_info[flow_id] = temp_flow_diff
                        temp_flow_diff.b4_fault_path = copy.deepcopy(flow_dict.b4_path['all']) # 故障前的路径,如[{},{},{}]所写，代表从a->b->c的流量路径            
                        temp_flow_diff.after_fault_path = [] # 故障后的路径为空

                    elif flow_dict.af_jump["all"] != flow_dict.b4_jump["all"]:
                        # 如果故障前后跳数次数不相同，那么这条流是改变了的
                        status = 'change'
                        cences_info.after_fault_flow_list.append(flow_id)
                        cences_info.flow_changed_info[flow_id] = temp_flow_diff
                        temp_flow_diff.b4_fault_path = copy.deepcopy(flow_dict.b4_path['all']) # 故障前的路径,如[{},{},{}]所写，代表从a->b->c的流量路径
                        temp_flow_diff.after_fault_path = copy.deepcopy(flow_dict.af_path['all']) # 故障后的路径
                        cences_info.changed_flow_num += 1

                    elif operator.eq(flow_dict.af_path["all"], flow_dict.b4_path["all"]) == False:
                        # 如果故障前后跳数次数相同，但是具体路径是不一样的，那么这条流也是改变了的
                        status = 'change'
                        cences_info.after_fault_flow_list.append(flow_id)
                        cences_info.flow_changed_info[flow_id] = temp_flow_diff
                        temp_flow_diff.b4_fault_path = copy.deepcopy(flow_dict.b4_path['all']) # 故障前的路径,如[{},{},{}]所写，代表从a->b->c的流量路径
                        temp_flow_diff.after_fault_path = copy.deepcopy(flow_dict.af_path['all']) # 故障后的路径
                        cences_info.changed_flow_num += 1
                    else:
                        status = 'unchange'
                        cences_info.after_fault_flow_list.append(flow_id)
                        cences_info.flow_unchanged_info[flow_id] = temp_flow_diff
                        temp_flow_diff.b4_fault_path = copy.deepcopy(flow_dict.b4_path['all']) # 故障前的路径,如[{},{},{}]所写，代表从a->b->c的流量路径
                        temp_flow_diff.after_fault_path = copy.deepcopy(flow_dict.af_path['all']) # 故障后的路径
                        cences_info.unchanged_flow_num += 1
                else:
                    temp_flow_diff.size = flow_dict.bandwidth[start_time]
                    temp_flow_diff.b4_fault_jump = flow_dict.b4_jump[start_time] # 故障前的跳数 
                    temp_flow_diff.after_fault_jump = flow_dict.af_jump[start_time]   # 故障后的跳数
                    temp_flow_diff.b4_fault_delay = 0  # 故障前的延时
                    temp_flow_diff.after_fault_delay= 0 # 故障后的延时
                    # 如果故障后，流量跳数为0，那么这条流量就是不可达的
                    if flow_dict.af_jump[start_time] == 0 and flow_dict.b4_jump[start_time] != 0:
                        status = 'interrupt'
                        cences_info.interrupt_flow_num += 1
                        cences_info.flow_interrupt_info[flow_id] = temp_flow_diff
                        temp_flow_diff.b4_fault_path = copy.deepcopy(flow_dict.b4_path[start_time]) # 故障前的路径,如[{},{},{}]所写，代表从a->b->c的流量路径            
                        temp_flow_diff.after_fault_path = [] # 故障后的路径为空

                    elif flow_dict.af_jump[start_time] != flow_dict.b4_jump[start_time]:
                        # 如果故障前后跳数次数不相同，那么这条流是改变了的
                        status = 'change'
                        cences_info.after_fault_flow_list.append(flow_id)
                        cences_info.flow_changed_info[flow_id] = temp_flow_diff
                        temp_flow_diff.b4_fault_path = copy.deepcopy(flow_dict.b4_path[start_time]) # 故障前的路径,如[{},{},{}]所写，代表从a->b->c的流量路径
                        temp_flow_diff.after_fault_path = copy.deepcopy(flow_dict.af_path[start_time]) # 故障后的路径
                        cences_info.changed_flow_num += 1

                    elif operator.eq(flow_dict.af_path[start_time], flow_dict.b4_path[start_time]) == False:
                        # 如果故障前后跳数次数相同，但是具体路径是不一样的，那么这条流也是改变了的
                        status = 'change'
                        cences_info.after_fault_flow_list.append(flow_id)
                        cences_info.flow_changed_info[flow_id] = temp_flow_diff
                        temp_flow_diff.b4_fault_path = copy.deepcopy(flow_dict.b4_path[start_time]) # 故障前的路径,如[{},{},{}]所写，代表从a->b->c的流量路径
                        temp_flow_diff.after_fault_path = copy.deepcopy(flow_dict.af_path[start_time]) # 故障后的路径
                        cences_info.changed_flow_num += 1
                    else:
                        status = 'unchange'
                        cences_info.after_fault_flow_list.append(flow_id)
                        cences_info.flow_unchanged_info[flow_id] = temp_flow_diff
                        temp_flow_diff.b4_fault_path = copy.deepcopy(flow_dict.b4_path[start_time]) # 故障前的路径,如[{},{},{}]所写，代表从a->b->c的流量路径
                        temp_flow_diff.after_fault_path = copy.deepcopy(flow_dict.af_path[start_time]) # 故障后的路径
                        cences_info.unchanged_flow_num += 1
            
                temp_flow_diff.id = flow_id  # 流量的ID
                temp_flow_diff.name = flow_dict.flow_name # 流量名称

                temp_flow_diff.status = status  #'change'.'interrupt'.'unchanged'

                for path_value in temp_flow_diff.b4_fault_path:
                    linkid = path_value['linkid']
                    if linkid in cences_info.b4_link_to_flow:
                        cences_info.b4_link_to_flow[linkid].append(flow_id)
                    else:
                        cences_info.b4_link_to_flow[linkid] = [flow_id]

                if status != 'interrupt':
                    for path_value in temp_flow_diff.after_fault_path:
                        linkid = path_value['linkid']
                        if linkid in cences_info.after_link_to_flow:
                            cences_info.after_link_to_flow[linkid].append(flow_id)
                        else:
                            cences_info.after_link_to_flow[linkid] = [flow_id]

    except Exception as e:
        print("count_flows_diff_info() Exception:", e)
        info_logger.error(e)
        error_logger.error(e)  

    return ErrCode.SUCCESS

# backFlowId: 背景流量的流量ID,与这个字典的key相同 
# bandWidth: 背景流量的带宽,单位是bps
# afterFaultExist: 故障后，这条背景流量是否还存在。例如，如果目的节点不存在了、源节点不存在了、源和目的之间不可达了，这样的背景流就会变成‘不存在’，即'no'
# b4FaultPath: 故障前的背景流路径
# afterFaultPath: 故障后的背景流路径
#all_back_ground_flows ={'123456789456': {'backFlowId': '123456789456','bandWidth':'20bps','afterFaultExist':'no','b4FaultPath':[],'afterFaultPath':[]}}

def parse_background_info(s_time, linkid, data_info):
    """解析某条链路的背景流,累加记录链路的背景流
    
    Args:
        s_time：开始时间
        linkid：链路ID
        data_info:链路的背景流信息
    Returns:
        none
    Raise:
        none
    """
    try:
        linkStep = g_sim.all_link_payload # sprint3 modify
        # 如果s_time这个值在其他的链路上之前已添加了，则sim.before_fault_link_info会存在s_time这个key，仅需在上面再添加即可
        if s_time not in linkStep:
            linkStep[s_time] = PeriodLinkInfo(s_time)
            period_link = linkStep[s_time]
            period_link.start_time = s_time
            sim_end_time = get_end_time(s_time)
            period_link.end_time = sim_end_time
        else:
            period_link = linkStep[s_time]

        # 获得链路信息
        topo_link = g_sim.topo.links[linkid]

        period_link.link_info[linkid] = OneLinkInfo(linkid)
        linkInfo = period_link.link_info[linkid]
        linkInfo.linkid = linkid
        linkInfo.asset_a = topo_link.nodeid1
        linkInfo.asset_b = topo_link.nodeid2
        linkInfo.a_to_b = OneDirectLink(topo_link.nodeid1)
        linkInfo.b_to_a = OneDirectLink(topo_link.nodeid2)

        temp_a_to_b = linkInfo.a_to_b
        temp_b_to_a = linkInfo.b_to_a

        temp_a_to_b.asset_net_name = topo_link.nodename1
        temp_b_to_a.asset_net_name = topo_link.nodename2
        temp_a_to_b.asset_port = topo_link.ifdesc1 # topo_link.ifindex1
        temp_b_to_a.asset_port = topo_link.ifdesc2 # topo_link.ifindex2
        temp_a_to_b.interface_type = topo_link.ifdesc1.split('net',-1)[0] + 'net' # topo_link.ifdesc1
        temp_b_to_a.interface_type = topo_link.ifdesc2.split('net',-1)[0] + 'net' # topo_link.ifdesc2
    
        temp_a_to_b.band_width = topo_link.snmpIfHighSpeed 
        temp_b_to_a.band_width = topo_link.snmpIfHighSpeed         

        # 1:everager(均值仿真) 2:peak(峰值仿真) 3:ninetyFivePeak(95%峰值仿真) 0:未设置
        if g_sim.data_manner == 1:
            mean_a_speed = parse_flow_to_kbps(data_info["meanSpeedAUnit"],  float(data_info["meanSpeedA"]))
            temp_a_to_b.back_speed =mean_a_speed

            mean_b_speed = parse_flow_to_kbps(data_info["meanSpeedBUnit"],  float(data_info["meanSpeedB"]))
            temp_b_to_a.back_speed = mean_b_speed

        elif  g_sim.data_manner == 2:
            max_a_speed = parse_flow_to_kbps(data_info["maxSpeedAUnit"],  float(data_info["maxSpeedA"]))
            temp_a_to_b.back_speed = max_a_speed
            
            max_b_speed = parse_flow_to_kbps(data_info["maxSpeedBUnit"],  float(data_info["maxSpeedB"]))
            temp_b_to_a.back_speed =max_b_speed

        else:         
            dic_value = get_nity_five_max_value(data_info['A'])
            temp_a_to_b.back_speed =dic_value.outSpeedList
            dic_value = get_nity_five_max_value(data_info['B'])
            temp_b_to_a.back_speed =dic_value.outSpeedList

    except Exception as e:
        print("parse_background_info Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.FAILED  

    return ErrCode.SUCCESS

def set_background_info_to_fix_value(s_time, linkid):
    """当某链路获取背景流量失败时，直接把这条链路填成固定值0
    
    Args:
        s_time：开始时间
        linkid：链路ID
        data_info:链路的背景流信息
    Returns:
        none
    Raise:
        none
    """ 
    try:
        linkStep = g_sim.all_link_payload
        # 如果s_time这个值在其他的链路上之前已添加了，则sim.before_fault_link_info会存在s_time这个key，仅需在上面再添加即可
        if s_time not in linkStep:
            linkStep[s_time] = PeriodLinkInfo(s_time)
            period_link = linkStep[s_time]
            period_link.start_time = s_time
            sim_end_time = get_end_time(s_time)
            period_link.end_time = sim_end_time
        else:
            period_link = linkStep[s_time]

        # 获得链路信息
        topo_link = g_sim.topo.links[linkid]

        period_link.link_info[linkid] = OneLinkInfo(linkid)
        linkInfo = period_link.link_info[linkid]
        linkInfo.linkid = linkid
        linkInfo.asset_a = topo_link.nodeid1
        linkInfo.asset_b = topo_link.nodeid2
        linkInfo.a_to_b = OneDirectLink(topo_link.nodeid1)
        linkInfo.b_to_a = OneDirectLink(topo_link.nodeid2)

        temp_a_to_b = linkInfo.a_to_b
        temp_b_to_a = linkInfo.b_to_a

        temp_a_to_b.asset_net_name = topo_link.nodename1
        temp_b_to_a.asset_net_name = topo_link.nodename2
        # add test 
        temp_a_to_b.asset_port = topo_link.ifdesc1 # topo_link.ifindex1
        temp_b_to_a.asset_port = topo_link.ifdesc2 # topo_link.ifindex2
        temp_a_to_b.interface_type = topo_link.ifdesc1.split('net',-1)[0] + 'net' # topo_link.ifdesc1
        temp_b_to_a.interface_type = topo_link.ifdesc2.split('net',-1)[0] + 'net' # topo_link.ifdesc2

        # 背景流写成0
        temp_b_to_a.back_speed = 0
        temp_b_to_a.speed = 0
        temp_a_to_b.back_speed = 0
        temp_a_to_b.speed = 0

        # 带宽填成获取topo时得到的带宽
        temp_a_to_b.band_width = topo_link.snmpIfHighSpeed
        temp_b_to_a.band_width = topo_link.snmpIfHighSpeed

        return ErrCode.SUCCESS
    except Exception as e:
        print("set_background_info_to_fix_value Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.FAILED 

def copy_all_linkd_background_flow(source_start_time, des_start_time,des_end_time):
    """把数据，直接存多份
        例如仿真的时间周期为1小时，而这1小时由于有flow导入被切分成5段了,在其他函数已经存了sim.before_fault_link_info[t1]了,
        这里把sim.before_fault_link_info[t2]到sim.before_fault_link_info[t5]都存成sim.before_fault_link_info[t1]一样的数据值    
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
            linkStep = g_sim.all_link_payload
            linkStep[start_time_new] = PeriodLinkInfo(start_time_new)
            linkStep[start_time_new] = copy.deepcopy(linkStep[source_start_time])
            linkStep[start_time_new].start_time = start_time_new
            sim_end_time = get_end_time(start_time_new)
            linkStep[start_time_new].end_time = sim_end_time
            start_time_new = sim_end_time

    except Exception as e:
        print("copy_all_linkd_background_flow Exception:", e)
        info_logger.error(e)
        error_logger.error(e)

def copy_all_linkd_aviliablities(source_start_time, des_start_time,des_end_time):
    try:
        start_time_new = des_start_time
        sim_end_time = des_start_time
        while sim_end_time != des_end_time:
            for linkId in g_sim.l3_topo.links:
                linkInfo = g_sim.l3_topo[linkId]
                linkInfo.jittery[start_time_new] = linkInfo.jittery[source_start_time]
                linkInfo.delay[start_time_new]  = linkInfo.delay[source_start_time]
                linkInfo.loss_rate[start_time_new]  = linkInfo.loss_rate[source_start_time]
            for linkId in g_sim.af_l3_topo.links:
                linkInfo = g_sim.af_l3_topo[linkId]
                linkInfo.jittery[start_time_new] = linkInfo.jittery[source_start_time]
                linkInfo.delay[start_time_new]  = linkInfo.delay[source_start_time]
                linkInfo.loss_rate[start_time_new]  = linkInfo.loss_rate[source_start_time]
            sim_end_time = get_end_time(start_time_new)
            start_time_new = sim_end_time
    except Exception as e:
        print("copy_all_linkd_background_flow Exception:", e)
        info_logger.error(e)
        error_logger.error(e)