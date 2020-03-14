# -*- encoding: utf-8 -*-
"""
@File    : api.py
@Time    : 2019/05/29 11:30:11
@Author  : 
@License : Copyright (c) 2004-2019 New H3C Tech. Co., Ltd. All rights reserved.
@Desc    : restful api接口提供模块
"""

import threading

from flask import request, json
from flask import make_response
from flask_restful import Resource

from apps.util import *
from apps.errcode import ErrCode

from apps.v1_0.topo import get_topo, save_topo, save_display_config, get_display_config
from apps.v1_0.datasync import sync_data, stop_sync_data, get_sync_status
from apps.v1_0.flow import *
from apps.v1_0.language import get_err_lang_str, get_sync_lang_str, set_lange
from apps.v1_0.fault import set_fault, get_fault_list, clear_fault, judge_fault
from apps.v1_0.bgpls import config_bgpls, get_bgpls_config
from apps.v1_0.record import *
from apps.v1_0.simulate import *
from apps.v1_0.analyse import *


def error_response(error_code, status_code):
    """操作失败, response信息返回。
    
    Args:
        error_code: 自定义的错误码
        status_code: 返回的http状态码
    Returns:
        返回response信息和状态码
    Raise:
        none
    """

    response = make_response()
    response.headers.set('Content-Type', 'application/json')

    response = {
        "status": "fail",
        "errorCode": error_code,
        "errorInfo": get_err_lang_str(error_code)}
    # print(response)
    return response, status_code


def success_response():
    """操作成功, response信息返回。
    
    Args:
        none
    Returns:
        返回response信息和状态码
    Raise:
        none
    """

    response = make_response()
    response.headers.set('Content-Type', 'application/json')

    response = {
        "status": "success",
        "errorCode": ErrCode.SUCCESS,
        "errorInfo": get_err_lang_str(ErrCode.SUCCESS)}
    # print(response)
    return response, 200


def data_response(data):
    """返回response,携带data信息
    
    Args:
        language_index,为避免前后不一致,在数据拼装的时候,就查询中英文设置,透传下来
    Returns:
        返回response信息和状态码
    Raise:
        none
    """

    response = make_response()
    response.headers.set('Content-Type', 'application/json')

    response = {
        "data": data,
        "status": "success",
        "errorCode": ErrCode.SUCCESS,
        "errorInfo": get_err_lang_str(ErrCode.SUCCESS)}
    # print(response)
    return response, 200


def err_data_response(error_code, status_code, data):
    """返回err response,携带data信息
    
    Args:
        language_index,为避免前后不一致,在数据拼装的时候,就查询中英文设置,透传下来
    Returns:
        返回response信息和状态码
    Raise:
        none
    """

    response = make_response()
    response.headers.set('Content-Type', 'application/json')

    response = {
        "data": data,
        "status": "fail",
        "errorCode": error_code,
        "errorInfo": get_err_lang_str(error_code)}
    # print(response)
    return response, status_code


class GetTopoApi(Resource):
    """获取topo资源信息。
    
    Attributes:
        none
    """

    def get(self):
        """获取topo信息,?layer=value"""

        # print(request.args)
        type = request.args.get("layer")
        if None == type:
            info_logger.warning('missing parameter(layer)')
            return error_response(ErrCode.INVALID_PARAMETER, 200)

        if type != 'physical' and type != 'layer3':
            info_logger.warning('invalid parameter(layer)')
            return error_response(ErrCode.INVALID_PARAMETER, 200)

        ret, data = get_topo(type)
        if ret != ErrCode.SUCCESS:
            info_logger.warning('get_topo failed')
            return error_response(ret, 200)

        return data_response(data)


class GetReport(Resource):
    """获取报表
    
    Attributes:
        none
    """

    def get(self):
        """获取报表"""
        curTime = request.args.get("curTime")
        get_type = request.args.get("type")

        if g_sim.status != 1:
            return error_response(ErrCode.NOT_SIMILATING_NO_DATA, 200)

        if None == curTime or None == get_type:
            info_logger.warning('missing parameter')
            return error_response(ErrCode.INVALID_PARAMETER, 200)

        if get_type != 'all' and get_type != 'current':
            return error_response(ErrCode.INVALID_PARAMETER, 200)

        if judge_curtime_in_simlate_time(curTime) != 0 and get_type == 'all':
            data = get_simlate_start_end_time()
            return err_data_response(ErrCode.TIME_NOT_IN_SIMILATING, 200, data)

        data = report_analyse_data(curTime, get_type)
        return data_response(data)


class SaveTopoApi(Resource):
    """保存topo资源信息
    
    Attributes:
        none
    """

    def post(self):
        """保存topo信息"""

        if request.is_json:
            # 数据参数检查
            data = request.json
            if "nodeNum" not in data or "nodes" not in data:
                return error_response(ErrCode.INVALID_PARAMETER, 200)
            if not isinstance(data["nodeNum"], int) or not isinstance(data["nodes"], list):
                return error_response(ErrCode.INVALID_PARAMETER, 200)
            if data["nodeNum"] != len(data["nodes"]):
                return error_response(ErrCode.INVALID_PARAMETER, 200)
            if len(data["nodes"]) == 0:
                return error_response(ErrCode.INVALID_PARAMETER, 200)

            for node in data["nodes"]:
                if not isinstance(node, dict):
                    return error_response(ErrCode.INVALID_PARAMETER, 200)
                if "assetId" not in node or "locationX" not in node or "locationY" not in node:
                    return error_response(ErrCode.INVALID_PARAMETER, 200)
                if not (isinstance(node["locationX"], int) or isinstance(node["locationX"], float)):
                    return error_response(ErrCode.INVALID_PARAMETER, 200)
                if not (isinstance(node["locationY"], int) or isinstance(node["locationY"], float)):
                    return error_response(ErrCode.INVALID_PARAMETER, 200)

            ret = save_topo(data)
            if ret != ErrCode.SUCCESS:
                info_logger.warning('save_topo failed')
                return error_response(ret, 200)
        else:
            info_logger.warning('invalid parameter')
            return error_response(ErrCode.INVALID_PARAMETER, 200)

        return success_response()


