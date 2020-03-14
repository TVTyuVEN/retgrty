# -*- encoding: utf-8 -*-
"""
@File    : util.py
@Time    : 2019/05/29 11:17:00
@Author  : 
@License : Copyright (c) 2004-2019 New H3C Tech. Co., Ltd. All rights reserved.
@Desc    : 公共函数文件
"""

import os
import time
import logging
from logging.handlers import RotatingFileHandler
from flask import current_app
import uuid
from apps.datacode import SyncModCode, SyncStatusCode

import threading

SIMLATAE_STATE_LOCK = threading.Lock()
FLOW_IMPORT_LOCK = threading.Lock()

# 解析好的流量信息，全部保存在这里
g_allFlows = {}  # {flowid:Flow类}


class DigitalTwins(object):
    """数据孪生
    
    Attributes:
        data_sync_status: 数据同步状态
    """

    def __init__(self):
        self.data_sync_status = 0  # 进行数据同步时置1
        self.init_data_status()  # 三类数据同步的状态初始化
        self.stop_sync_flag = 0
        self.phy_topo = None
        self.l3_topo = None
        self.app_info = None  # sprint 3 add，应用组控制信息

        # Topo显示设置相关信息
        self.dis_name = "on"
        self.dis_name_type = "name"  # name or ip
        self.dis_tip = "on"
        self.dis_interface = "off"
        self.auto_save_topo = "off"
        self.auto_save_time = 10

        # BGP LS相关信息
        self.bgp_enable = 0
        self.bgp_as = 300
        self.bgp_port_ip = "10.99.211.181"
        self.bgp_peer_ip = "192.40.40.3"
        self.bgp_state = "N/A"

    def init_data_status(self):  # 初始化拓扑同步、配置同步、链路控制同步的状态为“未同步”
        # 0 为未同步,1为同步中,2为同步失败,3为同步完成
        self.topo_sync_status = SyncStatusCode.SYNC_NOT
        self.topo_sync_progress = 0
        self.topo_sync_detail = {
            "time": "",
            "status": SyncModCode.SYNC_LOG_NONE,
            "reason": SyncModCode.SYNC_LOG_NONE}

        self.conf_sync_status = SyncStatusCode.SYNC_NOT
        self.conf_sync_progress = 0
        self.conf_sync_detail = {
            "time": "",
            "status": SyncModCode.SYNC_LOG_NONE,
            "reason": SyncModCode.SYNC_LOG_NONE}

        # sprint 3 add
        self.link_control_sync_status = SyncStatusCode.SYNC_NOT
        self.link_control_sync_progress = 0
        self.link_control_sync_detail = {
            "time": "",
            "status": SyncModCode.SYNC_LOG_NONE,
            "reason": SyncModCode.SYNC_LOG_NONE}
        # 保存当前同步时刻    
        self.sync_data_finish_time = 0


g_dt = DigitalTwins()


class AnalyseSetting():
    def __init__(self):
        self.analyse_time = 0  # 当前查看仿真的时间
        self.analyse_start_time = 0
        self.analyse_end_time = 0
        self.analyse_firstStepEnd = 25  # 暂定的初值，根据视频上设定
        self.analyse_secondStepEnd = 75
        self.analyse_thirdStepEnd = 90


g_ana = AnalyseSetting()


