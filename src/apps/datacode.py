# -*- encoding: utf-8 -*-
"""
@File    : dataCode.py
@Time    : 2019/06/22 15:34:39
@Author  : leijuyan
@License : Copyright (c) 2004-2019 New H3C Tech. Co., Ltd. All rights reserved.
@Desc    : 
"""


class SyncLogStatusCode:
    """同步详情状态"""

    SYNC_LOG_SUCCESS = 0
    SYNC_LOG_FAIL = 1


class SyncStatusCode:
    """同步详情状态"""

    # 同步状态，不可更改
    SYNC_NOT = 0
    SYNC_SYNCING = 1
    SYNC_FAIL = 2
    SYNC_FINISH = 3


class SyncModCode:
    """自定义同步状态。"""

    # 可以更改
    SYNC_LOG_NONE = ""
    SYNC_LOG_TOPO_GET_FAIL = 100
    SYNC_LOG_TOPO_PARSE_FAIL = 101
    SYNC_LOG_TOPO_NO_NODES = 102
    SYNC_LOG_CONF_GET_FAIL = 103
    SYNC_LOG_CONF_PARSE_FAIL = 104
    SYNC_LOG_USER_STOP = 105
    SYNC_LOG_PORT_IP_GET_FAIL = 106
    SYNC_LOG_PORT_IP_PARSE_FAIL = 107
    SYNC_LOG_GET_LAYER3_PORT_FAIL = 108
    SYNC_LOG_PARSER_LAYER3_FAIL = 109
    SYNC_LOG_PARSER_LINK_CONTROL_FAIL = 110  # sprint 3 add,获取链路控制失败.
    SYNC_LOG_PARSER_SNA_TUNNEL_FAIL = 111
    SYNC_LOG_PARSER_BIG_TUNNEL_FAIL = 112
    SYNC_LOG_PARSER_FLOWGROUP_FAIL = 113
    SYNC_LOG_SYNC_SUCCESS = 114

    SYNC_MSG = {
        SYNC_LOG_NONE: ["", ""],
        SYNC_LOG_TOPO_GET_FAIL: ["get topo data from itoa failed", "获取拓扑数据失败"],
        SYNC_LOG_TOPO_PARSE_FAIL: ["parse topo data failed", "解析拓扑数据失败"],
        SYNC_LOG_TOPO_NO_NODES: ["parse topo data failed,no network element", "无任何网元，所以解析拓扑失败"],
        SYNC_LOG_CONF_GET_FAIL: ["get config data from itoa failed", "获取配置数据失败"],
        SYNC_LOG_CONF_PARSE_FAIL: ["parse config data failed", "解析配置数据失败"],
        SYNC_LOG_USER_STOP: ["stoped by user", "用户强制停止"],
        SYNC_LOG_PORT_IP_GET_FAIL: ["get port ip info failed", "获取设备端口的IP信息失败"],
        SYNC_LOG_PORT_IP_PARSE_FAIL: ["parse port ip info failed", "解析设备端口的IP信息失败"],
        SYNC_LOG_GET_LAYER3_PORT_FAIL: ['get layer3 info failed', "获取三层信息失败"],
        SYNC_LOG_PARSER_LAYER3_FAIL: ['parse layer3 failed', "三层解析失败"],
        SYNC_LOG_PARSER_LINK_CONTROL_FAIL: ['parse link control failed', "获取链路控制失败"],  # sprint 3 add,获取链路控制失败.
        SYNC_LOG_PARSER_SNA_TUNNEL_FAIL: ['parse all sna tunnels failed', "解析SNA隧道失败"],
        SYNC_LOG_PARSER_BIG_TUNNEL_FAIL: ['parse all bigdata tunnels failed', "解析大数据隧道失败"],
        SYNC_LOG_PARSER_FLOWGROUP_FAIL: ['parse all flowgroup failed', "解析流组信息失败"],
        SYNC_LOG_SYNC_SUCCESS: ['sync data success', "数据同步成功"]

    }


class FlowLoadDetailCode:
    """自定义同步状态。"""

    # 自定义错误码
    TOPO_FINISH_SEARCH_FLOW = 0
    FIND_THE_FLOW_FILE = 1
    FIND_THE_FLOW_FAILED = 2
    FILE_PARSNG_FINISH_HAS_FAILED_DETAIL = 3
    FILE_PARSNG_FAILED = 4
    FILE_PARSNG_FINISH_SUCCESS = 5
    FILE_PARSNG_FINISH_SUCCESS_CHANGE_DES = 6

    FLOW_LOAD_MSG = {
        TOPO_FINISH_SEARCH_FLOW: ["add topo finish,beging to search flow file", "加载拓扑完成,开始查找flow文件"],
        FIND_THE_FLOW_FILE: ["find the flow file", "找到一个流量文件"],
        FIND_THE_FLOW_FAILED: ["can not find the flow file", "找流量文件失败"],
        FILE_PARSNG_FINISH_HAS_FAILED_DETAIL: ["parse file finished,success %d flows, failed %d flows",
                                               "完成文件解析，解析成功 %d 条流量, 解析失败 %d 条流量-- 流量内容字段错误"],
        FILE_PARSNG_FAILED: ["parse the file failed", "解析文件失败"],
        FILE_PARSNG_FINISH_SUCCESS: ["parse file finished,success %d flows", "完成文件解析，解析成功 %d 条流量"],
        FILE_PARSNG_FINISH_SUCCESS_CHANGE_DES: [
            "parse file finished,success %d flows include change destination %d flows",
            "完成文件解析，解析成功 %d 条流量,其中有%d条tunnel流根据tunnel路径改变了目的节点"],
    }