class StartDataSyncAPI(Resource):
    """开始数据同步
    
    Attributes:
        none
    """

    def post(self):
        """开始数据同步"""

        try:
            # 若正在同步,返回失败
            if g_dt.data_sync_status == SyncStatusCode.SYNC_SYNCING:
                return error_response(ErrCode.OPERATION_IN_PROGRESS, 200)
            data = request.json
            # 参数检查 
            if 'time' not in data or 'trytimes' not in data:
                return error_response(ErrCode.INVALID_PARAMETER, 200)

            data_time = data['time']
            trytimes = data['trytimes']

            if trytimes == 1:
                return error_response(ErrCode.SET_DATA_SYNC_WARNING, 200)
            else:
                g_dt.data_sync_status = SyncStatusCode.SYNC_SYNCING
                if g_sim.status == 1 or g_sim.status == 3:  # 仿真完成或正在仿真时进行数据同步，则仿真临时中止
                    SIMLATAE_STATE_LOCK.acquire()
                    g_sim.status = 2
                    g_sim.stop_simulate_flag = 1  # 停止仿真
                    SIMLATAE_STATE_LOCK.release()

            # 创建线程进行数据同步
            data_sync_thd = threading.Thread(target=sync_data, args=(data_time,))
            data_sync_thd.start()
            return success_response()

        except Exception as e:
            print("StartDataSyncAPI Exception:", e)
            return ErrCode.FAILED


class StopDataSyncAPI(Resource):
    """停止数据同步
    
    Attributes:
        none
    """

    def post(self):
        """停止数据同步"""

        ret = stop_sync_data()
        if ret != ErrCode.SUCCESS:
            info_logger.warning('stop_sync_data failed')
            return error_response(ret, 200)

        return success_response()


class GetDataSyncStatus(Resource):
    """获取数据同步状态
    
    Attributes:
        none
    """

    def get(self):
        """获取数据同步状态"""

        ret, data = get_sync_status()
        if ret != ErrCode.SUCCESS:
            info_logger.warning('get_sync_status failed')
            return error_response(ret, 200)

        return data_response(data)


class GetDataSyncLogApi(Resource):
    """获取数据同步详情
    
    Attributes:
        none
    """

    def get(self):
        """获取同步详情"""

        type = request.args.get("type")
        if None == type:
            info_logger.warning('missing parameter(type)')
            return error_response(ErrCode.INVALID_PARAMETER, 200)

        if type != 'topo' and type != 'config' and type != 'control':
            info_logger.warning('invalid parameter(type)')
            return error_response(ErrCode.INVALID_PARAMETER, 200)

        if type == "topo":
            data = {
                "time": g_dt.topo_sync_detail["time"],
                "status": g_dt.topo_sync_detail["status"],
                "reason": get_sync_lang_str(g_dt.topo_sync_detail["reason"])}
        elif type == "config":
            data = {
                "time": g_dt.conf_sync_detail["time"],
                "status": g_dt.conf_sync_detail["status"],
                "reason": get_sync_lang_str(g_dt.conf_sync_detail["reason"])}
        else:
            data = {
                "time": g_dt.link_control_sync_detail["time"],
                "status": g_dt.link_control_sync_detail["status"],
                "reason": get_sync_lang_str(g_dt.link_control_sync_detail["reason"])}

        return data_response(data)


class ConfigBgplsApi(Resource):
    """使能去使能bgpls
    
    Attributes:
        {
            "enable":0 or 1,
            "asNumber":300,
            "localIp":"192.60.60.3",
            "peerIp":"192.60.60.2"
        }
    """

    def post(self):
        if request.is_json:
            data_input = request.json
            data = data_input['data']
            # 参数检查 
            # print('data=',data)
            if "enable" not in data or "asNumber" not in data or "localIp" not in data or "peerIp" not in data:
                return error_response(ErrCode.INVALID_PARAMETER, 200)
            if not isinstance(data["asNumber"], int) or not isinstance(data["localIp"], str) or not isinstance(
                    data["peerIp"], str):
                return error_response(ErrCode.INVALID_PARAMETER, 200)
            if not data["enable"] in (0, 1):
                return error_response(ErrCode.INVALID_PARAMETER, 200)
            if not is_ipv4_str(data["localIp"]) or not is_ipv4_str(data["peerIp"]):
                return error_response(ErrCode.INVALID_PARAMETER, 200)

            # bgpls配置
            ret = config_bgpls(data)
            if ret != ErrCode.SUCCESS:
                info_logger.warning('config_bgpls failed')
                return error_response(ret, 200)
        else:
            info_logger.warning('invalid parameter')
            return error_response(ErrCode.INVALID_PARAMETER, 200)

        return success_response()


class GetBgplsConfigApi(Resource):
    """获取BGP LS的配置
    
    Attributes:
        none
    """

    def get(self):
        ret, data = get_bgpls_config()
        if ret != ErrCode.SUCCESS:
            info_logger.warning('get_bgpls_config failed')
            return error_response(ret, 200)

        return data_response(data)


class TopoDisplaySettingApi(Resource):
    """设置topo显示的配置
    
    Attributes:
        none
    """

    def post(self):
        """设置显示参数"""

        if request.is_json:
            # 参数检查
            data = request.json

            if "display" not in data or "autoSaveTopo" not in data or "autoSaveTime" not in data:
                return error_response(ErrCode.INVALID_PARAMETER, 200)
            if not isinstance(data["autoSaveTime"], int) or not isinstance(data["display"], dict):
                return error_response(ErrCode.INVALID_PARAMETER, 200)
            if not data["autoSaveTopo"] in ("on", "off"):
                return error_response(ErrCode.INVALID_PARAMETER, 200)
            if "disName" not in data["display"] or "nameType" not in data["display"] or "disTip" not in data[
                "display"] or "disInterface" not in data["display"]:
                return error_response(ErrCode.INVALID_PARAMETER, 200)
            if not data["display"]["disName"] in ("on", "off") or not data["display"]["disTip"] in ("on", "off") or not \
            data["display"]["disInterface"] in ("on", "off"):
                return error_response(ErrCode.INVALID_PARAMETER, 200)
            if not data["display"]["nameType"] in ("name", "ip"):
                return error_response(ErrCode.INVALID_PARAMETER, 200)

            ret = save_display_config(data)
            if ret != ErrCode.SUCCESS:
                info_logger.warning('save_display_config failed')
                return error_response(ret, 200)
        else:
            info_logger.warning('invalid parameter')
            return error_response(ErrCode.INVALID_PARAMETER, 200)

        return success_response()


class GetTopoDisplaySettingApi(Resource):
    """设置topo显示的配置
    
    Attributes:
        none
    """

    def get(self):
        """设置显示参数"""

        ret, data = get_display_config()
        if ret != ErrCode.SUCCESS:
            info_logger.warning('get_display_config failed')
            return error_response(ret, 200)

        return data_response(data)


"""
@funName    : SaveFlowModleApi
@function   : 获得流量模板
@Author     : leijuyan 11389
@注意事项    : 无.
"""