class SimulateInfo(object):
    """仿真信息
    
    Attributes:
        similate_status: 数据仿真状态
    """

    def __init__(self):
        self.inherit_flag = False  # sprint 3 add 是否增量仿真，False:重新仿真，True:增量仿真
        self.stop_simulate_flag = 0
        # 0:未仿真  1：仿真完成 2:仿真被迫停止 3：正在仿真中
        self.status = 0

        # 1:everager(均值仿真) 2:peak(峰值仿真) 3:ninetyFivePeak(95%峰值仿真) 0:未设置
        self.data_manner = 0

        # 仿真类型 单选,流量仿真和故障仿真,两者选其一
        self.type_route = False
        self.type_flow = True
        self.type_fault = True

        # 仿真对象 复选
        self.object_load = True
        self.object_tunnel_flow = False
        self.object_input_flow = True

        # 仿真时间 每个都必须有值
        self.time_cycle = 0  # 仿真的时间周期，单位是毫秒（为了计算方便）
        self.time_start = 0  # 仿真的开始时间 2019_7_15 10:20
        self.time_end = 0  # 仿真的结束时间 2019_7_15 16:00
        self.time_cycle_num = 0  # 仿真的周期,这个周期是根据 （time_end - time_start）/ time_cycle 向上取整

        # 仿真协议 复选
        self.agree_bgp = True
        self.agree_isis = False
        self.agree_ospf = False
        self.agree_mpls = False
        self.tunnel_optimize = True

        self.topo = None  # 这里是phy_topo,仿真的topo,这里需要保存一份以备数据同步了，TOPO改变了。
        self.l3_topo = None  # 仿真的layer3 topo
        self.af_topo = None  # sprint 3 add,增量仿真后的物理topo,为了保持代码的一致性，用after来表示,实际意义是inherit
        self.af_l3_topo = None  # sprint 3 add,增量仿真后的三层topo

        self.flow_info = {}  # {flowid:flowObj}
        self.org_flow = {}  # {t1:[flowid1, flowid2], t2:[flowid1,flowid2, flowid3]}  # 原始的无任何故障的流信息,各个时间段的key都存在，只是有可能对应的[]为空
        self.b4_flow = {}  # {t1:[flowid1, flowid2], t2:[flowid1,flowid2, flowid3]}
        self.af_flow = {}  # {t1:[flowid1, flowid2], t2:[flowid1,flowid2, flowid3]}
        self.analyse_time = 0  # 当前查看仿真的时间（跟随前台设置的时间点变动）

        self.time_section = 0  # 统计仿真的时间加入流量后，有多少个时间片
        self.time_sim_info = []
        # 调试完成，应该把上边的打开，把下边的关闭 need_modify

        # self.time_sim_info = [{'start_time':1563157200000,'end_time':1563159000000,'has_flow':'false'}, # 10:20~10:50
        #                       {'start_time':1563159000000,'end_time':1563160800000,'has_flow':'true'}, # 10:50~11:20
        #                       {'start_time':1563160800000,'end_time':1563164400000,'has_flow':'false'}, # 11:20~12:20 
        #                       {'start_time':1563164400000,'end_time':1563168000000,'has_flow':'true'}, # 12:20~13:20
        #                       {'start_time':1563168000000,'end_time':1563171600000,'has_flow':'true'},# 13:20~14:20
        #                       {'start_time':1563171600000,'end_time':1563172800000,'has_flow':'true'},# 14:20~14:40
        #                       {'start_time':1563172800000,'end_time':1563174000000,'has_flow':'true'},# 14:40~15:00
        #                       {'start_time':1563174000000,'end_time':1563175200000,'has_flow':'true'},# 15:00~15:20
        #                       {'start_time':1563175200000,'end_time':1563177600000,'has_flow':'true'}, # 15:20~16:00 
        #                     ]

        # sprint 3 add 所有链路的原始的负载信息，为保持一致性，沿用跟sim.before_fault_link_info一致的结构,虽然对于时刻点仿真而言,时间已无意义
        self.all_link_payload = {}
        self.before_fault_link_info = {}  # PeriodLinkInfo
        self.after_fault_link_info = {}

        # {'start_time的值':{''num':2,'flowinfo':[{'flowId': '', 'flow_name': '', 'source_node_name': '', 'des_node_name': ''}]}}
        self.flow_list_before_fault = {}  # 故障前后的按时间片存放流量信息
        self.flow_list_after_fault = {}  # 故障前后的按时间片存放流量信息

        self.statis_flow = {}  # 故障前后流量的统计信息
        self.statis_tunnel = None  # 暂时不做         

        self.statis_load = None  # 因为负载是改变一下时刻，就需要重新计算的值，所以不方便以字典来存储按时间的flow的统计信息

        self.sim_step_statis = {}  # 'before':,'after' 对应 SimStepStatisAll类
        # [{'host':'ip的值','port':'ifindex的值'}]
        self.all_fault = []

        # 跟故障点相关的背景流量的信息      
        # {‘start_time’:[{"ipv4_src_addr":"70.1.1.1","ipv4_dst_addr":"70.1.1.2","l4_src_port":10001, "l4_dst_port":10000,"protocol":17,
        #                "sum_bytes":100,"count":2,"avage_bit":0,"host":"10.99.211.201", "ifinex":15, "before_route":[], "after_route":[]},]}
        # 
        self.fault_backgrond_info = {}

    def clear_info(self):
        self.inherit_flag = False
        # self.stop_simulate_flag = 0

        # 1:everager(均值仿真) 2:peak(峰值仿真) 3:ninetyFivePeak(95%峰值仿真) 0:未设置
        self.data_manner = 0
        self.status = 0

        # 仿真类型 复选
        self.type_route = False
        self.type_flow = False

        # 仿真对象 复选
        self.object_load = False
        self.object_tunnel_flow = False
        self.object_input_flow = False

        # 仿真协议 复选
        self.agree_bgp = False
        self.agree_isis = False
        self.agree_ospf = False
        self.agree_mpls = False
        self.before_fault_link_info.clear()
        self.after_fault_link_info.clear()
        self.statis_flow.clear()
        self.flow_list_before_fault.clear()
        self.flow_list_after_fault.clear()
        self.statis_tunnel = None
        self.statis_load = None
        self.flow_info.clear()
        self.sim_step_statis.clear()
        self.time_sim_info.clear()
        self.fault_backgrond_info.clear()
        self.all_fault.clear()
        self.all_link_payload.clear()

    def show_sim_setting(self):
        print('123')
        print(self.status)
        print('self.status:', self.status)
        print('self.data_manner:', self.data_manner)
        print('self.type_route:', self.type_route)
        print('self.type_flow:', self.type_flow)
        print('self.object_load:', self.object_load)
        print('self.object_tunnel_flow:', self.object_tunnel_flow)
        print('self.object_input_flow:', self.object_input_flow)
        print('self.time_cycle:', self.time_cycle)
        print('self.time_start:', self.time_start)
        print('self.time_end:', self.time_end)
        print('self.time_cycle_num:', self.time_cycle_num)
        print('self.agree_bgp:', self.agree_bgp)
        print('self.agree_isis:', self.agree_isis)
        print('self.agree_ospf:', self.agree_ospf)
        print('self.agree_mpls:', self.agree_mpls)


