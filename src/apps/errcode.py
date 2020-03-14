# -*- encoding: utf-8 -*-
"""
@File    : errcode.py
@Time    : 2019/05/29 11:09:10
@Author  : 
@License : Copyright (c) 2004-2019 New H3C Tech. Co., Ltd. All rights reserved.
@Desc    : 错误信息定义
"""

from flask import json
from werkzeug.exceptions import HTTPException

class ErrCode:
    """自定义错误码和错误信息。"""

    # 自定义错误码
    # 基本错误码
    SUCCESS = 0
    FAILED = 1000
    INTERNAL_ERROR = 1001
    INVALID_PARAMETER = 1002
    RESOURCE_NOT_FOUND = 1003
    RESOURCE_ALREADY_EXIST = 1004
    OPERATION_IN_PROGRESS = 1005
    NO_OPERATION_IN_PROGRESS = 1006
    FORMAT_ERROR = 1007
    UNAUTHORIZED = 1008
    USER_STOP = 1009

    # 各模块错误
    TOPO_NOT_READY = 1100
    ID_NOT_EXIST = 1101
    TOPO_NOT_EXIST = 1102
    SYNCING = 1103
    NO_SYNCING = 1104
    BGP_ADD_ERROR = 1200
    BGP_DEL_ERROR = 1201
    BGP_PEER_ADD_ERROR = 1202
    BGP_TOPO_ADD_ERROR = 1203
    BGP_TOPO_DEL_ERROR = 1204
    BGP_ROUTE_UNREACH = 1205
    BGP_PORT_MOD_ERROR = 1206
    NO_NODES_IN_TOPO = 1207
    SET_FAULT_WILL_CHANGE_SIMLATE = 1208
    SET_FAULT_NUM_MAX = 1209
    SET_DATA_SYNC_WARNING = 1210
    SIMLATING_CANNOT_SETTING_FAULT = 1211
    ALL_NODES_ARE_FALSE = 1212
    ALL_LINKS_ARE_FALSE = 1213
    SIMLATING_CANNOT_CANCEL_FAULT = 1214

    FLOW_FILE_IS_NOT_EXIST = 2001
    FLOW_FILE_FORMAT_ERROR = 2002
    FLOW_EXCEL_HAS_NO_FLOW = 2003
    FLOW_IS_NOT_ANALYZING = 2004
    FLOW_IS_NOT_EXIST = 2005
    FLOW_NUM_NOT_EQU_LISTNUM = 2006  # post下发的删除流量个数与列表里写的具体的流量个数不等
    FLOW_SEARCH_PARA_FAILED = 2007
    FLOW_SEARCH_NOT_FOUND = 2008
    NO_FLOWS = 2009
    ALL_FLOWS_YOU_WANT_DEL_NOT_EXIST = 2010
    SAVE_FILENAME_ERROR = 2011
    FLOW_IMPORTING = 2012

    NOT_IN_SIMILATING_CAN_NOT_STOP = 3001
    IN_SIMILATING_CAN_NOT_START = 3002
    NOT_SIMILATING_NO_DATA = 3003
    IN_SIMILATING_CAN_NOT_STATIS = 3004
    NO_DATA_CAN_NOT_CALCULATE = 3005
    TIME_NOT_IN_SIMILATING = 3006
    OTHERS_IN_SIMILATING = 3007
    FLOWSIM_BUT_SET_FAULT = 3008

    TUNNEL_INF_FROM_BG = 4001
    TUNNEL_PATH_FROM_BG = 4002
    TUNNEL_FLOW_FROM_BG = 4003
    PARSE_TUNNEL_FROM_BG = 4004

    CAL_DIFFERENT_PATH = 5001
    NO_CONF_MESSAGE = 5002
    # 错误码对应的错误信息
    ERR_MSG = {
        SUCCESS: ["success", "成功"],
        FAILED: ["failed", "失败"],
        INTERNAL_ERROR: ["internal error", "内部错误"],
        INVALID_PARAMETER: ["invalid parameter", "无效参数"],
        RESOURCE_NOT_FOUND: ["resource not found", "未找到资源"],
        RESOURCE_ALREADY_EXIST: ["resource already exist", "资源已经存在"],
        OPERATION_IN_PROGRESS: ["operation in progress", "操作正在执行"],
        NO_OPERATION_IN_PROGRESS: ["no operation in progress", "没有操作在执行"],
        FORMAT_ERROR: ["format_error", "格式错误"],
        UNAUTHORIZED: ["Unauthorized", "认证失败"],
        USER_STOP: ["user stop", "用户强制停止"],

        TOPO_NOT_READY: ["topo not ready, please sync data first!", "TOPO不存在,请先同步数据"],
        ID_NOT_EXIST: ["id not exist", "ID号不存在"],
        TOPO_NOT_EXIST: ["topo not exist", "TOPO不存在"],
        SYNCING: ["syncing", "正在同步"],
        NO_SYNCING: ["no syncing，can't stop", "未在同步，不能停止"],
        BGP_ADD_ERROR: ["add bgp-ls config failed", "添加bgp-ls配置失败"],
        BGP_DEL_ERROR: ["delete bgp-ls config failed", "删除bgp-ls配置失败"],
        BGP_PEER_ADD_ERROR: ["add bgp-ls neighbour config failed", "添加bgp-ls邻居配置失败"],
        BGP_TOPO_ADD_ERROR: ["add bgp-ls network topology config failed", "添加bgp-ls网络拓扑配置失败"],
        BGP_TOPO_DEL_ERROR: ["delete bgp-ls network topology config failed", "删除bgp-ls网络拓扑配置失败"],
        BGP_ROUTE_UNREACH: ["route un reached", "路径不可达"],
        BGP_PORT_MOD_ERROR: ["modify bgp port config failed", "修改BGP端口号失败"],
        NO_NODES_IN_TOPO: ["there is not any netnode in topo", "TOPO上无网元"],
        SET_FAULT_WILL_CHANGE_SIMLATE: ["if you change the fault seting,will change the latest simlated result",
                                        "改变故障设置将把仿真结果清除,确定要继续此操作？"],
        SIMLATING_CANNOT_SETTING_FAULT: ["in simlating, you cannot set fault", "正在仿真中，不能设置故障"],
        SIMLATING_CANNOT_CANCEL_FAULT: ["in simlating, you cannot set fault", "正在仿真中，不能取消故障"],
        ALL_NODES_ARE_FALSE: ["All nodes are faulty, cannot simlate", "所有节点均为故障，不能仿真"],
        ALL_LINKS_ARE_FALSE: ["All links are faulty, cannot simlate", "所有链路均为故障，不能仿真"],

        SET_FAULT_NUM_MAX: ["fault num is max now", "故障设置的数量已达到最大值"],
        SET_DATA_SYNC_WARNING: ['if you sync the data,will change the latest setting and simluated result',
                                '同步数据，会改变之前的流量和故障设置及仿真结果，确定要继续此操作？'],
        FLOW_FILE_IS_NOT_EXIST: ["flow file is not exist!", "流量文件不存在，请先添加文件"],
        FLOW_FILE_FORMAT_ERROR: ["flow file format is not form data!", "上传的流量文件格式错误,请改成form data形式上传"],
        FLOW_EXCEL_HAS_NO_FLOW: ["no flows info in the file!", "流量文件中无流量信息"],
        FLOW_IS_NOT_ANALYZING: ["the file is not analyzing now!", "当前未在分析此文件"],
        FLOW_IS_NOT_EXIST: ["flow is not exist!", "流量不存在"],
        FLOW_NUM_NOT_EQU_LISTNUM: ["the flow num in the list is not equ the num!", "流量统计与列别里的流量个数不相等"],
        FLOW_SEARCH_PARA_FAILED: ["flow search para error!", "流量搜索参数错误"],
        FLOW_SEARCH_NOT_FOUND: ["can not found flow!", "未搜索到相符的流量"],
        NO_FLOWS: ["no flows!", "无流量"],
        ALL_FLOWS_YOU_WANT_DEL_NOT_EXIST: ["all flows you want del is not exist!", "计划删除的流量均不存在"],
        SAVE_FILENAME_ERROR: ["save_filename_error", "保存文件名错误"],
        FLOW_IMPORTING: ["Other users are importing, please try again later", "其他用户正在进行导入操作，请稍后再试"],

        NOT_IN_SIMILATING_CAN_NOT_STOP: ["not in similating,can not stop similate", "未在仿真过程中，不能按停止仿真按钮"],
        IN_SIMILATING_CAN_NOT_START: ["in similating,can not start similate", "正在执行仿真，不能按开始仿真按钮"],
        NOT_SIMILATING_NO_DATA: ["not similating,no data", "未仿真，没有数据"],
        IN_SIMILATING_CAN_NOT_STATIS: ["in similating, can not statis", "正在仿真中，不能统计"],
        NO_DATA_CAN_NOT_CALCULATE: ["no data can not calculate", "没有数据，不能计算"],
        TIME_NOT_IN_SIMILATING: ["time not in similating", "选取时间不在仿真时间范围内"],
        OTHERS_IN_SIMILATING: ["other people in simulating", "其他人正在仿真，不能进行仿真"],
        FLOWSIM_BUT_SET_FAULT: ["do flow simulate,can not set fault", "进行流量仿真时，在仿真定义界面不可以设置故障"],

        TUNNEL_INF_FROM_BG: ["get tunnel information from bigdate failed", "从大数据获取隧道信息失败"],
        TUNNEL_PATH_FROM_BG: ["get tunnel path from bigdate failed", "从大数据获取隧道信息失败"],
        TUNNEL_FLOW_FROM_BG: ["get tunnel flow from bigdate failed", "从大数据获取隧道信息失败"],
        PARSE_TUNNEL_FROM_BG: ["parse tunnel from bigdata failed", "解析大数据的隧道信息失败"],
        CAL_DIFFERENT_PATH: ["get different path", "得到不同的隧道路径"],
        NO_CONF_MESSAGE: ["no configure message", "没有配置信息"]

    }

class APIException(HTTPException):
    """重写异常，返回json格式。"""

    code = 500
    error_code = ErrCode.INTERNAL_ERROR
    error_msg = ErrCode.ERR_MSG[ErrCode.INTERNAL_ERROR]

    def __init__(self, error_code=None, code=None):
        if error_code:
            self.error_code = error_code
        if code:
            self.code = code
        super(APIException, self).__init__(self.error_msg, None)

    # 根据restful的特性，需要不论输入还是输出都需要是json格式，所以我们这里重写get_body方法，将返回值定义为json格式
    def get_body(self, environ):
        resp = dict(
            code=self.error_code,
            msg=self.error_msg
        )
        return json.dumps(resp)

    # 重写get_header方法，告诉浏览器返回的是json格式，按照json格式解析
    def get_header(self, environ):
        return [("content-type", "application/json")]