class SaveFlowModleApi(Resource):
    """保存流量模板文件
    
    Attributes:
        none
    """

    def get(self):
        """保存流量模板"""
        return data_response("/digitalTwins/static/flow/Flow.xlsx")


"""
@funName    : ShowImportFlowProApi
@function   : 流量的左树显示
@Author     : leijuyan 11389
@注意事项    : 无.
"""


class ShowImportFlowProApi(Resource):
    """显示导入流量进度信息"""

    def get(self):
        # print(request.args)
        flow_file_name = request.args.get("flowFile")
        if None == flow_file_name:
            info_logger.warning('missing parameter(flowFile)')
            return error_response(ErrCode.INVALID_PARAMETER, 200)

        ret, data = get_flow_import_progress(flow_file_name)
        if ret != ErrCode.SUCCESS:
            return error_response(ret, 200)

        return data_response(data)


"""
@funName    : ImportFlowApi
@function   : 导入流量
@Author     : leijuyan 11389
@注意事项    : 无.
"""


class ImportFlowApi(Resource):
    """导入流量
    
    Attributes:
        none
    """

    def post(self):
        """导入流量"""

        ret = import_flow_file()
        if ret != ErrCode.SUCCESS:
            # log_warning('import flow file failed')
            return error_response(ret, 200)
        else:
            return success_response()


"""
@funName    : GetFlowInfoApi
@function   : 通过流量ID获取流量信息
@Author     : leijuyan 11389
@注意事项    : 无.
"""


class GetFlowInfoApi(Resource):
    """获取流量信息,?flowId =value"""

    def get(self):
        # print(request.args)
        flow_id = request.args.get("flowId")
        if None == flow_id:
            info_logger.warning('missing parameter(layer)')
            return error_response(ErrCode.INVALID_PARAMETER, 200)

        ret, data = get_flow_Info_by_flowid(flow_id)
        if ret != ErrCode.SUCCESS:
            # log_warning('get_flow info failed')
            return error_response(ret, 200)

        return data_response(data)


"""
@funName    : GetLoadedFlowListApi
@function   : 流量列表
@Author     : leijuyan 11389
@注意事项    : 无.
"""


class GetLoadedFlowListApi(Resource):
    """获得流量列表文件
    
    Attributes:
        none
    """

    def get(self):
        ret, data = get_all_loaded_flow()
        if ret != ErrCode.SUCCESS:
            return error_response(ret, 200)

        return data_response(data)


"""
@funName    : DelFlowApi
@function   : 删除一条或多条流量
@Author     : leijuyan 11389
@注意事项    : 无.
"""


class DelFlowApi(Resource):
    def post(self):
        response = make_response()
        response.headers.set('Content-Type', 'application/json')
        if len(request.data) > 0:
            if request.is_json:
                del_info = request.json
                del_num = del_info.get("delNum")
                del_detail = del_info.get("delFlowInfo")
            else:
                return error_response(ErrCode.FORMAT_ERROR, 200)

        if isinstance(del_detail, list):
            if del_num != len(del_detail):
                return error_response(ErrCode.INVALID_PARAMETER, 200)
        else:
            return error_response(ErrCode.INVALID_PARAMETER, 200)

        ret, data = del_flow(del_num, del_detail)

        if ret != ErrCode.SUCCESS:
            return error_response(ret, 200)
        else:
            return data_response(data)


class SearchFlowListApi(Resource):
    def get(self):
        search_type = request.args.get("type")
        search_key = request.args.get("key")
        search_info = request.args.get("info")

        if None == search_type or None == search_info or None == search_key:
            info_logger.warning('missing parameter')
            return error_response(ErrCode.INVALID_PARAMETER, 200)
        search_type_deal = search_type.strip()

        if search_type_deal == 'flow':
            if search_info is '':
                ret, data = get_all_loaded_flow()
                if ret != ErrCode.SUCCESS:
                    return error_response(ret, 200)
                else:
                    return data_response(data)

            search_key_deal = search_key.strip()
            search_info_deal = search_info.strip()
            ret, data = search_flow_Info_at_gallflow(search_key_deal, search_info_deal)
        else:
            ret = ErrCode.FAILED

        if ret != ErrCode.SUCCESS:
            # log_warning('get_flow info failed')
            return error_response(ret, 200)

        return data_response(data)


class SetLanguageApi(Resource):
    def post(self):
        """设置显示中英文参数"""

        language = request.args.get("i18n")
        if None == language:
            info_logger.warning('missing parameter(type)')
            return error_response(ErrCode.INVALID_PARAMETER, 200)

        if language != 'EN' and language != 'CHS':
            info_logger.warning('invalid parameter(type)')
            return error_response(ErrCode.INVALID_PARAMETER, 200)

        _, data = set_lange(language)
        return data_response(data)


class SetFaultApi(Resource):
    def post(self):
        if request.is_json:
            # 数据参数检查
            data = request.json
            # print('data=', data)

            # 若正在同步,返回失败
            if g_dt.data_sync_status == 1:
                return error_response(ErrCode.OPERATION_IN_PROGRESS, 200)

            # 判断参数是否存在
            if "type" not in data or "id" not in data or "fault" not in data:
                return error_response(ErrCode.INVALID_PARAMETER, 200)

            # 判断type 、 fault的参数是否正确
            if data["type"] != "node" and data["type"] != "link":
                return error_response(ErrCode.INVALID_PARAMETER, 200)
            if data["fault"] != "yes" and data["fault"] != "no":
                return error_response(ErrCode.INVALID_PARAMETER, 200)

            #  判断有否有topo已经同步
            if g_dt.phy_topo == None:
                return error_response(ErrCode.TOPO_NOT_READY, 200)

            # print("g_dt.phy_topo.nodes = ", g_dt.phy_topo.nodes)
            id = data['id']

            # 判断node id是否存在
            if data["type"] == "node":
                if id not in g_dt.phy_topo.nodes:
                    return error_response(ErrCode.ID_NOT_EXIST, 200)

            # 判断link id是否存在
            if data["type"] == "link":
                if id not in g_dt.phy_topo.links:
                    return error_response(ErrCode.ID_NOT_EXIST, 200)

            if "trytimes" in data:
                trytimes = data["trytimes"]
                if trytimes == 1:
                    # sprint3 mark
                    # if g_sim.status == 1:
                    #    return error_response(ErrCode.SET_FAULT_WILL_CHANGE_SIMLATE, 200)
                    if g_sim.status == 3:
                        # sprint3 增加一个分支，用于修改大数据提的第8点问题
                        if data["fault"] == "yes":
                            return error_response(ErrCode.SIMLATING_CANNOT_SETTING_FAULT, 200)
                        else:
                            return error_response(ErrCode.SIMLATING_CANNOT_CANCEL_FAULT, 200)
                else:
                    if g_sim.status == 1:
                        SIMLATAE_STATE_LOCK.acquire()
                        g_sim.status = 2
                        g_sim.stop_simulate_flag = 1
                        SIMLATAE_STATE_LOCK.release()
                    elif g_sim.status == 3:
                        # sprint3 增加一个分支，用于修改大数据提的第8点问题
                        if data["fault"] == "yes":
                            return error_response(ErrCode.SIMLATING_CANNOT_SETTING_FAULT, 200)
                        else:
                            return error_response(ErrCode.SIMLATING_CANNOT_CANCEL_FAULT, 200)

            # 能设置故障数量的最大值 
            max_fault = 5
            if data["fault"] == "yes" and g_dt.phy_topo.fault_num > max_fault - 1:
                return error_response(ErrCode.SET_FAULT_NUM_MAX, 200)

            ret = set_fault(data)
            if ret != ErrCode.SUCCESS:
                info_logger.warning('set_fault failed')
                return error_response(ret, 200)

        else:
            info_logger.warning('invalid parameter')
            return error_response(ErrCode.INVALID_PARAMETER, 200)

        return success_response()