g_sim = SimulateInfo()


class TunnelRec(object):
    """所有的Tunnel信息
    
    Attributes:
        none
    """

    def __init__(self):
        self.sdntunnelid_to_tunneluuid = {}  # 将从sdn获取的tunnel_id转成存储的tunnel_uuid
        self.node_to_tunid = {}  # tunnel始节点对应tunnel id的字典，便于查找
        self.org_tuns = {}  # 数据同步时，获得的tuns 信息 {uuid:Tunnel类}，uuid= nodeId+tunnelName

        self.sim_orgtuns = {}  # 首次仿真时，获得的各个时间段的tunnel信息 {t1: {tunnel_id:Tunnel类}, t2: {tunnel_id:Tunnel类}}
        self.sim_b4tuns = {}  # 首次仿真时，故障前的tunnels；增量仿真时，继承仿真定义前的tunnels; {t1: {tunnel_id:Tunnel类}, t2: {tunnel_id:Tunnel类}}
        self.sim_aftuns = {}  # 首次仿真时，故障后的tunnels；增量仿真时，继承仿真定义后的tunnels;{t1: {tunnel_id:Tunnel类}, t2: {tunnel_id:Tunnel类}}

        self.change_tuns = {}  # 用于存放tunnel_id {t1:[tunnel_id1, tunnel_id2, tunnel_id3], t2:[],t3:[]}
        self.unchange_tuns = {}  # 用于存放tunnel_id {t1:[], t2:[],t3:[]}
        self.interrupt_tuns = {}  # 用于存放tunnel_id {t1:[], t2:[],t3:[]}

        self.occupy_cur = {}  # {t1:{tunnel_id1:[occupy_value, current_value], tunnelid2:[]}, }  # 隧道各个时刻的路径流量变化

    def clear_info(self):
        self.sdntunnelid_to_tunneluuid.clear()
        self.node_to_tunid.clear()
        self.org_tuns.clear()
        self.sim_orgtuns.clear()
        self.sim_b4tuns.clear()
        self.sim_aftuns.clear()
        self.change_tuns.clear()
        self.unchange_tuns.clear()
        self.interrupt_tuns.clear()


g_tunrec = TunnelRec()


class SdnPolicy(object):
    """SDN 策略相关的信息
    
    Attributes:
        none
    """

    def __init__(self):
        self.affinityEnable = 0
        self.calcLimit = 0
        self.reservedBandwidthPercent = 0
        self.flowgroup = {}  # 应用组的全局变量  {groupid:AppGroup, groupid:AppGroup}
        self.policy = {}  # 策略的全局变量  {policyid:Policy, policyid:Policy}
        self.sla_level = {}  # sla级别的全局变量 {slaid:Sla, slaid:Sla}

    def clear_info(self):
        self.flowgroup.clear()
        self.policy.clear()
        self.sla_level.clear()


g_sdnply = SdnPolicy()


class InfoFilter(logging.Filter):
    """log日志过滤."""

    def filter(self, record):
        """过滤器,过滤info level以下,error info以上的log"""

        if logging.INFO <= record.levelno < logging.ERROR:
            # 已经是INFO级别了, 然后利用父类, 返回 1
            return super().filter(record)
        else:
            return 0


info_logger = logging.getLogger(__name__ + ".info")
error_logger = logging.getLogger(__name__ + ".error")


