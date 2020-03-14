# -*- encoding: utf-8 -*-
"""
@File    : topo.py
@Time    : 2019/05/29 13:59:32
@Author  : 
@License : Copyright (c) 2004-2019 New H3C Tech. Co., Ltd. All rights reserved.
@Desc    : topo管理
"""

from apps.errcode import ErrCode
from apps.datacode import SyncModCode, SyncStatusCode
from apps.util import generate_uuid
from apps.util import g_dt, g_sim
from apps.util import info_logger, error_logger
from apps.util import get_current_time
from apps.v1_0.test import *
import json
from param import *


class L3TopoLink():
    """三层TOPO链路信息
    
    Attributes:
        none
    """

    def __init__(self, phy_id, id=None):
        if id == None:
            self.id = generate_uuid()
        else:
            self.id = id
        self.phy_id = phy_id
        self.fault = 'no'
        self.cost = 0
        self.src_ip = ''  # 端口IP
        self.des_ip = ''  # 端口IP
        self.src_id = ''  # L3 的节点ID
        # service layer agreement
        self.des_id = ''  # L3 的节点ID

        self.delay = {}  # ms
        self.jittery = {}  # ms
        self.loss_rate = {}  # %
        self.label = 0  # 标签转发
        self.bandwidth = 0  # sprint 3 add 
        self.reservableBandWidth = 0  # 单位kbps，从sdn获取的值的单位就是kbps
        self.attributeFlags = 0  # sprint4 新增亲和属性


class L3TopoNode():
    """三层TOPO节点信息
    
    Attributes:
        none
    """

    def __init__(self, phy_id, id=None):
        if id == None:
            self.id = generate_uuid()
        else:
            self.id = id

        self.phy_id = phy_id
        self.fault = 'no'
        self.x = 0
        self.y = 0
        self.cost = 6  # 待删除
        self.name = ''
        self.port = {}
        self.label = 0  # 标签转发
        self.tun_name = []  # sprint 3 add
        self.tun_id = {}  # sprint 3 add, {name:tun_uuid}


class L3Topo():
    """三层TOPO信息
    Attributes:
        none
    """

    def __init__(self):
        self.node_num = 0
        self.link_num = 0
        self.nodes = {}
        self.links = {}
        self.type = 'layer3'

    def add_node(self, phy_id, id=None):
        if id == None:
            uuid = generate_uuid()
            self.nodes[uuid] = L3TopoNode(phy_id, uuid)
        else:
            self.nodes[id] = L3TopoNode(phy_id, id)
        pass

    def remove_node(self, id):
        if self.nodes[id] != None:
            del self.nodes[id]

    def add_link(self, phy_id, id=None):
        if id == None:
            uuid = generate_uuid()
            self.links[uuid] = L3TopoLink(phy_id, uuid)
        else:
            self.links[id] = L3TopoLink(phy_id, id)
        pass

    def remove_link(self, id):
        if self.links[id] != None:
            del self.links[id]

    def clear_topo(self):
        """清除所有节点和链路信息"""

        for key in self.nodes.keys():
            self.nodes[key].port.clear()  # {neighbour_id: 本节点ID与neighbour_id相连接的链路ID}
            self.nodes[key].tun_name.clear()  # sprint 3 add
            self.nodes[key].tun_id.clear()  # sprint 3 add, {name:tun_uuid}

        # 清除节点信息
        self.nodes.clear()
        self.node_num = 0

        # 清除link信息
        self.links.clear()
        self.link_num = 0

    def to_json(self):
        nodelist = []
        for key in self.nodes.keys():
            phy_key = self.nodes[key].phy_id
            node = {
                "id": self.nodes[key].id,
                "l2_id": self.nodes[key].phy_id,
                "fault": self.nodes[key].fault,
                "cost": self.nodes[key].cost,

                "locationX": self.nodes[key].x,
                "locationY": self.nodes[key].y,

                "assetName": g_dt.phy_topo.nodes[phy_key].name,
                "assetNetAddress": g_dt.phy_topo.nodes[phy_key].mgrip,
                "netElementId": g_dt.phy_topo.nodes[phy_key].nettypeid,
                "netElementType": g_dt.phy_topo.nodes[phy_key].nettypedesc
            }
            nodelist.append(node)

        linklist = []
        for key in self.links.keys():
            phy_key = self.links[key].phy_id
            link = {
                "linkId": self.links[key].id,
                "l2_id": self.links[key].phy_id,
                "fault": self.links[key].fault,
                "cost": self.links[key].cost,
                "src_ip": self.links[key].src_ip,
                "des_ip": self.links[key].des_ip,
                "assetId1": self.links[key].src_id,
                "assetId2": self.links[key].des_id,

                "bandWithStage1to2": self.links[phy_key].bandwidthStage1to2,
                "bandWithStage2to1": self.links[phy_key].bandwidthStage2to1,

                "name": g_dt.phy_topo.links[phy_key].name
            }
            linklist.append(link)

        data = {}
        data["linkNum"] = len(linklist)
        data["links"] = linklist
        data["nodeNum"] = len(nodelist)
        data["nodes"] = nodelist

        return data