class GetAllFaultApi(Resource):
    def get(self):

        #  判断有否有topo已经同步
        if g_dt.phy_topo == None:
            return error_response(ErrCode.TOPO_NOT_READY, 200)
        # 若
        if len(g_dt.phy_topo.nodes) > 0 or len(g_dt.phy_topo.links) > 0:
            ret, data = get_fault_list()
            if ret == ErrCode.SUCCESS:
                return data_response(data)
        else:
            return success_response()

        return data_response(data)


class ClearAllSelFaultApi(Resource):
    def post(self):
        data = request.json['data']
        # print('data=', data)

        # 参数检查

        if g_dt.data_sync_status == 1:
            return error_response(ErrCode.OPERATION_IN_PROGRESS, 200)

        if "nodeNum" not in data or "linkNum" not in data:
            return error_response(ErrCode.INVALID_PARAMETER, 200)
        if "faultNode" not in data or "faultLink" not in data:
            return error_response(ErrCode.INVALID_PARAMETER, 200)

        if not isinstance(data["faultNode"], list):
            return error_response(ErrCode.INVALID_PARAMETER, 200)
        if not isinstance(data["faultLink"], list):
            return error_response(ErrCode.INVALID_PARAMETER, 200)

        # 判断id字段是否存在
        if len(data["faultNode"]) > 0:
            if "assetId" not in data['faultNode'][0]:
                return error_response(ErrCode.INVALID_PARAMETER, 200)
        if len(data["faultLink"]) > 0:
            if "linkId" not in data['faultLink'][0]:
                return error_response(ErrCode.INVALID_PARAMETER, 200)

        # 判断有否有topo已经同步
        if g_dt.phy_topo == None:
            return error_response(ErrCode.TOPO_NOT_READY, 200)

        # num == id num 判断参数个数是否一致
        if data['nodeNum'] != len(data['faultNode']) or data['linkNum'] != len(data['faultLink']):
            return error_response(ErrCode.INVALID_PARAMETER, 200)
        # 若数量都为0 ,则直接返回正确
        if data['nodeNum'] == 0 and data['linkNum'] == 0:
            return success_response()

        # 判断node id是否存在
        for i in range(data['nodeNum']):
            noteId = data['faultNode'][i]['assetId']
            if noteId not in g_dt.phy_topo.nodes:
                return error_response(ErrCode.INVALID_PARAMETER, 200)

        # 判断link id是否存在
        for i in range(data['linkNum']):
            linkId = data['faultLink'][i]['linkId']
            if linkId not in g_dt.phy_topo.links:
                return error_response(ErrCode.INVALID_PARAMETER, 200)

        # 开始清除错误
        ret = clear_fault(data)
        if ret == ErrCode.SUCCESS:
            return success_response()
        else:
            error_response(ErrCode.FAILED, 200)


class SetSimApi(Resource):
    """启动或停止仿真
    
    Attributes:
        none
    """

    def post(self):
        order = request.args.get("operate")
        if None == order:
            info_logger.warning('missing parameter(type)')
            return error_response(ErrCode.INVALID_PARAMETER, 200)

        if order != 'start' and order != 'stop':
            info_logger.warning('invalid parameter(type)')
            return error_response(ErrCode.INVALID_PARAMETER, 200)

        # 如果传参"start"则开始仿真，如果传参"stop"则停止仿真
        if order == 'start':
            data = request.json.get('data')

            if "trytimes" in data:
                trytimes = data["trytimes"]
                if trytimes == 1 and g_sim.inherit_flag == False:
                    if g_sim.status == 1:
                        return error_response(ErrCode.SET_FAULT_WILL_CHANGE_SIMLATE, 200)

            # 正在仿真的时候，不响应开始仿真的命令
            if g_sim.status >= 3:
                return error_response(ErrCode.IN_SIMILATING_CAN_NOT_START, 200)

            if "simType" not in data or "simObj" not in data or "dataManner" not in data or "agreement" not in data or "simTime" not in data:
                return error_response(ErrCode.INVALID_PARAMETER, 200)

            # 未设置任何一个仿真类型,直接返回失败
            simu_type_dict = data['simType']
            if simu_type_dict['routeSim'] != 1 and simu_type_dict['flowSim'] != 1 and simu_type_dict['faultSim'] != 1:
                return error_response(ErrCode.INVALID_PARAMETER, 200)

            if simu_type_dict['flowSim'] == 1:
                if judge_fault():
                    return error_response(ErrCode.FLOWSIM_BUT_SET_FAULT, 200)

            # 未设置任何一个仿真对象,直接返回失败
            simu_obj_dict = data['simObj']
            if simu_obj_dict['load'] != 1 and simu_obj_dict['tunnelFlow'] != 1 and simu_obj_dict['inputFlow'] != 1:
                return error_response(ErrCode.INVALID_PARAMETER, 200)

            # 未设置任何一个数据管理方式,直接返回失败
            data_manner_dict = data['dataManner']
            if data_manner_dict['everager'] != 1 and data_manner_dict['peak'] != 1 and data_manner_dict[
                'ninetyFivePeak'] != 1:
                return error_response(ErrCode.INVALID_PARAMETER, 200)

            # 未设置任何一个仿真协议,直接返回失败
            agree_dict = data['agreement']
            if agree_dict['bgp'] != 1 and agree_dict['isis'] != 1 and agree_dict['ospf'] != 1 and agree_dict[
                'mpls'] != 1:
                return error_response(ErrCode.INVALID_PARAMETER, 200)
            # 隧道优化参数判断    
            if agree_dict['tunnelOptimize'] != 1 and agree_dict['tunnelOptimize'] != 0:
                return error_response(ErrCode.INVALID_PARAMETER, 200)

            # 仿真设置的时间，开始时间晚于结束时间，直接返回失败    
            if data['simTime']['timeBegin'] >= data['simTime']['timeEnd']:
                return error_response(ErrCode.INVALID_PARAMETER, 200)

                # 仿真周期为0，直接返回参数错误
            if data['simTime']['cycleNum'] == 0 or data['simTime']['duration'] == 0:
                return error_response(ErrCode.INVALID_PARAMETER, 200)

                # 没有topo数据，不能仿真
            if not g_dt.phy_topo or not g_dt.l3_topo:
                return error_response(ErrCode.TOPO_NOT_READY, 200)

            if not g_dt.l3_topo.nodes or not g_dt.l3_topo.links:
                return error_response(ErrCode.TOPO_NOT_READY, 200)

            if not g_dt.phy_topo.nodes or not g_dt.phy_topo.links:
                return error_response(ErrCode.TOPO_NOT_READY, 200)

            if judge_all_nodes_is_fault():
                return error_response(ErrCode.ALL_NODES_ARE_FALSE, 200)

            if judge_all_links_is_fault():
                return error_response(ErrCode.ALL_LINKS_ARE_FALSE, 200)

            ret = start_simulate(data)
            if ret != ErrCode.SUCCESS:
                info_logger.warning('set_simulate failed')
                return error_response(ret, 200)
        else:
            ret = stop_simulate()
            if ret != ErrCode.SUCCESS:
                info_logger.warning('stop_simulate failed')
                return error_response(ret, 200)

        return success_response()


