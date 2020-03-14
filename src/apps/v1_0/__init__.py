# -*- encoding: utf-8 -*-
"""
@File    : __init__.py
@Time    : 2019/05/29 11:28:45
@Author  : 
@License : Copyright (c) 2004-2019 New H3C Tech. Co., Ltd. All rights reserved.
@Desc    : 
"""

from flask import Blueprint
from flask_restful import Api
from apps.v1_0.api import *

def register_views(app):
    """注册视图,添加资源。"""
    
    api = Api(app)
    # 获取l2、l3 topo
    api.add_resource(GetTopoApi, '/faultDefinition/getTopo')  # 获取数据同步之后得到的拓扑
    api.add_resource(SaveTopoApi, '/faultDefinition/saveTopo')  # 保存拓扑信息，更新前台的拓扑显示效果
    api.add_resource(TopoDisplaySettingApi, '/faultDefinition/setting')  # 第二步系统设置（自动保存拓扑、链路信息显示等）
    api.add_resource(GetTopoDisplaySettingApi, '/faultDefinition/getSetting')  # 获取系统设置具体信息
    api.add_resource(StartDataSyncAPI, '/dataSync/startSync')  # 第一步：数据同步
    api.add_resource(StopDataSyncAPI, '/dataSync/stopSync')  # 数据同步时终止同步
    api.add_resource(GetDataSyncStatus, '/dataSync/syncStatus')  # 即时获取数据同步的进度
    api.add_resource(GetDataSyncLogApi, '/dataSync/syncLog')
    # BGP LS配置
    api.add_resource(ConfigBgplsApi, '/dataSync/configBgpls')
    api.add_resource(GetBgplsConfigApi, '/dataSync/getBgplsConfig')

    # 获取flow示例
    api.add_resource(SaveFlowModleApi, '/faultDefinition/getFlowTemplates')  # 前台下载流量模板（按钮）
    api.add_resource(ImportFlowApi,'/faultDefinition/addNewFlow')  # 第二步：导入流量（流量模板解析，导入流量按钮）
    api.add_resource(GetFlowInfoApi,'/faultDefinition/GetFlowMgr')
    api.add_resource(ShowImportFlowProApi,'/faultDefinition/showFlowProgress')
    api.add_resource(GetLoadedFlowListApi,'/faultDefinition/GetLoadedFlow')  # 第二步导入后，获取导入的流量信息
    api.add_resource(SearchFlowListApi,'/faultDefinition/searchLoadedFlow')  # 导入流量之后，使用搜索框查询特定的流量信息
    api.add_resource(DelFlowApi,'/faultDefinition/delLoadedFlow')  # 删除已导入的流量（删除流量按钮）

    api.add_resource(SetLanguageApi,'/i18n/i18nParam')
    api.add_resource(SetFaultApi, '/faultDefinition/setFault')  # 第二步：故障定义，设置或取消设置链路或节点故障
    api.add_resource(GetAllFaultApi, '/faultDefinition/getAllFault')  # 获取设置的所有故障信息
    api.add_resource(ClearAllSelFaultApi, '/faultDefinition/clearAllSelFault')
    
    # 故障前后分析
    # 5.1
    api.add_resource(SetSetviewTimeAndRangeApi, '/analysis/setViewTimeAndRange')  # 负载阈值设置，传入新的阈值设置，返回设置前后的负载信息
    api.add_resource(GetSetviewTimeAndRangeApi, '/analysis/getViewTimeAndRange')  # 获取负载阈值设置数据
    api.add_resource(GetAnalysTopoInfoApi, '/analysis/getAnalysTopoInfo')  # 获取分析用的拓扑数据
    api.add_resource(SummaryApi, '/analysis/summary')  # 根据前台设置的仿真时间点获取对应的仿真对象统计信息
    api.add_resource(GetAnalysFlowsInfoApi, '/analysis/flows') 
    api.add_resource(LoadApi, '/analysis/load') 
    api.add_resource(FaultDefinitionApi, '/analysis/faultDefinition') 
    # 5.2
    api.add_resource(GetSelectLoadFlowApi, '/analysis/onlyOneTopo/getLoadFlowView')
    api.add_resource(GeFlowListInfoApi, '/analysis/onlyOneTopo/GetFlowList')  
    api.add_resource(SearchAnalysisFlowApi, '/analysis/onlyOneTopo/searchLoadedFlow') # 仿真流量搜索
    api.add_resource(ShowFlowIDirectionApi, '/analysis/getFlowInfo')  
    api.add_resource(GetSelectFlowInfoApi, '/analysis/onlyOneTopo/getFlowPath') 
    api.add_resource(GetSimParaApi,'/analysis/initSimData')   # 仿真分析界面获取仿真相关参数，仿真类型、起止时间、仿真对象等
    
    # 隧道相关 
    api.add_resource(TunnelsApi, '/analysis/tunnels') 
    api.add_resource(ListTunnelNameApi, '/analysis/listTunnelName') 
    api.add_resource(ShowTunnelPathApi, '/analysis/showTunnelPath') 
    api.add_resource(ShowAllTunnelPathApi, '/analysis/showAllTunnelPath') 
    api.add_resource(GetSelectTeInfoApi, '/analysis/onlyOneTopo/getTePath')
    api.add_resource(GetTunnelFlowApi, '/analysis/onlyOneTopo/getTunnelFlow')
    
    # 开始仿真相关
    api.add_resource(SetSimApi, '/analysis/setAnalysis')  # 第三步：开始仿真，传入设置的仿真参数
    api.add_resource(ReSimulateApi, '/analysis/reSimulate') 
    api.add_resource(GetSimProgressApi, '/analysis/getAnalysisProgress')
    api.add_resource(GetSimStepStatiscApi, '/analysis/getAnalysisStatistical')  # 获取仿真阶段的统计信息
    # 生成报表 
    api.add_resource(GetReport, '/analysis/getReport')  

def creat_blueprint_v1_0():
    """创建蓝图 v1.0版本。"""

    bp_v1_0 = Blueprint('v1_0', __name__)
    register_views(bp_v1_0)

    return bp_v1_0