class Interface():

    def __init__(self, ifindex):
        self.ifindex = ifindex
        self.ifdesc = ''
        self.ip = ''
        self.mask = ''
        self.speed = 0
        self.inbandwidth = 0
        self.outbandwidth = 0
        self.status = 'UP'


class TopoNode():

    def __init__(self, id=None):
        if id == None:
            self.id = generate_uuid()
        else:
            self.id = id
        self.l3_node_id = ''
        self.mgrip = ''  # 管理ip
        self.name = ''
        self.nettypeid = 0
        self.nettypedesc = ''
        self.cost = 0
        self.port = {}  # {1:Interface(),2:Interface()}
        self.x = 0
        self.y = 0
        self.fault = 'no'
        self.neighbour = {}  # {neighbour_id: 本节点ID与neighbour_id相连接的链路ID}
        self.tun_name = []  # sprint 3 add
        self.tun_id = {}  # sprint 3 add, {name:tun_uuid}


class TopoLink():

    def __init__(self, id=None):
        if id == None:
            self.id = generate_uuid()
        else:
            self.id = id
        self.name = ''
        self.nodeid1 = ''
        self.nodeid2 = ''
        self.ifindex1 = 0
        self.ifindex2 = 0
        self.ifflowindex1 = 0
        self.ifflowindex2 = 0
        self.ifdesc1 = ''
        self.ifdesc2 = ''
        self.speed = 0

        # t13686 add :带宽利用率的阶段(为百分比，一共分为4段:1\2\3\4)
        self.bandwidthStage1to2 = 1
        self.bandwidthStage2to1 = 1

        self.fault = 'no'
        self.l3_link_id = ["", ""]
        self.snmpIfHighSpeed = 0  # 带宽,单位转换为kbps
        self.ifdesc1cost = 0  # 端口1的cost
        self.ifdesc2cost = 0  # 端口2 的cost
        self.resBandWidth1 = 0  # 从1到2的可分配带宽，单位kbps
        self.resBandWidth2 = 0  # 从2到1的可分配带宽，单位kbps