def init_logger(app):
    """初始化日志记录。"""

    log_dir = os.path.join(os.path.dirname(__file__), os.pardir, 'logs')
    # 新建第一次的log文件夹
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # print(log_dir)
    err_log_path = os.path.join(log_dir, 'error-' + time.strftime('%Y-%m-%d', time.localtime(time.time())) + '.log')
    info_log_path = os.path.join(log_dir, 'info-' + time.strftime('%Y-%m-%d', time.localtime(time.time())) + '.log')

    # make_dir(err_log_path)
    # make_dir(info_log_path)

    formater = logging.Formatter('%(asctime)s %(threadName)s %(levelname)s %(pathname)s %(lineno)s : %(message)s')

    # info log
    file_handler_info = RotatingFileHandler(info_log_path)
    file_handler_info.setFormatter(formater)
    # info_filter = InfoFilter()
    # file_handler_info.addFilter(info_filter)
    info_logger.setLevel(logging.INFO)
    info_logger.addHandler(file_handler_info)

    # error log
    file_handler_err = RotatingFileHandler(err_log_path)
    file_handler_err.setFormatter(formater)
    error_logger.setLevel(logging.ERROR)
    error_logger.addHandler(file_handler_err)


# def log_info(msg):
#    info_logger.info(msg)

# def log_warning(msg):
#    info_logger.warning(msg)

# def log_error(msg):
#    error_logger.error(msg)

def generate_uuid():
    return str(uuid.uuid1())


def get_current_time():
    return int(round(time.time() * 1000))


def get_current_time_str():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


def get_end_time(start_time):
    """通过start_time获取sim.time_sim_info下，start_time对应的end_time
    
    Args:
        none
    Returns:
        none
    Raise:
        none
    """
    end_time = 0
    time_list = g_sim.time_sim_info

    for it in time_list:
        if it['start_time'] == start_time:
            end_time = it['end_time']
            break
    return end_time


def get_start_end_time(cur_time):  # 返回切片起始时间和结束时间
    try:
        n = len(g_sim.time_sim_info)
        start, end = 0, n - 1
        input_time = int(cur_time)
        if int(input_time) < g_sim.time_sim_info[0]['start_time'] or int(input_time) > g_sim.time_sim_info[end][
            'end_time']:
            return 0, 0
        if input_time == g_sim.time_sim_info[end]['end_time']:
            return g_sim.time_sim_info[end]['start_time'], g_sim.time_sim_info[end]['end_time']
        while start <= end:
            mid = (end + start) // 2
            if input_time >= g_sim.time_sim_info[mid]['start_time'] and input_time < g_sim.time_sim_info[mid][
                'end_time']:
                return g_sim.time_sim_info[mid]['start_time'], g_sim.time_sim_info[mid]['end_time']
            elif input_time < g_sim.time_sim_info[mid]['start_time']:
                end = mid - 1
            else:
                start = mid + 1
    except Exception as e:
        print("get_start_end_time Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return 0, 0


def get_start_end_time_fix(cur_time):  # 返回固定时间点的起始时间和结束时间
    try:
        start = int(cur_time)
        if start != g_sim.time_sim_info[0]['start_time']:
            start = g_sim.time_sim_info[0]['start_time']

        end = start + 300000
        return start, end
    except Exception as e:
        print("get_start_end_time_fix Exception:", e)
        info_logger.error(e)
        error_logger.error(e)


def judge_curtime_in_simlate_time(cur_time):
    if int(cur_time) < g_sim.time_sim_info[0]['start_time'] or int(cur_time) > g_sim.time_sim_info[-1]['end_time']:
        # 不在仿真时间范围内
        return -1
    else:
        # 在仿真时间范围内
        return 0


def get_simlate_start_end_time():
    try:
        if g_sim.time_sim_info and 'start_time' in g_sim.time_sim_info[0] and 'end_time' in g_sim.time_sim_info[-1]:
            s_time = g_sim.time_sim_info[0]['start_time']
            e_time = g_sim.time_sim_info[-1]['end_time']
        else:
            s_time = 0
            e_time = 0
        data = {
            'simStartTime': s_time,
            'simEndTime': e_time
        }
        return data
    except:
        data = {
            'simStartTime': 0,
            'simEndTime': 0
        }
        return data


def is_ipv4_str(addr):
    """判断字符串是否为IPV4地址"""

    data = addr.split(".")
    if len(data) == 4:
        for i in range(0, 4):
            if str.isdigit(data[i]):
                if 0 <= int(data[i]) <= 255:
                    pass
                else:
                    return False
            else:
                return False

        return True
    else:
        return False


def parse_flow_to_kbps(unit, value):
    """把流统一换算成单位：bps，便于后续计算
    
    Args:
        none
    Returns:
        none
    Raise:
        none
    """
    if unit == 'bps':
        result = value / 1000
    elif unit == 'kbps' or unit == 'Kbps':
        result = value
    elif unit == 'mbps' or unit == 'Mbps':
        result = value * 1000
    elif unit == 'gbps' or unit == 'Gbps':
        result = value * 1000000
    else:
        # 流量模板已改，默认为 Mbps
        result = value * 1000
    return result