class GetSimProgressApi(Resource):
    """获得仿真进度
    
    Attributes:
        none
    """

    def get(self):
        data = get_simulate_progress()
        return data_response(data)


class GetSimStepStatiscApi(Resource):
    """获得仿真完成后的统计信息
    Attributes:
        none
    """

    def get(self):
        # g_sim.status = 1
        if g_sim.status == 3:
            return error_response(ErrCode.IN_SIMILATING_CAN_NOT_STATIS, 200)

        elif g_sim.status == 0:
            return error_response(ErrCode.NOT_SIMILATING_NO_DATA, 200)

        elif g_sim.status == 1:
            ret, data = get_simulate_statisc_Info()

        else:
            return error_response(ErrCode.FAILED, 200)

        if ret != ErrCode.SUCCESS:
            return error_response(ret, 200)

        return data_response(data)


class GetSimParaApi(Resource):
    def get(self):
        try:
            data = get_sim_para()
            return data_response(data)
        except Exception as e:
            print("GetSimParaApi Exception:", e)
            data = {
                'simStartTime': 0,
                'simEndTime': 0,
                'state': 0
            }
            return data_response(data)


# 5.1.2	获得某个时间的故障前后的topo图
class GetAnalysTopoInfoApi(Resource):
    def get(self):
        # 若未仿真完成，则返回错误码
        if g_sim.status != 1:
            return error_response(ErrCode.NOT_SIMILATING_NO_DATA, 200)

        ret, data = get_analys_topo()
        if ret != ErrCode.SUCCESS:
            info_logger.warning('get_analys_topo failed')
            return error_response(ret, 200)

        return data_response(data)


# 5.1.3	下拉框统计信息的界面
class SummaryApi(Resource):
    def get(self):

        # 若未仿真完成，则返回错误码
        if g_sim.status != 1:
            return error_response(ErrCode.NOT_SIMILATING_NO_DATA, 200)

        cur_time = request.args.get("curTime")
        if None == cur_time:
            info_logger.warning('missing parameter')
            return error_response(ErrCode.INVALID_PARAMETER, 200)

        if judge_curtime_in_simlate_time(cur_time) != 0:
            data = get_simlate_start_end_time()
            return err_data_response(ErrCode.TIME_NOT_IN_SIMILATING, 200, data)

        ret, data = get_summary_info(cur_time)
        if ret != ErrCode.SUCCESS:
            info_logger.warning('get_summary_info failed')
            return error_response(ret, 200)

        return data_response(data)

# 5.1.4	FLOWS信息及FLOWS的ShowPath信息
class GetAnalysFlowsInfoApi(Resource):
    def get(self):
        cur_time = request.args.get("curTime")
        flow_type = request.args.get("type")

        # 若未仿真完成，则返回错误码
        if g_sim.status != 1:
            return error_response(ErrCode.NOT_SIMILATING_NO_DATA, 200)

        if None == cur_time or None == flow_type:
            info_logger.warning('missing parameter')
            return error_response(ErrCode.INVALID_PARAMETER, 200)

        if flow_type != 'all' and flow_type != 'unchange' and flow_type != 'change' and flow_type != 'interrupt':
            info_logger.warning('invalid parameter')
            return error_response(ErrCode.INVALID_PARAMETER, 200)

        if judge_curtime_in_simlate_time(cur_time) != 0:
            data = get_simlate_start_end_time()
            return err_data_response(ErrCode.TIME_NOT_IN_SIMILATING, 200, data)

        ret, data = get_flows_and_path_info(cur_time, flow_type)
        if ret != ErrCode.SUCCESS:
            info_logger.warning('get_flows_and_path_info failed')
            return error_response(ret, 200)

        return data_response(data)


# 5.1.6	负载信息
class LoadApi(Resource):
    def get(self):
        try:
            # 参数检查
            load_type = request.args.get("type")

            # 若未仿真完成，则返回错误码
            if g_sim.status != 1:
                return error_response(ErrCode.NOT_SIMILATING_NO_DATA, 200)

            # time = request.args.get("time")
            # thirdstepend = request.args.get("thirdstepend")
            if load_type == None:
                info_logger.warning('missing parameter')
                return error_response(ErrCode.INVALID_PARAMETER, 200)

            if load_type != 'overload' and load_type != 'other' and load_type != 'all':
                return error_response(ErrCode.INVALID_PARAMETER, 200)

            if not g_sim.statis_load:
                info = {'overloadData': 0, 'overloadNum': 0, 'changeloadData': 0, 'changeloadNum': 0}
                return data_response(info)

            # 获取load的信息      
            if load_type == 'overload':
                data_info = {'overloadData': g_sim.statis_load.overload_data,
                             'overloadNum': g_sim.statis_load.overload_num}
            elif load_type == 'other':
                # other 的部分，10.26协商不显示，包含Flow、load和tunnel
                data_info = {'changeloadData': '', 'changeloadNum': 0}
            else:
                # other 的部分，10.26协商不显示，包含Flow、load和tunnel
                data_info = {'overloadData': g_sim.statis_load.overload_data,
                             'overloadNum': g_sim.statis_load.overload_num, \
                             'changeloadData': [], 'changeloadNum': 0}

            return data_response(data_info)

        except Exception as e:
            print("LoadApi Exception:", e)
            info_logger.error(e)
            error_logger.error(e)
            return error_response(ErrCode.FAILED, 200)

        # 5.1.7	故障定义