class Topo():
    def __init__(self, type=None):
        self.node_num = 0
        self.link_num = 0
        self.nodes = {}
        self.links = {}
        self.fault_num = 0  # 记录故障的节点和链路的总数
        self.mgrip_nodeid = {}  # 建立节点的管理IP与节点的ID的对应关系
        if type == None:
            self.type = "physical"
        else:
            self.type = type

    def add_node(self, id=None):
        if id == None:
            uuid = generate_uuid()
            self.nodes[uuid] = TopoNode(uuid)
        else:
            self.nodes[id] = TopoNode(id)
        pass

    def remove_node(self, id):
        if self.nodes[id] != None:
            del self.nodes[id]

    def add_link(self, id=None):
        if id == None:
            uuid = generate_uuid()
            self.links[uuid] = TopoLink(uuid)
        else:
            self.links[id] = TopoLink(id)
        pass

    def remove_link(self, id):
        if self.links[id] != None:
            del self.links[id]

    def clear_topo(self):
        """清除所有节点和链路信息"""
        for key in self.nodes.keys():
            self.nodes[key].neighbour.clear()
            self.nodes[key].tun_name.clear()
            self.nodes[key].tun_id.clear()

        for key in self.links.keys():
            self.links[key].l3_link_id.clear()

        # 清除节点信息
        self.nodes.clear()
        self.node_num = 0
        # 清除link信息
        self.links.clear()
        self.link_num = 0
        self.fault_num = 0
        # 清除管理IP与物理层节点ID的对应关系
        self.mgrip_nodeid.clear()

    def to_json(self):
        nodelist = []
        for key in self.nodes.keys():
            # idms:202001080041 不要显示控制器
            # if key == 'controller':
            #     node = {
            #         "assetId": self.nodes[key].id,
            #         "assetName": self.nodes[key].name,
            #         "assetNetAddress": self.nodes[key].mgrip,
            #         "netElementId": self.nodes[key].nettypeid,
            #         "locationX": self.nodes[key].x,
            #         "locationY": self.nodes[key].y,
            #         "netElementType": self.nodes[key].nettypedesc,
            #         "fault":'no',
            #         "tunNameList":'N/A',
            #         "tunIdDic":'N/A'               
            #     }
            # else:
            node = {
                "assetId": self.nodes[key].id,
                "assetName": self.nodes[key].name,
                "assetNetAddress": self.nodes[key].mgrip,
                "netElementId": self.nodes[key].nettypeid,
                "locationX": self.nodes[key].x,
                "locationY": self.nodes[key].y,
                "netElementType": self.nodes[key].nettypedesc,
                "fault": self.nodes[key].fault,
                "tunNameList": self.nodes[key].tun_name,
                "tunIdDic": self.nodes[key].tun_id
                # "ifindex":self.nodes[key].port
            }
            nodelist.append(node)

        linklist = []
        for key in self.links.keys():
            link = {
                "assetId1": self.links[key].nodeid1,
                "assetId2": self.links[key].nodeid2,

                "assetName1": self.links[key].nodename1,
                "assetName2": self.links[key].nodename2,

                "ifDescr1": self.links[key].ifdesc1,
                "ifDescr2": self.links[key].ifdesc2,

                "ifIndex1": self.links[key].ifindex1,
                "ifIndex2": self.links[key].ifindex2,

                "bandWithStage1to2": self.links[key].bandwidthStage1to2,
                "bandWithStage2to1": self.links[key].bandwidthStage2to1,

                "linkId": self.links[key].id,
                "name": self.links[key].name,

                "fault": self.links[key].fault
            }
            linklist.append(link)

        data = {}
        data["linkNum"] = self.link_num
        data["links"] = linklist
        data["nodeNum"] = self.node_num
        data["nodes"] = nodelist

        return data


def layer3_topo_json():
    try:
        """基于sprint2 二层与三层需要返回一样的值，所以改成三层TOPO时返回二层的TOPO信息
        
        Args:
            none
        Returns:
            none
        Raise:
            none
        """

        nodes_ids = []
        links_ids = []
        for key in g_dt.l3_topo.nodes.keys():
            # phy_key = g_dt.l3_topo.nodes[key].phy_id
            # if phy_key not in nodes_ids:
            nodes_ids.append(key)

        for key in g_dt.l3_topo.links.keys():
            # phy_key = g_dt.l3_topo.links[key].phy_id
            # if phy_key not in links_ids:
            links_ids.append(key)

        nodelist = []
        for key in nodes_ids:
            phy_node_info = g_dt.l3_topo.nodes[key]
            node = {
                "assetId": phy_node_info.id,
                "assetName": phy_node_info.name,
                # "assetNetAddress": phy_node_info.mgrip,
                # "netElementId": phy_node_info.nettypeid,
                "locationX": phy_node_info.x,
                "locationY": phy_node_info.y,
                # "netElementType": phy_node_info.nettypedesc,
                "fault": phy_node_info.fault,
                "tunNameList": phy_node_info.tun_name,
                "tunIdDic": phy_node_info.tun_id
            }
            nodelist.append(node)

        linklist = []
        for key in links_ids:
            phy_link_info = g_dt.l3_topo.links[key]

            src_node_name = ''
            des_node_name = ''
            for nd in nodelist:
                if nd["assetId"] == phy_link_info.src_id:
                    src_node_name = nd["assetName"]

                if nd["assetId"] == phy_link_info.des_id:
                    des_node_name = nd["assetName"]

            link = {

                "cost": phy_link_info.cost,
                'id': phy_link_info.id,
                "src_node_id": phy_link_info.src_id,
                "des_node_id": phy_link_info.des_id,

                "src_node_name": src_node_name,
                "des_node_name": des_node_name,

                "bandwidth": phy_link_info.bandwidth,

                "fault": phy_link_info.fault
            }
            linklist.append(link)

        data = {}
        data["linkNum"] = len(linklist)
        data["links"] = linklist
        data["nodeNum"] = len(nodelist)
        data["nodes"] = nodelist

        return data
    except Exception as e:
        info_logger.error(e)
        error_logger.error(e)
        print("layer3_topo_json Exception:", e)
        return None