class FaultDefinitionApi(Resource):
    def get(self):
        # 若未仿真完成，则返回错误码
        if g_sim.status != 1:
            return error_response(ErrCode.NOT_SIMILATING_NO_DATA, 200)

        # 获取fault的信息
        data = get_fault_def()

        return data_response(data)


# 5.2.1	查看某条选择路径承载的flow
class GetSelectLoadFlowApi(Resource):
    def get(self):
        # get_fault_load
        cur_time = request.args.get("curTime")
        linkId = request.args.get("linkId")
        anlyseStep = request.args.get("anlyseStep")
        # print(time,linkId,anlyseStep)

        # 若未仿真完成，则返回错误码
        if g_sim.status != 1:
            return error_response(ErrCode.NOT_SIMILATING_NO_DATA, 200)

        if None == cur_time or None == linkId or None == anlyseStep:
            info_logger.warning('missing parameter')
            return error_response(ErrCode.INVALID_PARAMETER, 200)

        if anlyseStep != 'before' and anlyseStep != 'after':
            info_logger.warning('invalid parameter(anlyseStep)')
            return error_response(ErrCode.INVALID_PARAMETER, 200)

        if judge_curtime_in_simlate_time(cur_time) != 0:
            data = get_simlate_start_end_time()
            return err_data_response(ErrCode.TIME_NOT_IN_SIMILATING, 200, data)

        ret, data = get_select_flow_load(anlyseStep, cur_time, linkId)

        if ret != ErrCode.SUCCESS:
            info_logger.warning('get_fault_load failed')
            return error_response(ret, 200)

        # print('data = ', data)
        return data_response(data)


# 5.2.4	获取故障前后某个时刻的流量列表
class GeFlowListInfoApi(Resource):
    def get(self):
        # 参数检查 判断故障仿真是否已完成
        cur_time = request.args.get("curTime")
        anlyseStep = request.args.get("anlyseStep")

        # 若未仿真完成，则返回错误码
        if g_sim.status != 1:
            return error_response(ErrCode.NOT_SIMILATING_NO_DATA, 200)

        if None == cur_time or None == anlyseStep:
            info_logger.warning('missing parameter')
            return error_response(ErrCode.INVALID_PARAMETER, 200)
        if anlyseStep != 'before' and anlyseStep != 'after':
            info_logger.warning('invalid parameter(anlyseStep)')
            return error_response(ErrCode.INVALID_PARAMETER, 200)

        if judge_curtime_in_simlate_time(cur_time) != 0:
            data = get_simlate_start_end_time()
            return err_data_response(ErrCode.TIME_NOT_IN_SIMILATING, 200, data)

        ret, data = get_flow_list(anlyseStep, cur_time)

        if ret != ErrCode.SUCCESS:
            info_logger.warning('get_fault_load failed')
            return error_response(ret, 200)

        # print('data = ', data)
        return data_response(data)


# 5.2.5	流量搜索
class SearchAnalysisFlowApi(Resource):
    """
    
    Attributes:
        none
    """

    def get(self):
        anlyseStep = request.args.get("anlyseStep")
        cur_time = request.args.get("curTime")
        search_type = request.args.get("type")  # 'flow'
        search_info = request.args.get("search_dest")  # 待搜索的关键字符
        search_key = request.args.get("key")  # flowName/sourceNode/desNode/all

        # 若未仿真完成，则返回错误码
        if g_sim.status != 1:
            return error_response(ErrCode.NOT_SIMILATING_NO_DATA, 200)

        if None == cur_time or None == search_type or None == search_info or None == search_key:
            info_logger.warning('missing parameter')
            return error_response(ErrCode.INVALID_PARAMETER, 200)
        if anlyseStep != 'before' and anlyseStep != 'after':
            info_logger.warning('invalid parameter(anlyseStep)')
            return error_response(ErrCode.INVALID_PARAMETER, 200)

        if judge_curtime_in_simlate_time(cur_time) != 0:
            data = get_simlate_start_end_time()
            return err_data_response(ErrCode.TIME_NOT_IN_SIMILATING, 200, data)

            # 根据输入的时间，在flow_list_before_fault中，选出包含这个时间点的Flow
        # 需要找输入时间节点所在的时间段 
        start_time, _ = get_start_end_time(cur_time)
        search_flow = []
        if anlyseStep == 'before':
            if start_time in g_sim.flow_list_before_fault:
                search_flow = g_sim.flow_list_before_fault[start_time]['flowinfo']
        else:
            if start_time in g_sim.flow_list_after_fault:
                search_flow = g_sim.flow_list_after_fault[start_time]['flowinfo']

        if not search_flow:
            data = {}
            return data_response(data)

        search_type_deal = search_type.strip()

        if search_type_deal == 'flow':
            search_key_deal = search_key.strip()
            search_info_deal = search_info.strip()
            # print('!!search_key_deal = ',search_key_deal)
            # print('!!search_info_deal = ',search_info_deal)
            # print('!!search_flow = ',search_flow)
            # 暂时调用了原先的search接口，待搜索的数据字典内容有所删减，再调试
            ret, data = search_flow_Info_at_flow_list(search_key_deal, search_info_deal, search_flow)

        else:
            ret = ErrCode.FAILED

        if ret != ErrCode.SUCCESS:
            # log_warning('get_flow info failed')
            return error_response(ret, 200)

        # print('data = ', data)
        return data_response(data)


# 5.2.6	显示选中的流量路径
class ShowFlowIDirectionApi(Resource):
    def get(self):
        # 参数检查 判断故障仿真是否已完成

        anlyseStep = request.args.get("anlyseStep")
        cur_time = request.args.get("curTime")
        flowId = request.args.get("flowId")

        # 若未仿真完成，则返回错误码
        if g_sim.status != 1:
            return error_response(ErrCode.NOT_SIMILATING_NO_DATA, 200)

        if None == cur_time or None == type or None == flowId:
            info_logger.warning('missing parameter')
            return error_response(ErrCode.INVALID_PARAMETER, 200)
        if anlyseStep != 'before' and anlyseStep != 'after':
            info_logger.warning('invalid parameter(anlyseStep)')
            return error_response(ErrCode.INVALID_PARAMETER, 200)

        if judge_curtime_in_simlate_time(cur_time) != 0:
            data = get_simlate_start_end_time()
            return err_data_response(ErrCode.TIME_NOT_IN_SIMILATING, 200, data)

        ret, data = get_flow_direction(anlyseStep, cur_time, flowId)

        if ret != ErrCode.SUCCESS:
            info_logger.warning('get_fault_load failed')
            return error_response(ret, 200)

        # print('data = ', data)
        return data_response(data)


# 5.2.7	选择某条Flow，进行查看
class GetSelectFlowInfoApi(Resource):
    """     

    Attributes:
        none
    """

    def get(self):
        anlyseStep = request.args.get("anlyseStep")
        cur_time = request.args.get("curTime")
        flowId = request.args.get("flowId")

        # 若未仿真完成，则返回错误码
        if g_sim.status != 1:
            return error_response(ErrCode.NOT_SIMILATING_NO_DATA, 200)

        if None == cur_time or None == flowId:
            info_logger.warning('missing parameter')
            return error_response(ErrCode.INVALID_PARAMETER, 200)
        if anlyseStep != 'before' and anlyseStep != 'after':
            info_logger.warning('invalid parameter(anlyseStep)')
            return error_response(ErrCode.INVALID_PARAMETER, 200)

        if judge_curtime_in_simlate_time(cur_time) != 0:
            data = get_simlate_start_end_time()
            return err_data_response(ErrCode.TIME_NOT_IN_SIMILATING, 200, data)

        ret, data = get_select_flow_info(anlyseStep, cur_time, flowId)
        if ret != ErrCode.SUCCESS:
            info_logger.warning('get_fault_load failed')
            return error_response(ret, 200)

        # print('data = ', data)
        return data_response(data)


# 5.1.1	阈值设置
class SetSetviewTimeAndRangeApi(Resource):
    """
    
    Attributes:
        none
    """

    def post(self):
        data = request.json.get('data')
        input_time = data["time"]
        # time = 1563171650
        firstStepEnd = data["firstStepEnd"]
        secondStepEnd = data["secondStepEnd"]
        thirdStepEnd = data["thirdStepEnd"]
        if 'anlyseStep' in data:
            stepstatus = data["anlyseStep"]
        else:
            stepstatus = 'all'
        if None == input_time or None == firstStepEnd or None == secondStepEnd or None == thirdStepEnd or None == stepstatus:
            info_logger.warning('missing parameter')
            return error_response(ErrCode.INVALID_PARAMETER, 200)
        if firstStepEnd < 0 or firstStepEnd > secondStepEnd:
            return error_response(ErrCode.INVALID_PARAMETER, 200)
        if secondStepEnd > thirdStepEnd or thirdStepEnd > 100:
            return error_response(ErrCode.INVALID_PARAMETER, 200)
        if g_sim.status == 1:
            # sprint4 时间段放开
            start_time, end_time = get_start_end_time(input_time)
            if start_time == 0 and end_time == 0:
                data = get_simlate_start_end_time()
                return err_data_response(ErrCode.TIME_NOT_IN_SIMILATING, 200, data)
            else:
                # 记录仿真的设置
                g_ana.analyse_time = input_time
                g_ana.analyse_start_time = start_time
                g_ana.analyse_end_time = end_time
                g_ana.analyse_firstStepEnd = firstStepEnd
                g_ana.analyse_secondStepEnd = secondStepEnd
                g_ana.analyse_thirdStepEnd = thirdStepEnd
                # 计算负载的统计信息
                cal_load_info_by_threshold(start_time, thirdStepEnd)

                if stepstatus == 'before':
                    data = get_before_link_stage_info()
                    return data_response(data)
                elif stepstatus == 'after':
                    data = get_after_link_stage_info()
                    return data_response(data)
                elif stepstatus == 'all':
                    data = get_before_and_after_link_stage_info()
                    return data_response(data)
                else:
                    return error_response(ErrCode.INVALID_PARAMETER, 200)
        else:
            return error_response(ErrCode.NOT_SIMILATING_NO_DATA, 200)


class GetSetviewTimeAndRangeApi(Resource):
    """     

    Attributes:
        none
    """

    def get(self):
        try:
            firstStepEnd = g_ana.analyse_firstStepEnd
            secondStepEnd = g_ana.analyse_secondStepEnd
            thirdStepEnd = g_ana.analyse_thirdStepEnd
            data = {
                "firstStepEnd": firstStepEnd,  # 第一个阶段的结束点，
                "secondStepEnd": secondStepEnd,  # 第二个阶段的结束点，
                "thirdStepEnd": thirdStepEnd  # 第三个阶段的结束点，
            }
            return data_response(data)
        except:
            data = {
                "firstStepEnd": 25,  # 第一个阶段的结束点，
                "secondStepEnd": 75,  # 第二个阶段的结束点，
                "thirdStepEnd": 90  # 第三个阶段的结束点，
            }
            return data_response(data)


class ReSimulateApi(Resource):
    """     

    Attributes:
        none
    """

    def post(self):
        if request.is_json:
            # 用json.get就OK ，具体原因还未知 
            reSimType = request.json.get("reSimType")

            if None == reSimType:
                info_logger.warning('missing parameter')
                # 注释掉的原因是前台收不到reSimType这个参数 ，所以只能先注释了
                return error_response(ErrCode.INVALID_PARAMETER, 200)
                # reSimType = request.json.get("reSimType")

            if 'newSim' != reSimType and 'inheritSim' != reSimType:
                info_logger.warning('INVALID parameter')
                return error_response(ErrCode.INVALID_PARAMETER, 200)
                # reSimType = request.json.get("reSimType")

            ret = set_re_sim(reSimType)
            if ret != ErrCode.SUCCESS:
                return error_response(ErrCode.FAILED, 200)
        else:
            return error_response(ErrCode.FAILED, 200)

        return success_response()