def get_topo(type):
    try:
        """获取topo信息"""

        # 2 同步完成
        if g_dt.topo_sync_status != SyncStatusCode.SYNC_FINISH or g_dt.conf_sync_status != SyncStatusCode.SYNC_FINISH:
            return ErrCode.TOPO_NOT_READY, {}

        if type == "layer3":
            if g_dt.l3_topo == None:
                return ErrCode.TOPO_NOT_READY, {}
            # data = g_dt.l3_topo.to_json()
            data = layer3_topo_json()
        else:
            if g_dt.phy_topo == None:
                return ErrCode.TOPO_NOT_READY, {}

            data = g_dt.phy_topo.to_json()

        return ErrCode.SUCCESS, data
    except Exception as e:
        info_logger.error(e)
        error_logger.error(e)
        print("get_topo Exception:", e)
        return ErrCode.FAILED, None


def save_topo(data):
    """保存topo信息"""
    try:
        if g_dt.phy_topo == None:
            return ErrCode.TOPO_NOT_READY

        if g_dt.topo_sync_status != SyncStatusCode.SYNC_FINISH or g_dt.conf_sync_status != SyncStatusCode.SYNC_FINISH:
            return ErrCode.TOPO_NOT_READY

        nodes = data["nodes"]

        for node in nodes:
            temp = g_dt.phy_topo.nodes[node["assetId"]]
            temp.x = int(round(node["locationX"]))
            temp.y = int(round(node["locationY"]))

            # 把最新的位置 传给sim的topo，用于后面仿真后的topo位置改动,包含了控制器的位置
            try:
                if g_sim and g_sim.topo:
                    # print_in_log('#1# g_dt.phy_topo ===',g_dt.phy_topo)
                    # print_in_log('#2# g_dt.phy_topo.nodes ===', g_dt.phy_topo.nodes)

                    temp1 = g_sim.topo.nodes[node["assetId"]]
                    # print_in_log('#3# sim_b4_node ===', temp1)
                    temp1.x = int(round(node["locationX"]))
                    temp1.y = int(round(node["locationY"]))

                    temp2 = g_sim.af_topo.nodes[node["assetId"]]
                    # print_in_log('#4# sim_b4_node ===', temp2)
                    temp2.x = int(round(node["locationX"]))
                    temp2.y = int(round(node["locationY"]))

            except Exception as ex:
                info_logger.error(ex)
                error_logger.error(ex)

                # if node["assetId"] == 'controller':
            #     continue
            l3_node_id = g_dt.phy_topo.nodes[node["assetId"]].l3_node_id
            # 点击保存时，把三层TOPO的节点位置信息也进行保存
            l3_node = g_dt.l3_topo.nodes[l3_node_id]
            l3_node.x = int(round(node["locationX"]))
            l3_node.y = int(round(node["locationY"]))
        return ErrCode.SUCCESS

    except Exception as e:
        print("save_topo Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.FAILED


def save_display_config(data):
    try:
        """设置topo显示的配置参数"""

        g_dt.dis_interface = data["display"]["disInterface"]
        g_dt.dis_name = data["display"]["disName"]
        if g_dt.dis_name == "on":
            g_dt.dis_name_type = data["display"]["nameType"]
        g_dt.dis_tip = data["display"]["disTip"]
        g_dt.auto_save_topo = data["autoSaveTopo"]
        if g_dt.auto_save_topo == "on":
            g_dt.auto_save_time = data["autoSaveTime"]
            if g_dt.auto_save_time > 60:
                return ErrCode.FAILED

        return ErrCode.SUCCESS
    except Exception as e:
        print("save_display_config Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.FAILED


def get_display_config():
    try:
        """获取topo显示的配置参数"""

        data = {
            "display": {
                "disName": g_dt.dis_name,
                "nameType": g_dt.dis_name_type,
                "disTip": g_dt.dis_tip,
                "disInterface": g_dt.dis_interface
            },
            "autoSaveTopo": g_dt.auto_save_topo,
            "autoSaveTime": g_dt.auto_save_time
        }

        return ErrCode.SUCCESS, data
    except Exception as e:
        print("get_display_config Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.FAILED, None