# Tunnel相关接口函数
class TunnelsApi(Resource):
    def get(self):

        # 若未仿真完成，则返回错误码
        if g_sim.status != 1:
            return error_response(ErrCode.NOT_SIMILATING_NO_DATA, 200)

        anlyseType = request.args.get("type")
        if anlyseType != 'all' and anlyseType != 'unchange' and anlyseType != 'change' and anlyseType != 'interrupt':
            info_logger.warning('invalid parameter(TunnelsApi)')
            return error_response(ErrCode.INVALID_PARAMETER, 200)
        curTime = request.args.get("curTime")
        if None == curTime:
            info_logger.warning('missing parameter')
            return error_response(ErrCode.INVALID_PARAMETER, 200)
        if judge_curtime_in_simlate_time(curTime) != 0:
            data = get_simlate_start_end_time()
            return err_data_response(ErrCode.TIME_NOT_IN_SIMILATING, 200, data)

        ret, data = get_tunnels_info(curTime, anlyseType)
        if ret != ErrCode.SUCCESS:
            info_logger.warning('get_tunnels_info failed')
            return error_response(ret, 200)

        return data_response(data)


class ListTunnelNameApi(Resource):
    def get(self):

        if g_sim.status != 1:
            return error_response(ErrCode.NOT_SIMILATING_NO_DATA, 200)
        anlyseStep = request.args.get("anlyseStep")
        if anlyseStep != 'before' and anlyseStep != 'after':
            info_logger.warning('invalid parameter(anlyseStep)')
            return error_response(ErrCode.INVALID_PARAMETER, 200)
        curTime = request.args.get("curTime")
        if None == curTime:
            info_logger.warning('missing parameter')
            return error_response(ErrCode.INVALID_PARAMETER, 200)
        if judge_curtime_in_simlate_time(curTime) != 0:
            data = get_simlate_start_end_time()
            return err_data_response(ErrCode.TIME_NOT_IN_SIMILATING, 200, data)

        data = get_te_name_list(curTime, anlyseStep)
        return data_response(data)


class ShowTunnelPathApi(Resource):
    def get(self):
        if g_sim.status != 1:
            return error_response(ErrCode.NOT_SIMILATING_NO_DATA, 200)
        curTime = request.args.get("curTime")
        nodeId = request.args.get("nodeId")
        anlyseStep = request.args.get("anlyseStep")

        if None == curTime:
            info_logger.warning('missing parameter')
            return error_response(ErrCode.INVALID_PARAMETER, 200)
        if None == nodeId:
            info_logger.warning('missing parameter')
            return error_response(ErrCode.INVALID_PARAMETER, 200)
        if anlyseStep != 'before' and anlyseStep != 'after':
            info_logger.warning('invalid parameter(anlyseStep)')
            return error_response(ErrCode.INVALID_PARAMETER, 200)
        if judge_curtime_in_simlate_time(curTime) != 0:
            data = get_simlate_start_end_time()
            return err_data_response(ErrCode.TIME_NOT_IN_SIMILATING, 200, data)

        data = get_te_path_info(curTime, anlyseStep, nodeId)

        return data_response(data)


class ShowAllTunnelPathApi(Resource):
    def get(self):
        if g_sim.status != 1:
            return error_response(ErrCode.NOT_SIMILATING_NO_DATA, 200)
        cur_time = request.args.get("curTime")
        anlyseStep = request.args.get("anlyseStep")
        tunnelId = request.args.get("tunnelId")

        if None == cur_time:
            info_logger.warning('missing parameter')
            return error_response(ErrCode.INVALID_PARAMETER, 200)
        if None == tunnelId:
            info_logger.warning('missing parameter')
            return error_response(ErrCode.INVALID_PARAMETER, 200)
        if anlyseStep != 'before' and anlyseStep != 'after':
            info_logger.warning('invalid parameter(anlyseStep)')
            return error_response(ErrCode.INVALID_PARAMETER, 200)
        if judge_curtime_in_simlate_time(cur_time) != 0:
            data = get_simlate_start_end_time()
            return err_data_response(ErrCode.TIME_NOT_IN_SIMILATING, 200, data)

        ret, data = get_all_te_path(cur_time, anlyseStep, tunnelId)
        if ret != ErrCode.SUCCESS:
            data = {}

        return data_response(data)


class GetSelectTeInfoApi(Resource):
    def get(self):
        # 参数检查 判断有否有topo已经同步
        if g_sim.status != 1:
            return error_response(ErrCode.NOT_SIMILATING_NO_DATA, 200)

        cur_time = request.args.get("curTime")
        anlyseStep = request.args.get("anlyseStep")
        tunnelId = request.args.get("tunnelId")

        if None == cur_time:
            info_logger.warning('missing parameter')
            return error_response(ErrCode.INVALID_PARAMETER, 200)
        if None == tunnelId:
            info_logger.warning('missing parameter')
            return error_response(ErrCode.INVALID_PARAMETER, 200)
        if anlyseStep != 'before' and anlyseStep != 'after':
            info_logger.warning('invalid parameter(anlyseStep)')
            return error_response(ErrCode.INVALID_PARAMETER, 200)
        if judge_curtime_in_simlate_time(cur_time) != 0:
            data = get_simlate_start_end_time()
            return err_data_response(ErrCode.TIME_NOT_IN_SIMILATING, 200, data)

        ret, data = get_select_te_info(cur_time, anlyseStep, tunnelId)
        if ret != ErrCode.SUCCESS:
            info_logger.warning('get_fault_load failed')
            return error_response(ret, 200)

        # print('data = ', data)
        return data_response(data)


class GetTunnelFlowApi(Resource):
    def get(self):
        if g_sim.status != 1:
            return error_response(ErrCode.NOT_SIMILATING_NO_DATA, 200)

        cur_time = request.args.get("curTime")
        anlyseStep = request.args.get("anlyseStep")
        tunnelId = request.args.get("tunnelId")
        path_type = request.args.get("pathType")

        if None == cur_time:
            info_logger.warning('missing parameter')
            return error_response(ErrCode.INVALID_PARAMETER, 200)
        if None == tunnelId:
            info_logger.warning('missing parameter')
            return error_response(ErrCode.INVALID_PARAMETER, 200)
        if anlyseStep != 'before' and anlyseStep != 'after':
            info_logger.warning('invalid parameter(anlyseStep)')
            return error_response(ErrCode.INVALID_PARAMETER, 200)
        if path_type != 'primary' and path_type != 'standby' and path_type != 'all':
            info_logger.warning('invalid parameter(anlyseStep)')
            return error_response(ErrCode.INVALID_PARAMETER, 200)
        if judge_curtime_in_simlate_time(cur_time) != 0:
            data = get_simlate_start_end_time()
            return err_data_response(ErrCode.TIME_NOT_IN_SIMILATING, 200, data)

        ret, data = get_tunnel_flow_info(cur_time, anlyseStep, tunnelId, path_type)
        if ret != ErrCode.SUCCESS:
            info_logger.warning('get_fault_load failed')
            return error_response(ret, 200)

        # print('data = ', data)
        return data_response(data)