# -*- encoding: utf-8 -*-
"""
@File    : test.py
@Time    : 2019/05/29 14:05:15
@Author  : 
@License : Copyright (c) 2004-2019 New H3C Tech. Co., Ltd. All rights reserved.
@Desc    : 测试
"""
import random

import time
from apps.util import info_logger, error_logger
import json
import operator

from apps.util import info_logger, error_logger
from param import *

def print_in_log(info,*info2):
  try:
      if log_print_debug:
          error_logger.error(info)
          print(info)
          for inf in info2:
            print(inf)
            error_logger.error(inf)
      else:
          pass
  except Exception as e:
      error_logger.error(" Exception in  print_in_log")
      info_logger.error(e)
      error_logger.error(e)


def delay_s(second):
  try:
    if not debug_postman:
        time.sleep(second)
    else:
        pass
  except Exception as e:
      error_logger.error(" Exception in  delay_s")
      info_logger.error(e)
      error_logger.error(e)

test_sdn_resp_data = {
  "msg": "\u6210\u529f", "code": 0, 
  "data": [
  {"standby": {"strictStatus": 1, "linkList": 
  ["27f06554-6854-412e-8f6d-5758a2c43075", 
  "6bb45218-bb58-4adc-aa28-f085fdd1ec62", 
  "3b71a3a2-7bdf-4e31-92dd-948bd08c2b20"], "pathNumber": 1}, 
  "primary": {"strictStatus": 1, "linkList":
   ["6308d6ad-eb76-41db-8e92-85672f533c32"], "pathNumber": 0}, 
   "tunnelId": "5fc7e69a-709b-409d-b1e9-093c02394d5aTunnel4"}, 

   {"standby": {"strictStatus": 3, "linkList": [], "pathNumber": 1}, 
   "primary": {"strictStatus": 3, "linkList": [], "pathNumber": 0}, 
   "tunnelId": "5fc7e69a-709b-409d-b1e9-093c02394d5aTunnel2"}, 

   {"standby": {"strictStatus": 1, 
   "linkList": ["27f06554-6854-412e-8f6d-5758a2c43075", 
   "6bb45218-bb58-4adc-aa28-f085fdd1ec62", "3490f918-c557-4d73-a283-91fe6779d417"], 
   "pathNumber": 1}, "primary": {"strictStatus": 1, "linkList": 
   ["6308d6ad-eb76-41db-8e92-85672f533c32", "9d7bc3d2-b550-4e34-aca6-3891fbe5f254"], 
   "pathNumber": 0}, "tunnelId": "5fc7e69a-709b-409d-b1e9-093c02394d5aTunnel6"}

   ]}

operator.eq(1,2)
#print("CMP ===",operator.eq(test_sdn_resp_data,test_sdn_resp_data2))

# 测试用的topo数据

debug_topo_data = {
    "result": {
        "isCreated": True,
        "linkNum": 11,
        "alertNum": 0,
        "nodes": [
            {
                "locationY": 498,
                "image": "router",
                "firstTypeId": 2,
                "secondTypeIdValue": "路由器",
                "locationX": 610,
                "netElementType": 7,
                "collectType": "SNMP",
                "firstTypeIdValue": "网络设备",
                "assetId": "04165eb6-48f0-4e7f-aa08-3e0967fda9a5",
                "assetNetAddress": "10.99.211.214",
                "width": 'null',
                "assetName": "VSR4",
                "client": "{\"assetId\":\"04165eb6-48f0-4e7f-aa08-3e0967fda9a5\",\"assetNetAddress\":\"10.99.211.214\",\"netElementType\":7,\"secondTypeIdValue\":\"路由器\",\"collectType\":\"SNMP\"}",
                "style": 'null',
                "position": 'null',
                "height": 'null'
            },
            {
                "locationY": 284,
                "image": "router",
                "firstTypeId": 2,
                "secondTypeIdValue": "路由器",
                "locationX": 618,
                "netElementType": 7,
                "collectType": "SNMP",
                "firstTypeIdValue": "网络设备",
                "assetId": "a92e557a-542e-445f-a38e-9d3cd438110b",
                "assetNetAddress": "10.99.211.213",
                "width": 'null',
                "assetName": "VSR3",
                "client": "{\"assetId\":\"a92e557a-542e-445f-a38e-9d3cd438110b\",\"assetNetAddress\":\"10.99.211.213\",\"netElementType\":7,\"secondTypeIdValue\":\"路由器\",\"collectType\":\"SNMP\"}",
                "style": 'null',
                "position": 'null',
                "height": 'null'
            },
            {
                "locationY": 496,
                "image": "router",
                "firstTypeId": 2,
                "secondTypeIdValue": "路由器",
                "locationX": 393,
                "netElementType": 7,
                "collectType": "SNMP",
                "firstTypeIdValue": "网络设备",
                "assetId": "d235cae2-848e-404c-88e3-1576668834cc",
                "assetNetAddress": "10.99.211.212",
                "width": 'null',
                "assetName": "VSR2",
                "client": "{\"assetId\":\"d235cae2-848e-404c-88e3-1576668834cc\",\"assetNetAddress\":\"10.99.211.212\",\"netElementType\":7,\"secondTypeIdValue\":\"路由器\",\"collectType\":\"SNMP\"}",
                "style": 'null',
                "position": 'null',
                "height": 'null'
            },
            {
                "locationY": 282,
                "image": "router",
                "firstTypeId": 2,
                "secondTypeIdValue": "路由器",
                "locationX": 396,
                "netElementType": 7,
                "collectType": "SNMP",
                "firstTypeIdValue": "网络设备",
                "assetId": "5fc7e69a-709b-409d-b1e9-093c02394d5a",
                "assetNetAddress": "10.99.211.211",
                "width": 'null',
                "assetName": "VSR1",
                "client": "{\"assetId\":\"5fc7e69a-709b-409d-b1e9-093c02394d5a\",\"assetNetAddress\":\"10.99.211.211\",\"netElementType\":7,\"secondTypeIdValue\":\"路由器\",\"collectType\":\"SNMP\"}",
                "style": 'null',
                "position": 'null',
                "height": 'null'
            },
            {
                "locationY": 505,
                "image": "router",
                "firstTypeId": 2,
                "secondTypeIdValue": "路由器",
                "locationX": 841,
                "netElementType": 7,
                "collectType": "SNMP",
                "firstTypeIdValue": "网络设备",
                "assetId": "951b9eda-f804-4bfe-a4e1-a648dd7b4fe7",
                "assetNetAddress": "10.99.211.216",
                "width": 'null',
                "assetName": "VSR6",
                "client": "{\"assetId\":\"951b9eda-f804-4bfe-a4e1-a648dd7b4fe7\",\"assetNetAddress\":\"10.99.211.216\",\"netElementType\":7,\"secondTypeIdValue\":\"路由器\",\"collectType\":\"SNMP\"}",
                "style": 'null',
                "position": 'null',
                "height": 'null'
            },
            {
                "locationY": 292,
                "image": "router",
                "firstTypeId": 2,
                "secondTypeIdValue": "路由器",
                "locationX": 849,
                "netElementType": 7,
                "collectType": "SNMP",
                "firstTypeIdValue": "网络设备",
                "assetId": "bb0e3e1d-7541-4a59-80e6-b55d9ae3d4ac",
                "assetNetAddress": "10.99.211.215",
                "width": 'null',
                "assetName": "VSR5",
                "client": "{\"assetId\":\"bb0e3e1d-7541-4a59-80e6-b55d9ae3d4ac\",\"assetNetAddress\":\"10.99.211.215\",\"netElementType\":7,\"secondTypeIdValue\":\"路由器\",\"collectType\":\"SNMP\"}",
                "style": 'null',
                "position": 'null',
                "height": 'null'
            }
        ],
        "nodeNum": 6,
        "deviceAllAlertNum": 0,
        "links": [
            {
                "inputNetUsedRatioTotal": "0.01%",
                "assetId2": "d235cae2-848e-404c-88e3-1576668834cc",
                "assetId1": "5fc7e69a-709b-409d-b1e9-093c02394d5a",
                "ifDescr1": "GigabitEthernet2/0",
                "source": 2,
                "ifDescr2": "GigabitEthernet2/0",
                "ifFlowIndex1": 33,
                "ifFlowIndex2": 33,
                "assetName2": "VSR2",
                "assetName1": "VSR1",
                "flowRatio1": 1,
                "flowRatio2": 1,
                "linkId": "3ae2a7e8-9759-412c-a32f-1b4e3e96a755",
                "outputNetUsedRatioTotal": "0.01%",
                "ifIndex2": 33,
                "name": "VSR1--VSR2",
                "ifIndex1": 33,
                "client": "{\"linkId\":\"3ae2a7e8-9759-412c-a32f-1b4e3e96a755\",\"assetId1\":\"5fc7e69a-709b-409d-b1e9-093c02394d5a\",\"assetId2\":\"d235cae2-848e-404c-88e3-1576668834cc\",\"assetName1\":\"VSR1\",\"assetName2\":\"VSR2\",\"ifIndex1\":33,\"ifIndex2\":33,\"flowRatio1\":1,\"flowRatio2\":1,\"ifDescr1\":\"GigabitEthernet2/0\",\"ifDescr2\":\"GigabitEthernet2/0\",\"ifFlowIndex1\":33,\"ifFlowIndex2\":33,\"snmpIfHighSpeed\":\"1.0Gbps\"}",
                "linkType": 'null',
                "style": "{\"link.type\":\"parallel\",\"link.bundle.offset\":10,\"link.color\":\"#B8B8B8\",\"select.style\":\"border\",\"select.color\":\"#53D628\"}",
                "time": 1578279322039,
                "activeStandby": 0,
                "ifOperStatus": "up",
                "snmpIfHighSpeed": "1.0Gbps"
            },
            {
                "inputNetUsedRatioTotal": "0.02%",
                "assetId2": "bb0e3e1d-7541-4a59-80e6-b55d9ae3d4ac",
                "assetId1": "a92e557a-542e-445f-a38e-9d3cd438110b",
                "ifDescr1": "GigabitEthernet5/0",
                "source": 2,
                "ifDescr2": "GigabitEthernet3/0",
                "ifFlowIndex1": 81,
                "ifFlowIndex2": 49,
                "assetName2": "VSR5",
                "assetName1": "VSR3",
                "flowRatio1": 1,
                "flowRatio2": 1,
                "linkId": "0053cd6b-d471-4e95-8936-d1167977e13c",
                "outputNetUsedRatioTotal": "0.02%",
                "ifIndex2": 49,
                "name": "VSR3--VSR5",
                "ifIndex1": 81,
                "client": "{\"linkId\":\"0053cd6b-d471-4e95-8936-d1167977e13c\",\"assetId1\":\"a92e557a-542e-445f-a38e-9d3cd438110b\",\"assetId2\":\"bb0e3e1d-7541-4a59-80e6-b55d9ae3d4ac\",\"assetName1\":\"VSR3\",\"assetName2\":\"VSR5\",\"ifIndex1\":81,\"ifIndex2\":49,\"flowRatio1\":1,\"flowRatio2\":1,\"ifDescr1\":\"GigabitEthernet5/0\",\"ifDescr2\":\"GigabitEthernet3/0\",\"ifFlowIndex1\":81,\"ifFlowIndex2\":49,\"snmpIfHighSpeed\":\"1.0Gbps\"}",
                "linkType": 'null',
                "style": "{\"link.type\":\"parallel\",\"link.bundle.offset\":10,\"link.color\":\"#B8B8B8\",\"select.style\":\"border\",\"select.color\":\"#53D628\"}",
                "time": 1578279322054,
                "activeStandby": 0,
                "ifOperStatus": "up",
                "snmpIfHighSpeed": "1.0Gbps"
            },
            {
                "inputNetUsedRatioTotal": "0.02%",
                "assetId2": "951b9eda-f804-4bfe-a4e1-a648dd7b4fe7",
                "assetId1": "04165eb6-48f0-4e7f-aa08-3e0967fda9a5",
                "ifDescr1": "GigabitEthernet6/0",
                "source": 2,
                "ifDescr2": "GigabitEthernet4/0",
                "ifFlowIndex1": 97,
                "ifFlowIndex2": 65,
                "assetName2": "VSR6",
                "assetName1": "VSR4",
                "flowRatio1": 1,
                "flowRatio2": 1,
                "linkId": "5b1af664-5a91-4e58-85f2-4cf10ebfddcb",
                "outputNetUsedRatioTotal": "0.02%",
                "ifIndex2": 65,
                "name": "VSR4--VSR6",
                "ifIndex1": 97,
                "client": "{\"linkId\":\"5b1af664-5a91-4e58-85f2-4cf10ebfddcb\",\"assetId1\":\"04165eb6-48f0-4e7f-aa08-3e0967fda9a5\",\"assetId2\":\"951b9eda-f804-4bfe-a4e1-a648dd7b4fe7\",\"assetName1\":\"VSR4\",\"assetName2\":\"VSR6\",\"ifIndex1\":97,\"ifIndex2\":65,\"flowRatio1\":1,\"flowRatio2\":1,\"ifDescr1\":\"GigabitEthernet6/0\",\"ifDescr2\":\"GigabitEthernet4/0\",\"ifFlowIndex1\":97,\"ifFlowIndex2\":65,\"snmpIfHighSpeed\":\"1.0Gbps\"}",
                "linkType": 'null',
                "style": "{\"link.type\":\"parallel\",\"link.bundle.offset\":10,\"link.color\":\"#B8B8B8\",\"select.style\":\"border\",\"select.color\":\"#53D628\"}",
                "time": 1578279322066,
                "activeStandby": 0,
                "ifOperStatus": "up",
                "snmpIfHighSpeed": "1.0Gbps"
            },
            {
                "inputNetUsedRatioTotal": "0.02%",
                "assetId2": "04165eb6-48f0-4e7f-aa08-3e0967fda9a5",
                "assetId1": "a92e557a-542e-445f-a38e-9d3cd438110b",
                "ifDescr1": "GigabitEthernet4/0",
                "source": 2,
                "ifDescr2": "GigabitEthernet3/0",
                "ifFlowIndex1": 65,
                "ifFlowIndex2": 49,
                "assetName2": "VSR4",
                "assetName1": "VSR3",
                "flowRatio1": 1,
                "flowRatio2": 1,
                "linkId": "d699a580-ae6a-4f56-b541-cce1a7c915ae",
                "outputNetUsedRatioTotal": "0.02%",
                "ifIndex2": 49,
                "name": "VSR3--VSR4",
                "ifIndex1": 65,
                "client": "{\"linkId\":\"d699a580-ae6a-4f56-b541-cce1a7c915ae\",\"assetId1\":\"a92e557a-542e-445f-a38e-9d3cd438110b\",\"assetId2\":\"04165eb6-48f0-4e7f-aa08-3e0967fda9a5\",\"assetName1\":\"VSR3\",\"assetName2\":\"VSR4\",\"ifIndex1\":65,\"ifIndex2\":49,\"flowRatio1\":1,\"flowRatio2\":1,\"ifDescr1\":\"GigabitEthernet4/0\",\"ifDescr2\":\"GigabitEthernet3/0\",\"ifFlowIndex1\":65,\"ifFlowIndex2\":49,\"snmpIfHighSpeed\":\"1.0Gbps\"}",
                "linkType": 'null',
                "style": "{\"link.type\":\"parallel\",\"link.bundle.offset\":10,\"link.color\":\"#B8B8B8\",\"select.style\":\"border\",\"select.color\":\"#53D628\"}",
                "time": 1578279322072,
                "activeStandby": 0,
                "ifOperStatus": "up",
                "snmpIfHighSpeed": "1.0Gbps"
            },
            {
                "inputNetUsedRatioTotal": "0.02%",
                "assetId2": "951b9eda-f804-4bfe-a4e1-a648dd7b4fe7",
                "assetId1": "bb0e3e1d-7541-4a59-80e6-b55d9ae3d4ac",
                "ifDescr1": "GigabitEthernet6/0",
                "source": 2,
                "ifDescr2": "GigabitEthernet5/0",
                "ifFlowIndex1": 97,
                "ifFlowIndex2": 81,
                "assetName2": "VSR6",
                "assetName1": "VSR5",
                "flowRatio1": 1,
                "flowRatio2": 1,
                "linkId": "0d086db5-7350-4e72-95bb-f71cb7c09bd9",
                "outputNetUsedRatioTotal": "0.02%",
                "ifIndex2": 81,
                "name": "VSR5--VSR6",
                "ifIndex1": 97,
                "client": "{\"linkId\":\"0d086db5-7350-4e72-95bb-f71cb7c09bd9\",\"assetId1\":\"bb0e3e1d-7541-4a59-80e6-b55d9ae3d4ac\",\"assetId2\":\"951b9eda-f804-4bfe-a4e1-a648dd7b4fe7\",\"assetName1\":\"VSR5\",\"assetName2\":\"VSR6\",\"ifIndex1\":97,\"ifIndex2\":81,\"flowRatio1\":1,\"flowRatio2\":1,\"ifDescr1\":\"GigabitEthernet6/0\",\"ifDescr2\":\"GigabitEthernet5/0\",\"ifFlowIndex1\":97,\"ifFlowIndex2\":81,\"snmpIfHighSpeed\":\"1.0Gbps\"}",
                "linkType": 'null',
                "style": "{\"link.type\":\"parallel\",\"link.bundle.offset\":10,\"link.color\":\"#B8B8B8\",\"select.style\":\"border\",\"select.color\":\"#53D628\"}",
                "time": 1578279322080,
                "activeStandby": 0,
                "ifOperStatus": "up",
                "snmpIfHighSpeed": "1.0Gbps"
            },
            {
                "inputNetUsedRatioTotal": "0.02%",
                "assetId2": "04165eb6-48f0-4e7f-aa08-3e0967fda9a5",
                "assetId1": "5fc7e69a-709b-409d-b1e9-093c02394d5a",
                "ifDescr1": "GigabitEthernet4/0",
                "source": 2,
                "ifDescr2": "GigabitEthernet4/0",
                "ifFlowIndex1": 65,
                "ifFlowIndex2": 65,
                "assetName2": "VSR4",
                "assetName1": "VSR1",
                "flowRatio1": 1,
                "flowRatio2": 1,
                "linkId": "ea7ed0c4-af53-41a5-adc4-eb651e950f62",
                "outputNetUsedRatioTotal": "0.02%",
                "ifIndex2": 65,
                "name": "VSR1--VSR4",
                "ifIndex1": 65,
                "client": "{\"linkId\":\"ea7ed0c4-af53-41a5-adc4-eb651e950f62\",\"assetId1\":\"5fc7e69a-709b-409d-b1e9-093c02394d5a\",\"assetId2\":\"04165eb6-48f0-4e7f-aa08-3e0967fda9a5\",\"assetName1\":\"VSR1\",\"assetName2\":\"VSR4\",\"ifIndex1\":65,\"ifIndex2\":65,\"flowRatio1\":1,\"flowRatio2\":1,\"ifDescr1\":\"GigabitEthernet4/0\",\"ifDescr2\":\"GigabitEthernet4/0\",\"ifFlowIndex1\":65,\"ifFlowIndex2\":65,\"snmpIfHighSpeed\":\"1.0Gbps\"}",
                "linkType": 'null',
                "style": "{\"link.type\":\"parallel\",\"link.bundle.offset\":10,\"link.color\":\"#B8B8B8\",\"select.style\":\"border\",\"select.color\":\"#53D628\"}",
                "time": 1578279322086,
                "activeStandby": 0,
                "ifOperStatus": "up",
                "snmpIfHighSpeed": "1.0Gbps"
            },
            {
                "inputNetUsedRatioTotal": "0.02%",
                "assetId2": "a92e557a-542e-445f-a38e-9d3cd438110b",
                "assetId1": "d235cae2-848e-404c-88e3-1576668834cc",
                "ifDescr1": "GigabitEthernet3/0",
                "source": 2,
                "ifDescr2": "GigabitEthernet2/0",
                "ifFlowIndex1": 49,
                "ifFlowIndex2": 33,
                "assetName2": "VSR3",
                "assetName1": "VSR2",
                "flowRatio1": 1,
                "flowRatio2": 1,
                "linkId": "7674bc3a-b348-460d-a9f4-64e38376b297",
                "outputNetUsedRatioTotal": "0.02%",
                "ifIndex2": 33,
                "name": "VSR2--VSR3",
                "ifIndex1": 49,
                "client": "{\"linkId\":\"7674bc3a-b348-460d-a9f4-64e38376b297\",\"assetId1\":\"d235cae2-848e-404c-88e3-1576668834cc\",\"assetId2\":\"a92e557a-542e-445f-a38e-9d3cd438110b\",\"assetName1\":\"VSR2\",\"assetName2\":\"VSR3\",\"ifIndex1\":49,\"ifIndex2\":33,\"flowRatio1\":1,\"flowRatio2\":1,\"ifDescr1\":\"GigabitEthernet3/0\",\"ifDescr2\":\"GigabitEthernet2/0\",\"ifFlowIndex1\":49,\"ifFlowIndex2\":33,\"snmpIfHighSpeed\":\"1.0Gbps\"}",
                "linkType": 'null',
                "style": "{\"link.type\":\"parallel\",\"link.bundle.offset\":10,\"link.color\":\"#B8B8B8\",\"select.style\":\"border\",\"select.color\":\"#53D628\"}",
                "time": 1578279322091,
                "activeStandby": 0,
                "ifOperStatus": "up",
                "snmpIfHighSpeed": "1.0Gbps"
            },
            {
                "inputNetUsedRatioTotal": "0.02%",
                "assetId2": "bb0e3e1d-7541-4a59-80e6-b55d9ae3d4ac",
                "assetId1": "04165eb6-48f0-4e7f-aa08-3e0967fda9a5",
                "ifDescr1": "GigabitEthernet5/0",
                "source": 2,
                "ifDescr2": "GigabitEthernet4/0",
                "ifFlowIndex1": 81,
                "ifFlowIndex2": 65,
                "assetName2": "VSR5",
                "assetName1": "VSR4",
                "flowRatio1": 1,
                "flowRatio2": 1,
                "linkId": "7fee0e65-3f47-48c5-a78d-561606fd5ee1",
                "outputNetUsedRatioTotal": "0.02%",
                "ifIndex2": 65,
                "name": "VSR4--VSR5",
                "ifIndex1": 81,
                "client": "{\"linkId\":\"7fee0e65-3f47-48c5-a78d-561606fd5ee1\",\"assetId1\":\"04165eb6-48f0-4e7f-aa08-3e0967fda9a5\",\"assetId2\":\"bb0e3e1d-7541-4a59-80e6-b55d9ae3d4ac\",\"assetName1\":\"VSR4\",\"assetName2\":\"VSR5\",\"ifIndex1\":81,\"ifIndex2\":65,\"flowRatio1\":1,\"flowRatio2\":1,\"ifDescr1\":\"GigabitEthernet5/0\",\"ifDescr2\":\"GigabitEthernet4/0\",\"ifFlowIndex1\":81,\"ifFlowIndex2\":65,\"snmpIfHighSpeed\":\"1.0Gbps\"}",
                "linkType": 'null',
                "style": "{\"link.type\":\"parallel\",\"link.bundle.offset\":10,\"link.color\":\"#B8B8B8\",\"select.style\":\"border\",\"select.color\":\"#53D628\"}",
                "time": 1578279322102,
                "activeStandby": 0,
                "ifOperStatus": "up",
                "snmpIfHighSpeed": "1.0Gbps"
            },
            {
                "inputNetUsedRatioTotal": "0.01%",
                "assetId2": "a92e557a-542e-445f-a38e-9d3cd438110b",
                "assetId1": "5fc7e69a-709b-409d-b1e9-093c02394d5a",
                "ifDescr1": "GigabitEthernet3/0",
                "source": 2,
                "ifDescr2": "GigabitEthernet3/0",
                "ifFlowIndex1": 49,
                "ifFlowIndex2": 49,
                "assetName2": "VSR3",
                "assetName1": "VSR1",
                "flowRatio1": 1,
                "flowRatio2": 1,
                "linkId": "0d121ef1-7d25-4894-a9f7-ca6e18d19c90",
                "outputNetUsedRatioTotal": "0.02%",
                "ifIndex2": 49,
                "name": "VSR1--VSR3",
                "ifIndex1": 49,
                "client": "{\"linkId\":\"0d121ef1-7d25-4894-a9f7-ca6e18d19c90\",\"assetId1\":\"5fc7e69a-709b-409d-b1e9-093c02394d5a\",\"assetId2\":\"a92e557a-542e-445f-a38e-9d3cd438110b\",\"assetName1\":\"VSR1\",\"assetName2\":\"VSR3\",\"ifIndex1\":49,\"ifIndex2\":49,\"flowRatio1\":1,\"flowRatio2\":1,\"ifDescr1\":\"GigabitEthernet3/0\",\"ifDescr2\":\"GigabitEthernet3/0\",\"ifFlowIndex1\":49,\"ifFlowIndex2\":49,\"snmpIfHighSpeed\":\"1.0Gbps\"}",
                "linkType": 'null',
                "style": "{\"link.type\":\"parallel\",\"link.bundle.offset\":10,\"link.color\":\"#B8B8B8\",\"select.style\":\"border\",\"select.color\":\"#53D628\"}",
                "time": 1578279322030,
                "activeStandby": 0,
                "ifOperStatus": "up",
                "snmpIfHighSpeed": "1.0Gbps"
            },
            {
                "inputNetUsedRatioTotal": "0.02%",
                "assetId2": "04165eb6-48f0-4e7f-aa08-3e0967fda9a5",
                "assetId1": "d235cae2-848e-404c-88e3-1576668834cc",
                "ifDescr1": "GigabitEthernet4/0",
                "source": 2,
                "ifDescr2": "GigabitEthernet2/0",
                "ifFlowIndex1": 65,
                "ifFlowIndex2": 33,
                "assetName2": "VSR4",
                "assetName1": "VSR2",
                "flowRatio1": 1,
                "flowRatio2": 1,
                "linkId": "2c7ae88f-92d0-4514-b6f7-5cd384321b35",
                "outputNetUsedRatioTotal": "0.02%",
                "ifIndex2": 33,
                "name": "VSR2--VSR4",
                "ifIndex1": 65,
                "client": "{\"linkId\":\"2c7ae88f-92d0-4514-b6f7-5cd384321b35\",\"assetId1\":\"d235cae2-848e-404c-88e3-1576668834cc\",\"assetId2\":\"04165eb6-48f0-4e7f-aa08-3e0967fda9a5\",\"assetName1\":\"VSR2\",\"assetName2\":\"VSR4\",\"ifIndex1\":65,\"ifIndex2\":33,\"flowRatio1\":1,\"flowRatio2\":1,\"ifDescr1\":\"GigabitEthernet4/0\",\"ifDescr2\":\"GigabitEthernet2/0\",\"ifFlowIndex1\":65,\"ifFlowIndex2\":33,\"snmpIfHighSpeed\":\"1.0Gbps\"}",
                "linkType": 'null',
                "style": "{\"link.type\":\"parallel\",\"link.bundle.offset\":10,\"link.color\":\"#B8B8B8\",\"select.style\":\"border\",\"select.color\":\"#53D628\"}",
                "time": 1578279322047,
                "activeStandby": 0,
                "ifOperStatus": "up",
                "snmpIfHighSpeed": "1.0Gbps"
            },
            {
                "inputNetUsedRatioTotal": "0.02%",
                "assetId2": "951b9eda-f804-4bfe-a4e1-a648dd7b4fe7",
                "assetId1": "a92e557a-542e-445f-a38e-9d3cd438110b",
                "ifDescr1": "GigabitEthernet6/0",
                "source": 2,
                "ifDescr2": "GigabitEthernet3/0",
                "ifFlowIndex1": 97,
                "ifFlowIndex2": 49,
                "assetName2": "VSR6",
                "assetName1": "VSR3",
                "flowRatio1": 1,
                "flowRatio2": 1,
                "linkId": "7f7a693f-f3a5-41e9-8e2d-30ba89ca6814",
                "outputNetUsedRatioTotal": "0.02%",
                "ifIndex2": 49,
                "name": "VSR3--VSR6",
                "ifIndex1": 97,
                "client": "{\"linkId\":\"7f7a693f-f3a5-41e9-8e2d-30ba89ca6814\",\"assetId1\":\"a92e557a-542e-445f-a38e-9d3cd438110b\",\"assetId2\":\"951b9eda-f804-4bfe-a4e1-a648dd7b4fe7\",\"assetName1\":\"VSR3\",\"assetName2\":\"VSR6\",\"ifIndex1\":97,\"ifIndex2\":49,\"flowRatio1\":1,\"flowRatio2\":1,\"ifDescr1\":\"GigabitEthernet6/0\",\"ifDescr2\":\"GigabitEthernet3/0\",\"ifFlowIndex1\":97,\"ifFlowIndex2\":49,\"snmpIfHighSpeed\":\"1.0Gbps\"}",
                "linkType": 'null',
                "style": "{\"link.type\":\"parallel\",\"link.bundle.offset\":10,\"link.color\":\"#B8B8B8\",\"select.style\":\"border\",\"select.color\":\"#53D628\"}",
                "time": 1578279322096,
                "activeStandby": 0,
                "ifOperStatus": "up",
                "snmpIfHighSpeed": "1.0Gbps"
            }
        ],
        "linkAllEarlyWarningNum": 0,
        "linkAlertNum": 0
    },
    "success": True
}


debug_topo_data_old = {
  "result": {
    "isCreated": True,
    "linkNum": 11,
    "alertNum": 0,
    "nodes": [
      {
        "locationY": 342,
        "image": "router",
        "firstTypeId": 2,
        "secondTypeIdValue": "路由器",
        "locationX": 767,
        "netElementType": 7,
        "collectType": "SNMP",
        "firstTypeIdValue": "网络设备",
        "assetId": "f34f84c3-aa6b-4ec8-9bad-2b8f81fd9ee5",
        "assetNetAddress": "172.100.1.55",
        "width": 'null',
        "assetName": "PE4",
        "client": "{\"assetId\":\"f34f84c3-aa6b-4ec8-9bad-2b8f81fd9ee5\",\"assetNetAddress\":\"172.100.1.55\",\"netElementType\":7,\"secondTypeIdValue\":\"路由器\",\"collectType\":\"SNMP\"}",
        "style": 'null',
        "position": 'null',
        "height": 'null'
      },
  {
        "locationY": 335,
        "image": "router",
        "firstTypeId": 2,
        "secondTypeIdValue": "路由器",
        "locationX": 476,
        "netElementType": 7,
        "collectType": "SNMP",
        "firstTypeIdValue": "网络设备",
        "assetId": "64f8ca77-0d64-4418-bc33-35f11dabc3c7",
        "assetNetAddress": "172.100.1.53",
        "width": 'null',
        "assetName": "P2",
        "client": "{\"assetId\":\"64f8ca77-0d64-4418-bc33-35f11dabc3c7\",\"assetNetAddress\":\"172.100.1.53\",\"netElementType\":7,\"secondTypeIdValue\":\"路由器\",\"collectType\":\"SNMP\"}",
        "style": 'null',
        "position": 'null',
        "height": 'null'
      },
 {
        "locationY": 328,
        "image": "router",
        "firstTypeId": 2,
        "secondTypeIdValue": "路由器",
        "locationX": 249,
        "netElementType": 7,
        "collectType": "SNMP",
        "firstTypeIdValue": "网络设备",
        "assetId": "2b35d549-3dc8-4031-8743-ebdab0470ded",
        "assetNetAddress": "172.100.1.51",
        "width": 'null',
        "assetName": "PE2",
        "client": "{\"assetId\":\"2b35d549-3dc8-4031-8743-ebdab0470ded\",\"assetNetAddress\":\"172.100.1.51\",\"netElementType\":7,\"secondTypeIdValue\":\"路由器\",\"collectType\":\"SNMP\"}",
        "style": 'null',
        "position": 'null',
        "height": 'null'
      },
 {
        "locationY": 109,
        "image": "router",
        "firstTypeId": 2,
        "secondTypeIdValue": "路由器",
        "locationX": 771,
        "netElementType": 7,
        "collectType": "SNMP",
        "firstTypeIdValue": "网络设备",
        "assetId": "0c2ef3e4-581b-42d2-b7e3-e0c48638b645",
        "assetNetAddress": "172.100.1.54",
        "width": 'null',
        "assetName": "PE3",
        "client": "{\"assetId\":\"0c2ef3e4-581b-42d2-b7e3-e0c48638b645\",\"assetNetAddress\":\"172.100.1.54\",\"netElementType\":7,\"secondTypeIdValue\":\"路由器\",\"collectType\":\"SNMP\"}",
        "style": 'null',
        "position": 'null',
        "height": 'null'
      },
 {
        "locationY": 110,
        "image": "router",
        "firstTypeId": 2,
        "secondTypeIdValue": "路由器",
        "locationX": 481,
        "netElementType": 7,
        "collectType": "SNMP",
        "firstTypeIdValue": "网络设备",
        "assetId": "4ea1dd48-de95-428b-8180-3a9be2b47392",
        "assetNetAddress": "172.100.1.52",
        "width": 'null',
        "assetName": "P1",
        "client": "{\"assetId\":\"4ea1dd48-de95-428b-8180-3a9be2b47392\",\"assetNetAddress\":\"172.100.1.52\",\"netElementType\":7,\"secondTypeIdValue\":\"路由器\",\"collectType\":\"SNMP\"}",
        "style": 'null',
        "position": 'null',
        "height": 'null'
      },
{
        "locationY": 112,
        "image": "router",
        "firstTypeId": 2,
        "secondTypeIdValue": "路由器",
        "locationX": 250,
        "netElementType": 7,
        "collectType": "SNMP",
        "firstTypeIdValue": "网络设备",
        "assetId": "41ea97fa-ce74-4e0b-80fa-73cf6c49d877",
        "assetNetAddress": "172.100.1.50",
        "width": 'null',
        "assetName": "PE1",
        "client": "{\"assetId\":\"41ea97fa-ce74-4e0b-80fa-73cf6c49d877\",\"assetNetAddress\":\"172.100.1.50\",\"netElementType\":7,\"secondTypeIdValue\":\"路由器\",\"collectType\":\"SNMP\"}",
        "style": 'null',
        "position": 'null',
        "height": 'null'
      }
    ],
	"nodeNum": 6,
    "deviceAllAlertNum": 0,
    "links": [
 {
        "inputNetUsedRatioTotal": "0.02%",
        "assetId2": "4ea1dd48-de95-428b-8180-3a9be2b47392",
        "assetId1": "41ea97fa-ce74-4e0b-80fa-73cf6c49d877",
        "ifDescr1": "GigabitEthernet3/2/2",
        "source": 2,
        "ifDescr2": "GigabitEthernet3/2/2",
        "ifFlowIndex1": 314,
        "ifFlowIndex2": 314,
        "assetName2": "P1",
        "assetName1": "PE1",
        "flowRatio1": 1,
        "flowRatio2": 1,
        "linkId": "a3423880-d444-4fd5-99b9-e5f569c31231",
        "outputNetUsedRatioTotal": "9.19%",
        "ifIndex2": 314,
        "name": "PE1--P1",
        "ifIndex1": 314,
        "client": "{\"linkId\":\"a3423880-d444-4fd5-99b9-e5f569c31231\",\"assetId1\":\"41ea97fa-ce74-4e0b-80fa-73cf6c49d877\",\"assetId2\":\"4ea1dd48-de95-428b-8180-3a9be2b47392\",\"assetName1\":\"PE1\",\"assetName2\":\"P1\",\"ifIndex1\":314,\"ifIndex2\":314,\"flowRatio1\":1,\"flowRatio2\":1,\"ifDescr1\":\"GigabitEthernet3/2/2\",\"ifDescr2\":\"GigabitEthernet3/2/2\",\"ifFlowIndex1\":314,\"ifFlowIndex2\":314,\"snmpIfHighSpeed\":\"1.0Gbps\"}",
        "linkType": 'null',
        "style": "{\"link.type\":\"parallel\",\"link.bundle.offset\":10,\"link.color\":\"#B8B8B8\",\"select.style\":\"border\",\"select.color\":\"#53D628\"}",
        "time": 1570852136656,
        "activeStandby": 0,
        "ifOperStatus": "up",
        "snmpIfHighSpeed": "1.0Gbps"
      },
{
        "inputNetUsedRatioTotal": "0.02%",
        "assetId2": "0c2ef3e4-581b-42d2-b7e3-e0c48638b645",
        "assetId1": "4ea1dd48-de95-428b-8180-3a9be2b47392",
        "ifDescr1": "GigabitEthernet3/2/3",
        "source": 2,
        "ifDescr2": "GigabitEthernet3/1/2",
        "ifFlowIndex1": 315,
        "ifFlowIndex2": 290,
        "assetName2": "PE3",
        "assetName1": "P1",
        "flowRatio1": 1,
        "flowRatio2": 1,
        "linkId": "ba6382d7-8faf-41c2-86be-9d86c6c1a4fa",
        "outputNetUsedRatioTotal": "8.93%",
        "ifIndex2": 290,
        "name": "P1--PE3",
        "ifIndex1": 315,
        "client": "{\"linkId\":\"ba6382d7-8faf-41c2-86be-9d86c6c1a4fa\",\"assetId1\":\"4ea1dd48-de95-428b-8180-3a9be2b47392\",\"assetId2\":\"0c2ef3e4-581b-42d2-b7e3-e0c48638b645\",\"assetName1\":\"P1\",\"assetName2\":\"PE3\",\"ifIndex1\":315,\"ifIndex2\":290,\"flowRatio1\":1,\"flowRatio2\":1,\"ifDescr1\":\"GigabitEthernet3/2/3\",\"ifDescr2\":\"GigabitEthernet3/1/2\",\"ifFlowIndex1\":315,\"ifFlowIndex2\":290,\"snmpIfHighSpeed\":\"1.0Gbps\"}",
        "linkType": 'null',
        "style": "{\"link.type\":\"parallel\",\"link.bundle.offset\":10,\"link.color\":\"#B8B8B8\",\"select.style\":\"border\",\"select.color\":\"#53D628\"}",
        "time": 1570852136676,
        "activeStandby": 0,
        "ifOperStatus": "up",
        "snmpIfHighSpeed": "1.0Gbps"
      },
  {
        "inputNetUsedRatioTotal": "0.01%",
        "assetId2": "2b35d549-3dc8-4031-8743-ebdab0470ded",
        "assetId1": "41ea97fa-ce74-4e0b-80fa-73cf6c49d877",
        "ifDescr1": "GigabitEthernet3/2/1",
        "source": 2,
        "ifDescr2": "GigabitEthernet3/2/1",
        "ifFlowIndex1": 313,
        "ifFlowIndex2": 313,
        "assetName2": "PE2",
        "assetName1": "PE1",
        "flowRatio1": 1,
        "flowRatio2": 1,
        "linkId": "6229e610-7ed7-4ba7-aa49-49f7a8e38199",
        "outputNetUsedRatioTotal": "0.01%",
        "ifIndex2": 313,
        "name": "PE1--PE2",
        "ifIndex1": 313,
        "client": "{\"assetId1\":\"41ea97fa-ce74-4e0b-80fa-73cf6c49d877\",\"assetName1\":\"PE1\",\"assetId2\":\"2b35d549-3dc8-4031-8743-ebdab0470ded\",\"assetName2\":\"PE2\",\"flowRatio1\":'null',\"ifIndex1\":313,\"ifDescr1\":\"GigabitEthernet3/2/1\",\"ifFlowIndex1\":313,\"ifIndex2\":313,\"ifDescr2\":\"GigabitEthernet3/2/1\",\"ifFlowIndex2\":313}",
        "linkType": 'null',
        "style": "{\"link.type\":\"parallel\",\"link.bundle.offset\":10,\"link.color\":\"#B8B8B8\",\"select.style\":\"border\",\"select.color\":\"#53D628\"}",
        "time": 1571137875835,
        "activeStandby": 0,
        "ifOperStatus": "up",
        "snmpIfHighSpeed": "1.0Gbps"
      },
 {
        "inputNetUsedRatioTotal": "0.01%",
        "assetId2": "64f8ca77-0d64-4418-bc33-35f11dabc3c7",
        "assetId1": "2b35d549-3dc8-4031-8743-ebdab0470ded",
        "ifDescr1": "GigabitEthernet3/2/2",
        "source": 2,
        "ifDescr2": "GigabitEthernet3/2/2",
        "ifFlowIndex1": 314,
        "ifFlowIndex2": 314,
        "assetName2": "P2",
        "assetName1": "PE2",
        "flowRatio1": 1,
        "flowRatio2": 1,
        "linkId": "71ba3e2d-735b-4da0-948f-4e68cfe35376",
        "outputNetUsedRatioTotal": "0.01%",
        "ifIndex2": 314,
        "name": "PE2--P2",
        "ifIndex1": 314,
        "client": "{\"assetId1\":\"2b35d549-3dc8-4031-8743-ebdab0470ded\",\"assetName1\":\"PE2\",\"assetId2\":\"64f8ca77-0d64-4418-bc33-35f11dabc3c7\",\"assetName2\":\"P2\",\"ifIndex1\":314,\"ifDescr1\":\"GigabitEthernet3/2/2\",\"ifFlowIndex1\":314,\"ifIndex2\":314,\"ifDescr2\":\"GigabitEthernet3/2/2\",\"ifFlowIndex2\":314}",
        "linkType": 'null',
        "style": "{\"link.type\":\"parallel\",\"link.bundle.offset\":10,\"link.color\":\"#B8B8B8\",\"select.style\":\"border\",\"select.color\":\"#53D628\"}",
        "time": 1571137875846,
        "activeStandby": 0,
        "ifOperStatus": "up",
        "snmpIfHighSpeed": "1.0Gbps"
      },
   {
        "inputNetUsedRatioTotal": "0.01%",
        "assetId2": "f34f84c3-aa6b-4ec8-9bad-2b8f81fd9ee5",
        "assetId1": "64f8ca77-0d64-4418-bc33-35f11dabc3c7",
        "ifDescr1": "GigabitEthernet3/2/3",
        "source": 2,
        "ifDescr2": "GigabitEthernet3/1/2",
        "ifFlowIndex1": 315,
        "ifFlowIndex2": 290,
        "assetName2": "PE4",
        "assetName1": "P2",
        "flowRatio1": 1,
        "flowRatio2": 1,
        "linkId": "a5fc9213-d8d8-4179-a519-05a9ea8e8aac",
        "outputNetUsedRatioTotal": "0.01%",
        "ifIndex2": 290,
        "name": "P2--PE4",
        "ifIndex1": 315,
        "client": "{\"assetId1\":\"64f8ca77-0d64-4418-bc33-35f11dabc3c7\",\"assetName1\":\"P2\",\"assetId2\":\"f34f84c3-aa6b-4ec8-9bad-2b8f81fd9ee5\",\"assetName2\":\"PE4\",\"ifIndex1\":315,\"ifDescr1\":\"GigabitEthernet3/2/3\",\"ifFlowIndex1\":315,\"ifIndex2\":290,\"ifDescr2\":\"GigabitEthernet3/1/2\",\"ifFlowIndex2\":290}",
        "linkType": 'null',
        "style": "{\"link.type\":\"parallel\",\"link.bundle.offset\":10,\"link.color\":\"#B8B8B8\",\"select.style\":\"border\",\"select.color\":\"#53D628\"}",
        "time": 1571137875852,
        "activeStandby": 0,
        "ifOperStatus": "up",
        "snmpIfHighSpeed": "1.0Gbps"
      },
 {
        "inputNetUsedRatioTotal": "0.01%",
        "assetId2": "f34f84c3-aa6b-4ec8-9bad-2b8f81fd9ee5",
        "assetId1": "0c2ef3e4-581b-42d2-b7e3-e0c48638b645",
        "ifDescr1": "GigabitEthernet3/1/1",
        "source": 2,
        "ifDescr2": "GigabitEthernet3/1/1",
        "ifFlowIndex1": 289,
        "ifFlowIndex2": 289,
        "assetName2": "PE4",
        "assetName1": "PE3",
        "flowRatio1": 1,
        "flowRatio2": 1,
        "linkId": "d481b0da-fb4b-4aa7-8528-8bfde4da961f",
        "outputNetUsedRatioTotal": "0.01%",
        "ifIndex2": 289,
        "name": "PE3--PE4",
        "ifIndex1": 289,
        "client": "{\"assetId1\":\"0c2ef3e4-581b-42d2-b7e3-e0c48638b645\",\"assetName1\":\"PE3\",\"assetId2\":\"f34f84c3-aa6b-4ec8-9bad-2b8f81fd9ee5\",\"assetName2\":\"PE4\",\"ifIndex1\":289,\"ifDescr1\":\"GigabitEthernet3/1/1\",\"ifFlowIndex1\":289,\"ifIndex2\":289,\"ifDescr2\":\"GigabitEthernet3/1/1\",\"ifFlowIndex2\":289}",
        "linkType": 'null',
        "style": "{\"link.type\":\"parallel\",\"link.bundle.offset\":10,\"link.color\":\"#B8B8B8\",\"select.style\":\"border\",\"select.color\":\"#53D628\"}",
        "time": 1571137875856,
        "activeStandby": 0,
        "ifOperStatus": "up",
        "snmpIfHighSpeed": "1.0Gbps"
      },
 {
        "inputNetUsedRatioTotal": "0.01%",
        "assetId2": "64f8ca77-0d64-4418-bc33-35f11dabc3c7",
        "assetId1": "4ea1dd48-de95-428b-8180-3a9be2b47392",
        "ifDescr1": "GigabitEthernet3/2/1",
        "source": 2,
        "ifDescr2": "GigabitEthernet3/2/1",
        "ifFlowIndex1": 313,
        "ifFlowIndex2": 313,
        "assetName2": "P2",
        "assetName1": "P1",
        "flowRatio1": 1,
        "flowRatio2": 1,
        "linkId": "169acacf-a984-417d-b1c3-cf8404ef6a1d",
        "outputNetUsedRatioTotal": "0.01%",
        "ifIndex2": 313,
        "name": "P1--P2",
        "ifIndex1": 313,
        "client": "{\"assetId1\":\"4ea1dd48-de95-428b-8180-3a9be2b47392\",\"assetName1\":\"P1\",\"assetId2\":\"64f8ca77-0d64-4418-bc33-35f11dabc3c7\",\"assetName2\":\"P2\",\"ifIndex1\":313,\"ifDescr1\":\"GigabitEthernet3/2/1\",\"ifFlowIndex1\":313,\"ifIndex2\":313,\"ifDescr2\":\"GigabitEthernet3/2/1\",\"ifFlowIndex2\":313}",
        "linkType": 'null',
        "style": "{\"link.type\":\"parallel\",\"link.bundle.offset\":10,\"link.color\":\"#B8B8B8\",\"select.style\":\"border\",\"select.color\":\"#53D628\"}",
        "time": 1571137875863,
        "activeStandby": 0,
        "ifOperStatus": "up",
        "snmpIfHighSpeed": "1.0Gbps"
      },
 {
        "inputNetUsedRatioTotal": "0.01%",
        "assetId2": "4ea1dd48-de95-428b-8180-3a9be2b47392",
        "assetId1": "2b35d549-3dc8-4031-8743-ebdab0470ded",
        "ifDescr1": "GigabitEthernet3/2/3",
        "source": 2,
        "ifDescr2": "GigabitEthernet3/2/4",
        "ifFlowIndex1": 315,
        "ifFlowIndex2": 316,
        "assetName2": "P1",
        "assetName1": "PE2",
        "flowRatio1": 1,
        "flowRatio2": 1,
        "linkId": "a8eef786-31fe-4319-a269-06381ae36a4a",
        "outputNetUsedRatioTotal": "0.01%",
        "ifIndex2": 316,
        "name": "PE2--P1",
        "ifIndex1": 315,
        "client": "{\"assetId1\":\"2b35d549-3dc8-4031-8743-ebdab0470ded\",\"assetName1\":\"PE2\",\"assetId2\":\"4ea1dd48-de95-428b-8180-3a9be2b47392\",\"assetName2\":\"P1\",\"ifIndex1\":315,\"ifDescr1\":\"GigabitEthernet3/2/3\",\"ifFlowIndex1\":315,\"ifIndex2\":316,\"ifDescr2\":\"GigabitEthernet3/2/4\",\"ifFlowIndex2\":316}",
        "linkType": 'null',
        "style": "{\"link.type\":\"parallel\",\"link.bundle.offset\":10,\"link.color\":\"#B8B8B8\",\"select.style\":\"border\",\"select.color\":\"#53D628\"}",
        "time": 1571137875872,
        "activeStandby": 0,
        "ifOperStatus": "up",
        "snmpIfHighSpeed": "1.0Gbps"
      },
    {
        "inputNetUsedRatioTotal": "0.01%",
        "assetId2": "64f8ca77-0d64-4418-bc33-35f11dabc3c7",
        "assetId1": "41ea97fa-ce74-4e0b-80fa-73cf6c49d877",
        "ifDescr1": "GigabitEthernet3/2/3",
        "source": 2,
        "ifDescr2": "GigabitEthernet3/2/4",
        "ifFlowIndex1": 315,
        "ifFlowIndex2": 316,
        "assetName2": "P2",
        "assetName1": "PE1",
        "flowRatio1": 1,
        "flowRatio2": 1,
        "linkId": "90c3f686-aae8-4c6e-8b70-af497cc8acb8",
        "outputNetUsedRatioTotal": "0.01%",
        "ifIndex2": 316,
        "name": "PE1--P2",
        "ifIndex1": 315,
        "client": "{\"assetId1\":\"41ea97fa-ce74-4e0b-80fa-73cf6c49d877\",\"assetName1\":\"PE1\",\"assetId2\":\"64f8ca77-0d64-4418-bc33-35f11dabc3c7\",\"assetName2\":\"P2\",\"ifIndex1\":315,\"ifDescr1\":\"GigabitEthernet3/2/3\",\"ifFlowIndex1\":315,\"ifIndex2\":316,\"ifDescr2\":\"GigabitEthernet3/2/4\",\"ifFlowIndex2\":316}",
        "linkType": 'null',
        "style": "{\"link.type\":\"parallel\",\"link.bundle.offset\":10,\"link.color\":\"#B8B8B8\",\"select.style\":\"border\",\"select.color\":\"#53D628\"}",
        "time": 1571137875876,
        "activeStandby": 0,
        "ifOperStatus": "up",
        "snmpIfHighSpeed": "1.0Gbps"
      },
  {
        "inputNetUsedRatioTotal": "0.01%",
        "assetId2": "0c2ef3e4-581b-42d2-b7e3-e0c48638b645",
        "assetId1": "64f8ca77-0d64-4418-bc33-35f11dabc3c7",
        "ifDescr1": "GigabitEthernet3/2/5",
        "source": 2,
        "ifDescr2": "GigabitEthernet3/1/3",
        "ifFlowIndex1": 317,
        "ifFlowIndex2": 291,
        "assetName2": "PE3",
        "assetName1": "P2",
        "flowRatio1": 1,
        "flowRatio2": 1,
        "linkId": "8cd2c8f8-a469-4f4f-8d4a-f69d91d9d67b",
        "outputNetUsedRatioTotal": "0.01%",
        "ifIndex2": 291,
        "name": "P2--PE3",
        "ifIndex1": 317,
        "client": "{\"assetId1\":\"64f8ca77-0d64-4418-bc33-35f11dabc3c7\",\"assetName1\":\"P2\",\"assetId2\":\"0c2ef3e4-581b-42d2-b7e3-e0c48638b645\",\"assetName2\":\"PE3\",\"ifIndex1\":317,\"ifDescr1\":\"GigabitEthernet3/2/5\",\"ifFlowIndex1\":317,\"ifIndex2\":291,\"ifDescr2\":\"GigabitEthernet3/1/3\",\"ifFlowIndex2\":291}",
        "linkType": 'null',
        "style": "{\"link.type\":\"parallel\",\"link.bundle.offset\":10,\"link.color\":\"#B8B8B8\",\"select.style\":\"border\",\"select.color\":\"#53D628\"}",
        "time": 1571137875883,
        "activeStandby": 0,
        "ifOperStatus": "up",
        "snmpIfHighSpeed": "1.0Gbps"
      },
 {
        "inputNetUsedRatioTotal": "0.01%",
        "assetId2": "f34f84c3-aa6b-4ec8-9bad-2b8f81fd9ee5",
        "assetId1": "4ea1dd48-de95-428b-8180-3a9be2b47392",
        "ifDescr1": "GigabitEthernet3/2/5",
        "source": 2,
        "ifDescr2": "GigabitEthernet3/1/3",
        "ifFlowIndex1": 317,
        "ifFlowIndex2": 291,
        "assetName2": "PE4",
        "assetName1": "P1",
        "flowRatio1": 1,
        "flowRatio2": 1,
        "linkId": "e954a5ad-afc8-4178-9c18-4c772527c41a",
        "outputNetUsedRatioTotal": "0.01%",
        "ifIndex2": 291,
        "name": "P1--PE4",
        "ifIndex1": 317,
        "client": "{\"assetId1\":\"4ea1dd48-de95-428b-8180-3a9be2b47392\",\"assetName1\":\"P1\",\"assetId2\":\"f34f84c3-aa6b-4ec8-9bad-2b8f81fd9ee5\",\"assetName2\":\"PE4\",\"ifIndex1\":317,\"ifDescr1\":\"GigabitEthernet3/2/5\",\"ifFlowIndex1\":317,\"ifIndex2\":291,\"ifDescr2\":\"GigabitEthernet3/1/3\",\"ifFlowIndex2\":291}",
        "linkType": 'null',
        "style": "{\"link.type\":\"parallel\",\"link.bundle.offset\":10,\"link.color\":\"#B8B8B8\",\"select.style\":\"border\",\"select.color\":\"#53D628\"}",
        "time": 1571137875889,
        "activeStandby": 0,
        "ifOperStatus": "up",
        "snmpIfHighSpeed": "1.0Gbps"
      }
    ],
	"linkAllEarlyWarningNum": 0,
    "linkAlertNum": 0
  },
  "success": True
}


sdn_global_data = {'affinityEnable': 0, 'firstThresholdPercent': 100, 'reservedBandwidthPercent': 80, 'globalScheduleEnable': 1, 'calcLimit': 0, 'secondThresholdPercent': 100, 'pathOptimizeStrategy': 'sysContinuedOptimize', 'srlgEnable': 0}


port_ip_node_id = {'0105d773-ee52-415d-a76e-8e3a5441c94c': {'message': '', 'data': [{'mask': '255.255.255.0', 'ifIndex': 1, 'ip': '156.10.10.2'}, {'mask': '255.255.255.0', 'ifIndex': 2, 'ip': '139.10.10.5'}], 'errorCode': 0}, 'cd38f11b-ce6e-4058-bbc6-4a9f89264f63': {'message': '', 'data': [{'mask': '255.255.255.0', 'ifIndex': 1, 'ip': '192.100.100.2'}, {'mask': '255.255.255.0', 'ifIndex': 2, 'ip': '156.10.10.3'}], 'errorCode': 0}, '687b2666-e16c-4a7d-b67d-705d7760714b': {'message': '', 'data': [{'mask': '255.255.255.0', 'ifIndex': 1, 'ip': '192.100.100.3'}, {'mask': '255.255.255.0', 'ifIndex': 2, 'ip': '186.10.10.3'}], 'errorCode': 0}, '5e114946-638f-459e-80e3-2da37eff98e3': {'message': '', 'data': [{'mask': '255.255.255.0', 'ifIndex': 3, 'ip': '192.30.30.2'}, {'mask': '255.255.255.0', 'ifIndex': 17, 'ip': '192.20.20.3'}], 'errorCode': 0}, 'ed860291-29b9-4be7-894e-682a62009f5f': {'message': '', 'data': [{'mask': '255.255.255.0', 'ifIndex': 3, 'ip': '192.30.30.3'}, {'mask': '255.255.255.0', 'ifIndex': 7, 'ip': '192.50.50.2'}], 'errorCode': 0}, 'fdba8a1d-6fb7-4de5-9630-1ca0a14ee3fd': {'message': '', 'data': [{'mask': '255.255.255.0', 'ifIndex': 1, 'ip': '158.50.50.2'}, {'mask': '255.255.255.0', 'ifIndex': 2, 'ip': '172.40.40.5'}, {'mask': '255.255.255.0', 'ifIndex': 3, 'ip': '142.100.100.8'}], 'errorCode': 0}, '3dbc31f6-27f6-4228-bb7a-d8945615503e': {'message': '', 'data': [{'mask': '255.255.255.0', 'ifIndex': 1, 'ip': '101.70.70.2'}, {'mask': '255.255.255.0', 'ifIndex': 2, 'ip': '184.100.100.9'}, {'mask': '255.255.255.0', 'ifIndex': 3, 'ip': '157.20.20.3'}], 'errorCode': 0}, '67588303-3ee5-4531-9026-6c6b666cb853': {'message': '', 'data': [{'mask': '255.255.255.0', 'ifIndex': 7, 'ip': '192.50.50.3'}], 'errorCode': 0}, '1c9c565e-e37b-47b4-b8e2-40e2fe757b66': {'message': '', 'data': [{'mask': '255.255.255.0', 'ifIndex': 3, 'ip': '192.10.10.2'}, {'mask': '255.255.255.0', 'ifIndex': 24, 'ip': '139.10.10.3'}], 'errorCode': 0}, '6220d79e-7fba-428e-81fd-5decdd359e3e': {'message': '', 'data': [{'mask': '255.255.255.0', 'ifIndex': 1, 'ip': '157.20.20.2'}, {'mask': '255.255.255.0', 'ifIndex': 2, 'ip': '112.10.10.3'}, {'mask': '255.255.255.0', 'ifIndex': 3, 'ip': '142.100.100.9'}], 'errorCode': 0}, '98b9e299-2d0e-41a0-9b2e-57f6afaf2440': {'message': '', 'data': [{'mask': '255.255.255.0', 'ifIndex': 1, 'ip': '112.10.10.4'}, {'mask': '255.255.255.0', 'ifIndex': 2, 'ip': '194.10.10.2'}, {'mask': '255.255.255.0', 'ifIndex': 3, 'ip': '143.100.100.7'}], 'errorCode': 0}, 'd8a6c86b-67ec-4913-87d6-c4a06f505842': {'message': '', 'data': [{'mask': '255.255.255.0', 'ifIndex': 1, 'ip': '186.10.10.4'}, {'mask': '255.255.255.0', 'ifIndex': 2, 'ip': '172.40.40.2'}, {'mask': '255.255.255.0', 'ifIndex': 3, 'ip': '143.100.100.5'}], 'errorCode': 0}, 'b2be3a0e-3a52-4a56-a808-f3861483f1de': {'message': '', 'data': [{'mask': '255.255.255.0', 'ifIndex': 1, 'ip': '194.10.10.5'}, {'mask': '255.255.255.0', 'ifIndex': 3, 'ip': '101.70.70.6'}], 'errorCode': 0}, '187be7be-1f9e-43ca-abe0-662036764ea8': {'message': '', 'data': [{'mask': '255.255.255.0', 'ifIndex': 3, 'ip': '192.10.10.3'}, {'mask': '255.255.255.0', 'ifIndex': 17, 'ip': '192.20.20.2'}], 'errorCode': 0}, 'ae7798ff-a5c3-4f6c-83e8-2428b5f24fd3': {'message': '', 'data': [{'mask': '255.255.255.0', 'ifIndex': 2, 'ip': '158.50.50.5'}, {'mask': '255.255.255.0', 'ifIndex': 3, 'ip': '184.100.100.6'}], 'errorCode': 0}}

sna_topology_data = {'output': {'topos': [{'description': 'vxlan-vpn', 'topoId': '989bf05e-385c-4923-af54-3cd70acf0295', 'topoName': 'vxlan-vpn'}, {'topoNodes': [{'nodeId': '8acb51db-e2d6-4a53-a74e-9ff272f653de'}, {'nodeId': 'd235cae2-848e-404c-88e3-1576668834cc'}, {'nodeId': 'ea5620bc-32ee-46ea-8011-6e0c495d9a7b'}, {'nodeId': 'c62b5cf9-08d7-4217-9b51-d1a7fabf2d8a'}, {'nodeId': '211b0abe-dad8-46fe-9bbd-6d2abfd65d97'}, {'nodeId': 'a969e5d2-e31c-4d02-afe9-c49c5ac05270'}, {'nodeId': '04165eb6-48f0-4e7f-aa08-3e0967fda9a5'}, {'nodeId': '91ecc1ea-b09a-4b1c-add3-f596d87b4843'}, {'nodeId': '65fa4986-4ac6-4438-a168-8e32e0e69a18'}, {'nodeId': '5fc7e69a-709b-409d-b1e9-093c02394d5a'}, {'nodeId': 'a92e557a-542e-445f-a38e-9d3cd438110b'}, {'nodeId': '951b9eda-f804-4bfe-a4e1-a648dd7b4fe7'}, {'nodeId': 'a7e591c4-23ad-4245-9614-ae33b769c1d4'}, {'nodeId': 'bb0e3e1d-7541-4a59-80e6-b55d9ae3d4ac'}, {'nodeId': '8c163703-cd34-49fa-b69d-e89866614405'}, {'nodeId': '0006c91d-0d48-470c-8070-0ca22ff174b0'}, {'nodeId': '49933ff8-3c61-4bb8-a559-46e072744763'}], 'description': 'underLay topology', 'topoId': 'example-linkstate-topology', 'topoName': 'underLay topology', 'topoLinks': [{'LinkId': '49451261-f38b-491b-b862-97330980f2a5'}, {'LinkId': '3490f918-c557-4d73-a283-91fe6779d417'}, {'LinkId': '31c18cbc-4d8f-400a-a135-fd99492e7f07'}, {'LinkId': '166eab8f-b8da-4b52-ad3f-104d1699ad17'}, {'LinkId': 'e06f12d1-4da3-41f2-82a2-f16662fd3703'}, {'LinkId': '70841762-dc20-449c-8b2c-2b47bf1bb70c'}, {'LinkId': '36d6c757-9d8d-4748-ad84-734eb691e638'}, {'LinkId': '31bcd6f2-8f39-49d4-aa8a-a7793be297f1'}, {'LinkId': '69c95b93-9c59-471b-8d51-441f1e8193fb'}, {'LinkId': 'a513e0c7-b134-47fc-b4cf-1b8e7f8e0f33'}, {'LinkId': '6308d6ad-eb76-41db-8e92-85672f533c32'}, {'LinkId': '27f06554-6854-412e-8f6d-5758a2c43075'}, {'LinkId': '8737a1e0-c05c-4ce4-8043-6a17d0484171'}, {'LinkId': '3ca74a78-b8a1-4a15-94c7-2bdd729496bd'}, {'LinkId': '39105d81-86b0-4522-a822-339768a9200b'}, {'LinkId': '45aaf289-e8fc-4619-acbe-84820b6c3194'}, {'LinkId': '6bb45218-bb58-4adc-aa28-f085fdd1ec62'}, {'LinkId': '9d7bc3d2-b550-4e34-aca6-3891fbe5f254'}, {'LinkId': 'd277c528-36c3-449b-a409-5c301acf33c6'}, {'LinkId': '3b71a3a2-7bdf-4e31-92dd-948bd08c2b20'}, {'LinkId': 'e02d9152-a8c1-4b2a-a759-bd1401c31dba'}, {'LinkId': '534f5e43-a493-42a6-a29f-57b199b73f6e'}]}]}}

sna_topology_data_old = {
  "output": {
    "topos": [
      {
        "topoId": "0983ad63-5832-4999-9b48-f9058a2a5fac",
        "description": "vxlan-vpn",
        "topoName": "vxlan-vpn"
      },
      {
        "topoId": "example-linkstate-topology",
        "description": "underLay topology",
        "topoLinks": [
          {
            "LinkId": "0e9fd576-10bf-475a-bf41-da1d683dc356"
          },
          {
            "LinkId": "40db4afe-1337-490a-824e-6d0e5cd6fe19"
          },
          {
            "LinkId": "6ba6a58c-54b5-40a6-9a20-812e5ad254b8"
          },
          {
            "LinkId": "bdb460ba-c408-4693-b3ae-f8dcfd90d8a4"
          },
          {
            "LinkId": "4b62f1d4-9cef-4db2-8085-b4760042afe7"
          },
          {
            "LinkId": "db835f07-3ae6-43f8-9ba9-24dfef46513b"
          },
          {
            "LinkId": "2594f424-89a5-4673-bb25-52a20d0b3dd6"
          },
          {
            "LinkId": "3d8dc8c2-9e32-492e-a3b0-c788ae62ebdb"
          },
          {
            "LinkId": "00f0f007-9cf2-492b-8747-cac5035b81da"
          },
          {
            "LinkId": "a323de9c-665d-4cdb-95e0-e69d3dd92e3a"
          },
          {
			"LinkId": "b972ff48-5fbe-4514-8378-3388969ec032"
          },
          {
            "LinkId": "bc16d72f-c284-4e48-96fb-5e9eb4894efe"
          },
          {
            "LinkId": "7b8b8a2c-c8e4-46ba-8c25-24fa3b4c4089"
          },
          {
            "LinkId": "9735b71f-380d-4bf3-91e6-eba6e15902bb"
          },
          {
            "LinkId": "3095c1c7-5f87-4ffd-9122-992733046082"
          },
          {
            "LinkId": "6133946c-9030-4cd4-b518-53b68386344c"
          },
          {
            "LinkId": "933c1acd-d0ed-4aa0-b600-8ef506610611"
          },
          {
	        "LinkId": "5a43e5c6-f99a-4217-b3cf-a76cb54c198e"
          },
          {
            "LinkId": "6bfbf637-2020-4d7d-b027-da6fae977d45"
          },
          {
            "LinkId": "0db2e099-6487-4ac8-ab0d-387d0ce3c432"
          },
          {
            "LinkId": "9db2814c-6751-4c13-b79a-3656fd5eaf94"
          },
          {
            "LinkId": "d53b4a65-fd52-4162-9906-67f4631f55fb"
          }
        ],
        "topoName": "underLay topology",
        "topoNodes": [
          {
            "nodeId": "95390e43-74e3-4910-8e14-f2720711f6e3"
          },
          {
           "nodeId": "d3501601-faed-4d5d-b57b-e528dc1e266e"
          },
          {
            "nodeId": "ffdce32e-97dc-4b39-88c0-f6a494e59658"
          },
          {
            "nodeId": "3716b792-59ad-4035-87b5-6a10289fab7b"
          },
          {
            "nodeId": "a835c187-7c1d-4452-8139-d8d6eecb9cc3"
          },
          {
            "nodeId": "375e2205-da93-4349-a120-571de7496738"
          }
        ]
      }
    ]
  }
}

def data_b46131aecfa6():
    data ={
        "meanSpeedB": random.randint(850,1020),
        "A": [
            {
                "time": "2019-07-15 10:20",
                "outUseRatioList": "",
                "loseRatioList": "",
                "outSpeedList": ""
            },
            {
                "time": "2019-07-15 10:22",
                "outUseRatioList": "",
                "loseRatioList": "",
                "outSpeedList": ""
            },
            {
                "time": "2019-07-15 10:24",
                "outUseRatioList": "",
                "loseRatioList": "",
                "outSpeedList": ""
            },
            {
                "time": "2019-07-15 10:26",
                "outUseRatioList": "",
                "loseRatioList": "",
                "outSpeedList": ""
            },
            {
                "time": "2019-07-15 10:28",
                "outUseRatioList": "",
                "loseRatioList": "",
                "outSpeedList": ""
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 10:30",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "176.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 10:32",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 10:34",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 10:36",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 10:38",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 10:40",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 10:42",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 10:44",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 10:46",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "200.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 10:48",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 10:50",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 10:52",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "168.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 10:54",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "160.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 10:56",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "168.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 10:58",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "176.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 11:00",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 11:02",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "96.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 11:04",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 11:06",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "192.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 11:08",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 11:10",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 11:12",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 11:14",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "200.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 11:16",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 11:18",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 11:20",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 11:22",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "168.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 11:24",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "168.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 11:26",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "176.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 11:28",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 11:30",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 11:32",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 11:34",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 11:36",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 11:38",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 11:40",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 11:42",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "200.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 11:44",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 11:46",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 11:48",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 11:50",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "176.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 11:52",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 11:54",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 11:56",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 11:58",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 12:00",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 12:02",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 12:04",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 12:06",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 12:08",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 12:10",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "184.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 12:12",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 12:14",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 12:16",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 12:18",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "176.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 12:20",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 12:22",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 12:24",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 12:26",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 12:28",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 12:30",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 12:32",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 12:34",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 12:36",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 12:38",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 12:40",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "160.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 12:42",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 12:44",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 12:46",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "168.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 12:48",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "176.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 12:50",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 12:52",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 12:54",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 12:56",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 12:58",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 13:00",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 13:02",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 13:04",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 13:06",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 13:08",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 13:10",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 13:12",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 13:14",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "184.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 13:16",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "176.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 13:18",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 13:20",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 13:22",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "160.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 13:24",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "160.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 13:26",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 13:28",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 13:30",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 13:32",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 13:34",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 13:36",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "160.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 13:38",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "160.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 13:40",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 13:42",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "168.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 13:44",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "176.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 13:46",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "168.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 13:48",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "176.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 13:50",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 13:52",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 13:54",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 13:56",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 13:58",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "160.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 14:00",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 14:02",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 14:04",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "184.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 14:06",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 14:08",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 14:10",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "168.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 14:12",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "160.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 14:14",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "168.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 14:16",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "176.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 14:18",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 14:20",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 14:22",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 14:24",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 14:26",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 14:28",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 14:30",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 14:32",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "208.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 14:34",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "192.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 14:36",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 14:38",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "168.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 14:40",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "160.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 14:42",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "168.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 14:44",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "176.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 14:46",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 14:48",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 14:50",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 14:52",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 14:54",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 14:56",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "160.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 14:58",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 15:00",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "200.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 15:02",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 15:04",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 15:06",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 15:08",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "160.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 15:10",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "168.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 15:12",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 15:14",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 15:16",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "160.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 15:18",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 15:20",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 15:22",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 15:24",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 15:26",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 15:28",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "192.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 15:30",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 15:32",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 15:34",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 15:36",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "176.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 15:38",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 15:40",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 15:42",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 15:44",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "160.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 15:46",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 15:48",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 15:50",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 15:52",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 15:54",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 15:56",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "160.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 15:58",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 16:00",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 16:02",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 16:04",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "168.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 16:06",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "176.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 16:08",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 16:10",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 16:12",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 16:14",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "160.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 16:16",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 16:18",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 16:20",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 16:22",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 16:24",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 16:26",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 16:28",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 16:30",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 16:32",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "184.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 16:34",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "176.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 16:36",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 16:38",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 16:40",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 16:42",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 16:44",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 16:46",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 16:48",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 16:50",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 16:52",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "160.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 16:54",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 16:56",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 16:58",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 17:00",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "184.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 17:02",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "176.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 17:04",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "168.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 17:06",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "176.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 17:08",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 17:10",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 17:12",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "160.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 17:14",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 17:16",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 17:18",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 17:20",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 17:22",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "176.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 17:24",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 17:26",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 17:28",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "168.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 17:30",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "176.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 17:32",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "176.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 17:34",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "176.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 17:36",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 17:38",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 17:40",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 17:42",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 17:44",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 17:46",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 17:48",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 17:50",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "200.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 17:52",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 17:54",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 17:56",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "168.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 17:58",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "160.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 18:00",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "168.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 18:02",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "176.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 18:04",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 18:06",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "160.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 18:08",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 18:10",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 18:12",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "104.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 18:14",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 18:16",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 18:18",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "200.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 18:20",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 18:22",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 18:24",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 18:26",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "160.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 18:28",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "168.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 18:30",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "184.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 18:32",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 18:34",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 18:36",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 18:38",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 18:40",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 18:42",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 18:44",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 18:46",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "192.00"
            },
            {
                "time": "2019-07-15 18:48",
                "outUseRatioList": "",
                "loseRatioList": "",
                "outSpeedList": ""
            },
            {
                "time": "2019-07-15 18:50",
                "outUseRatioList": "",
                "loseRatioList": "",
                "outSpeedList": ""
            }
        ],
        "meanSpeedAUnit": "bps",
        "B": [
            {
                "time": "2019-07-15 10:20",
                "outUseRatioList": "",
                "loseRatioList": "",
                "outSpeedList": ""
            },
            {
                "time": "2019-07-15 10:22",
                "outUseRatioList": "",
                "loseRatioList": "",
                "outSpeedList": ""
            },
            {
                "time": "2019-07-15 10:24",
                "outUseRatioList": "",
                "loseRatioList": "",
                "outSpeedList": ""
            },
            {
                "time": "2019-07-15 10:26",
                "outUseRatioList": "",
                "loseRatioList": "",
                "outSpeedList": ""
            },
            {
                "time": "2019-07-15 10:28",
                "outUseRatioList": "",
                "loseRatioList": "",
                "outSpeedList": ""
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 10:30",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "168.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 10:32",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 10:34",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 10:36",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 10:38",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 10:40",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 10:42",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 10:44",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 10:46",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "200.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 10:48",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 10:50",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 10:52",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "168.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 10:54",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "168.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 10:56",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "184.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 10:58",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "176.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 11:00",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 11:02",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 11:04",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 11:06",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 11:08",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 11:10",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 11:12",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 11:14",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "200.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 11:16",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 11:18",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 11:20",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 11:22",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "176.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 11:24",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "184.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 11:26",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "176.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 11:28",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "160.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 11:30",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 11:32",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 11:34",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 11:36",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 11:38",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 11:40",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 11:42",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "208.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 11:44",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 11:46",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 11:48",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "192.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 11:50",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "184.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 11:52",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 11:54",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 11:56",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 11:58",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 12:00",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 12:02",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 12:04",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 12:06",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 12:08",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 12:10",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "176.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 12:12",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 12:14",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 12:16",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 12:18",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "184.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 12:20",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 12:22",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 12:24",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 12:26",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 12:28",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 12:30",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 12:32",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 12:34",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 12:36",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 12:38",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "144.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 12:40",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "160.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 12:42",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "160.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 12:44",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 12:46",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "176.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 12:48",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "176.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 12:50",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 12:52",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 12:54",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 12:56",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 12:58",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 13:00",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 13:02",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 13:04",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 13:06",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 13:08",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 13:10",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 13:12",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 13:14",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "192.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 13:16",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "176.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 13:18",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 13:20",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 13:22",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 13:24",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 13:26",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 13:28",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 13:30",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 13:32",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 13:34",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 13:36",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "168.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 13:38",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "160.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 13:40",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 13:42",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "168.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 13:44",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "176.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 13:46",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "184.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 13:48",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "176.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 13:50",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 13:52",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 13:54",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 13:56",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 13:58",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "160.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 14:00",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 14:02",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 14:04",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "192.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 14:06",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 14:08",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 14:10",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "168.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 14:12",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 14:14",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "184.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 14:16",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "168.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 14:18",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 14:20",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 14:22",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 14:24",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 14:26",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 14:28",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 14:30",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 14:32",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "200.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 14:34",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 14:36",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 14:38",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "168.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 14:40",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "168.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 14:42",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "184.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 14:44",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "168.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 14:46",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 14:48",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 14:50",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 14:52",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 14:54",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 14:56",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "160.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 14:58",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "160.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 15:00",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "192.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 15:02",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "160.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 15:04",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 15:06",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 15:08",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "168.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 15:10",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "184.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 15:12",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 15:14",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 15:16",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "160.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 15:18",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 15:20",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 15:22",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 15:24",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 15:26",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "192.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 15:28",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "176.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 15:30",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 15:32",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 15:34",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 15:36",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "184.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 15:38",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 15:40",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 15:42",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 15:44",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 15:46",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 15:48",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 15:50",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 15:52",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 15:54",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 15:56",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 15:58",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 16:00",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 16:02",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 16:04",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "176.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 16:06",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "168.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 16:08",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 16:10",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 16:12",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 16:14",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "160.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 16:16",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 16:18",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "160.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 16:20",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 16:22",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 16:24",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 16:26",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 16:28",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 16:30",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 16:32",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "192.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 16:34",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "176.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 16:36",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 16:38",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 16:40",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 16:42",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 16:44",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 16:46",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 16:48",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 16:50",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 16:52",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 16:54",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 16:56",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 16:58",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 17:00",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "192.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 17:02",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "176.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 17:04",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "184.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 17:06",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "176.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 17:08",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 17:10",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 17:12",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "160.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 17:14",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 17:16",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 17:18",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 17:20",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 17:22",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "176.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 17:24",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 17:26",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "144.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 17:28",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "168.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 17:30",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "176.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 17:32",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "192.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 17:34",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "176.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 17:36",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 17:38",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 17:40",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 17:42",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 17:44",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 17:46",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 17:48",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 17:50",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "200.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 17:52",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 17:54",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 17:56",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "168.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 17:58",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "168.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 18:00",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "184.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 18:02",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "168.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 18:04",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 18:06",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 18:08",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 18:10",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 18:12",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 18:14",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 18:16",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 18:18",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "200.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 18:20",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 18:22",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 18:24",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 18:26",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "168.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 18:28",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "184.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 18:30",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "176.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 18:32",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 18:34",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "160.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 18:36",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 18:38",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 18:40",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 18:42",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 18:44",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "152.00"
            },
            {
                "errorRatioList": 0,
                "time": "2019-07-15 18:46",
                "outUseRatioList": 0,
                "loseRatioList": 0,
                "outSpeedList": "192.00"
            },
            {
                "time": "2019-07-15 18:48",
                "outUseRatioList": "",
                "loseRatioList": "",
                "outSpeedList": ""
            },
            {
                "time": "2019-07-15 18:50",
                "outUseRatioList": "",
                "loseRatioList": "",
                "outSpeedList": ""
            }
        ],
        "maxSpeedA": random.randint(100,800),
        "maxSpeedB": random.randint(850,1020),
        "minSpeedA": random.randint(100,200),
        "minSpeedB": random.randint(850,900),
        "minSpeedAUnit": "Mbps",
        "linkBandWidth": "1Gbps", #10Gbps
        "maxSpeedBUnit": "Mbps",
        "speedUnit": "Mbps",
        "meanSpeedBUnit": "Mbps",
        "minSpeedBUnit": "Mbps",
        "maxSpeedAUnit": "Mbps",
        "meanSpeedA": random.randint(100,800)
    }
    return data 


big_data_linkIndicatorChangeTrend ={
  "data": {
    "meanSpeedB": "169.31",
    "A": [
      {
        "errorRatioList": 0,
        "time": "2019-10-15 19:40:35",
        "outUseRatioList": 9.21,
        "loseRatioList": 0,
        "outSpeedList": "92.06"
      },
    {
        "errorRatioList": 0,
        "time": "2019-10-15 19:40:40",
        "outUseRatioList": 9.21,
        "loseRatioList": 0,
        "outSpeedList": "92.06"
    },
    {
        "errorRatioList": 0,
        "time": "2019-10-15 19:40:45",
        "outUseRatioList": 9.21,
        "loseRatioList": 0,
        "outSpeedList": "92.06"
    },
    {
        "errorRatioList": 0,
        "time": "2019-10-15 19:40:50",
        "outUseRatioList": 9.21,
        "loseRatioList": 0,
        "outSpeedList": "92.05"
    },
    {
        "errorRatioList": 0,
        "time": "2019-10-15 19:40:55",
        "outUseRatioList": 9.21,
        "loseRatioList": 0,
        "outSpeedList": "92.05"
    },
    {
        "errorRatioList": 0,
        "time": "2019-10-15 19:41:00",
        "outUseRatioList": 9.21,
        "loseRatioList": 0,
        "outSpeedList": "92.05"
    },
    #  ......(五秒取一次，基本不变，省略)
    ],
    "B": [
    {
        "errorRatioList": 0,
        "time": "2019-10-15 19:40:35",
        "outUseRatioList": 0.02,
        "loseRatioList": 0,
        "outSpeedList": "0.17"
    },
    {
        "errorRatioList": 0,
        "time": "2019-10-15 19:40:40",
        "outUseRatioList": 0.02,
        "loseRatioList": 0,
        "outSpeedList": "0.17"
    },
    {
        "errorRatioList": 0,
        "time": "2019-10-15 19:40:45",
        "outUseRatioList": 0.02,
        "loseRatioList": 0,
        "outSpeedList": "0.17"
    },
    {
        "errorRatioList": 0,
        "time": "2019-10-15 19:40:50",
        "outUseRatioList": 0.02,
        "loseRatioList": 0,
        "outSpeedList": "0.17"
    }
    
    ],
	"meanSpeedAUnit": "Mbps",
	"maxSpeedA": "184.10",
    "maxSpeedB": "318.46",
    "minSpeedA": "91.76",
    "minSpeedB": "139.89",
    "minSpeedAUnit": "Mbps",
    "linkBandWidth": "1Gbps",
    "maxSpeedBUnit": "Kbps",
    "speedUnit": "Mbps",
    "meanSpeedBUnit": "Kbps",
    "minSpeedBUnit": "Kbps",
    "maxSpeedAUnit": "Mbps",
    "meanSpeedA": "98.29"
  },
  "errorInfo": "OK",
  "errorCode": 0,
  "status": True
}


# http://172.100.1.15:10080/restconf/operations/topology-modelV2:get-topo-node
sna_topo_node_data = {
    "95390e43-74e3-4910-8e14-f2720711f6e3":{
    "output": {
    "nodes": [
      {
        "serialNum": "210235A0YVX1361200112",
        "snmpCfgId": "cbc3b90e-3a9f-4e72-b24f-401940e76f55",
        "ipv4Bgp": {
          "enable": 0,
          "peerAddr": "0.0.0.0",
          "peerStatus": 0,
          "peerAsNum": 0,
          "initiateConnection": False
        },
        "model": "SR8804-X",
        "deviceCapabilitys": {
          "segmentRoutingCapability": {
            "upper": 1023,
            "depth": 16,
            "lower": 16
          }
        },
        "asNum": 0,
        "deviceId": "95390e43-74e3-4910-8e14-f2720711f6e3",
        "netconfCfgId": "ad9f765f-90f4-4f18-b252-8a401bd0fc79",
        "manageIp": "172.100.1.52",
        "nodeOperStatus": 1,
        "scene": 1,
        "licenseStatus": 1,
        "deviceStatus": 1,
        "nodeIsolationStatus": 1,
        "deviceType": 1,
        "role": 1,
        "company": 0,
        "tpIds": [
          {
            "tpId": "4eb6ad3e-0371-47ec-9a5f-50d09e8176ae"
          },
          {
            "tpId": "ce68a0d3-968f-46e4-99ae-0a2a6f4558da"
          },
          {
            "tpId": "55684970-603c-4fc7-854c-e22836fb2ff2"
          },
          {
            "tpId": "eb0ad418-ac06-45d6-beb9-996285a5a0fc"
          },
          {
            "tpId": "6fef4cc8-6c2a-4272-bd5f-df0a3047aa43"
          },
          {
            "tpId": "b347e305-69e3-438e-975e-43f8886d8596"
          },
          {
            "tpId": "b494e1a6-aa7f-4d74-bcc4-4b19ab0d85d7"
          },
          {
            "tpId": "531b5a2f-5f1e-434f-9640-a63933879e50"
          },
          {
            "tpId": "10ed7ef6-06b1-406c-8c72-67e3a51a0718"
          },
          {
            "tpId": "8acf5549-4fac-49c9-bd2d-783913bd5ba0"
          },
          {
            "tpId": "648b70cd-92f8-4866-990e-4f3c3ea2b36c"
          },
          {
            "tpId": "76fe575d-7a91-420e-8933-3a385212aad8"
          },
          {
            "tpId": "486970d6-5ac6-4250-a742-3c9cd136fa43"
          },
          {
            "tpId": "32b927bf-0a05-4855-9a2c-7f7ceee89436"
          },
          {
            "tpId": "af789177-91de-4766-a2da-2d656481dfbe"
          },
          {
            "tpId": "1c2eab38-e0d8-4f24-9a23-8a51d9725ee0"
          },
          {
            "tpId": "5b9173f2-9c9c-4c42-8924-1fe16c84fd06"
          },
          {
            "tpId": "32222946-6fdd-4400-b63b-cf15b02b2910"
          },
          {
            "tpId": "180b4fa8-4995-4690-864a-3d8b43b9cf78"
          },
          {
            "tpId": "8c4d1c9f-2152-4a0f-8903-16b140e4dec7"
          },
          {
            "tpId": "22f2792e-7b4f-4074-b446-f4d44e14e2b6"
          },
          {
            "tpId": "4824aa7a-8a68-4e0f-9172-9f3d03ed8339"
          },
          {
            "tpId": "7047ea5f-e3d5-46d5-bdcf-adcd686348d7"
          },
          {
            "tpId": "d5cc8d09-6fcd-47a0-b004-b247da0f4b7f"
          },
          {
            "tpId": "f3a3536c-6d51-4dd9-8320-f1e6ac4dc059"
          },
          {
            "tpId": "f1f474d9-bddc-4dd4-82fe-a438d6e062d6"
          }
        ],
        "mpBgp": {
          "enable": 0,
          "peerAddr": "0.0.0.0",
          "peerStatus": 0,
          "peerAsNum": 0,
          "initiateConnection": False
        },
        "nodeWarningStatus": 1,
        "comeFrom": 0,
        "nodeWarningMsg": "Failed to deploy a node label. The failed reason is:null",
        "deviceName": "P1",
        "sysObjectOid": "1.3.6.1.4.1.25506.1.920",
        "deviceDisplay": 1,
        "softVersion": "Version 7.1.075, Release 8151P01"
      }
    ]
  }
    },

    "d3501601-faed-4d5d-b57b-e528dc1e266e":{
    "output": {
    "nodes": [
      {
        "serialNum": "210235A0YVX1361200114",
        "snmpCfgId": "cbc3b90e-3a9f-4e72-b24f-401940e76f55",
        "ipv4Bgp": {
          "enable": 0,
          "peerAddr": "0.0.0.0",
          "peerStatus": 0,
          "peerAsNum": 0,
          "initiateConnection": False
        },
        "model": "SR8804-X",
        "deviceCapabilitys": {
          "segmentRoutingCapability": {
            "upper": 1023,
            "depth": 16,
            "lower": 16
          }
        },
        "asNum": 0,
        "deviceId": "d3501601-faed-4d5d-b57b-e528dc1e266e",
        "netconfCfgId": "ad9f765f-90f4-4f18-b252-8a401bd0fc79",
        "manageIp": "172.100.1.54",
        "nodeOperStatus": 1,
        "scene": 1,
        "licenseStatus": 1,
        "deviceStatus": 1,
        "nodeIsolationStatus": 1,
        "deviceType": 1,
        "role": 2,
        "company": 0,
        "tpIds": [
          {
            "tpId": "9db89923-83ab-4e9c-9a54-439713a51cea"
          },
          {
            "tpId": "7703e15f-db1b-44dd-9bb8-03ec2d57f2dc"
          },
          {
            "tpId": "76407893-7767-4383-afe7-4104058a794c"
          },
          {
            "tpId": "4d74e896-8eb2-41ff-ba30-0e2eb3209374"
          },
          {
            "tpId": "970be4d9-3dd3-458e-9ef2-15e53cc23b98"
          },
          {
            "tpId": "665fc16a-9071-48af-8119-db7a9713638a"
          },
          {
            "tpId": "42ac071d-dc50-43ea-903f-f2d210359078"
          },
          {
            "tpId": "e7eb7ead-15c5-4dfc-91db-940c1e893a9e"
          },
          {
            "tpId": "d41367ad-266c-42e3-bb7e-de49ddf984d5"
          },
          {
            "tpId": "d8d8890f-a34e-4e3d-b85b-0eec243bfb76"
          },
          {
            "tpId": "a48c011c-020f-4d86-8836-c913182191af"
          },
          {
            "tpId": "9f252d93-3873-4d80-aef2-93a397e88e60"
          },
          {
            "tpId": "91ba03ca-417f-4b74-8c72-7028193c654f"
          },
          {
            "tpId": "9bf6bf58-184f-46de-b311-ad5d667d963e"
          },
          {
            "tpId": "53ab2fdf-4bc3-4f09-88c0-1fe24ab2eab7"
          },
          {
            "tpId": "0ef1d221-4243-4b91-909c-81b1f5d9b68d"
          },
          {
            "tpId": "af88a52e-e664-40d2-b523-24306c673e40"
          },
          {
            "tpId": "a26aed30-363c-44e9-b1ef-0b5a1b01702f"
          },
          {
            "tpId": "efff05a1-4873-4b07-bb43-0bc5d97f3f2c"
          },
          {
            "tpId": "3b68c2c0-45ea-4919-a169-8aceccb8ea45"
          },
          {
            "tpId": "b35a7c9a-eaac-4597-889c-af441e7162da"
          },
          {
            "tpId": "401108dc-df26-440f-af12-4dd58e493343"
          },
          {
            "tpId": "23f48989-5019-499a-8d2b-4742917fa8c4"
          },
          {
            "tpId": "5697c1ac-a7a7-47f6-9b11-cf5d9aade132"
          },
          {
            "tpId": "6e1f31e5-137b-4bb7-bb6a-c4d25a1f3820"
          },
          {
            "tpId": "81f99ec5-512b-4375-922d-343c839116bc"
          },
          {
            "tpId": "d8cb48dd-3dde-496e-b568-3b38fbd3f019"
          }
        ],
        "mpBgp": {
          "enable": 0,
          "peerAddr": "0.0.0.0",
          "peerStatus": 0,
          "peerAsNum": 0,
          "initiateConnection": False
        },
        "nodeWarningStatus": 3,
        "comeFrom": 0,
        "nodeWarningMsg": "Failed to deploy a node label. The failed reason is:nullthe board of device is replaced.Board position0/3@boardStatus:5&",
        "deviceName": "PE3",
        "sysObjectOid": "1.3.6.1.4.1.25506.1.920",
        "deviceDisplay": 5,
        "softVersion": "Version 7.1.075, Release 8151P01"
      }
    ]
  }
},

    "ffdce32e-97dc-4b39-88c0-f6a494e59658":{
    "output": {
    "nodes": [
      {
        "serialNum": "210235A0YVX1361200115",
        "snmpCfgId": "cbc3b90e-3a9f-4e72-b24f-401940e76f55",
        "ipv4Bgp": {
          "enable": 0,
          "peerAddr": "0.0.0.0",
          "peerStatus": 0,
          "peerAsNum": 0,
          "initiateConnection": False
        },
        "model": "SR8804-X",
        "deviceCapabilitys": {
          "segmentRoutingCapability": {
            "upper": 1023,
            "depth": 16,
            "lower": 16
          }
        },
        "asNum": 0,
        "deviceId": "ffdce32e-97dc-4b39-88c0-f6a494e59658",
        "netconfCfgId": "ad9f765f-90f4-4f18-b252-8a401bd0fc79",
        "manageIp": "172.100.1.55",
        "nodeOperStatus": 1,
        "scene": 1,
        "licenseStatus": 1,
        "deviceStatus": 1,
        "nodeIsolationStatus": 1,
        "deviceType": 1,
        "role": 2,
        "company": 0,
        "tpIds": [
          {
            "tpId": "22760471-6f00-41c5-8ca5-6b1051e3e293"
          },
          {
            "tpId": "f5d0df56-bc12-4134-b914-645bc4934970"
          },
          {
            "tpId": "51bd5bad-e1ed-4a9b-9b20-e697b9c5b392"
          },
          {
            "tpId": "7a523a80-d2de-42fc-9e53-933bbd1b9865"
          },
          {
            "tpId": "f90c968e-8b3d-48b8-8994-beff97158f5a"
          },
          {
            "tpId": "05d035d7-f944-4467-b6c3-25803542464a"
          },
          {
            "tpId": "1277e6c8-9942-475b-9e3c-68dd89907f21"
          },
          {
            "tpId": "2e0fd4c0-faec-4da0-84ee-3c5d80682cbe"
          },
          {
            "tpId": "62858d68-ca7b-4a82-a0e4-06aa17078ffd"
          },
          {
            "tpId": "939d6ed6-a0f5-44c2-9968-90f241460202"
          },
          {
            "tpId": "eebb740f-82c8-4a44-a960-0581eab94142"
          },
          {
            "tpId": "a2396b02-817e-446f-892b-211acce51db4"
          },
          {
            "tpId": "4a131218-f046-4b1c-bb5d-822d102fac00"
          },
          {
            "tpId": "3efea2eb-e66e-4bd5-abea-5ce1b4cd1a56"
          },
          {
            "tpId": "3ff47b00-d073-4141-b2f4-a491b840ce67"
          },
          {
            "tpId": "f1f04ff4-e704-474c-aca3-263af4d94b19"
          },
          {
            "tpId": "c61d8475-1423-4447-b9d1-29568ccabe2f"
          },
          {
            "tpId": "798b626e-78bc-4beb-975c-90e27484dd02"
          },
          {
            "tpId": "dcc70a01-2ca1-4163-a6d6-759aac04a5e7"
          },
          {
            "tpId": "60e440d5-afa6-4512-b3b8-b5bb4c17027a"
          },
          {
            "tpId": "891cbe2e-be44-4156-a015-2e1e429dfb87"
          },
          {
            "tpId": "af1f9d91-5a55-4476-84f9-bb7ba36a5f66"
          },
          {
            "tpId": "b48d41ec-912f-46ef-800f-3642590d15f1"
          },
          {
            "tpId": "b4a2ebef-606f-4540-9b08-8c9848b77ee0"
          },
          {
            "tpId": "cc65c833-5017-4617-abfd-6971579358bb"
          },
          {
            "tpId": "48e4f6a1-b18e-43bd-9350-7825cecd2527"
          }
        ],
        "mpBgp": {
          "enable": 0,
          "peerAddr": "0.0.0.0",
          "peerStatus": 0,
          "peerAsNum": 0,
          "initiateConnection": False
        },
        "nodeWarningStatus": 1,
        "comeFrom": 0,
        "nodeWarningMsg": "Failed to deploy a node label. The failed reason is:null",
        "deviceName": "PE4",
        "sysObjectOid": "1.3.6.1.4.1.25506.1.920",
        "deviceDisplay": 1,
        "softVersion": "Version 7.1.075, Release 8151P01"
      }
    ]
  }
},
    "3716b792-59ad-4035-87b5-6a10289fab7b":{
    "output": {
    "nodes": [
      {
        "serialNum": "210235A0YVX1361200110",
        "snmpCfgId": "cbc3b90e-3a9f-4e72-b24f-401940e76f55",
        "ipv4Bgp": {
          "enable": 0,
          "peerAddr": "0.0.0.0",
          "peerStatus": 0,
          "peerAsNum": 0,
          "initiateConnection": False
        },
        "model": "SR8804-X",
        "deviceCapabilitys": {
          "segmentRoutingCapability": {
            "upper": 1023,
            "depth": 16,
            "lower": 16
          }
        },
        "asNum": 0,
        "deviceId": "3716b792-59ad-4035-87b5-6a10289fab7b",
        "netconfCfgId": "ad9f765f-90f4-4f18-b252-8a401bd0fc79",
        "manageIp": "172.100.1.50",
        "nodeOperStatus": 1,
 
        "scene": 1,
        "licenseStatus": 1,
        "deviceStatus": 1,
        "nodeIsolationStatus": 1,
        "deviceType": 1,
        "role": 2,
        "company": 0,
        "tpIds": [
          {
            "tpId": "fe24f920-4ff2-4078-bce5-6cb630643ef9"
          },
          {
            "tpId": "65839550-df7f-4bd3-a52d-e98e6add2f36"
          },
          {
            "tpId": "aa568a28-2fae-49e6-bcca-33d36a50cf63"
          },
          {
            "tpId": "4c3b07f1-a22c-488f-8155-f8bdbac5cb7b"
          },
          {
            "tpId": "c5aed25c-d8a4-41b0-b6dc-d67b91a0ae8e"
          },
          {
            "tpId": "63658e3e-b65c-4d7f-bb0e-741865a62345"
          },
          {
            "tpId": "364e795c-9ee1-478d-b9a2-fcb2fe2eb0eb"
          },
          {
            "tpId": "14a6548c-bb5a-4eaf-8acb-0fc9add39fca"
          },
          {
            "tpId": "7db5afe6-4a60-49d4-9dfd-a005f12c48a1"
          },
          {
            "tpId": "f8d83a59-b15d-43b7-8551-4f9a353ca885"
          },
          {
            "tpId": "326d5aea-9029-4174-b26f-7fb58139f7e1"
          },
          {
            "tpId": "8288bdcb-02ea-425a-814f-080feae88cd0"
          },
          {
            "tpId": "56e71805-e9e7-486f-9da7-8b64dd8718e2"
          },
          {
            "tpId": "bf9d6a9a-b518-4423-b529-fbbcbc78543f"
          },
          {
            "tpId": "5d0d9ffa-a000-48ba-84ff-74aee7ea1278"
          },
          {
            "tpId": "995ab614-39b5-4b17-b9b3-a2125af5bd17"
          },
          {
            "tpId": "57a18ade-9d75-4e4a-b2b4-302465eb0933"
          },
          {
            "tpId": "73328edd-ab5b-4411-a395-8ed668a3d215"
          },
          {
            "tpId": "3b717a50-5d69-4ec9-871c-93fe22c230db"
          },
          {
            "tpId": "1560dcf6-cb21-4388-bf4a-b3ba6f8c35d3"
          },
          {
            "tpId": "3e2e0d1c-64bf-4481-b6f6-1f7ba3fcfb36"
          },
          {
            "tpId": "30fef89d-3531-4d6c-8efe-37326bf550bc"
          },
          {
            "tpId": "d8b12e12-3e0d-497e-8dd9-3929ad7ce0a2"
          },
          {
            "tpId": "8f15e999-44fc-4005-b3aa-eefbbf1e5cf8"
          },
          {
            "tpId": "cba11b3e-f1c9-462c-82e8-d58a521d69a7"
          },
          {
            "tpId": "c8fbc891-92c8-4fcb-868b-062a1c129f4f"
          },
          {
            "tpId": "23251b09-8001-4eb9-9c6c-fb6f65f1e8a2"
          },
          {
            "tpId": "2a71323f-6190-4bb7-8613-c99570fe4f46"
          }
        ],
        "mpBgp": {
          "enable": 0,
          "peerAddr": "0.0.0.0",
          "peerStatus": 0,
          
		  "peerAsNum": 0,
          "initiateConnection": False
        },
        "nodeWarningStatus": 1,
        "comeFrom": 0,
        "nodeWarningMsg": "Failed to deploy a node label. The failed reason is:null",
        "deviceName": "PE1",
        "sysObjectOid": "1.3.6.1.4.1.25506.1.920",
        "deviceDisplay": 1,
        "softVersion": "Version 7.1.075, Release 8151P01"
      }
    ]
  }
},
    "a835c187-7c1d-4452-8139-d8d6eecb9cc3":
    {
    "output": {
    "nodes": [
      {
        "serialNum": "210235A0YVX1361200111",
        "snmpCfgId": "cbc3b90e-3a9f-4e72-b24f-401940e76f55",
        "ipv4Bgp": {
          "enable": 0,
          "peerAddr": "0.0.0.0",
          "peerStatus": 0,
          "peerAsNum": 0,
          "initiateConnection": False
        },
        "model": "SR8804-X",
        "deviceCapabilitys": {
          "segmentRoutingCapability": {
            "upper": 1023,
            "depth": 16,
            "lower": 16
          }
        },
        "asNum": 0,
        "deviceId": "a835c187-7c1d-4452-8139-d8d6eecb9cc3",
        "netconfCfgId": "ad9f765f-90f4-4f18-b252-8a401bd0fc79",
        "manageIp": "172.100.1.51",
        "nodeOperStatus": 1,
        "scene": 1,
        "licenseStatus": 1,
        "deviceStatus": 1,
        "nodeIsolationStatus": 1,
        "deviceType": 1,
        "role": 2,
        "company": 0,
        "tpIds": [
          {
            "tpId": "9e661ebd-a2a9-4d75-baaf-d9b81ec1d2b3"
          },
          {
            "tpId": "4a20e2ee-8838-49c9-923a-78d1879f83e5"
          },
          {
            "tpId": "0f16cbd1-5f2b-4234-9bff-5e30541f60a6"
          },
          {
            "tpId": "fd69500f-fd1c-4c49-abbc-fb321b0c45d7"
          },
          {
            "tpId": "c7b07120-a0e2-4b4f-9b12-8dbd75f0fafe"
          },
          {
            "tpId": "e881849c-ae5a-486a-94db-dad09d6290bc"
          },
          {
            "tpId": "fa4280f1-9cd3-4d5d-8fe7-aeba82c28005"
          },
          {
            "tpId": "0eec274f-3ba2-4171-90d0-3d6311fbfd10"
          },
          {
            "tpId": "8901dbc1-4790-4a4f-99bf-f400bfdee905"
          },
          {
            "tpId": "f448eb3e-ba13-4f24-b943-9127f4908a88"
          },
          {
            "tpId": "6fa9c88d-96c2-406e-a255-433cc34d35a6"
          },
          {
            "tpId": "0e86f39f-0b2a-47de-aec3-cf7179149a0e"
          },
          {
            "tpId": "d4a110dd-e4b9-47e6-b24a-c4bf1d5dc864"
          },
          {
            "tpId": "593f9a0b-ed15-4623-8fcd-806cb21ddb12"
          },
          {
            "tpId": "c390e1b1-02b3-4076-a5d0-57a46bf244bc"
          },
          {
            "tpId": "1230395e-e0b4-4106-944a-f09fddbb07af"
          },
          {
            "tpId": "7762a569-4098-4322-bae2-a842044cd760"
          },
          {
            "tpId": "ba2d9e75-ee82-4cfa-8357-2a538760225f"
          },
          {
            "tpId": "f3022353-aa48-4593-9672-fdff4408baa4"
          },
          {
            "tpId": "4d439795-8bb6-421b-8ee3-896e3984aaac"
          },
          {
            "tpId": "460f2d1b-1a44-49d9-a945-956c3adc2bb4"
          },
          {
            "tpId": "4b505c7a-9a11-4e0d-b0cb-fb3b9f44632f"
          },
          {
            "tpId": "30e64d82-5856-4206-87e4-99914d0d36cb"
          },
          {
            "tpId": "be3b56ed-36de-4f7f-b7f7-680c884ef156"
          },
          {
            "tpId": "70547ca5-6de9-4ced-bab9-82054ad45408"
          },
          {
            "tpId": "8596f1db-c425-46d4-9e28-9a07d28aa56a"
          }
        ],
        "mpBgp": {
          "enable": 0,
          "peerAddr": "0.0.0.0",
          "peerStatus": 0,
          "peerAsNum": 0,
          "initiateConnection": False
        },
        "nodeWarningStatus": 1,
        "comeFrom": 0,
        "nodeWarningMsg": "Failed to deploy a node label. The failed reason is:null",
        "deviceName": "PE2",
        "sysObjectOid": "1.3.6.1.4.1.25506.1.920",
        "deviceDisplay": 1,
        "softVersion": "Version 7.1.075, Release 8151P01"
      }
    ]
  }
},
    "375e2205-da93-4349-a120-571de7496738":
    {
    "output": {
    "nodes": [
      {
        "serialNum": "210235A0YVX1361200113",
        "snmpCfgId": "cbc3b90e-3a9f-4e72-b24f-401940e76f55",
        "ipv4Bgp": {
          "enable": 0,
          "peerAddr": "0.0.0.0",
          "peerStatus": 0,
          "peerAsNum": 0,
          "initiateConnection": False
        },
        "model": "SR8804-X",
        "deviceCapabilitys": {
          "segmentRoutingCapability": {
            "upper": 1023,
            "depth": 16,
            "lower": 16
          }
        },
        "asNum": 0,
        "deviceId": "375e2205-da93-4349-a120-571de7496738",
        "netconfCfgId": "ad9f765f-90f4-4f18-b252-8a401bd0fc79",
        "manageIp": "172.100.1.53",
        "nodeOperStatus": 1,
        "scene": 1,
        "licenseStatus": 1,
        "deviceStatus": 1,
        "nodeIsolationStatus": 1,
        "deviceType": 1,
        "role": 1,
        "company": 0,
        "tpIds": [
          {
            "tpId": "926e94ca-098e-4110-a54c-a7978c6c291c"
          },
          {
            "tpId": "dc4bd971-9797-4c28-bcc2-ac56d8f43d3c"
          },
          {
            "tpId": "fdb4cb67-c367-4090-b736-cc654756129c"
          },
          {
            "tpId": "9b34f775-8103-49a9-9496-96e84887db68"
          },
          {
            "tpId": "e46cb628-1f0c-460f-a546-41e41a30ed5c"
          },
          {
            "tpId": "23b61c2c-46b9-4efa-aa7f-521fd9503b66"
          },
          {
            "tpId": "d1ffe0c8-ab76-455b-a135-85b6be94703e"
          },
          {
            "tpId": "95eb1655-bee3-46ea-873c-03fd5be455ce"
          },
          {
            "tpId": "2d13e16e-584c-411a-bf2a-f97268ce9464"
          },
          {
            "tpId": "b2a79005-647a-4920-9709-574368a26381"
          },
          {
            "tpId": "c98938ef-88a6-4a9e-b30d-53e66f99f10a"
          },
          {
            "tpId": "64f31904-aba3-41ea-be26-b4a0aa01b156"
          },
          {
            "tpId": "6bf30c6e-3af6-4f4d-8b99-c928bbb55380"
          },
          {
            "tpId": "0b9c731f-da85-47dc-94fd-b72ee377128d"
          },
          {
            "tpId": "cf70722e-4948-42c6-aba1-ac0954c7fa92"
          },
          {
            "tpId": "feed91b9-e4a0-4b6b-919d-3f21170605a1"
          },
          {
            "tpId": "9a9a1c03-048e-41fa-afcd-fc13d49e78c2"
          },
          {
            "tpId": "3ea8d493-0087-40f8-b2fd-cb16a8e53393"
          },
          {
            "tpId": "5b34f034-b801-4632-9706-cbba9f699528"
          },
          {
            "tpId": "58a4b9d0-dd65-4b00-8b6a-a20140d40e1e"
          },
          {
            "tpId": "8218b387-30d0-4b24-aee9-f47657658d3c"
          },
          {
            "tpId": "4ae8d7a2-4b33-4264-b627-70c3554356cd"
          },
          {
            "tpId": "44284cda-fa9b-4c68-9183-437e2da15576"
          },
          {
            "tpId": "31aa053e-7e81-4d21-b05b-a6f793c165a3"
          },
          {
            "tpId": "00843f44-6595-4bd3-a24c-00fdaa1659b1"
          },
          {
            "tpId": "0048bc03-e880-452e-afd0-4888fc7d64e0"
          }
        ],
        "mpBgp": {
          "enable": 0,
          "peerAddr": "0.0.0.0",
          "peerStatus": 0,
          "peerAsNum": 0,
          "initiateConnection": False
        },
        "nodeWarningStatus": 1,
        "comeFrom": 0,
        "nodeWarningMsg": "Failed to deploy a node label. The failed reason is:null",
        "deviceName": "P2",
        "sysObjectOid": "1.3.6.1.4.1.25506.1.920",
        "deviceDisplay": 1,
        "softVersion": "Version 7.1.075, Release 8151P01"
      }
    ]
  }
}
}
sna_link_data = {'output': {'links': [{'reservableBandWidth': 1000000, 'bandwidth': 1000000, 'dstTpName': 'GigabitEthernet2/0', 'threshold': -1, 'dstDeviceName': 'VSR2', 'operStatus': 1, 'linkName': 'VSR1 To VSR2 Link1', 'srcDeviceName': 'VSR1', 'availableState': False, 'attributeFlags': 0, 'color': 0, 'linkStatus': 1, 'srcNodeId': '5fc7e69a-709b-409d-b1e9-093c02394d5a', 'srcTpId': 'c76c2543-3651-4cea-9352-b54f0e613f60', 'available': 100, 'dstNodeId': 'd235cae2-848e-404c-88e3-1576668834cc', 'linkType': 100, 'adminStatus': 1, 'enableRateLimit': False, 'srcTpName': 'GigabitEthernet2/0', 'metric': 30, 'dstTpId': 'eeddfa76-eb07-4779-b8ec-b20598379377', 'linkId': '27f06554-6854-412e-8f6d-5758a2c43075', 'strategy': False}, {'reservableBandWidth': 1000000, 'bandwidth': 1000000, 'dstTpName': 'GigabitEthernet5/0', 'threshold': -1, 'dstDeviceName': 'VSR4', 'operStatus': 1, 'linkName': 'VSR5 To VSR4 Link1', 'srcDeviceName': 'VSR5', 'availableState': False, 'attributeFlags': 0, 'color': 0, 'linkStatus': 1, 'srcNodeId': 'bb0e3e1d-7541-4a59-80e6-b55d9ae3d4ac', 'srcTpId': '7b0e86e9-9e8e-49d5-a146-521d30308381', 'available': 100, 'dstNodeId': '04165eb6-48f0-4e7f-aa08-3e0967fda9a5', 'linkType': 100, 'adminStatus': 1, 'enableRateLimit': False, 'srcTpName': 'GigabitEthernet4/0', 'metric': 15, 'dstTpId': 'c09a74ba-6d8a-4e9c-870b-25ad0c3b3b2f', 'linkId': '45aaf289-e8fc-4619-acbe-84820b6c3194', 'strategy': False}, {'reservableBandWidth': 1000000, 'bandwidth': 1000000, 'dstTpName': 'GigabitEthernet3/0', 'threshold': -1, 'dstDeviceName': 'VSR3', 'operStatus': 1, 'linkName': 'VSR1 To VSR3 Link1', 'srcDeviceName': 'VSR1', 'availableState': False, 'attributeFlags': 0, 'color': 0, 'linkStatus': 1, 'srcNodeId': '5fc7e69a-709b-409d-b1e9-093c02394d5a', 'srcTpId': '512626f4-9840-40ee-92fd-08a57623ee3d', 'available': 100, 'dstNodeId': 'a92e557a-542e-445f-a38e-9d3cd438110b', 'linkType': 100, 'adminStatus': 1, 'enableRateLimit': False, 'srcTpName': 'GigabitEthernet3/0', 'metric': 10, 'dstTpId': '00ca837d-3c80-4112-8f3f-85620cf0ae2b', 'linkId': '166eab8f-b8da-4b52-ad3f-104d1699ad17', 'strategy': False}, {'reservableBandWidth': 1000000, 'bandwidth': 1000000, 'dstTpName': 'GigabitEthernet3/0', 'threshold': -1, 'dstDeviceName': 'VSR1', 'operStatus': 1, 'linkName': 'VSR3 To VSR1 Link1', 'srcDeviceName': 'VSR3', 'availableState': False, 'attributeFlags': 0, 'color': 0, 'linkStatus': 1, 'srcNodeId': 'a92e557a-542e-445f-a38e-9d3cd438110b', 'srcTpId': '00ca837d-3c80-4112-8f3f-85620cf0ae2b', 'available': 100, 'dstNodeId': '5fc7e69a-709b-409d-b1e9-093c02394d5a', 'linkType': 100, 'adminStatus': 1, 'enableRateLimit': False, 'srcTpName': 'GigabitEthernet3/0', 'metric': 10, 'dstTpId': '512626f4-9840-40ee-92fd-08a57623ee3d', 'linkId': 'e06f12d1-4da3-41f2-82a2-f16662fd3703', 'strategy': False}, {'reservableBandWidth': 1000000, 'bandwidth': 1000000, 'dstTpName': 'GigabitEthernet4/0', 'threshold': -1, 'dstDeviceName': 'VSR1', 'operStatus': 1, 'linkName': 'VSR4 To VSR1 Link1', 'srcDeviceName': 'VSR4', 'availableState': False, 'attributeFlags': 0, 'color': 0, 'linkStatus': 1, 'srcNodeId': '04165eb6-48f0-4e7f-aa08-3e0967fda9a5', 'srcTpId': '9b11fe23-e163-4fa9-8fd5-6c819800047a', 'available': 100, 'dstNodeId': '5fc7e69a-709b-409d-b1e9-093c02394d5a', 'linkType': 100, 'adminStatus': 1, 'enableRateLimit': False, 'srcTpName': 'GigabitEthernet4/0', 'metric': 25, 'dstTpId': '0906b532-bf89-4fd7-9d93-b6601d72e548', 'linkId': '70841762-dc20-449c-8b2c-2b47bf1bb70c', 'strategy': False}, {'reservableBandWidth': 1000000, 'bandwidth': 1000000, 'dstTpName': 'GigabitEthernet4/0', 'threshold': -1, 'dstDeviceName': 'VSR3', 'operStatus': 1, 'linkName': 'VSR4 To VSR3 Link1', 'srcDeviceName': 'VSR4', 'availableState': False, 'attributeFlags': 0, 'color': 0, 'linkStatus': 1, 'srcNodeId': '04165eb6-48f0-4e7f-aa08-3e0967fda9a5', 'srcTpId': '3e906922-b4b7-4ef2-b0a3-39814439b855', 'available': 100, 'dstNodeId': 'a92e557a-542e-445f-a38e-9d3cd438110b', 'linkType': 100, 'adminStatus': 1, 'enableRateLimit': False, 'srcTpName': 'GigabitEthernet3/0', 'metric': 20, 'dstTpId': '3d604a7b-49d5-4e15-bef8-d60da980fcee', 'linkId': '39105d81-86b0-4522-a822-339768a9200b', 'strategy': False}, {'reservableBandWidth': 1000000, 'bandwidth': 1000000, 'dstTpName': 'GigabitEthernet4/0', 'threshold': -1, 'dstDeviceName': 'VSR6', 'operStatus': 1, 'linkName': 'VSR4 To VSR6 Link1', 'srcDeviceName': 'VSR4', 'availableState': False, 'attributeFlags': 0, 'color': 0, 'linkStatus': 1, 'srcNodeId': '04165eb6-48f0-4e7f-aa08-3e0967fda9a5', 'srcTpId': '17b47d3d-5336-4c87-8ad2-04f35da42506', 'available': 100, 'dstNodeId': '951b9eda-f804-4bfe-a4e1-a648dd7b4fe7', 'linkType': 100, 'adminStatus': 1, 'enableRateLimit': False, 'srcTpName': 'GigabitEthernet6/0', 'metric': 15, 'dstTpId': '6e3da6f4-dece-4fee-88fc-0598e6c19664', 'linkId': '9d7bc3d2-b550-4e34-aca6-3891fbe5f254', 'strategy': False}, {'reservableBandWidth': 1000000, 'bandwidth': 1000000, 'dstTpName': 'GigabitEthernet4/0', 'threshold': -1, 'dstDeviceName': 'VSR5', 'operStatus': 1, 'linkName': 'VSR4 To VSR5 Link1', 'srcDeviceName': 'VSR4', 'availableState': False, 'attributeFlags': 0, 'color': 0, 'linkStatus': 1, 'srcNodeId': '04165eb6-48f0-4e7f-aa08-3e0967fda9a5', 'srcTpId': 'c09a74ba-6d8a-4e9c-870b-25ad0c3b3b2f', 'available': 100, 'dstNodeId': 'bb0e3e1d-7541-4a59-80e6-b55d9ae3d4ac', 'linkType': 100, 'adminStatus': 1, 'enableRateLimit': False, 'srcTpName': 'GigabitEthernet5/0', 'metric': 10, 'dstTpId': '7b0e86e9-9e8e-49d5-a146-521d30308381', 'linkId': '49451261-f38b-491b-b862-97330980f2a5', 'strategy': False}, {'reservableBandWidth': 1000000, 'bandwidth': 1000000, 'dstTpName': 'GigabitEthernet3/0', 'threshold': -1, 'dstDeviceName': 'VSR6', 'operStatus': 1, 'linkName': 'VSR3 To VSR6 Link1', 'srcDeviceName': 'VSR3', 'availableState': False, 'attributeFlags': 0, 'color': 0, 'linkStatus': 1, 'srcNodeId': 'a92e557a-542e-445f-a38e-9d3cd438110b', 'srcTpId': 'f30f04a8-ed6e-4a23-8913-f47b62d858f7', 'available': 100, 'dstNodeId': '951b9eda-f804-4bfe-a4e1-a648dd7b4fe7', 'linkType': 100, 'adminStatus': 1, 'enableRateLimit': False, 'srcTpName': 'GigabitEthernet6/0', 'metric': 15, 'dstTpId': '91a5a214-08f1-4d92-b104-7941df5a3fee', 'linkId': '3490f918-c557-4d73-a283-91fe6779d417', 'strategy': False}, {'reservableBandWidth': 1000000, 'bandwidth': 1000000, 'dstTpName': 'GigabitEthernet3/0', 'threshold': -1, 'dstDeviceName': 'VSR2', 'operStatus': 1, 'linkName': 'VSR3 To VSR2 Link1', 'srcDeviceName': 'VSR3', 'availableState': False, 'attributeFlags': 0, 'color': 0, 'linkStatus': 1, 'srcNodeId': 'a92e557a-542e-445f-a38e-9d3cd438110b', 'srcTpId': '2e5453aa-5add-4159-8467-02c037689ea9', 'available': 100, 'dstNodeId': 'd235cae2-848e-404c-88e3-1576668834cc', 'linkType': 100, 'adminStatus': 1, 'enableRateLimit': False, 'srcTpName': 'GigabitEthernet2/0', 'metric': 25, 'dstTpId': 'a8d5727b-2d66-4f09-93b4-e014ff43285e', 'linkId': '31bcd6f2-8f39-49d4-aa8a-a7793be297f1', 'strategy': False}, {'reservableBandWidth': 1000000, 'bandwidth': 1000000, 'dstTpName': 'GigabitEthernet4/0', 'threshold': -1, 'dstDeviceName': 'VSR4', 'operStatus': 1, 'linkName': 'VSR1 To VSR4 Link1', 'srcDeviceName': 'VSR1', 'availableState': False, 'attributeFlags': 0, 'color': 0, 'linkStatus': 1, 'srcNodeId': '5fc7e69a-709b-409d-b1e9-093c02394d5a', 'srcTpId': '0906b532-bf89-4fd7-9d93-b6601d72e548', 'available': 100, 'dstNodeId': '04165eb6-48f0-4e7f-aa08-3e0967fda9a5', 'linkType': 100, 'adminStatus': 1, 'enableRateLimit': False, 'srcTpName': 'GigabitEthernet4/0', 'metric': 25, 'dstTpId': '9b11fe23-e163-4fa9-8fd5-6c819800047a', 'linkId': '6308d6ad-eb76-41db-8e92-85672f533c32', 'strategy': False}, {'reservableBandWidth': 1000000, 'bandwidth': 1000000, 'dstTpName': 'GigabitEthernet3/0', 'threshold': -1, 'dstDeviceName': 'VSR5', 'operStatus': 1, 'linkName': 'VSR3 To VSR5 Link1', 'srcDeviceName': 'VSR3', 'availableState': False, 'attributeFlags': 0, 'color': 0, 'linkStatus': 1, 'srcNodeId': 'a92e557a-542e-445f-a38e-9d3cd438110b', 'srcTpId': '839abf41-3320-4db1-96d4-689dd1fd28a4', 'available': 100, 'dstNodeId': 'bb0e3e1d-7541-4a59-80e6-b55d9ae3d4ac', 'linkType': 100, 'adminStatus': 1, 'enableRateLimit': False, 'srcTpName': 'GigabitEthernet5/0', 'metric': 10, 'dstTpId': '452c2c0b-7fb6-4a48-9a4a-2333e8ed0b41', 'linkId': 'e02d9152-a8c1-4b2a-a759-bd1401c31dba', 'strategy': False}, {'reservableBandWidth': 1000000, 'bandwidth': 1000000, 'dstTpName': 'GigabitEthernet2/0', 'threshold': -1, 'dstDeviceName': 'VSR4', 'operStatus': 1, 'linkName': 'VSR2 To VSR4 Link1', 'srcDeviceName': 'VSR2', 'availableState': False, 'attributeFlags': 0, 'color': 0, 'linkStatus': 1, 'srcNodeId': 'd235cae2-848e-404c-88e3-1576668834cc', 'srcTpId': '67eec417-f1f6-43fd-aaf2-79146b5809ba', 'available': 100, 'dstNodeId': '04165eb6-48f0-4e7f-aa08-3e0967fda9a5', 'linkType': 100, 'adminStatus': 1, 'enableRateLimit': False, 'srcTpName': 'GigabitEthernet4/0', 'metric': 10, 'dstTpId': 'b47f7c61-43c8-4e19-902a-28e7b7139a01', 'linkId': '534f5e43-a493-42a6-a29f-57b199b73f6e', 'strategy': False}, {'reservableBandWidth': 1000000, 'bandwidth': 1000000, 'dstTpName': 'GigabitEthernet5/0', 'threshold': -1, 'dstDeviceName': 'VSR3', 'operStatus': 1, 'linkName': 'VSR5 To VSR3 Link1', 'srcDeviceName': 'VSR5', 'availableState': False, 'attributeFlags': 0, 'color': 0, 'linkStatus': 1, 'srcNodeId': 'bb0e3e1d-7541-4a59-80e6-b55d9ae3d4ac', 'srcTpId': '452c2c0b-7fb6-4a48-9a4a-2333e8ed0b41', 'available': 100, 'dstNodeId': 'a92e557a-542e-445f-a38e-9d3cd438110b', 'linkType': 100, 'adminStatus': 1, 'enableRateLimit': False, 'srcTpName': 'GigabitEthernet3/0', 'metric': 10, 'dstTpId': '839abf41-3320-4db1-96d4-689dd1fd28a4', 'linkId': '31c18cbc-4d8f-400a-a135-fd99492e7f07', 'strategy': False}, {'reservableBandWidth': 1000000, 'bandwidth': 1000000, 'dstTpName': 'GigabitEthernet6/0', 'threshold': -1, 'dstDeviceName': 'VSR5', 'operStatus': 1, 'linkName': 'VSR6 To VSR5 Link1', 'srcDeviceName': 'VSR6', 'availableState': False, 'attributeFlags': 0, 'color': 0, 'linkStatus': 1, 'srcNodeId': '951b9eda-f804-4bfe-a4e1-a648dd7b4fe7', 'srcTpId': '79afe820-ff3a-417e-b9d7-4d3d9c766b0f', 'available': 100, 'dstNodeId': 'bb0e3e1d-7541-4a59-80e6-b55d9ae3d4ac', 'linkType': 100, 'adminStatus': 1, 'enableRateLimit': False, 'srcTpName': 'GigabitEthernet5/0', 'metric': 10, 'dstTpId': '9213ae84-61b7-47c4-a6e5-bffadc80e0f7', 'linkId': '36d6c757-9d8d-4748-ad84-734eb691e638', 'strategy': False}, {'reservableBandWidth': 1000000, 'bandwidth': 1000000, 'dstTpName': 'GigabitEthernet6/0', 'threshold': -1, 'dstDeviceName': 'VSR3', 'operStatus': 1, 'linkName': 'VSR6 To VSR3 Link1', 'srcDeviceName': 'VSR6', 'availableState': False, 'attributeFlags': 0, 'color': 0, 'linkStatus': 1, 'srcNodeId': '951b9eda-f804-4bfe-a4e1-a648dd7b4fe7', 'srcTpId': '91a5a214-08f1-4d92-b104-7941df5a3fee', 'available': 100, 'dstNodeId': 'a92e557a-542e-445f-a38e-9d3cd438110b', 'linkType': 100, 'adminStatus': 1, 'enableRateLimit': False, 'srcTpName': 'GigabitEthernet3/0', 'metric': 15, 'dstTpId': 'f30f04a8-ed6e-4a23-8913-f47b62d858f7', 'linkId': '69c95b93-9c59-471b-8d51-441f1e8193fb', 'strategy': False}, {'reservableBandWidth': 1000000, 'bandwidth': 1000000, 'dstTpName': 'GigabitEthernet4/0', 'threshold': -1, 'dstDeviceName': 'VSR2', 'operStatus': 1, 'linkName': 'VSR4 To VSR2 Link1', 'srcDeviceName': 'VSR4', 'availableState': False, 'attributeFlags': 0, 'color': 0, 'linkStatus': 1, 'srcNodeId': '04165eb6-48f0-4e7f-aa08-3e0967fda9a5', 'srcTpId': 'b47f7c61-43c8-4e19-902a-28e7b7139a01', 'available': 100, 'dstNodeId': 'd235cae2-848e-404c-88e3-1576668834cc', 'linkType': 100, 'adminStatus': 1, 'enableRateLimit': False, 'srcTpName': 'GigabitEthernet2/0', 'metric': 10, 'dstTpId': '67eec417-f1f6-43fd-aaf2-79146b5809ba', 'linkId': 'a513e0c7-b134-47fc-b4cf-1b8e7f8e0f33', 'strategy': False}, {'reservableBandWidth': 1000000, 'bandwidth': 1000000, 'dstTpName': 'GigabitEthernet5/0', 'threshold': -1, 'dstDeviceName': 'VSR6', 'operStatus': 1, 'linkName': 'VSR5 To VSR6 Link1', 'srcDeviceName': 'VSR5', 'availableState': False, 'attributeFlags': 0, 'color': 0, 'linkStatus': 1, 'srcNodeId': 'bb0e3e1d-7541-4a59-80e6-b55d9ae3d4ac', 'srcTpId': '9213ae84-61b7-47c4-a6e5-bffadc80e0f7', 'available': 100, 'dstNodeId': '951b9eda-f804-4bfe-a4e1-a648dd7b4fe7', 'linkType': 100, 'adminStatus': 1, 'enableRateLimit': False, 'srcTpName': 'GigabitEthernet6/0', 'metric': 10, 'dstTpId': '79afe820-ff3a-417e-b9d7-4d3d9c766b0f', 'linkId': '8737a1e0-c05c-4ce4-8043-6a17d0484171', 'strategy': False}, {'reservableBandWidth': 1000000, 'bandwidth': 1000000, 'dstTpName': 'GigabitEthernet2/0', 'threshold': -1, 'dstDeviceName': 'VSR1', 'operStatus': 1, 'linkName': 'VSR2 To VSR1 Link1', 'srcDeviceName': 'VSR2', 'availableState': False, 'attributeFlags': 0, 'color': 0, 'linkStatus': 1, 'srcNodeId': 'd235cae2-848e-404c-88e3-1576668834cc', 'srcTpId': 'eeddfa76-eb07-4779-b8ec-b20598379377', 'available': 100, 'dstNodeId': '5fc7e69a-709b-409d-b1e9-093c02394d5a', 'linkType': 100, 'adminStatus': 1, 'enableRateLimit': False, 'srcTpName': 'GigabitEthernet2/0', 'metric': 30, 'dstTpId': 'c76c2543-3651-4cea-9352-b54f0e613f60', 'linkId': '3ca74a78-b8a1-4a15-94c7-2bdd729496bd', 'strategy': False}, {'reservableBandWidth': 1000000, 'bandwidth': 1000000, 'dstTpName': 'GigabitEthernet2/0', 'threshold': -1, 'dstDeviceName': 'VSR3', 'operStatus': 1, 'linkName': 'VSR2 To VSR3 Link1', 'srcDeviceName': 'VSR2', 'availableState': False, 'attributeFlags': 0, 'color': 0, 'linkStatus': 1, 'srcNodeId': 'd235cae2-848e-404c-88e3-1576668834cc', 'srcTpId': 'a8d5727b-2d66-4f09-93b4-e014ff43285e', 'available': 100, 'dstNodeId': 'a92e557a-542e-445f-a38e-9d3cd438110b', 'linkType': 100, 'adminStatus': 1, 'enableRateLimit': False, 'srcTpName': 'GigabitEthernet3/0', 'metric': 25, 'dstTpId': '2e5453aa-5add-4159-8467-02c037689ea9', 'linkId': '6bb45218-bb58-4adc-aa28-f085fdd1ec62', 'strategy': False}, {'reservableBandWidth': 1000000, 'bandwidth': 1000000, 'dstTpName': 'GigabitEthernet6/0', 'threshold': -1, 'dstDeviceName': 'VSR4', 'operStatus': 1, 'linkName': 'VSR6 To VSR4 Link1', 'srcDeviceName': 'VSR6', 'availableState': False, 'attributeFlags': 0, 'color': 0, 'linkStatus': 1, 'srcNodeId': '951b9eda-f804-4bfe-a4e1-a648dd7b4fe7', 'srcTpId': '6e3da6f4-dece-4fee-88fc-0598e6c19664', 'available': 100, 'dstNodeId': '04165eb6-48f0-4e7f-aa08-3e0967fda9a5', 'linkType': 100, 'adminStatus': 1, 'enableRateLimit': False, 'srcTpName': 'GigabitEthernet4/0', 'metric': 10, 'dstTpId': '17b47d3d-5336-4c87-8ad2-04f35da42506', 'linkId': 'd277c528-36c3-449b-a409-5c301acf33c6', 'strategy': False}, {'reservableBandWidth': 1000000, 'bandwidth': 1000000, 'dstTpName': 'GigabitEthernet3/0', 'threshold': -1, 'dstDeviceName': 'VSR4', 'operStatus': 1, 'linkName': 'VSR3 To VSR4 Link1', 'srcDeviceName': 'VSR3', 'availableState': False, 'attributeFlags': 0, 'color': 0, 'linkStatus': 1, 'srcNodeId': 'a92e557a-542e-445f-a38e-9d3cd438110b', 'srcTpId': '3d604a7b-49d5-4e15-bef8-d60da980fcee', 'available': 100, 'dstNodeId': '04165eb6-48f0-4e7f-aa08-3e0967fda9a5', 'linkType': 100, 'adminStatus': 1, 'enableRateLimit': False, 'srcTpName': 'GigabitEthernet4/0', 'metric': 20, 'dstTpId': '3e906922-b4b7-4ef2-b0a3-39814439b855', 'linkId': '3b71a3a2-7bdf-4e31-92dd-948bd08c2b20', 'strategy': False}], 'pageNum': 1, 'totalPage': 1, 'totalItem': 22}}

sna_link_data_old = {
    "output": {
    "totalPage": 1,
    "links": [
      {
        "metric": 10,
        "attributeFlags": 0,
        "srcTpId": "5697c1ac-a7a7-47f6-9b11-cf5d9aade132",
        "enableRateLimit": False,
        "dstTpName": "GigabitEthernet3/1/1",
        "dstTpId": "cc65c833-5017-4617-abfd-6971579358bb",
        "srcNodeId": "d3501601-faed-4d5d-b57b-e528dc1e266e",
        "color": 0,
        "srcDeviceName": "PE3",
        "adminStatus": 1,
        "linkType": 100,
        "srcTpName": "GigabitEthernet3/1/1",
        "dstNodeId": "ffdce32e-97dc-4b39-88c0-f6a494e59658",
        "reservableBandWidth": 1000000,
        "linkId": "bdb460ba-c408-4693-b3ae-f8dcfd90d8a4",
        "linkStatus": 1,
        "operStatus": 1,
        "dstDeviceName": "PE4",
        "linkName": "PE3->PE4",
        "bandwidth": 1000000
      },
      {
        "metric": 20,
        "attributeFlags": 0,
        "srcTpId": "0048bc03-e880-452e-afd0-4888fc7d64e0",
        "enableRateLimit": False,
        "dstTpName": "GigabitEthernet3/2/1",
        "dstTpId": "4eb6ad3e-0371-47ec-9a5f-50d09e8176ae",
        "srcNodeId": "375e2205-da93-4349-a120-571de7496738",
        "color": 0,
        "srcDeviceName": "P2",
        "adminStatus": 1,
        "linkType": 100,
        "srcTpName": "GigabitEthernet3/2/1",
        "dstNodeId": "95390e43-74e3-4910-8e14-f2720711f6e3",
        "reservableBandWidth": 1000000,
        "linkId": "db835f07-3ae6-43f8-9ba9-24dfef46513b",
        "linkStatus": 1,
        "operStatus": 1,
        "dstDeviceName": "P1",
        "linkName": "P2->P1",
        "bandwidth": 1000000
      },
      {
        "metric": 10,
        "attributeFlags": 0,
        "srcTpId": "2a71323f-6190-4bb7-8613-c99570fe4f46",
        "enableRateLimit": False,
        "dstTpName": "GigabitEthernet3/2/2",
        "dstTpId": "ce68a0d3-968f-46e4-99ae-0a2a6f4558da",
        "srcNodeId": "3716b792-59ad-4035-87b5-6a10289fab7b",
        "color": 0,
        "srcDeviceName": "PE1",
        "adminStatus": 1,
        "linkType": 100,
        "srcTpName": "GigabitEthernet3/2/2",
        "dstNodeId": "95390e43-74e3-4910-8e14-f2720711f6e3",
        "reservableBandWidth": 1000000,
        "linkId": "2594f424-89a5-4673-bb25-52a20d0b3dd6",
        "linkStatus": 1,
        "operStatus": 1,
        "dstDeviceName": "P1",
        "linkName": "PE1->P1",
        "bandwidth": 1000000
      },
      {
        "metric": 10,
        "attributeFlags": 0,
        "srcTpId": "b4a2ebef-606f-4540-9b08-8c9848b77ee0",
        "enableRateLimit": False,
        "dstTpName": "GigabitEthernet3/2/3",
        "dstTpId": "4ae8d7a2-4b33-4264-b627-70c3554356cd",
        "srcNodeId": "ffdce32e-97dc-4b39-88c0-f6a494e59658",
        "color": 0,
        "srcDeviceName": "PE4",
        "adminStatus": 1,
        "linkType": 100,
        "srcTpName": "GigabitEthernet3/1/2",
        "dstNodeId": "375e2205-da93-4349-a120-571de7496738",
        "reservableBandWidth": 1000000,
        "linkId": "3d8dc8c2-9e32-492e-a3b0-c788ae62ebdb",
        "linkStatus": 1,
        "operStatus": 1,
        "dstDeviceName": "P2",
        "linkName": "PE4->P2",
        "bandwidth": 1000000
      },
      {
        "metric": 30,
        "attributeFlags": 0,
        "srcTpId": "cba11b3e-f1c9-462c-82e8-d58a521d69a7",
        "enableRateLimit": False,
        "dstTpName": "GigabitEthernet3/2/4",
        "dstTpId": "44284cda-fa9b-4c68-9183-437e2da15576",
        "srcNodeId": "3716b792-59ad-4035-87b5-6a10289fab7b",
        "color": 0,
        "srcDeviceName": "PE1",
        "adminStatus": 1,
        "linkType": 100,
        "srcTpName": "GigabitEthernet3/2/3",
        "dstNodeId": "375e2205-da93-4349-a120-571de7496738",
        "reservableBandWidth": 1000000,
        "linkId": "00f0f007-9cf2-492b-8747-cac5035b81da",
        "linkStatus": 1,
        "operStatus": 1,
        "dstDeviceName": "P2",
        "linkName": "PE1->P2",
        "bandwidth": 1000000
      },
      {
        "metric": 10,
        "attributeFlags": 0,
        "srcTpId": "cc65c833-5017-4617-abfd-6971579358bb",
        "enableRateLimit": False,
        "dstTpName": "GigabitEthernet3/1/1",
        "dstTpId": "5697c1ac-a7a7-47f6-9b11-cf5d9aade132",
        "srcNodeId": "ffdce32e-97dc-4b39-88c0-f6a494e59658",
        "color": 0,
        "srcDeviceName": "PE4",
        "adminStatus": 1,
        "linkType": 100,
        "srcTpName": "GigabitEthernet3/1/1",
        "dstNodeId": "d3501601-faed-4d5d-b57b-e528dc1e266e",
        "reservableBandWidth": 1000000,
        "linkId": "9735b71f-380d-4bf3-91e6-eba6e15902bb",
        "linkStatus": 1,
        "operStatus": 1,
        "dstDeviceName": "PE3",
        "linkName": "PE4->PE3",
        "bandwidth": 1000000
      },
      {
        "metric": 25,
        "attributeFlags": 0,
        "srcTpId": "eb0ad418-ac06-45d6-beb9-996285a5a0fc",
        "enableRateLimit": False,
        "dstTpName": "GigabitEthernet3/2/3",
        "dstTpId": "8596f1db-c425-46d4-9e28-9a07d28aa56a",
        "srcNodeId": "95390e43-74e3-4910-8e14-f2720711f6e3",
        "color": 0,
        "srcDeviceName": "P1",
        "adminStatus": 1,
        "linkType": 100,
        "srcTpName": "GigabitEthernet3/2/4",
        "dstNodeId": "a835c187-7c1d-4452-8139-d8d6eecb9cc3",
        "reservableBandWidth": 1000000,
        "linkId": "40db4afe-1337-490a-824e-6d0e5cd6fe19",
        "linkStatus": 1,
        "operStatus": 1,
        "dstDeviceName": "PE2",
        "linkName": "P1->PE2",
        "bandwidth": 1000000
      },
      {
        "metric": 20,
        "attributeFlags": 0,
        "srcTpId": "4eb6ad3e-0371-47ec-9a5f-50d09e8176ae",
        "enableRateLimit": False,
        "dstTpName": "GigabitEthernet3/2/1",
        "dstTpId": "0048bc03-e880-452e-afd0-4888fc7d64e0",
        "srcNodeId": "95390e43-74e3-4910-8e14-f2720711f6e3",
        "color": 0,
        "srcDeviceName": "P1",
        "adminStatus": 1,
        "linkType": 100,
        "srcTpName": "GigabitEthernet3/2/1",
        "dstNodeId": "375e2205-da93-4349-a120-571de7496738",
        "reservableBandWidth": 1000000,
        "linkId": "bc16d72f-c284-4e48-96fb-5e9eb4894efe",
        "linkStatus": 1,
        "operStatus": 1,
        "dstDeviceName": "P2",
        "linkName": "P1->P2",
        "bandwidth": 1000000
      },
      {
        "metric": 10,
        "attributeFlags": 0,
        "srcTpId": "d8cb48dd-3dde-496e-b568-3b38fbd3f019",
        "enableRateLimit": False,
        "dstTpName": "GigabitEthernet3/2/3",
        "dstTpId": "55684970-603c-4fc7-854c-e22836fb2ff2",
        "srcNodeId": "d3501601-faed-4d5d-b57b-e528dc1e266e",
        "color": 0,
        "srcDeviceName": "PE3",
        "adminStatus": 1,
        "linkType": 100,
        "srcTpName": "GigabitEthernet3/1/2",
        "dstNodeId": "95390e43-74e3-4910-8e14-f2720711f6e3",
        "reservableBandWidth": 1000000,
        "linkId": "933c1acd-d0ed-4aa0-b600-8ef506610611",
        "linkStatus": 1,
        "operStatus": 1,
        "dstDeviceName": "P1",
        "linkName": "PE3->P1",
        "bandwidth": 1000000
      },
      {
        "metric": 30,
        "attributeFlags": 0,
        "srcTpId": "be3b56ed-36de-4f7f-b7f7-680c884ef156",
        "enableRateLimit": False,
        "dstTpName": "GigabitEthernet3/2/1",
        "dstTpId": "d8b12e12-3e0d-497e-8dd9-3929ad7ce0a2",
        "srcNodeId": "a835c187-7c1d-4452-8139-d8d6eecb9cc3",
        "color": 0,
        "srcDeviceName": "PE2",
        "adminStatus": 1,
        "linkType": 100,
        "srcTpName": "GigabitEthernet3/2/1",
        "dstNodeId": "3716b792-59ad-4035-87b5-6a10289fab7b",
        "reservableBandWidth": 1000000,
        "linkId": "0e9fd576-10bf-475a-bf41-da1d683dc356",
        "linkStatus": 1,
        "operStatus": 1,
        "dstDeviceName": "PE1",
        "linkName": "PE2->PE1",
        "bandwidth":1000000
      },
      {
        "metric": 15,
        "attributeFlags": 0,
        "srcTpId": "6fef4cc8-6c2a-4272-bd5f-df0a3047aa43",
        "enableRateLimit": False,
        "dstTpName": "GigabitEthernet3/1/3",
        "dstTpId": "48e4f6a1-b18e-43bd-9350-7825cecd2527",
        "srcNodeId": "95390e43-74e3-4910-8e14-f2720711f6e3",
        "color": 0,
        "srcDeviceName": "P1",
        "adminStatus": 1,
        "linkType": 100,
        "srcTpName": "GigabitEthernet3/2/5",
        "dstNodeId": "ffdce32e-97dc-4b39-88c0-f6a494e59658",
        "reservableBandWidth": 1000000,
        "linkId": "3095c1c7-5f87-4ffd-9122-992733046082",
        "linkStatus": 1,
        "operStatus": 1,
        "dstDeviceName": "PE4",
        "linkName": "P1->PE4",
        "bandwidth": 1000000
      },
      {
        "metric": 10,
        "attributeFlags": 0,
        "srcTpId": "70547ca5-6de9-4ced-bab9-82054ad45408",
        "enableRateLimit": False,
        "dstTpName": "GigabitEthernet3/2/2",
        "dstTpId": "31aa053e-7e81-4d21-b05b-a6f793c165a3",
        "srcNodeId": "a835c187-7c1d-4452-8139-d8d6eecb9cc3",
        "color": 0,
        "srcDeviceName": "PE2",
        "adminStatus": 1,
        "linkType": 100,
        "srcTpName": "GigabitEthernet3/2/2",
        "dstNodeId": "375e2205-da93-4349-a120-571de7496738",
        "reservableBandWidth": 1000000,
        "linkId": "9db2814c-6751-4c13-b79a-3656fd5eaf94",
        "linkStatus": 1,
        "operStatus": 1,
        "dstDeviceName": "P2",
        "linkName": "PE2->P2",
        "bandwidth": 1000000
      },
      {
        "metric": 25,
        "attributeFlags": 0,
        "srcTpId": "8596f1db-c425-46d4-9e28-9a07d28aa56a",
        "enableRateLimit": False,
        "dstTpName": "GigabitEthernet3/2/4",
        "dstTpId": "eb0ad418-ac06-45d6-beb9-996285a5a0fc",
        "srcNodeId": "a835c187-7c1d-4452-8139-d8d6eecb9cc3",
        "color": 0,
        "srcDeviceName": "PE2",
        "adminStatus": 1,
        "linkType": 100,
        "srcTpName": "GigabitEthernet3/2/3",
        "dstNodeId": "95390e43-74e3-4910-8e14-f2720711f6e3",
        "reservableBandWidth": 1000000,
        "linkId": "6ba6a58c-54b5-40a6-9a20-812e5ad254b8",
        "linkStatus": 1,
        "operStatus": 1,
        "dstDeviceName": "P1",
        "linkName": "PE2->P1",
        "bandwidth": 1000000
      },
      {
        "metric": 30,
        "attributeFlags": 0,
        "srcTpId": "d8b12e12-3e0d-497e-8dd9-3929ad7ce0a2",
        "enableRateLimit": False,
        "dstTpName": "GigabitEthernet3/2/1",
        "dstTpId": "be3b56ed-36de-4f7f-b7f7-680c884ef156",
        "srcNodeId": "3716b792-59ad-4035-87b5-6a10289fab7b",
        "color": 0,
        "srcDeviceName": "PE1",
        "adminStatus": 1,
        "linkType": 100,
        "srcTpName": "GigabitEthernet3/2/1",
        "dstNodeId": "a835c187-7c1d-4452-8139-d8d6eecb9cc3",
        "reservableBandWidth": 1000000,
        "linkId": "4b62f1d4-9cef-4db2-8085-b4760042afe7",
        "linkStatus": 1,
        "operStatus": 1,
        "dstDeviceName": "PE2",
        "linkName": "PE1->PE2",
        "bandwidth": 1000000
      },
      {
        "metric": 15,
        "attributeFlags": 0,
        "srcTpId": "6e1f31e5-137b-4bb7-bb6a-c4d25a1f3820",
        "enableRateLimit": False,
        "dstTpName": "GigabitEthernet3/2/5",
        "dstTpId": "00843f44-6595-4bd3-a24c-00fdaa1659b1",
        "srcNodeId": "d3501601-faed-4d5d-b57b-e528dc1e266e",
        "color": 0,
        "srcDeviceName": "PE3",
        "adminStatus": 1,
        "linkType": 100,
        "srcTpName": "GigabitEthernet3/1/3",
        "dstNodeId": "375e2205-da93-4349-a120-571de7496738",
        "reservableBandWidth": 1000000,
        "linkId": "a323de9c-665d-4cdb-95e0-e69d3dd92e3a",
        "linkStatus": 1,
        "operStatus": 1,
        "dstDeviceName": "P2",
        "linkName": "PE3->P2",
        "bandwidth": 1000000
      },
      {
        "metric": 15,
        "attributeFlags": 0,
        "srcTpId": "00843f44-6595-4bd3-a24c-00fdaa1659b1",
        "enableRateLimit": False,
        "dstTpName": "GigabitEthernet3/1/3",
        "dstTpId": "6e1f31e5-137b-4bb7-bb6a-c4d25a1f3820",
        "srcNodeId": "375e2205-da93-4349-a120-571de7496738",
        "color": 0,
        "srcDeviceName": "P2",
        "adminStatus": 1,
        "linkType": 100,
        "srcTpName": "GigabitEthernet3/2/5",
        "dstNodeId": "d3501601-faed-4d5d-b57b-e528dc1e266e",
        "reservableBandWidth": 1000000,
        "linkId": "b972ff48-5fbe-4514-8378-3388969ec032",
        "linkStatus": 1,
        "operStatus": 1,
        "dstDeviceName": "PE3",
        "linkName": "P2->PE3",
        "bandwidth": 1000000
      },
      {
        "metric": 15,
        "attributeFlags": 0,
        "srcTpId": "48e4f6a1-b18e-43bd-9350-7825cecd2527",
        "enableRateLimit": False,
        "dstTpName": "GigabitEthernet3/2/5",
        "dstTpId": "6fef4cc8-6c2a-4272-bd5f-df0a3047aa43",
        "srcNodeId": "ffdce32e-97dc-4b39-88c0-f6a494e59658",
        "color": 0,
        "srcDeviceName": "PE4",
        "adminStatus": 1,
        "linkType": 100,
        "srcTpName": "GigabitEthernet3/1/3",
        "dstNodeId": "95390e43-74e3-4910-8e14-f2720711f6e3",
        "reservableBandWidth": 1000000,
        "linkId": "7b8b8a2c-c8e4-46ba-8c25-24fa3b4c4089",
        "linkStatus": 1,
        "operStatus": 1,
        "dstDeviceName": "P1",
        "linkName": "PE4->P1",
        "bandwidth": 1000000
      },
      {
        "metric": 10,
        "attributeFlags": 0,
        "srcTpId": "4ae8d7a2-4b33-4264-b627-70c3554356cd",
        "enableRateLimit": False,
        "dstTpName": "GigabitEthernet3/1/2",
        "dstTpId": "b4a2ebef-606f-4540-9b08-8c9848b77ee0",
        "srcNodeId": "375e2205-da93-4349-a120-571de7496738",
        "color": 0,
        "srcDeviceName": "P2",
        "adminStatus": 1,
        "linkType": 100,
        "srcTpName": "GigabitEthernet3/2/3",
        "dstNodeId": "ffdce32e-97dc-4b39-88c0-f6a494e59658",
        "reservableBandWidth": 1000000,
        "linkId": "6133946c-9030-4cd4-b518-53b68386344c",
        "linkStatus": 1,
        "operStatus": 1,
        "dstDeviceName": "PE4",
        "linkName": "P2->PE4",
        "bandwidth": 1000000
      },
      {
        "metric": 10,
        "attributeFlags": 0,
        "srcTpId": "55684970-603c-4fc7-854c-e22836fb2ff2",
        "enableRateLimit": False,
        "dstTpName": "GigabitEthernet3/1/2",
        "dstTpId": "d8cb48dd-3dde-496e-b568-3b38fbd3f019",
        "srcNodeId": "95390e43-74e3-4910-8e14-f2720711f6e3",
        "color": 0,
        "srcDeviceName": "P1",
        "adminStatus": 1,
        "linkType": 100,
        "srcTpName": "GigabitEthernet3/2/3",
        "dstNodeId": "d3501601-faed-4d5d-b57b-e528dc1e266e",
        "reservableBandWidth": 1000000,
        "linkId": "5a43e5c6-f99a-4217-b3cf-a76cb54c198e",
        "linkStatus": 1,
        "operStatus": 1,
        "dstDeviceName": "PE3",
        "linkName": "P1->PE3",
        "bandwidth": 1000000
      },
      {
        "metric": 10,
        "attributeFlags": 0,
        "srcTpId": "ce68a0d3-968f-46e4-99ae-0a2a6f4558da",
        "enableRateLimit": False,
        "dstTpName": "GigabitEthernet3/2/2",
        "dstTpId": "2a71323f-6190-4bb7-8613-c99570fe4f46",
        "srcNodeId": "95390e43-74e3-4910-8e14-f2720711f6e3",
        "color": 0,
        "srcDeviceName": "P1",
        "adminStatus": 1,
        "linkType": 100,
        "srcTpName": "GigabitEthernet3/2/2",
        "dstNodeId": "3716b792-59ad-4035-87b5-6a10289fab7b",
        "reservableBandWidth": 1000000,
        "linkId": "6bfbf637-2020-4d7d-b027-da6fae977d45",
        "linkStatus": 1,
        "operStatus": 1,
        "dstDeviceName": "PE1",
        "linkName": "P1->PE1",
        "bandwidth": 1000000
      },
      {
        "metric": 10,
        "attributeFlags": 0,
        "srcTpId": "31aa053e-7e81-4d21-b05b-a6f793c165a3",
        "enableRateLimit": False,
        "dstTpName": "GigabitEthernet3/2/2",
        "dstTpId": "70547ca5-6de9-4ced-bab9-82054ad45408",
        "srcNodeId": "375e2205-da93-4349-a120-571de7496738",
        "color": 0,
        "srcDeviceName": "P2",
        "adminStatus": 1,
        "linkType": 100,
        "srcTpName": "GigabitEthernet3/2/2",
        "dstNodeId": "a835c187-7c1d-4452-8139-d8d6eecb9cc3",
        "reservableBandWidth": 1000000,
        "linkId": "0db2e099-6487-4ac8-ab0d-387d0ce3c432",
        "linkStatus": 1,
        "operStatus": 1,
        "dstDeviceName": "PE2",
        "linkName": "P2->PE2",
        "bandwidth": 1000000
      },
      {
        "metric": 25,
        "attributeFlags": 0,
        "srcTpId": "44284cda-fa9b-4c68-9183-437e2da15576",
        "enableRateLimit": False,
        "dstTpName": "GigabitEthernet3/2/3",
        "dstTpId": "cba11b3e-f1c9-462c-82e8-d58a521d69a7",
        "srcNodeId": "375e2205-da93-4349-a120-571de7496738",
        "color": 0,
        "srcDeviceName": "P2",
        "adminStatus": 1,
        "linkType": 100,
        "srcTpName": "GigabitEthernet3/2/4",
        "dstNodeId": "3716b792-59ad-4035-87b5-6a10289fab7b",
        "reservableBandWidth": 1000000,
        "linkId": "d53b4a65-fd52-4162-9906-67f4631f55fb",
        "linkStatus": 1,
        "operStatus": 1,
        "dstDeviceName": "PE1",
        "linkName": "P2->PE1",
        "bandwidth": 1000000
      }
    ],
    "totalItem": 22,
    "pageNum": 1
  }
}


sna_terminal_point_data = {
"c76c2543-3651-4cea-9352-b54f0e613f60":{'output': {'totalItem': 1, 'terminalPoints': [{'tpNumber': '2/0', 'operStatus': 1, 'tpType': 1, 'tpMac': '00:0C:29:7C:A2:01', 'ifIndex': 33, 'tpId': 'c76c2543-3651-4cea-9352-b54f0e613f60', 'tpBandwidth': 1000000, 'tpName': 'GigabitEthernet2/0', 'deviceId': '5fc7e69a-709b-409d-b1e9-093c02394d5a', 'abbreviatedTpName': 'GE2/0', 'tpIpList': [{'tpMask': '255.255.255.0', 'tpIp': '112.40.40.4'}], 'tpMask': '255.255.255.0', 'tpStatus': 1, 'tpMode': 3, 'tpIp': '112.40.40.4'}], 'totalPage': 1, 'pageNum': 1}},
"eeddfa76-eb07-4779-b8ec-b20598379377":{'output': {'totalItem': 1, 'terminalPoints': [{'tpNumber': '2/0', 'operStatus': 1, 'tpType': 1, 'tpMac': '00:0C:29:CF:85:28', 'ifIndex': 33, 'tpId': 'eeddfa76-eb07-4779-b8ec-b20598379377', 'tpBandwidth': 1000000, 'tpName': 'GigabitEthernet2/0', 'deviceId': 'd235cae2-848e-404c-88e3-1576668834cc', 'abbreviatedTpName': 'GE2/0', 'tpIpList': [{'tpMask': '255.255.255.0', 'tpIp': '112.40.40.5'}], 'tpMask': '255.255.255.0', 'tpStatus': 1, 'tpMode': 3, 'tpIp': '112.40.40.5'}], 'totalPage': 1, 'pageNum': 1}},
"7b0e86e9-9e8e-49d5-a146-521d30308381":{'output': {'totalItem': 1, 'terminalPoints': [{'tpNumber': '4/0', 'operStatus': 1, 'tpType': 1, 'tpMac': '00:0C:29:EA:0C:EA', 'ifIndex': 65, 'tpId': '7b0e86e9-9e8e-49d5-a146-521d30308381', 'tpBandwidth': 1000000, 'tpName': 'GigabitEthernet4/0', 'deviceId': 'bb0e3e1d-7541-4a59-80e6-b55d9ae3d4ac', 'abbreviatedTpName': 'GE4/0', 'tpIpList': [{'tpMask': '255.255.255.0', 'tpIp': '116.80.80.4'}], 'tpMask': '255.255.255.0', 'tpStatus': 1, 'tpMode': 3, 'tpIp': '116.80.80.4'}], 'totalPage': 1, 'pageNum': 1}},
"c09a74ba-6d8a-4e9c-870b-25ad0c3b3b2f":{'output': {'totalItem': 1, 'terminalPoints': [{'tpNumber': '5/0', 'operStatus': 1, 'tpType': 1, 'tpMac': '00:0C:29:14:6D:01', 'ifIndex': 81, 'tpId': 'c09a74ba-6d8a-4e9c-870b-25ad0c3b3b2f', 'tpBandwidth': 1000000, 'tpName': 'GigabitEthernet5/0', 'deviceId': '04165eb6-48f0-4e7f-aa08-3e0967fda9a5', 'abbreviatedTpName': 'GE5/0', 'tpIpList': [{'tpMask': '255.255.255.0', 'tpIp': '116.80.80.3'}], 'tpMask': '255.255.255.0', 'tpStatus': 1, 'tpMode': 3, 'tpIp': '116.80.80.3'}], 'totalPage': 1, 'pageNum': 1}},
"512626f4-9840-40ee-92fd-08a57623ee3d":{'output': {'totalItem': 1, 'terminalPoints': [{'tpNumber': '3/0', 'operStatus': 1, 'tpType': 1, 'tpMac': '00:0C:29:7C:A2:0B', 'ifIndex': 49, 'tpId': '512626f4-9840-40ee-92fd-08a57623ee3d', 'tpBandwidth': 1000000, 'tpName': 'GigabitEthernet3/0', 'deviceId': '5fc7e69a-709b-409d-b1e9-093c02394d5a', 'abbreviatedTpName': 'GE3/0', 'tpIpList': [{'tpMask': '255.255.255.0', 'tpIp': '110.10.10.2'}], 'tpMask': '255.255.255.0', 'tpStatus': 1, 'tpMode': 3, 'tpIp': '110.10.10.2'}], 'totalPage': 1, 'pageNum': 1}},
"00ca837d-3c80-4112-8f3f-85620cf0ae2b":{'output': {'totalItem': 1, 'terminalPoints': [{'tpNumber': '3/0', 'operStatus': 1, 'tpType': 1, 'tpMac': '00:0C:29:98:5B:16', 'ifIndex': 49, 'tpId': '00ca837d-3c80-4112-8f3f-85620cf0ae2b', 'tpBandwidth': 1000000, 'tpName': 'GigabitEthernet3/0', 'deviceId': 'a92e557a-542e-445f-a38e-9d3cd438110b', 'abbreviatedTpName': 'GE3/0', 'tpIpList': [{'tpMask': '255.255.255.0', 'tpIp': '110.10.10.3'}], 'tpMask': '255.255.255.0', 'tpStatus': 1, 'tpMode': 3, 'tpIp': '110.10.10.3'}], 'totalPage': 1, 'pageNum': 1}},
"00ca837d-3c80-4112-8f3f-85620cf0ae2b":{'output': {'totalItem': 1, 'terminalPoints': [{'tpNumber': '3/0', 'operStatus': 1, 'tpType': 1, 'tpMac': '00:0C:29:98:5B:16', 'ifIndex': 49, 'tpId': '00ca837d-3c80-4112-8f3f-85620cf0ae2b', 'tpBandwidth': 1000000, 'tpName': 'GigabitEthernet3/0', 'deviceId': 'a92e557a-542e-445f-a38e-9d3cd438110b', 'abbreviatedTpName': 'GE3/0', 'tpIpList': [{'tpMask': '255.255.255.0', 'tpIp': '110.10.10.3'}], 'tpMask': '255.255.255.0', 'tpStatus': 1, 'tpMode': 3, 'tpIp': '110.10.10.3'}], 'totalPage': 1, 'pageNum': 1}},
"512626f4-9840-40ee-92fd-08a57623ee3d":{'output': {'totalItem': 1, 'terminalPoints': [{'tpNumber': '3/0', 'operStatus': 1, 'tpType': 1, 'tpMac': '00:0C:29:7C:A2:0B', 'ifIndex': 49, 'tpId': '512626f4-9840-40ee-92fd-08a57623ee3d', 'tpBandwidth': 1000000, 'tpName': 'GigabitEthernet3/0', 'deviceId': '5fc7e69a-709b-409d-b1e9-093c02394d5a', 'abbreviatedTpName': 'GE3/0', 'tpIpList': [{'tpMask': '255.255.255.0', 'tpIp': '110.10.10.2'}], 'tpMask': '255.255.255.0', 'tpStatus': 1, 'tpMode': 3, 'tpIp': '110.10.10.2'}], 'totalPage': 1, 'pageNum': 1}},
"9b11fe23-e163-4fa9-8fd5-6c819800047a":{'output': {'totalItem': 1, 'terminalPoints': [{'tpNumber': '4/0', 'operStatus': 1, 'tpType': 1, 'tpMac': '00:0C:29:14:6D:F7', 'ifIndex': 65, 'tpId': '9b11fe23-e163-4fa9-8fd5-6c819800047a', 'tpBandwidth': 1000000, 'tpName': 'GigabitEthernet4/0', 'deviceId': '04165eb6-48f0-4e7f-aa08-3e0967fda9a5', 'abbreviatedTpName': 'GE4/0', 'tpIpList': [{'tpMask': '255.255.255.0', 'tpIp': '111.20.20.4'}], 'tpMask': '255.255.255.0', 'tpStatus': 1, 'tpMode': 3, 'tpIp': '111.20.20.4'}], 'totalPage': 1, 'pageNum': 1}},
"0906b532-bf89-4fd7-9d93-b6601d72e548":{'output': {'totalItem': 1, 'terminalPoints': [{'tpNumber': '4/0', 'operStatus': 1, 'tpType': 1, 'tpMac': '00:0C:29:7C:A2:15', 'ifIndex': 65, 'tpId': '0906b532-bf89-4fd7-9d93-b6601d72e548', 'tpBandwidth': 1000000, 'tpName': 'GigabitEthernet4/0', 'deviceId': '5fc7e69a-709b-409d-b1e9-093c02394d5a', 'abbreviatedTpName': 'GE4/0', 'tpIpList': [{'tpMask': '255.255.255.0', 'tpIp': '111.20.20.3'}], 'tpMask': '255.255.255.0', 'tpStatus': 1, 'tpMode': 3, 'tpIp': '111.20.20.3'}], 'totalPage': 1, 'pageNum': 1}},
"3e906922-b4b7-4ef2-b0a3-39814439b855":{'output': {'totalItem': 1, 'terminalPoints': [{'tpNumber': '3/0', 'operStatus': 1, 'tpType': 1, 'tpMac': '00:0C:29:14:6D:ED', 'ifIndex': 49, 'tpId': '3e906922-b4b7-4ef2-b0a3-39814439b855', 'tpBandwidth': 1000000, 'tpName': 'GigabitEthernet3/0', 'deviceId': '04165eb6-48f0-4e7f-aa08-3e0967fda9a5', 'abbreviatedTpName': 'GE3/0', 'tpIpList': [{'tpMask': '255.255.255.0', 'tpIp': '115.70.70.6'}], 'tpMask': '255.255.255.0', 'tpStatus': 1, 'tpMode': 3, 'tpIp': '115.70.70.6'}], 'totalPage': 1, 'pageNum': 1}},
"3d604a7b-49d5-4e15-bef8-d60da980fcee":{'output': {'totalItem': 1, 'terminalPoints': [{'tpNumber': '4/0', 'operStatus': 1, 'tpType': 1, 'tpMac': '00:0C:29:98:5B:20', 'ifIndex': 65, 'tpId': '3d604a7b-49d5-4e15-bef8-d60da980fcee', 'tpBandwidth': 1000000, 'tpName': 'GigabitEthernet4/0', 'deviceId': 'a92e557a-542e-445f-a38e-9d3cd438110b', 'abbreviatedTpName': 'GE4/0', 'tpIpList': [{'tpMask': '255.255.255.0', 'tpIp': '115.70.70.4'}], 'tpMask': '255.255.255.0', 'tpStatus': 1, 'tpMode': 3, 'tpIp': '115.70.70.4'}], 'totalPage': 1, 'pageNum': 1}},
"17b47d3d-5336-4c87-8ad2-04f35da42506":{'output': {'totalItem': 1, 'terminalPoints': [{'tpNumber': '6/0', 'operStatus': 1, 'tpType': 1, 'tpMac': '00:0C:29:14:6D:0B', 'ifIndex': 97, 'tpId': '17b47d3d-5336-4c87-8ad2-04f35da42506', 'tpBandwidth': 1000000, 'tpName': 'GigabitEthernet6/0', 'deviceId': '04165eb6-48f0-4e7f-aa08-3e0967fda9a5', 'abbreviatedTpName': 'GE6/0', 'tpIpList': [{'tpMask': '255.255.255.0', 'tpIp': '117.90.90.2'}], 'tpMask': '255.255.255.0', 'tpStatus': 1, 'tpMode': 3, 'tpIp': '117.90.90.2'}], 'totalPage': 1, 'pageNum': 1}},
"6e3da6f4-dece-4fee-88fc-0598e6c19664":{'output': {'totalItem': 1, 'terminalPoints': [{'tpNumber': '4/0', 'operStatus': 1, 'tpType': 1, 'tpMac': '00:0C:29:95:8D:16', 'ifIndex': 65, 'tpId': '6e3da6f4-dece-4fee-88fc-0598e6c19664', 'tpBandwidth': 1000000, 'tpName': 'GigabitEthernet4/0', 'deviceId': '951b9eda-f804-4bfe-a4e1-a648dd7b4fe7', 'abbreviatedTpName': 'GE4/0', 'tpIpList': [{'tpMask': '255.255.255.0', 'tpIp': '117.90.90.3'}], 'tpMask': '255.255.255.0', 'tpStatus': 1, 'tpMode': 3, 'tpIp': '117.90.90.3'}], 'totalPage': 1, 'pageNum': 1}},
"c09a74ba-6d8a-4e9c-870b-25ad0c3b3b2f":{'output': {'totalItem': 1, 'terminalPoints': [{'tpNumber': '5/0', 'operStatus': 1, 'tpType': 1, 'tpMac': '00:0C:29:14:6D:01', 'ifIndex': 81, 'tpId': 'c09a74ba-6d8a-4e9c-870b-25ad0c3b3b2f', 'tpBandwidth': 1000000, 'tpName': 'GigabitEthernet5/0', 'deviceId': '04165eb6-48f0-4e7f-aa08-3e0967fda9a5', 'abbreviatedTpName': 'GE5/0', 'tpIpList': [{'tpMask': '255.255.255.0', 'tpIp': '116.80.80.3'}], 'tpMask': '255.255.255.0', 'tpStatus': 1, 'tpMode': 3, 'tpIp': '116.80.80.3'}], 'totalPage': 1, 'pageNum': 1}},
"7b0e86e9-9e8e-49d5-a146-521d30308381":{'output': {'totalItem': 1, 'terminalPoints': [{'tpNumber': '4/0', 'operStatus': 1, 'tpType': 1, 'tpMac': '00:0C:29:EA:0C:EA', 'ifIndex': 65, 'tpId': '7b0e86e9-9e8e-49d5-a146-521d30308381', 'tpBandwidth': 1000000, 'tpName': 'GigabitEthernet4/0', 'deviceId': 'bb0e3e1d-7541-4a59-80e6-b55d9ae3d4ac', 'abbreviatedTpName': 'GE4/0', 'tpIpList': [{'tpMask': '255.255.255.0', 'tpIp': '116.80.80.4'}], 'tpMask': '255.255.255.0', 'tpStatus': 1, 'tpMode': 3, 'tpIp': '116.80.80.4'}], 'totalPage': 1, 'pageNum': 1}},
"f30f04a8-ed6e-4a23-8913-f47b62d858f7":{'output': {'totalItem': 1, 'terminalPoints': [{'tpNumber': '6/0', 'operStatus': 1, 'tpType': 1, 'tpMac': '00:0C:29:98:5B:34', 'ifIndex': 97, 'tpId': 'f30f04a8-ed6e-4a23-8913-f47b62d858f7', 'tpBandwidth': 1000000, 'tpName': 'GigabitEthernet6/0', 'deviceId': 'a92e557a-542e-445f-a38e-9d3cd438110b', 'abbreviatedTpName': 'GE6/0', 'tpIpList': [{'tpMask': '255.255.255.0', 'tpIp': '119.20.20.6'}], 'tpMask': '255.255.255.0', 'tpStatus': 1, 'tpMode': 3, 'tpIp': '119.20.20.6'}], 'totalPage': 1, 'pageNum': 1}},
"91a5a214-08f1-4d92-b104-7941df5a3fee":{'output': {'totalItem': 1, 'terminalPoints': [{'tpNumber': '3/0', 'operStatus': 1, 'tpType': 1, 'tpMac': '00:0C:29:95:8D:0C', 'ifIndex': 49, 'tpId': '91a5a214-08f1-4d92-b104-7941df5a3fee', 'tpBandwidth': 1000000, 'tpName': 'GigabitEthernet3/0', 'deviceId': '951b9eda-f804-4bfe-a4e1-a648dd7b4fe7', 'abbreviatedTpName': 'GE3/0', 'tpIpList': [{'tpMask': '255.255.255.0', 'tpIp': '119.20.20.7'}], 'tpMask': '255.255.255.0', 'tpStatus': 1, 'tpMode': 3, 'tpIp': '119.20.20.7'}], 'totalPage': 1, 'pageNum': 1}},
"2e5453aa-5add-4159-8467-02c037689ea9":{'output': {'totalItem': 1, 'terminalPoints': [{'tpNumber': '2/0', 'operStatus': 1, 'tpType': 1, 'tpMac': '00:0C:29:98:5B:0C', 'ifIndex': 33, 'tpId': '2e5453aa-5add-4159-8467-02c037689ea9', 'tpBandwidth': 1000000, 'tpName': 'GigabitEthernet2/0', 'deviceId': 'a92e557a-542e-445f-a38e-9d3cd438110b', 'abbreviatedTpName': 'GE2/0', 'tpIpList': [{'tpMask': '255.255.255.0', 'tpIp': '113.50.50.7'}], 'tpMask': '255.255.255.0', 'tpStatus': 1, 'tpMode': 3, 'tpIp': '113.50.50.7'}], 'totalPage': 1, 'pageNum': 1}},
"a8d5727b-2d66-4f09-93b4-e014ff43285e":{'output': {'totalItem': 1, 'terminalPoints': [{'tpNumber': '3/0', 'operStatus': 1, 'tpType': 1, 'tpMac': '00:0C:29:CF:85:32', 'ifIndex': 49, 'tpId': 'a8d5727b-2d66-4f09-93b4-e014ff43285e', 'tpBandwidth': 1000000, 'tpName': 'GigabitEthernet3/0', 'deviceId': 'd235cae2-848e-404c-88e3-1576668834cc', 'abbreviatedTpName': 'GE3/0', 'tpIpList': [{'tpMask': '255.255.255.0', 'tpIp': '113.50.50.6'}], 'tpMask': '255.255.255.0', 'tpStatus': 1, 'tpMode': 3, 'tpIp': '113.50.50.6'}], 'totalPage': 1, 'pageNum': 1}},
"0906b532-bf89-4fd7-9d93-b6601d72e548":{'output': {'totalItem': 1, 'terminalPoints': [{'tpNumber': '4/0', 'operStatus': 1, 'tpType': 1, 'tpMac': '00:0C:29:7C:A2:15', 'ifIndex': 65, 'tpId': '0906b532-bf89-4fd7-9d93-b6601d72e548', 'tpBandwidth': 1000000, 'tpName': 'GigabitEthernet4/0', 'deviceId': '5fc7e69a-709b-409d-b1e9-093c02394d5a', 'abbreviatedTpName': 'GE4/0', 'tpIpList': [{'tpMask': '255.255.255.0', 'tpIp': '111.20.20.3'}], 'tpMask': '255.255.255.0', 'tpStatus': 1, 'tpMode': 3, 'tpIp': '111.20.20.3'}], 'totalPage': 1, 'pageNum': 1}},
"9b11fe23-e163-4fa9-8fd5-6c819800047a":{'output': {'totalItem': 1, 'terminalPoints': [{'tpNumber': '4/0', 'operStatus': 1, 'tpType': 1, 'tpMac': '00:0C:29:14:6D:F7', 'ifIndex': 65, 'tpId': '9b11fe23-e163-4fa9-8fd5-6c819800047a', 'tpBandwidth': 1000000, 'tpName': 'GigabitEthernet4/0', 'deviceId': '04165eb6-48f0-4e7f-aa08-3e0967fda9a5', 'abbreviatedTpName': 'GE4/0', 'tpIpList': [{'tpMask': '255.255.255.0', 'tpIp': '111.20.20.4'}], 'tpMask': '255.255.255.0', 'tpStatus': 1, 'tpMode': 3, 'tpIp': '111.20.20.4'}], 'totalPage': 1, 'pageNum': 1}},
"839abf41-3320-4db1-96d4-689dd1fd28a4":{'output': {'totalItem': 1, 'terminalPoints': [{'tpNumber': '5/0', 'operStatus': 1, 'tpType': 1, 'tpMac': '00:0C:29:98:5B:2A', 'ifIndex': 81, 'tpId': '839abf41-3320-4db1-96d4-689dd1fd28a4', 'tpBandwidth': 1000000, 'tpName': 'GigabitEthernet5/0', 'deviceId': 'a92e557a-542e-445f-a38e-9d3cd438110b', 'abbreviatedTpName': 'GE5/0', 'tpIpList': [{'tpMask': '255.255.255.0', 'tpIp': '118.100.100.5'}], 'tpMask': '255.255.255.0', 'tpStatus': 1, 'tpMode': 3, 'tpIp': '118.100.100.5'}], 'totalPage': 1, 'pageNum': 1}},
"452c2c0b-7fb6-4a48-9a4a-2333e8ed0b41":{'output': {'totalItem': 1, 'terminalPoints': [{'tpNumber': '3/0', 'operStatus': 1, 'tpType': 1, 'tpMac': '00:0C:29:EA:0C:E0', 'ifIndex': 49, 'tpId': '452c2c0b-7fb6-4a48-9a4a-2333e8ed0b41', 'tpBandwidth': 1000000, 'tpName': 'GigabitEthernet3/0', 'deviceId': 'bb0e3e1d-7541-4a59-80e6-b55d9ae3d4ac', 'abbreviatedTpName': 'GE3/0', 'tpIpList': [{'tpMask': '255.255.255.0', 'tpIp': '118.100.100.6'}], 'tpMask': '255.255.255.0', 'tpStatus': 1, 'tpMode': 3, 'tpIp': '118.100.100.6'}], 'totalPage': 1, 'pageNum': 1}},
"67eec417-f1f6-43fd-aaf2-79146b5809ba":{'output': {'totalItem': 1, 'terminalPoints': [{'tpNumber': '4/0', 'operStatus': 1, 'tpType': 1, 'tpMac': '00:0C:29:CF:85:3C', 'ifIndex': 65, 'tpId': '67eec417-f1f6-43fd-aaf2-79146b5809ba', 'tpBandwidth': 1000000, 'tpName': 'GigabitEthernet4/0', 'deviceId': 'd235cae2-848e-404c-88e3-1576668834cc', 'abbreviatedTpName': 'GE4/0', 'tpIpList': [{'tpMask': '255.255.255.0', 'tpIp': '114.60.60.3'}], 'tpMask': '255.255.255.0', 'tpStatus': 1, 'tpMode': 3, 'tpIp': '114.60.60.3'}], 'totalPage': 1, 'pageNum': 1}},
"b47f7c61-43c8-4e19-902a-28e7b7139a01":{'output': {'totalItem': 1, 'terminalPoints': [{'tpNumber': '2/0', 'operStatus': 1, 'tpType': 1, 'tpMac': '00:0C:29:14:6D:E3', 'ifIndex': 33, 'tpId': 'b47f7c61-43c8-4e19-902a-28e7b7139a01', 'tpBandwidth': 1000000, 'tpName': 'GigabitEthernet2/0', 'deviceId': '04165eb6-48f0-4e7f-aa08-3e0967fda9a5', 'abbreviatedTpName': 'GE2/0', 'tpIpList': [{'tpMask': '255.255.255.0', 'tpIp': '114.60.60.5'}], 'tpMask': '255.255.255.0', 'tpStatus': 1, 'tpMode': 3, 'tpIp': '114.60.60.5'}], 'totalPage': 1, 'pageNum': 1}},
"452c2c0b-7fb6-4a48-9a4a-2333e8ed0b41":{'output': {'totalItem': 1, 'terminalPoints': [{'tpNumber': '3/0', 'operStatus': 1, 'tpType': 1, 'tpMac': '00:0C:29:EA:0C:E0', 'ifIndex': 49, 'tpId': '452c2c0b-7fb6-4a48-9a4a-2333e8ed0b41', 'tpBandwidth': 1000000, 'tpName': 'GigabitEthernet3/0', 'deviceId': 'bb0e3e1d-7541-4a59-80e6-b55d9ae3d4ac', 'abbreviatedTpName': 'GE3/0', 'tpIpList': [{'tpMask': '255.255.255.0', 'tpIp': '118.100.100.6'}], 'tpMask': '255.255.255.0', 'tpStatus': 1, 'tpMode': 3, 'tpIp': '118.100.100.6'}], 'totalPage': 1, 'pageNum': 1}},
"839abf41-3320-4db1-96d4-689dd1fd28a4":{'output': {'totalItem': 1, 'terminalPoints': [{'tpNumber': '5/0', 'operStatus': 1, 'tpType': 1, 'tpMac': '00:0C:29:98:5B:2A', 'ifIndex': 81, 'tpId': '839abf41-3320-4db1-96d4-689dd1fd28a4', 'tpBandwidth': 1000000, 'tpName': 'GigabitEthernet5/0', 'deviceId': 'a92e557a-542e-445f-a38e-9d3cd438110b', 'abbreviatedTpName': 'GE5/0', 'tpIpList': [{'tpMask': '255.255.255.0', 'tpIp': '118.100.100.5'}], 'tpMask': '255.255.255.0', 'tpStatus': 1, 'tpMode': 3, 'tpIp': '118.100.100.5'}], 'totalPage': 1, 'pageNum': 1}},
"79afe820-ff3a-417e-b9d7-4d3d9c766b0f":{'output': {'totalItem': 1, 'terminalPoints': [{'tpNumber': '5/0', 'operStatus': 1, 'tpType': 1, 'tpMac': '00:0C:29:95:8D:20', 'ifIndex': 81, 'tpId': '79afe820-ff3a-417e-b9d7-4d3d9c766b0f', 'tpBandwidth': 1000000, 'tpName': 'GigabitEthernet5/0', 'deviceId': '951b9eda-f804-4bfe-a4e1-a648dd7b4fe7', 'abbreviatedTpName': 'GE5/0', 'tpIpList': [{'tpMask': '255.255.255.0', 'tpIp': '120.30.30.6'}], 'tpMask': '255.255.255.0', 'tpStatus': 1, 'tpMode': 3, 'tpIp': '120.30.30.6'}], 'totalPage': 1, 'pageNum': 1}},
"9213ae84-61b7-47c4-a6e5-bffadc80e0f7":{'output': {'totalItem': 1, 'terminalPoints': [{'tpNumber': '6/0', 'operStatus': 1, 'tpType': 1, 'tpMac': '00:0C:29:EA:0C:FE', 'ifIndex': 97, 'tpId': '9213ae84-61b7-47c4-a6e5-bffadc80e0f7', 'tpBandwidth': 1000000, 'tpName': 'GigabitEthernet6/0', 'deviceId': 'bb0e3e1d-7541-4a59-80e6-b55d9ae3d4ac', 'abbreviatedTpName': 'GE6/0', 'tpIpList': [{'tpMask': '255.255.255.0', 'tpIp': '120.30.30.5'}], 'tpMask': '255.255.255.0', 'tpStatus': 1, 'tpMode': 3, 'tpIp': '120.30.30.5'}], 'totalPage': 1, 'pageNum': 1}},
"91a5a214-08f1-4d92-b104-7941df5a3fee":{'output': {'totalItem': 1, 'terminalPoints': [{'tpNumber': '3/0', 'operStatus': 1, 'tpType': 1, 'tpMac': '00:0C:29:95:8D:0C', 'ifIndex': 49, 'tpId': '91a5a214-08f1-4d92-b104-7941df5a3fee', 'tpBandwidth': 1000000, 'tpName': 'GigabitEthernet3/0', 'deviceId': '951b9eda-f804-4bfe-a4e1-a648dd7b4fe7', 'abbreviatedTpName': 'GE3/0', 'tpIpList': [{'tpMask': '255.255.255.0', 'tpIp': '119.20.20.7'}], 'tpMask': '255.255.255.0', 'tpStatus': 1, 'tpMode': 3, 'tpIp': '119.20.20.7'}], 'totalPage': 1, 'pageNum': 1}},
"f30f04a8-ed6e-4a23-8913-f47b62d858f7":{'output': {'totalItem': 1, 'terminalPoints': [{'tpNumber': '6/0', 'operStatus': 1, 'tpType': 1, 'tpMac': '00:0C:29:98:5B:34', 'ifIndex': 97, 'tpId': 'f30f04a8-ed6e-4a23-8913-f47b62d858f7', 'tpBandwidth': 1000000, 'tpName': 'GigabitEthernet6/0', 'deviceId': 'a92e557a-542e-445f-a38e-9d3cd438110b', 'abbreviatedTpName': 'GE6/0', 'tpIpList': [{'tpMask': '255.255.255.0', 'tpIp': '119.20.20.6'}], 'tpMask': '255.255.255.0', 'tpStatus': 1, 'tpMode': 3, 'tpIp': '119.20.20.6'}], 'totalPage': 1, 'pageNum': 1}},
"b47f7c61-43c8-4e19-902a-28e7b7139a01":{'output': {'totalItem': 1, 'terminalPoints': [{'tpNumber': '2/0', 'operStatus': 1, 'tpType': 1, 'tpMac': '00:0C:29:14:6D:E3', 'ifIndex': 33, 'tpId': 'b47f7c61-43c8-4e19-902a-28e7b7139a01', 'tpBandwidth': 1000000, 'tpName': 'GigabitEthernet2/0', 'deviceId': '04165eb6-48f0-4e7f-aa08-3e0967fda9a5', 'abbreviatedTpName': 'GE2/0', 'tpIpList': [{'tpMask': '255.255.255.0', 'tpIp': '114.60.60.5'}], 'tpMask': '255.255.255.0', 'tpStatus': 1, 'tpMode': 3, 'tpIp': '114.60.60.5'}], 'totalPage': 1, 'pageNum': 1}},
"67eec417-f1f6-43fd-aaf2-79146b5809ba":{'output': {'totalItem': 1, 'terminalPoints': [{'tpNumber': '4/0', 'operStatus': 1, 'tpType': 1, 'tpMac': '00:0C:29:CF:85:3C', 'ifIndex': 65, 'tpId': '67eec417-f1f6-43fd-aaf2-79146b5809ba', 'tpBandwidth': 1000000, 'tpName': 'GigabitEthernet4/0', 'deviceId': 'd235cae2-848e-404c-88e3-1576668834cc', 'abbreviatedTpName': 'GE4/0', 'tpIpList': [{'tpMask': '255.255.255.0', 'tpIp': '114.60.60.3'}], 'tpMask': '255.255.255.0', 'tpStatus': 1, 'tpMode': 3, 'tpIp': '114.60.60.3'}], 'totalPage': 1, 'pageNum': 1}},
"9213ae84-61b7-47c4-a6e5-bffadc80e0f7":{'output': {'totalItem': 1, 'terminalPoints': [{'tpNumber': '6/0', 'operStatus': 1, 'tpType': 1, 'tpMac': '00:0C:29:EA:0C:FE', 'ifIndex': 97, 'tpId': '9213ae84-61b7-47c4-a6e5-bffadc80e0f7', 'tpBandwidth': 1000000, 'tpName': 'GigabitEthernet6/0', 'deviceId': 'bb0e3e1d-7541-4a59-80e6-b55d9ae3d4ac', 'abbreviatedTpName': 'GE6/0', 'tpIpList': [{'tpMask': '255.255.255.0', 'tpIp': '120.30.30.5'}], 'tpMask': '255.255.255.0', 'tpStatus': 1, 'tpMode': 3, 'tpIp': '120.30.30.5'}], 'totalPage': 1, 'pageNum': 1}},
"79afe820-ff3a-417e-b9d7-4d3d9c766b0f":{'output': {'totalItem': 1, 'terminalPoints': [{'tpNumber': '5/0', 'operStatus': 1, 'tpType': 1, 'tpMac': '00:0C:29:95:8D:20', 'ifIndex': 81, 'tpId': '79afe820-ff3a-417e-b9d7-4d3d9c766b0f', 'tpBandwidth': 1000000, 'tpName': 'GigabitEthernet5/0', 'deviceId': '951b9eda-f804-4bfe-a4e1-a648dd7b4fe7', 'abbreviatedTpName': 'GE5/0', 'tpIpList': [{'tpMask': '255.255.255.0', 'tpIp': '120.30.30.6'}], 'tpMask': '255.255.255.0', 'tpStatus': 1, 'tpMode': 3, 'tpIp': '120.30.30.6'}], 'totalPage': 1, 'pageNum': 1}},
"eeddfa76-eb07-4779-b8ec-b20598379377":{'output': {'totalItem': 1, 'terminalPoints': [{'tpNumber': '2/0', 'operStatus': 1, 'tpType': 1, 'tpMac': '00:0C:29:CF:85:28', 'ifIndex': 33, 'tpId': 'eeddfa76-eb07-4779-b8ec-b20598379377', 'tpBandwidth': 1000000, 'tpName': 'GigabitEthernet2/0', 'deviceId': 'd235cae2-848e-404c-88e3-1576668834cc', 'abbreviatedTpName': 'GE2/0', 'tpIpList': [{'tpMask': '255.255.255.0', 'tpIp': '112.40.40.5'}], 'tpMask': '255.255.255.0', 'tpStatus': 1, 'tpMode': 3, 'tpIp': '112.40.40.5'}], 'totalPage': 1, 'pageNum': 1}},
"c76c2543-3651-4cea-9352-b54f0e613f60":{'output': {'totalItem': 1, 'terminalPoints': [{'tpNumber': '2/0', 'operStatus': 1, 'tpType': 1, 'tpMac': '00:0C:29:7C:A2:01', 'ifIndex': 33, 'tpId': 'c76c2543-3651-4cea-9352-b54f0e613f60', 'tpBandwidth': 1000000, 'tpName': 'GigabitEthernet2/0', 'deviceId': '5fc7e69a-709b-409d-b1e9-093c02394d5a', 'abbreviatedTpName': 'GE2/0', 'tpIpList': [{'tpMask': '255.255.255.0', 'tpIp': '112.40.40.4'}], 'tpMask': '255.255.255.0', 'tpStatus': 1, 'tpMode': 3, 'tpIp': '112.40.40.4'}], 'totalPage': 1, 'pageNum': 1}},
"a8d5727b-2d66-4f09-93b4-e014ff43285e":{'output': {'totalItem': 1, 'terminalPoints': [{'tpNumber': '3/0', 'operStatus': 1, 'tpType': 1, 'tpMac': '00:0C:29:CF:85:32', 'ifIndex': 49, 'tpId': 'a8d5727b-2d66-4f09-93b4-e014ff43285e', 'tpBandwidth': 1000000, 'tpName': 'GigabitEthernet3/0', 'deviceId': 'd235cae2-848e-404c-88e3-1576668834cc', 'abbreviatedTpName': 'GE3/0', 'tpIpList': [{'tpMask': '255.255.255.0', 'tpIp': '113.50.50.6'}], 'tpMask': '255.255.255.0', 'tpStatus': 1, 'tpMode': 3, 'tpIp': '113.50.50.6'}], 'totalPage': 1, 'pageNum': 1}},
"2e5453aa-5add-4159-8467-02c037689ea9":{'output': {'totalItem': 1, 'terminalPoints': [{'tpNumber': '2/0', 'operStatus': 1, 'tpType': 1, 'tpMac': '00:0C:29:98:5B:0C', 'ifIndex': 33, 'tpId': '2e5453aa-5add-4159-8467-02c037689ea9', 'tpBandwidth': 1000000, 'tpName': 'GigabitEthernet2/0', 'deviceId': 'a92e557a-542e-445f-a38e-9d3cd438110b', 'abbreviatedTpName': 'GE2/0', 'tpIpList': [{'tpMask': '255.255.255.0', 'tpIp': '113.50.50.7'}], 'tpMask': '255.255.255.0', 'tpStatus': 1, 'tpMode': 3, 'tpIp': '113.50.50.7'}], 'totalPage': 1, 'pageNum': 1}},
"6e3da6f4-dece-4fee-88fc-0598e6c19664":{'output': {'totalItem': 1, 'terminalPoints': [{'tpNumber': '4/0', 'operStatus': 1, 'tpType': 1, 'tpMac': '00:0C:29:95:8D:16', 'ifIndex': 65, 'tpId': '6e3da6f4-dece-4fee-88fc-0598e6c19664', 'tpBandwidth': 1000000, 'tpName': 'GigabitEthernet4/0', 'deviceId': '951b9eda-f804-4bfe-a4e1-a648dd7b4fe7', 'abbreviatedTpName': 'GE4/0', 'tpIpList': [{'tpMask': '255.255.255.0', 'tpIp': '117.90.90.3'}], 'tpMask': '255.255.255.0', 'tpStatus': 1, 'tpMode': 3, 'tpIp': '117.90.90.3'}], 'totalPage': 1, 'pageNum': 1}},
"17b47d3d-5336-4c87-8ad2-04f35da42506":{'output': {'totalItem': 1, 'terminalPoints': [{'tpNumber': '6/0', 'operStatus': 1, 'tpType': 1, 'tpMac': '00:0C:29:14:6D:0B', 'ifIndex': 97, 'tpId': '17b47d3d-5336-4c87-8ad2-04f35da42506', 'tpBandwidth': 1000000, 'tpName': 'GigabitEthernet6/0', 'deviceId': '04165eb6-48f0-4e7f-aa08-3e0967fda9a5', 'abbreviatedTpName': 'GE6/0', 'tpIpList': [{'tpMask': '255.255.255.0', 'tpIp': '117.90.90.2'}], 'tpMask': '255.255.255.0', 'tpStatus': 1, 'tpMode': 3, 'tpIp': '117.90.90.2'}], 'totalPage': 1, 'pageNum': 1}},
"3d604a7b-49d5-4e15-bef8-d60da980fcee":{'output': {'totalItem': 1, 'terminalPoints': [{'tpNumber': '4/0', 'operStatus': 1, 'tpType': 1, 'tpMac': '00:0C:29:98:5B:20', 'ifIndex': 65, 'tpId': '3d604a7b-49d5-4e15-bef8-d60da980fcee', 'tpBandwidth': 1000000, 'tpName': 'GigabitEthernet4/0', 'deviceId': 'a92e557a-542e-445f-a38e-9d3cd438110b', 'abbreviatedTpName': 'GE4/0', 'tpIpList': [{'tpMask': '255.255.255.0', 'tpIp': '115.70.70.4'}], 'tpMask': '255.255.255.0', 'tpStatus': 1, 'tpMode': 3, 'tpIp': '115.70.70.4'}], 'totalPage': 1, 'pageNum': 1}},
"3e906922-b4b7-4ef2-b0a3-39814439b855":{'output': {'totalItem': 1, 'terminalPoints': [{'tpNumber': '3/0', 'operStatus': 1, 'tpType': 1, 'tpMac': '00:0C:29:14:6D:ED', 'ifIndex': 49, 'tpId': '3e906922-b4b7-4ef2-b0a3-39814439b855', 'tpBandwidth': 1000000, 'tpName': 'GigabitEthernet3/0', 'deviceId': '04165eb6-48f0-4e7f-aa08-3e0967fda9a5', 'abbreviatedTpName': 'GE3/0', 'tpIpList': [{'tpMask': '255.255.255.0', 'tpIp': '115.70.70.6'}], 'tpMask': '255.255.255.0', 'tpStatus': 1, 'tpMode': 3, 'tpIp': '115.70.70.6'}], 'totalPage': 1, 'pageNum': 1}}
}


sna_terminal_point_data_old = {
    "5697c1ac-a7a7-47f6-9b11-cf5d9aade132":{
    "output": {
    "totalPage": 1,
    "totalItem": 1,
    "pageNum": 1,
    "terminalPoints": [
      {
        "tpIpList": [
          {
            "tpIp": "120.30.30.5",
            "tpMask": "255.255.255.0"
          }
        ],
        "tpNumber": "3/1/1",
        "tpName": "GigabitEthernet3/1/1",
        "tpMode": 3,
        "tpId": "5697c1ac-a7a7-47f6-9b11-cf5d9aade132",
        "abbreviatedTpName": "GE3/1/1",
        "tpIp": "120.30.30.5",
        "tpStatus": 1,
        "ifIndex": 289,
        "tpBandwidth": 1000000,
        "deviceId": "d3501601-faed-4d5d-b57b-e528dc1e266e",
        "tpType": 1,
        "tpMac": "AC:74:09:87:C8:C6",
        "operStatus": 1,
        "tpMask": "255.255.255.0"
      }
    ]
  }
},
    "0048bc03-e880-452e-afd0-4888fc7d64e0":{
    "output": {
    "totalPage": 1,
    "totalItem": 1,
    "pageNum": 1,
    "terminalPoints": [
      {
        "tpIpList": [
          {
            "tpIp": "115.70.70.6",
            "tpMask": "255.255.255.0"
          }
        ],
        "tpNumber": "3/2/1",
        "tpName": "GigabitEthernet3/2/1",
        "tpMode": 3,
        "tpId": "0048bc03-e880-452e-afd0-4888fc7d64e0",
        "abbreviatedTpName": "GE3/2/1",
        "tpIp": "115.70.70.6",
        "tpStatus": 1,
        "ifIndex": 313,
        "tpBandwidth": 1000000,
        "deviceId": "375e2205-da93-4349-a120-571de7496738",
        "tpType": 1,
        "tpMac": "3C:F5:CC:A1:B0:DE",
        "operStatus": 1,
        "tpMask": "255.255.255.0"
      }
    ]
  }
},
    "2a71323f-6190-4bb7-8613-c99570fe4f46":{
    "output": {
    "totalPage": 1,
    "totalItem": 1,
    "pageNum": 1,
    "terminalPoints": [
      {
        "tpIpList": [
          {
            "tpIp": "110.10.10.2",
            "tpMask": "255.255.255.0"
          }
        ],
        "tpNumber": "3/2/2",
        "tpName": "GigabitEthernet3/2/2",
        "tpMode": 3,
        "tpId": "2a71323f-6190-4bb7-8613-c99570fe4f46",
        "abbreviatedTpName": "GE3/2/2",
        "tpIp": "110.10.10.2",
        "tpStatus": 1,
        "ifIndex": 314,
        "tpBandwidth": 1000000,
        "deviceId": "3716b792-59ad-4035-87b5-6a10289fab7b",
        "tpType": 1,
        "tpMac": "3C:F5:CC:A1:D8:DF",
        "operStatus": 1,
        "tpMask": "255.255.255.0"
      }
    ]
  }
},
    "b4a2ebef-606f-4540-9b08-8c9848b77ee0":{
    "output": {
    "totalPage": 1,
    "totalItem": 1,
    "pageNum": 1,
    "terminalPoints": [
      {
        "tpIpList": [
          {
            "tpIp": "117.90.90.3",
            "tpMask": "255.255.255.0"
          }
        ],
        "tpNumber": "3/1/2",
        "tpName": "GigabitEthernet3/1/2",
        "tpMode": 3,
        "tpId": "b4a2ebef-606f-4540-9b08-8c9848b77ee0",
        "abbreviatedTpName": "GE3/1/2",
        "tpIp": "117.90.90.3",
        "tpStatus": 1,
        "ifIndex": 290,
        "tpBandwidth": 1000000,
        "deviceId": "ffdce32e-97dc-4b39-88c0-f6a494e59658",
        "tpType": 1,
        "tpMac": "AC:74:09:87:D0:C7",
        "operStatus": 1,
        "tpMask": "255.255.255.0"
      }
    ]
  }
},
    "cba11b3e-f1c9-462c-82e8-d58a521d69a7":{
    "output": {
    "totalPage": 1,
    "totalItem": 1,
    "pageNum": 1,
    "terminalPoints": [
      {
        "tpIpList": [
          {
            "tpIp": "111.20.20.3",
            "tpMask": "255.255.255.0"
          }
        ],
        "tpNumber": "3/2/3",
        "tpName": "GigabitEthernet3/2/3",
        "tpMode": 3,
        "tpId": "cba11b3e-f1c9-462c-82e8-d58a521d69a7",
        "abbreviatedTpName": "GE3/2/3",
        "tpIp": "111.20.20.3",
        "tpStatus": 1,
        "ifIndex": 315,
        "tpBandwidth": 1000000,
        "deviceId": "3716b792-59ad-4035-87b5-6a10289fab7b",
        "tpType": 1,
        "tpMac": "3C:F5:CC:A1:D8:E0",
        "operStatus": 1,
        "tpMask": "255.255.255.0"
      }
    ]
  }
},
    "cc65c833-5017-4617-abfd-6971579358bb":{
    "output": {
    "totalPage": 1,
    "totalItem": 1,
    "pageNum": 1,
    "terminalPoints": [
      {
        "tpIpList": [
          {
            "tpIp": "120.30.30.6",
            "tpMask": "255.255.255.0"
          }
        ],
        "tpNumber": "3/1/1",
        "tpName": "GigabitEthernet3/1/1",
        "tpMode": 3,
        "tpId": "cc65c833-5017-4617-abfd-6971579358bb",
        "abbreviatedTpName": "GE3/1/1",
        "tpIp": "120.30.30.6",
        "tpStatus": 1,
        "ifIndex": 289,
        "tpBandwidth": 1000000,
        "deviceId": "ffdce32e-97dc-4b39-88c0-f6a494e59658",
        "tpType": 1,
        "tpMac": "AC:74:09:87:D0:C6",
        "operStatus": 1,
        "tpMask": "255.255.255.0"
      }
    ]
  }
},
    "eb0ad418-ac06-45d6-beb9-996285a5a0fc":{
    "output": {
    "totalPage": 1,
    "totalItem": 1,
    "pageNum": 1,
    "terminalPoints": [
      {
        "tpIpList": [
          {
            "tpIp": "113.50.50.7",
            "tpMask": "255.255.255.0"
          }
        ],
        "tpNumber": "3/2/4",
        "tpName": "GigabitEthernet3/2/4",
        "tpMode": 3,
        "tpId": "eb0ad418-ac06-45d6-beb9-996285a5a0fc",
        "abbreviatedTpName": "GE3/2/4",
        "tpIp": "113.50.50.7",
        "tpStatus": 1,
        "ifIndex": 316,
        "tpBandwidth": 1000000,
        "deviceId": "95390e43-74e3-4910-8e14-f2720711f6e3",
        "tpType": 1,
        "tpMac": "50:DA:00:58:00:E1",
        "operStatus": 1,
        "tpMask": "255.255.255.0"
      }
    ]
  }
},
    "4eb6ad3e-0371-47ec-9a5f-50d09e8176ae":{
    "output": {
    "totalPage": 1,
    "totalItem": 1,
    "pageNum": 1,
    "terminalPoints": [
      {
        "tpIpList": [
          {
            "tpIp": "115.70.70.4",
            "tpMask": "255.255.255.0"
          }
        ],
        "tpNumber": "3/2/1",
        "tpName": "GigabitEthernet3/2/1",
        "tpMode": 3,
        "tpId": "4eb6ad3e-0371-47ec-9a5f-50d09e8176ae",
        "abbreviatedTpName": "GE3/2/1",
        "tpIp": "115.70.70.4",
        "tpStatus": 1,
        "ifIndex": 313,
        "tpBandwidth": 1000000,
        "deviceId": "95390e43-74e3-4910-8e14-f2720711f6e3",
        "tpType": 1,
        "tpMac": "50:DA:00:58:00:DE",
        "operStatus": 1,
        "tpMask": "255.255.255.0"
      }
    ]
  }
},
    "d8cb48dd-3dde-496e-b568-3b38fbd3f019":{
    "output": {
    "totalPage": 1,
    "totalItem": 1,
    "pageNum": 1,
    "terminalPoints": [
      {
        "tpIpList": [
          {
            "tpIp": "118.100.100.6",
            "tpMask": "255.255.255.0"
          }
        ],
        "tpNumber": "3/1/2",
        "tpName": "GigabitEthernet3/1/2",
        "tpMode": 3,
        "tpId": "d8cb48dd-3dde-496e-b568-3b38fbd3f019",
        "abbreviatedTpName": "GE3/1/2",
        "tpIp": "118.100.100.6",
        "tpStatus": 1,
        "ifIndex": 290,
        "tpBandwidth": 1000000,
        "deviceId": "d3501601-faed-4d5d-b57b-e528dc1e266e",
        "tpType": 1,
        "tpMac": "AC:74:09:87:C8:C7",
        "operStatus": 1,
        "tpMask": "255.255.255.0"
      }
    ]
  }
},
    "be3b56ed-36de-4f7f-b7f7-680c884ef156":{
    "output": {
    "totalPage": 1,
    "totalItem": 1,
    "pageNum": 1,
    "terminalPoints": [
      {
        "tpIpList": [
          {
            "tpIp": "112.40.40.5",
            "tpMask": "255.255.255.0"
          }
        ],
        "tpNumber": "3/2/1",
        "tpName": "GigabitEthernet3/2/1",
        "tpMode": 3,
        "tpId": "be3b56ed-36de-4f7f-b7f7-680c884ef156",
        "abbreviatedTpName": "GE3/2/1",
        "tpIp": "112.40.40.5",
        "tpStatus": 1,
        "ifIndex": 313,
        "tpBandwidth": 1000000,
        "deviceId": "a835c187-7c1d-4452-8139-d8d6eecb9cc3",
        "tpType": 1,
        "tpMac": "74:1F:4A:53:18:DE",
        "operStatus": 1,
        "tpMask": "255.255.255.0"
      }
    ]
  }
},
"6fef4cc8-6c2a-4272-bd5f-df0a3047aa43":{
  "output": {
    "totalPage": 1,
    "totalItem": 1,
    "pageNum": 1,
    "terminalPoints": [
      {
        "tpIpList": [
          {
            "tpIp": "119.20.20.6",
            "tpMask": "255.255.255.0"
          }
        ],
        "tpNumber": "3/2/5",
        "tpName": "GigabitEthernet3/2/5",
        "tpMode": 3,
        "tpId": "6fef4cc8-6c2a-4272-bd5f-df0a3047aa43",
        "abbreviatedTpName": "GE3/2/5",
        "tpIp": "119.20.20.6",
        "tpStatus": 1,
        "ifIndex": 317,
        "tpBandwidth": 1000000,
        "deviceId": "95390e43-74e3-4910-8e14-f2720711f6e3",
        "tpType": 1,
        "tpMac": "50:DA:00:58:00:E2",
        "operStatus": 1,
        "tpMask": "255.255.255.0"
      }
    ]
  }
},
    "70547ca5-6de9-4ced-bab9-82054ad45408":{
    "output": {
    "totalPage": 1,
    "totalItem": 1,
    "pageNum": 1,
    "terminalPoints": [
      {
        "tpIpList": [
          {
            "tpIp": "114.60.60.3",
            "tpMask": "255.255.255.0"
          }
        ],
        "tpNumber": "3/2/2",
        "tpName": "GigabitEthernet3/2/2",
        "tpMode": 3,
        "tpId": "70547ca5-6de9-4ced-bab9-82054ad45408",
        "abbreviatedTpName": "GE3/2/2",
        "tpIp": "114.60.60.3",
        "tpStatus": 1,
        "ifIndex": 314,
        "tpBandwidth": 1000000,
        "deviceId": "a835c187-7c1d-4452-8139-d8d6eecb9cc3",
        "tpType": 1,
        "tpMac": "74:1F:4A:53:18:DF",
        "operStatus": 1,
        "tpMask": "255.255.255.0"
      }
    ]
  }
},
    "8596f1db-c425-46d4-9e28-9a07d28aa56a":{
    "output": {
    "totalPage": 1,
    "totalItem": 1,
    "pageNum": 1,
    "terminalPoints": [
      {
        "tpIpList": [
          {
            "tpIp": "113.50.50.6",
            "tpMask": "255.255.255.0"
          }
        ],
        "tpNumber": "3/2/3",
        "tpName": "GigabitEthernet3/2/3",
        "tpMode": 3,
        "tpId": "8596f1db-c425-46d4-9e28-9a07d28aa56a",
        "abbreviatedTpName": "GE3/2/3",
        "tpIp": "113.50.50.6",
        "tpStatus": 1,
        "ifIndex": 315,
        "tpBandwidth": 1000000,
        "deviceId": "a835c187-7c1d-4452-8139-d8d6eecb9cc3",
        "tpType": 1,
        "tpMac": "74:1F:4A:53:18:E0",
        "operStatus": 1,
        "tpMask": "255.255.255.0"
      }
    ]
  }
},
    "d8b12e12-3e0d-497e-8dd9-3929ad7ce0a2":{
    "output": {
    "totalPage": 1,
    "totalItem": 1,
    "pageNum": 1,
    "terminalPoints": [
      {
        "tpIpList": [
          {
            "tpIp": "112.40.40.4",
            "tpMask": "255.255.255.0"
          }
        ],
        "tpNumber": "3/2/1",
        "tpName": "GigabitEthernet3/2/1",
        "tpMode": 3,
        "tpId": "d8b12e12-3e0d-497e-8dd9-3929ad7ce0a2",
        "abbreviatedTpName": "GE3/2/1",
        "tpIp": "112.40.40.4",
        "tpStatus": 1,
        "ifIndex": 313,
        "tpBandwidth": 1000000,
        "deviceId": "3716b792-59ad-4035-87b5-6a10289fab7b",
        "tpType": 1,
        "tpMac": "3C:F5:CC:A1:D8:DE",
        "operStatus": 1,
        "tpMask": "255.255.255.0"
      }
    ]
  }
},
    "6e1f31e5-137b-4bb7-bb6a-c4d25a1f3820":{
    "output": {
    "totalPage": 1,
    "totalItem": 1,
    "pageNum": 1,
    "terminalPoints": [
      {
        "tpIpList": [
          {
            "tpIp": "116.80.80.4",
            "tpMask": "255.255.255.0"
          }
        ],
        "tpNumber": "3/1/3",
        "tpName": "GigabitEthernet3/1/3",
        "tpMode": 3,
        "tpId": "6e1f31e5-137b-4bb7-bb6a-c4d25a1f3820",
        "abbreviatedTpName": "GE3/1/3",
        "tpIp": "116.80.80.4",
        "tpStatus": 1,
        "ifIndex": 291,
        "tpBandwidth": 1000000,
        "deviceId": "d3501601-faed-4d5d-b57b-e528dc1e266e",
        "tpType": 1,
        "tpMac": "AC:74:09:87:C8:C8",
        "operStatus": 1,
        "tpMask": "255.255.255.0"
      }
    ]
  }
},

    # 从这里继续 把deviceId 改为 key 
    "00843f44-6595-4bd3-a24c-00fdaa1659b1":{
    "output": {
    "totalPage": 1,
    "totalItem": 1,
    "pageNum": 1,
    "terminalPoints": [
      {
        "tpIpList": [
          {
            "tpIp": "116.80.80.3",
            "tpMask": "255.255.255.0"
          }
        ],
        "tpNumber": "3/2/5",
        "tpName": "GigabitEthernet3/2/5",
        "tpMode": 3,
        "tpId": "00843f44-6595-4bd3-a24c-00fdaa1659b1",
        "abbreviatedTpName": "GE3/2/5",
        "tpIp": "116.80.80.3",
        "tpStatus": 1,
        "ifIndex": 317,
        "tpBandwidth": 1000000,
        "deviceId": "375e2205-da93-4349-a120-571de7496738",
        "tpType": 1,
        "tpMac": "3C:F5:CC:A1:B0:E2",
        "operStatus": 1,
        "tpMask": "255.255.255.0"
      }
    ]
  }
},
    "48e4f6a1-b18e-43bd-9350-7825cecd2527":{
    "output": {
    "totalPage": 1,
    "totalItem": 1,
    "pageNum": 1,
    "terminalPoints": [
      {
        "tpIpList": [
          {
            "tpIp": "119.20.20.7",
            "tpMask": "255.255.255.0"
          }
        ],
        "tpNumber": "3/1/3",
        "tpName": "GigabitEthernet3/1/3",
        "tpMode": 3,
        "tpId": "48e4f6a1-b18e-43bd-9350-7825cecd2527",
        "abbreviatedTpName": "GE3/1/3",
        "tpIp": "119.20.20.7",
        "tpStatus": 1,
        "ifIndex": 291,
        "tpBandwidth": 1000000,
        "deviceId": "ffdce32e-97dc-4b39-88c0-f6a494e59658",
        "tpType": 1,
        "tpMac": "AC:74:09:87:D0:C8",
        "operStatus": 1,
        "tpMask": "255.255.255.0"
      }
    ]
  }
},
    "4ae8d7a2-4b33-4264-b627-70c3554356cd":{
    "output": {
    "totalPage": 1,
    "totalItem": 1,
    "pageNum": 1,
    "terminalPoints": [
      {
        "tpIpList": [
          {
            "tpIp": "117.90.90.2",
            "tpMask": "255.255.255.0"
          }
        ],
        "tpNumber": "3/2/3",
        "tpName": "GigabitEthernet3/2/3",
        "tpMode": 3,
        "tpId": "4ae8d7a2-4b33-4264-b627-70c3554356cd",
        "abbreviatedTpName": "GE3/2/3",
        "tpIp": "117.90.90.2",
        "tpStatus": 1,
        "ifIndex": 315,
        "tpBandwidth": 1000000,
        "deviceId": "375e2205-da93-4349-a120-571de7496738",
        "tpType": 1,
        "tpMac": "3C:F5:CC:A1:B0:E0",
        "operStatus": 1,
        "tpMask": "255.255.255.0"
      }
    ]
  }
},
    "55684970-603c-4fc7-854c-e22836fb2ff2":{
    "output": {
    "totalPage": 1,
    "totalItem": 1,
    "pageNum": 1,
    "terminalPoints": [
      {
        "tpIpList": [
          {
            "tpIp": "118.100.100.5",
            "tpMask": "255.255.255.0"
          }
        ],
        "tpNumber": "3/2/3",
        "tpName": "GigabitEthernet3/2/3",
        "tpMode": 3,
        "tpId": "55684970-603c-4fc7-854c-e22836fb2ff2",
        "abbreviatedTpName": "GE3/2/3",
        "tpIp": "118.100.100.5",
        "tpStatus": 1,
        "ifIndex": 315,
        "tpBandwidth": 1000000,
        "deviceId": "95390e43-74e3-4910-8e14-f2720711f6e3",
        "tpType": 1,
        "tpMac": "50:DA:00:58:00:E0",
        "operStatus": 1,
        "tpMask": "255.255.255.0"
      }
    ]
  }
},
    "ce68a0d3-968f-46e4-99ae-0a2a6f4558da":{
    "output": {
    "totalPage": 1,
    "totalItem": 1,
    "pageNum": 1,
    "terminalPoints": [
      {
        "tpIpList": [
          {
            "tpIp": "110.10.10.3",
            "tpMask": "255.255.255.0"
          }
        ],
        "tpNumber": "3/2/2",
        "tpName": "GigabitEthernet3/2/2",
        "tpMode": 3,
        "tpId": "ce68a0d3-968f-46e4-99ae-0a2a6f4558da",
        "abbreviatedTpName": "GE3/2/2",
        "tpIp": "110.10.10.3",
        "tpStatus": 1,
        "ifIndex": 314,
        "tpBandwidth": 1000000,
        "deviceId": "95390e43-74e3-4910-8e14-f2720711f6e3",
        "tpType": 1,
        "tpMac": "50:DA:00:58:00:DF",
        "operStatus": 1,
        "tpMask": "255.255.255.0"
      }
    ]
  }
},
    "31aa053e-7e81-4d21-b05b-a6f793c165a3":{
    "output": {
    "totalPage": 1,
    "totalItem": 1,
    "pageNum": 1,
    "terminalPoints": [
      {
        "tpIpList": [
          {
            "tpIp": "114.60.60.5",
            "tpMask": "255.255.255.0"
          }
        ],
        "tpNumber": "3/2/2",
        "tpName": "GigabitEthernet3/2/2",
        "tpMode": 3,
        "tpId": "31aa053e-7e81-4d21-b05b-a6f793c165a3",
        "abbreviatedTpName": "GE3/2/2",
        "tpIp": "114.60.60.5",
        "tpStatus": 1,
        "ifIndex": 314,
        "tpBandwidth": 1000000,
        "deviceId": "375e2205-da93-4349-a120-571de7496738",
        "tpType": 1,
        "tpMac": "3C:F5:CC:A1:B0:DF",
        "operStatus": 1,
        "tpMask": "255.255.255.0"
      }
    ]
  }
},
    "44284cda-fa9b-4c68-9183-437e2da15576":{
    "output": {
    "totalPage": 1,
    "totalItem": 1,
    "pageNum": 1,
    "terminalPoints": [
      {
        "tpIpList": [
          {
            "tpIp": "111.20.20.4",
            "tpMask": "255.255.255.0"
          }
        ],
        "tpNumber": "3/2/4",
        "tpName": "GigabitEthernet3/2/4",
        "tpMode": 3,
        "tpId": "44284cda-fa9b-4c68-9183-437e2da15576",
        "abbreviatedTpName": "GE3/2/4",
        "tpIp": "111.20.20.4",
        "tpStatus": 1,
        "ifIndex": 316,
        "tpBandwidth": 1000000,
        "deviceId": "375e2205-da93-4349-a120-571de7496738",
        "tpType": 1,
        "tpMac": "3C:F5:CC:A1:B0:E1",
        "operStatus": 1,
        "tpMask": "255.255.255.0"
        }
        ]
    }
    }
}

sna_link_quality_data = {
"27f06554-6854-412e-8f6d-5758a2c43075":{'output': {'qualitySource': 0, 'sampleInterval': 5000, 'jitter': 1, 'packetLossRatio': 0, 'delay': 0, 'timeStamp': 1582012083092, 'linkId': '27f06554-6854-412e-8f6d-5758a2c43075'}},
"45aaf289-e8fc-4619-acbe-84820b6c3194":{'output': {'qualitySource': 0, 'sampleInterval': 5000, 'jitter': 1, 'packetLossRatio': 0, 'delay': 0, 'timeStamp': 1582012079266, 'linkId': '45aaf289-e8fc-4619-acbe-84820b6c3194'}},
"166eab8f-b8da-4b52-ad3f-104d1699ad17":{'output': {'qualitySource': 0, 'sampleInterval': 5000, 'jitter': 1, 'packetLossRatio': 0, 'delay': 0, 'timeStamp': 1582012085281, 'linkId': '166eab8f-b8da-4b52-ad3f-104d1699ad17'}},
"e06f12d1-4da3-41f2-82a2-f16662fd3703":{'output': {'qualitySource': 0, 'sampleInterval': 5000, 'jitter': 1, 'packetLossRatio': 0, 'delay': 0, 'timeStamp': 1582012085281, 'linkId': 'e06f12d1-4da3-41f2-82a2-f16662fd3703'}},
"70841762-dc20-449c-8b2c-2b47bf1bb70c":{'output': {'qualitySource': 0, 'sampleInterval': 5000, 'jitter': 1, 'packetLossRatio': 0, 'delay': 0, 'timeStamp': 1582012083107, 'linkId': '70841762-dc20-449c-8b2c-2b47bf1bb70c'}},
"39105d81-86b0-4522-a822-339768a9200b":{'output': {'qualitySource': 0, 'sampleInterval': 5000, 'jitter': 1, 'packetLossRatio': 0, 'delay': 0, 'timeStamp': 1582012085281, 'linkId': '39105d81-86b0-4522-a822-339768a9200b'}},
"9d7bc3d2-b550-4e34-aca6-3891fbe5f254":{'output': {'qualitySource': 0, 'sampleInterval': 5000, 'jitter': 1, 'packetLossRatio': 0, 'delay': 0, 'timeStamp': 1582012080282, 'linkId': '9d7bc3d2-b550-4e34-aca6-3891fbe5f254'}},
"49451261-f38b-491b-b862-97330980f2a5":{'output': {'qualitySource': 0, 'sampleInterval': 5000, 'jitter': 1, 'packetLossRatio': 0, 'delay': 0, 'timeStamp': 1582012079266, 'linkId': '49451261-f38b-491b-b862-97330980f2a5'}},
"3490f918-c557-4d73-a283-91fe6779d417":{'output': {'qualitySource': 0, 'sampleInterval': 5000, 'jitter': 1, 'packetLossRatio': 0, 'delay': 0, 'timeStamp': 1582012085281, 'linkId': '3490f918-c557-4d73-a283-91fe6779d417'}},
"31bcd6f2-8f39-49d4-aa8a-a7793be297f1":{'output': {'qualitySource': 0, 'sampleInterval': 5000, 'jitter': 1, 'packetLossRatio': 0, 'delay': 0, 'timeStamp': 1582012083092, 'linkId': '31bcd6f2-8f39-49d4-aa8a-a7793be297f1'}},
"6308d6ad-eb76-41db-8e92-85672f533c32":{'output': {'qualitySource': 0, 'sampleInterval': 5000, 'jitter': 1, 'packetLossRatio': 0, 'delay': 0, 'timeStamp': 1582012083107, 'linkId': '6308d6ad-eb76-41db-8e92-85672f533c32'}},
"e02d9152-a8c1-4b2a-a759-bd1401c31dba":{'output': {'qualitySource': 0, 'sampleInterval': 5000, 'jitter': 1, 'packetLossRatio': 0, 'delay': 0, 'timeStamp': 1582012079266, 'linkId': 'e02d9152-a8c1-4b2a-a759-bd1401c31dba'}},
"534f5e43-a493-42a6-a29f-57b199b73f6e":{'output': {'qualitySource': 0, 'sampleInterval': 5000, 'jitter': 1, 'packetLossRatio': 0, 'delay': 0, 'timeStamp': 1582012083092, 'linkId': '534f5e43-a493-42a6-a29f-57b199b73f6e'}},
"31c18cbc-4d8f-400a-a135-fd99492e7f07":{'output': {'qualitySource': 0, 'sampleInterval': 5000, 'jitter': 1, 'packetLossRatio': 0, 'delay': 0, 'timeStamp': 1582012079266, 'linkId': '31c18cbc-4d8f-400a-a135-fd99492e7f07'}},
"36d6c757-9d8d-4748-ad84-734eb691e638":{'output': {'qualitySource': 0, 'sampleInterval': 5000, 'jitter': 1, 'packetLossRatio': 0, 'delay': 0, 'timeStamp': 1582012079266, 'linkId': '36d6c757-9d8d-4748-ad84-734eb691e638'}},
"69c95b93-9c59-471b-8d51-441f1e8193fb":{'output': {'qualitySource': 0, 'sampleInterval': 5000, 'jitter': 1, 'packetLossRatio': 0, 'delay': 0, 'timeStamp': 1582012085281, 'linkId': '69c95b93-9c59-471b-8d51-441f1e8193fb'}},
"a513e0c7-b134-47fc-b4cf-1b8e7f8e0f33":{'output': {'qualitySource': 0, 'sampleInterval': 5000, 'jitter': 1, 'packetLossRatio': 0, 'delay': 0, 'timeStamp': 1582012083092, 'linkId': 'a513e0c7-b134-47fc-b4cf-1b8e7f8e0f33'}},
"8737a1e0-c05c-4ce4-8043-6a17d0484171":{'output': {'qualitySource': 0, 'sampleInterval': 5000, 'jitter': 1, 'packetLossRatio': 0, 'delay': 0, 'timeStamp': 1582012079266, 'linkId': '8737a1e0-c05c-4ce4-8043-6a17d0484171'}},
"3ca74a78-b8a1-4a15-94c7-2bdd729496bd":{'output': {'qualitySource': 0, 'sampleInterval': 5000, 'jitter': 1, 'packetLossRatio': 0, 'delay': 0, 'timeStamp': 1582012083092, 'linkId': '3ca74a78-b8a1-4a15-94c7-2bdd729496bd'}},
"6bb45218-bb58-4adc-aa28-f085fdd1ec62":{'output': {'qualitySource': 0, 'sampleInterval': 5000, 'jitter': 1, 'packetLossRatio': 0, 'delay': 0, 'timeStamp': 1582012083092, 'linkId': '6bb45218-bb58-4adc-aa28-f085fdd1ec62'}},
"d277c528-36c3-449b-a409-5c301acf33c6":{'output': {'qualitySource': 0, 'sampleInterval': 5000, 'jitter': 1, 'packetLossRatio': 0, 'delay': 0, 'timeStamp': 1582012080282, 'linkId': 'd277c528-36c3-449b-a409-5c301acf33c6'}},
"3b71a3a2-7bdf-4e31-92dd-948bd08c2b20":{'output': {'qualitySource': 0, 'sampleInterval': 5000, 'jitter': 1, 'packetLossRatio': 0, 'delay': 0, 'timeStamp': 1582012085281, 'linkId': '3b71a3a2-7bdf-4e31-92dd-948bd08c2b20'}}
}


sna_link_quality_data_old = {

    "0e9fd576-10bf-475a-bf41-da1d683dc356":{
        "output": {
            "jitter": 1,
            "timeStamp": 1571136873148,
            "qualitySource": 0,
            "packetLossRatio": 0,
            "linkId": "0e9fd576-10bf-475a-bf41-da1d683dc356",
            "sampleInterval": 5000,
            "delay": 0
        }
    },
    
    "40db4afe-1337-490a-824e-6d0e5cd6fe19":{
        "output": {
            "jitter": 1,
            "timeStamp": 1571137243814,
            "qualitySource": 0,
            "packetLossRatio": 0,
            "linkId": "40db4afe-1337-490a-824e-6d0e5cd6fe19",
            "sampleInterval": 5000,
            "delay": 0
        }
    },

    "6ba6a58c-54b5-40a6-9a20-812e5ad254b8":{
        "output": {
            "jitter": 0,
            "timeStamp": 1571137357158,
            "qualitySource": 0,
            "packetLossRatio": 0,
            "linkId": "6ba6a58c-54b5-40a6-9a20-812e5ad254b8",
            "sampleInterval": 5000,
            "delay": 0
        }
    },

    "bdb460ba-c408-4693-b3ae-f8dcfd90d8a4":{
        "output": {
            "jitter": 0,
            "timeStamp": 1571138233894,
            "qualitySource": 0,
            "packetLossRatio": 0,
            "linkId": "bdb460ba-c408-4693-b3ae-f8dcfd90d8a4",
            "sampleInterval": 5000,
            "delay": 0
        }
    },

    "4b62f1d4-9cef-4db2-8085-b4760042afe7":{
        "output": {
            "jitter": 0,
            "timeStamp": 1571138327961,
            "qualitySource": 0,
            "packetLossRatio": 0,
            "linkId": "4b62f1d4-9cef-4db2-8085-b4760042afe7",
            "sampleInterval": 5000,
            "delay": 0
        }
    },

    "db835f07-3ae6-43f8-9ba9-24dfef46513b":{
        "output": {
            "jitter": 1,
            "timeStamp": 1571138367911,
            "qualitySource": 0,
            "packetLossRatio": 0,
            "linkId": "db835f07-3ae6-43f8-9ba9-24dfef46513b",
            "sampleInterval": 5000,
            "delay": 0
        }
    },

    "2594f424-89a5-4673-bb25-52a20d0b3dd6":{
        "output": {
            "jitter": 1,
            "timeStamp": 1571138417906,
            "qualitySource": 0,
            "packetLossRatio": 0,
            "linkId": "2594f424-89a5-4673-bb25-52a20d0b3dd6",
            "sampleInterval": 5000,
            "delay": 0
        }
    },

    "3d8dc8c2-9e32-492e-a3b0-c788ae62ebdb":{
        "output": {
            "jitter": 1,
            "timeStamp": 1571138457892,
            "qualitySource": 0,
            "packetLossRatio": 0,
            "linkId": "3d8dc8c2-9e32-492e-a3b0-c788ae62ebdb",
            "sampleInterval": 5000,
            "delay": 0
        }
    },

    "00f0f007-9cf2-492b-8747-cac5035b81da":{
        "output": {
            "jitter": 0,
            "timeStamp": 1571138587914,
            "qualitySource": 0,
            "packetLossRatio": 300,
            "linkId": "00f0f007-9cf2-492b-8747-cac5035b81da",
            "sampleInterval": 5000,
            "delay": 0
        }
    },
 
    "a323de9c-665d-4cdb-95e0-e69d3dd92e3a":{
        "output": {
            "jitter": 0,
            "timeStamp": 1571138737923,
            "qualitySource": 0,
            "packetLossRatio": 0,
            "linkId": "a323de9c-665d-4cdb-95e0-e69d3dd92e3a",
            "sampleInterval": 5000,
            "delay": 0
        }
    },

    "b972ff48-5fbe-4514-8378-3388969ec032":{
        "output": {
            "jitter": 1,
            "timeStamp": 1571138777954,
            "qualitySource": 0,
            "packetLossRatio": 0,
            "linkId": "b972ff48-5fbe-4514-8378-3388969ec032",
            "sampleInterval": 5000,
            "delay": 0
        }
    },

    "bc16d72f-c284-4e48-96fb-5e9eb4894efe":{
        "output": {
            "jitter": 1,
            "timeStamp": 1571138817946,
            "qualitySource": 0,
            "packetLossRatio": 0,
            "linkId": "bc16d72f-c284-4e48-96fb-5e9eb4894efe",
            "sampleInterval": 5000,
            "delay": 0
        }
    },

    "7b8b8a2c-c8e4-46ba-8c25-24fa3b4c4089":{
        "output": {
            "jitter": 1,
            "timeStamp": 1571138857932,
            "qualitySource": 0,
            "packetLossRatio": 0,
            "linkId": "7b8b8a2c-c8e4-46ba-8c25-24fa3b4c4089",
            "sampleInterval": 5000,
            "delay": 0
        }
    },

    "9735b71f-380d-4bf3-91e6-eba6e15902bb":{
        "output": {
            "jitter": 0,
            "timeStamp": 1571138897948,
            "qualitySource": 0,
            "packetLossRatio": 0,
            "linkId": "9735b71f-380d-4bf3-91e6-eba6e15902bb",
            "sampleInterval": 5000,
            "delay": 0
        }
    },


    "3095c1c7-5f87-4ffd-9122-992733046082":{
        "output": {
            "jitter": 1,
            "timeStamp": 1571138937957,
            "qualitySource": 0,
            "packetLossRatio": 0,
            "linkId": "3095c1c7-5f87-4ffd-9122-992733046082",
            "sampleInterval": 5000,
            "delay": 0
        }
    },

    "6133946c-9030-4cd4-b518-53b68386344c":{
        "output": {
            "jitter": 1,
            "timeStamp": 1571138987976,
            "qualitySource": 0,
            "packetLossRatio": 0,
            "linkId": "6133946c-9030-4cd4-b518-53b68386344c",
            "sampleInterval": 5000,
            "delay": 0
        }
    },

    "933c1acd-d0ed-4aa0-b600-8ef506610611":{
        "output": {
            "jitter": 0,
            "timeStamp": 1571139028011,
            "qualitySource": 0,
            "packetLossRatio": 0,
            "linkId": "933c1acd-d0ed-4aa0-b600-8ef506610611",
            "sampleInterval": 5000,
            "delay": 0
        }
    },


    "5a43e5c6-f99a-4217-b3cf-a76cb54c198e":{
        "output": {
            "jitter": 1,
            "timeStamp": 1571139067975,
            "qualitySource": 0,
            "packetLossRatio": 0,
            "linkId": "5a43e5c6-f99a-4217-b3cf-a76cb54c198e",
            "sampleInterval": 5000,
            "delay": 0
        }
    },

    "6bfbf637-2020-4d7d-b027-da6fae977d45":{
        "output": {
            "jitter": 1,
            "timeStamp": 1571139107983,
            "qualitySource": 0,
            "packetLossRatio": 0,
            "linkId": "6bfbf637-2020-4d7d-b027-da6fae977d45",
            "sampleInterval": 5000,
            "delay": 0
        }
    },

    "0db2e099-6487-4ac8-ab0d-387d0ce3c432":{
        "output": {
            "jitter": 1,
            "timeStamp": 1571139147994,
            "qualitySource": 0,
            "packetLossRatio": 0,
            "linkId": "0db2e099-6487-4ac8-ab0d-387d0ce3c432",
            "sampleInterval": 5000,
            "delay": 0
        }
    },

    "9db2814c-6751-4c13-b79a-3656fd5eaf94":{
        "output": {
            "jitter": 0,
            "timeStamp": 1571139194207,
            "qualitySource": 0,
            "packetLossRatio": 600,
            "linkId": "9db2814c-6751-4c13-b79a-3656fd5eaf94",
            "sampleInterval": 5000,
            "delay": 0
        }
    },

    "d53b4a65-fd52-4162-9906-67f4631f55fb":{
        "output": {
            "jitter": 1,
            "timeStamp": 1571139267990,
            "qualitySource": 0,
            "packetLossRatio": 1000,
            "linkId": "d53b4a65-fd52-4162-9906-67f4631f55fb",
            "sampleInterval": 5000,
            "delay": 0
        }
    }
}

big_assetDeviceIp_data = {
"5fc7e69a-709b-409d-b1e9-093c02394d5a":{'errorCode': 0, 'data': [{'ip': '112.40.40.4', 'ifIndex': 33, 'mask': '255.255.255.0'}, {'ip': '110.10.10.2', 'ifIndex': 49, 'mask': '255.255.255.0'}, {'ip': '111.20.20.3', 'ifIndex': 65, 'mask': '255.255.255.0'}], 'message': ''},
"04165eb6-48f0-4e7f-aa08-3e0967fda9a5":{'errorCode': 0, 'data': [{'ip': '114.60.60.5', 'ifIndex': 33, 'mask': '255.255.255.0'}, {'ip': '115.70.70.6', 'ifIndex': 49, 'mask': '255.255.255.0'}, {'ip': '111.20.20.4', 'ifIndex': 65, 'mask': '255.255.255.0'}, {'ip': '116.80.80.3', 'ifIndex': 81, 'mask': '255.255.255.0'}, {'ip': '117.90.90.2', 'ifIndex': 97, 'mask': '255.255.255.0'}], 'message': ''},
"a92e557a-542e-445f-a38e-9d3cd438110b":{'errorCode': 0, 'data': [{'ip': '113.50.50.7', 'ifIndex': 33, 'mask': '255.255.255.0'}, {'ip': '110.10.10.3', 'ifIndex': 49, 'mask': '255.255.255.0'}, {'ip': '115.70.70.4', 'ifIndex': 65, 'mask': '255.255.255.0'}, {'ip': '118.100.100.5', 'ifIndex': 81, 'mask': '255.255.255.0'}, {'ip': '119.20.20.6', 'ifIndex': 97, 'mask': '255.255.255.0'}], 'message': ''},
"d235cae2-848e-404c-88e3-1576668834cc":{'errorCode': 0, 'data': [{'ip': '112.40.40.5', 'ifIndex': 33, 'mask': '255.255.255.0'}, {'ip': '113.50.50.6', 'ifIndex': 49, 'mask': '255.255.255.0'}, {'ip': '114.60.60.3', 'ifIndex': 65, 'mask': '255.255.255.0'}], 'message': ''},
"951b9eda-f804-4bfe-a4e1-a648dd7b4fe7":{'errorCode': 0, 'data': [{'ip': '119.20.20.7', 'ifIndex': 49, 'mask': '255.255.255.0'}, {'ip': '117.90.90.3', 'ifIndex': 65, 'mask': '255.255.255.0'}, {'ip': '120.30.30.6', 'ifIndex': 81, 'mask': '255.255.255.0'}], 'message': ''},
"bb0e3e1d-7541-4a59-80e6-b55d9ae3d4ac":{'errorCode': 0, 'data': [{'ip': '118.100.100.6', 'ifIndex': 49, 'mask': '255.255.255.0'}, {'ip': '116.80.80.4', 'ifIndex': 65, 'mask': '255.255.255.0'}, {'ip': '120.30.30.5', 'ifIndex': 97, 'mask': '255.255.255.0'}], 'message': ''}
}


big_assetDeviceIp_data_old = {
    "f34f84c3-aa6b-4ec8-9bad-2b8f81fd9ee5":{
        "data": [
        {
            "ifIndex": 289,
            "ip": "120.30.30.6",
            "mask": "255.255.255.0"
        },
        {
            "ifIndex": 290,
            "ip": "117.90.90.3",
            "mask": "255.255.255.0"
        },
        {
            "ifIndex": 291,
            "ip": "119.20.20.7",
            "mask": "255.255.255.0"
        },
        ],
        "errorCode": 0,
        "message": ""
    },

    "64f8ca77-0d64-4418-bc33-35f11dabc3c7":{
        "data":[
        {
            "ifIndex": 313,
            "ip": "115.70.70.6",
            "mask": "255.255.255.0"
        },
        {
            "ifIndex": 314,
            "ip": "114.60.60.5",
            "mask": "255.255.255.0"
        },
        {
            "ifIndex": 315,
            "ip": "117.90.90.2",
            "mask": "255.255.255.0"
        },
        {
            "ifIndex": 316,
            "ip": "111.20.20.4",
            "mask": "255.255.255.0"
        },
        {
            "ifIndex": 317,
            "ip": "116.80.80.3",
            "mask": "255.255.255.0"
        }
        ],
        "errorCode": 0,
        "message": ""
    },

    "2b35d549-3dc8-4031-8743-ebdab0470ded":{
        "data": [
        {
            "ifIndex": 313,
            "ip": "112.40.40.5",
            "mask": "255.255.255.0"
        },
        {
            "ifIndex": 314,
            "ip": "114.60.60.3",
            "mask": "255.255.255.0"
        },
        {
            "ifIndex": 315,
            "ip": "113.50.50.6",
            "mask": "255.255.255.0"
        }
        ],
        "errorCode": 0,
        "message": ""
    },

    "0c2ef3e4-581b-42d2-b7e3-e0c48638b645":{
        "data":[
        {
            "ifIndex": 289,
            "ip": "120.30.30.5",
            "mask": "255.255.255.0"
        },
        {
            "ifIndex": 290,
            "ip": "118.100.100.6",
            "mask": "255.255.255.0"
        },
        {
            "ifIndex": 291,
            "ip": "116.80.80.4",
            "mask": "255.255.255.0"
        }
        ],
        "errorCode": 0,
        "message": ""
    },

    "4ea1dd48-de95-428b-8180-3a9be2b47392":{
        "data":[
        {
            "ifIndex": 313,
            "ip": "115.70.70.4",
            "mask": "255.255.255.0"
        },
        {
            "ifIndex": 314,
            "ip": "110.10.10.3",
            "mask": "255.255.255.0"
        },
        {
            "ifIndex": 315,
            "ip": "118.100.100.5",
            "mask": "255.255.255.0"
        },
        {
            "ifIndex": 316,
            "ip": "113.50.50.7",
            "mask": "255.255.255.0"
        },
        {
            "ifIndex": 317,
            "ip": "119.20.20.6",
            "mask": "255.255.255.0"
        }
        ],
        "errorCode": 0,
        "message": ""
    },

    "41ea97fa-ce74-4e0b-80fa-73cf6c49d877":{
        "data":[
        {
            "ifIndex": 313,
            "ip": "112.40.40.4",
            "mask": "255.255.255.0"
        },
        {
            "ifIndex": 314,
            "ip": "110.10.10.2",
            "mask": "255.255.255.0"
        },
        {
            "ifIndex": 315,
            "ip": "111.20.20.3",
            "mask": "255.255.255.0"
        }
        ],
        "errorCode": 0,
        "message": ""
    }    
}

big_tunnel_info_list = [{'tunnelUid': '5d1f31fd64096a7e4f8bb8f62ec655b3', 'ingressLsrIp': '10.99.211.211', 'createTime': 1581994645000, 'fec': '10.99.211.211/2', 'egressLsrIp': '10.99.211.215', 'tunnelId': 2, 'type': 'SR-TE.ILM'}, {'tunnelUid': '6579a18e6ac60c7cf27c63a8a6741ef6', 'ingressLsrIp': '10.99.211.211', 'createTime': 1581994645000, 'fec': '10.99.211.211/1', 'egressLsrIp': '10.99.211.215', 'tunnelId': 1, 'type': 'SR-TE.ILM'}, {'tunnelUid': '698c9cb03b1cfae27db6c9a558c5e40b', 'ingressLsrIp': '10.99.211.212', 'createTime': 1581993620000, 'fec': '10.99.211.212/3', 'egressLsrIp': '10.99.211.216', 'tunnelId': 3, 'type': 'SR-TE.ILM'}, {'tunnelUid': '8d483571dff95a5848e127bfeafbac1b', 'ingressLsrIp': '10.99.211.211', 'createTime': 1581994645000, 'fec': '10.99.211.211/4', 'egressLsrIp': '10.99.211.214', 'tunnelId': 4, 'type': 'SR-TE.ILM'}, {'tunnelUid': '97b76dfdd3390698de3baa8f1a1b16a2', 'ingressLsrIp': '10.99.211.212', 'createTime': 1581993620000, 'fec': '10.99.211.212/1', 'egressLsrIp': '10.99.211.216', 'tunnelId': 1, 'type': 'SR-TE.ILM'}, {'tunnelUid': 'e63747d586c4897d9e203f3c2209e18a', 'ingressLsrIp': '10.99.211.211', 'createTime': 1581994645000, 'fec': '10.99.211.211/6', 'egressLsrIp': '10.99.211.216', 'tunnelId': 6, 'type': 'SR-TE.ILM'}, {'tunnelUid': 'ef8ddaa4a9f9ab43164a186bd3fc63eb', 'ingressLsrIp': '10.99.211.211', 'createTime': 1581994645000, 'fec': '10.99.211.211/3', 'egressLsrIp': '10.99.211.214', 'tunnelId': 3, 'type': 'SR-TE.ILM'}, {'tunnelUid': 'f181ce72c97dbf81600336bf81c5d41a', 'ingressLsrIp': '10.99.211.211', 'createTime': 1581994645000, 'fec': '10.99.211.211/5', 'egressLsrIp': '10.99.211.216', 'tunnelId': 5, 'type': 'SR-TE.ILM'}, {'tunnelUid': 'f3ee79622becaa40e0645419232f92ed', 'ingressLsrIp': '10.99.211.212', 'createTime': 1581993620000, 'fec': '10.99.211.212/2', 'egressLsrIp': '10.99.211.216', 'tunnelId': 2, 'type': 'SR-TE.ILM'}]


big_tunnel_info_list_old = [
      {
        "tunnelUid": "00538f025157c78a06dcdddacceb8f91",
        "ingressLsrIp": "172.100.1.50",
        "egressLsrIp": "172.100.1.54",
        "fec": "172.100.1.50/2",
        "tunnelId": 2,
        "type": "SR-TE.ILM",
        "createTime": 20191015113910
      },
      {
        "tunnelUid": "a0180f1c8001c62664f915943ad60dba",
        "ingressLsrIp": "172.100.1.50",
        "egressLsrIp": "172.100.1.54",
        "fec": "172.100.1.50/1",
        "tunnelId": 1,
        "type": "SR-TE.ILM",
        "createTime": 20191015113910
      }
    ]


big_tunnelPath_list = [{'tunnelUid': '5d1f31fd64096a7e4f8bb8f62ec655b3', 'backupNodes': None, 'mainNodes': [{'backupOutLabel': 0, 'nodeUid': '10.99.211.211/2@10.99.211.211', 'nextHop': '10.99.211.213', 'inLabel': 0, 'outLabel': 0, 'nodeLsrIp': '10.99.211.211', 'backupNextHop': None}, {'backupOutLabel': 0, 'nodeUid': '10.99.211.211/2@10.99.211.213', 'nextHop': '10.99.211.215', 'inLabel': 0, 'outLabel': 0, 'nodeLsrIp': '10.99.211.213', 'backupNextHop': None}, {'backupOutLabel': 0, 'nodeUid': '10.99.211.211/2@10.99.211.215', 'nextHop': None, 'inLabel': 0, 'outLabel': 0, 'nodeLsrIp': '10.99.211.215', 'backupNextHop': None}]}, {'tunnelUid': '6579a18e6ac60c7cf27c63a8a6741ef6', 'backupNodes': None, 'mainNodes': [{'backupOutLabel': 0, 'nodeUid': '10.99.211.211/1@10.99.211.211', 'nextHop': '10.99.211.213', 'inLabel': 0, 'outLabel': 0, 'nodeLsrIp': '10.99.211.211', 'backupNextHop': None}, {'backupOutLabel': 0, 'nodeUid': '10.99.211.211/1@10.99.211.213', 'nextHop': '10.99.211.215', 'inLabel': 0, 'outLabel': 0, 'nodeLsrIp': '10.99.211.213', 'backupNextHop': None}, {'backupOutLabel': 0, 'nodeUid': '10.99.211.211/1@10.99.211.215', 'nextHop': None, 'inLabel': 0, 'outLabel': 0, 'nodeLsrIp': '10.99.211.215', 'backupNextHop': None}]}, {'tunnelUid': '698c9cb03b1cfae27db6c9a558c5e40b', 'backupNodes': None, 'mainNodes': [{'backupOutLabel': 0, 'nodeUid': '10.99.211.212/3@10.99.211.212', 'nextHop': '10.99.211.214', 'inLabel': 0, 'outLabel': 0, 'nodeLsrIp': '10.99.211.212', 'backupNextHop': None}, {'backupOutLabel': 0, 'nodeUid': '10.99.211.212/3@10.99.211.214', 'nextHop': '10.99.211.216', 'inLabel': 0, 'outLabel': 0, 'nodeLsrIp': '10.99.211.214', 'backupNextHop': None}, {'backupOutLabel': 0, 'nodeUid': '10.99.211.212/3@10.99.211.216', 'nextHop': None, 'inLabel': 0, 'outLabel': 0, 'nodeLsrIp': '10.99.211.216', 'backupNextHop': None}]}, {'tunnelUid': '8d483571dff95a5848e127bfeafbac1b', 'backupNodes': None, 'mainNodes': [{'backupOutLabel': 0, 'nodeUid': '10.99.211.211/4@10.99.211.211', 'nextHop': '10.99.211.214', 'inLabel': 0, 'outLabel': 0, 'nodeLsrIp': '10.99.211.211', 'backupNextHop': None}, {'backupOutLabel': 0, 'nodeUid': '10.99.211.211/4@10.99.211.214', 'nextHop': None, 'inLabel': 0, 'outLabel': 0, 'nodeLsrIp': '10.99.211.214', 'backupNextHop': None}]}, {'tunnelUid': '97b76dfdd3390698de3baa8f1a1b16a2', 'backupNodes': None, 'mainNodes': [{'backupOutLabel': 0, 'nodeUid': '10.99.211.212/1@10.99.211.212', 'nextHop': '10.99.211.214', 'inLabel': 0, 'outLabel': 0, 'nodeLsrIp': '10.99.211.212', 'backupNextHop': None}, {'backupOutLabel': 0, 'nodeUid': '10.99.211.212/1@10.99.211.214', 'nextHop': '10.99.211.216', 'inLabel': 0, 'outLabel': 0, 'nodeLsrIp': '10.99.211.214', 'backupNextHop': None}, {'backupOutLabel': 0, 'nodeUid': '10.99.211.212/1@10.99.211.216', 'nextHop': None, 'inLabel': 0, 'outLabel': 0, 'nodeLsrIp': '10.99.211.216', 'backupNextHop': None}]}, {'tunnelUid': 'e63747d586c4897d9e203f3c2209e18a', 'backupNodes': None, 'mainNodes': [{'backupOutLabel': 0, 'nodeUid': '10.99.211.211/6@10.99.211.211', 'nextHop': '10.99.211.213', 'inLabel': 0, 'outLabel': 0, 'nodeLsrIp': '10.99.211.211', 'backupNextHop': None}, {'backupOutLabel': 0, 'nodeUid': '10.99.211.211/6@10.99.211.213', 'nextHop': '10.99.211.216', 'inLabel': 0, 'outLabel': 0, 'nodeLsrIp': '10.99.211.213', 'backupNextHop': None}, {'backupOutLabel': 0, 'nodeUid': '10.99.211.211/6@10.99.211.216', 'nextHop': None, 'inLabel': 0, 'outLabel': 0, 'nodeLsrIp': '10.99.211.216', 'backupNextHop': None}]}, {'tunnelUid': 'ef8ddaa4a9f9ab43164a186bd3fc63eb', 'backupNodes': None, 'mainNodes': [{'backupOutLabel': 0, 'nodeUid': '10.99.211.211/3@10.99.211.211', 'nextHop': '10.99.211.214', 'inLabel': 0, 'outLabel': 0, 'nodeLsrIp': '10.99.211.211', 'backupNextHop': None}, {'backupOutLabel': 0, 'nodeUid': '10.99.211.211/3@10.99.211.214', 'nextHop': None, 'inLabel': 0, 'outLabel': 0, 'nodeLsrIp': '10.99.211.214', 'backupNextHop': None}]}, {'tunnelUid': 'f181ce72c97dbf81600336bf81c5d41a', 'backupNodes': None, 'mainNodes': [{'backupOutLabel': 0, 'nodeUid': '10.99.211.211/5@10.99.211.211', 'nextHop': '10.99.211.213', 'inLabel': 0, 'outLabel': 0, 'nodeLsrIp': '10.99.211.211', 'backupNextHop': None}, {'backupOutLabel': 0, 'nodeUid': '10.99.211.211/5@10.99.211.213', 'nextHop': '10.99.211.216', 'inLabel': 0, 'outLabel': 0, 'nodeLsrIp': '10.99.211.213', 'backupNextHop': None}, {'backupOutLabel': 0, 'nodeUid': '10.99.211.211/5@10.99.211.216', 'nextHop': None, 'inLabel': 0, 'outLabel': 0, 'nodeLsrIp': '10.99.211.216', 'backupNextHop': None}]}, {'tunnelUid': 'f3ee79622becaa40e0645419232f92ed', 'backupNodes': None, 'mainNodes': [{'backupOutLabel': 0, 'nodeUid': '10.99.211.212/2@10.99.211.212', 'nextHop': '10.99.211.213', 'inLabel': 0, 'outLabel': 0, 'nodeLsrIp': '10.99.211.212', 'backupNextHop': None}, {'backupOutLabel': 0, 'nodeUid': '10.99.211.212/2@10.99.211.213', 'nextHop': '10.99.211.214', 'inLabel': 0, 'outLabel': 0, 'nodeLsrIp': '10.99.211.213', 'backupNextHop': None}, {'backupOutLabel': 0, 'nodeUid': '10.99.211.212/2@10.99.211.214', 'nextHop': '10.99.211.215', 'inLabel': 0, 'outLabel': 0, 'nodeLsrIp': '10.99.211.214', 'backupNextHop': None}, {'backupOutLabel': 0, 'nodeUid': '10.99.211.212/2@10.99.211.215', 'nextHop': '10.99.211.216', 'inLabel': 0, 'outLabel': 0, 'nodeLsrIp': '10.99.211.215', 'backupNextHop': None}, {'backupOutLabel': 0, 'nodeUid': '10.99.211.212/2@10.99.211.216', 'nextHop': None, 'inLabel': 0, 'outLabel': 0, 'nodeLsrIp': '10.99.211.216', 'backupNextHop': None}]}]



big_tunnelPath_list_old = [
{
    "tunnelUid": "00538f025157c78a06dcdddacceb8f91",
    "backupNodes": "null",
    "mainNodes": [
{
    "nodeUid": "172.100.1.50/2@172.100.1.50",
    "nodeLsrIp": "172.100.1.50",
    "inLabel": 0,
    "outLabel": 0,
    "nextHop": "172.100.1.52",
    "backupOutLabel": 0,
    "backupNextHop": 'null'
},
{
    "nodeUid": "172.100.1.50/2@172.100.1.52",
    "nodeLsrIp": "172.100.1.52",
    "inLabel": 0,
    "outLabel": 0,
    "nextHop": "172.100.1.54",
    "backupOutLabel": 0,
    "backupNextHop": 'null'
},
{
    "nodeUid": "172.100.1.50/2@172.100.1.54",
    "nodeLsrIp": "172.100.1.54",
    "inLabel": 0,
    "outLabel": 0,
    "nextHop": 'null',
    "backupOutLabel": 0,
    "backupNextHop": 'null'
}
]
},
{
    "tunnelUid": "a0180f1c8001c62664f915943ad60dba",
    "backupNodes": "null",
    "mainNodes": [
{
    "nodeUid": "172.100.1.50/1@172.100.1.50",
    "nodeLsrIp": "172.100.1.50",
    "inLabel": 0,
    "outLabel": 0,
    "nextHop": "172.100.1.52",
    "backupOutLabel": 0,
    "backupNextHop": 'null'
},
{
    "nodeUid": "172.100.1.50/1@172.100.1.52",
    "nodeLsrIp": "172.100.1.52",
    "inLabel": 0,
    "outLabel": 0,
    "nextHop": "172.100.1.54",
    "backupOutLabel": 0,
    "backupNextHop": 'null'
},
{
    "nodeUid": "172.100.1.50/1@172.100.1.54",
    "nodeLsrIp": "172.100.1.54",
    "inLabel": 0,
    "outLabel": 0,
    "nextHop": 'null',
    "backupOutLabel": 0,
    "backupNextHop": 'null'
}
]
}
]


big_tunnelTraffic_list = [{'tunnelUid': '5d1f31fd64096a7e4f8bb8f62ec655b3', 'flow': 0.0, 'throughput': 0.0, 'packetLossRate': 0.0, 'packetErrorRate': 0.0}, {'tunnelUid': '6579a18e6ac60c7cf27c63a8a6741ef6', 'flow': 0.0, 'throughput': 0.0, 'packetLossRate': 0.0, 'packetErrorRate': 0.0}, {'tunnelUid': '698c9cb03b1cfae27db6c9a558c5e40b', 'flow': 0.0, 'throughput': 0.0, 'packetLossRate': 0.0, 'packetErrorRate': 0.0}, {'tunnelUid': '8d483571dff95a5848e127bfeafbac1b', 'flow': 0.0, 'throughput': 0.0, 'packetLossRate': 0.0, 'packetErrorRate': 0.0}, {'tunnelUid': '97b76dfdd3390698de3baa8f1a1b16a2', 'flow': 0.0, 'throughput': 0.0, 'packetLossRate': 0.0, 'packetErrorRate': 0.0}, {'tunnelUid': 'e63747d586c4897d9e203f3c2209e18a', 'flow': 0.0, 'throughput': 0.0, 'packetLossRate': 0.0, 'packetErrorRate': 0.0}, {'tunnelUid': 'ef8ddaa4a9f9ab43164a186bd3fc63eb', 'flow': 0.0, 'throughput': 0.0, 'packetLossRate': 0.0, 'packetErrorRate': 0.0}, {'tunnelUid': 'f181ce72c97dbf81600336bf81c5d41a', 'flow': 0.0, 'throughput': 0.0, 'packetLossRate': 0.0, 'packetErrorRate': 0.0}, {'tunnelUid': 'f3ee79622becaa40e0645419232f92ed', 'flow': 0.0, 'throughput': 0.0, 'packetLossRate': 0.0, 'packetErrorRate': 0.0}]


big_tunnelTraffic_list_old = [
      {
        "tunnelUid": "00538f025157c78a06dcdddacceb8f91",
        "flow": 0,
        "throughput": 0,
        "packetLossRate": 0,
        "packetErrorRate": 0
      },
      {
        "tunnelUid": "a0180f1c8001c62664f915943ad60dba",
        "flow": 2.114,
        "throughput": 72.172,
        "packetLossRate": 0,
        "packetErrorRate": 0
      }
    ]

sna_tunnel_info_data_0000 = {
"output": {
        "totalSize": 2,
        "tunnel": [
            {
                "tunnelId": "c8fbc891-92c8-4fcb-868b-062a1c129f4f",
                "name": "Tunnel2",
                "destIp": "12.5.5.5",
                "deviceId": "3716b792-59ad-4035-87b5-6a10289fab7b",
                "application": [
                    {
                        "name": "DEFAULT"
                    },
                    {
                        "name": "ac7de5c6-6e90-4bf6-8f82-424b7da3411f"
                    }
                ],
                "tunnelType": False,
                "deviceName": "PE1",
                "mode": 0,
                "address": "30fef89d-3531-4d6c-8efe-37326bf550bc",
                "status": 1,
                "tpId": "c8fbc891-92c8-4fcb-868b-062a1c129f4f",
                "number": 2,
                "description": "ADWAN-Tunnel-2",
                "tunnelPaths": {
                    "tunnelPath": [
                        {
                            "status": 1,
                            "tunnelLink": [
                                {
                                    "linkId": "2594f424-89a5-4673-bb25-52a20d0b3dd6"
                                },
                                {
                                    "linkId": "5a43e5c6-f99a-4217-b3cf-a76cb54c198e"
                                }
                            ],
                            "number": 0
                        },
                        {
                            "status": 1,
                            "tunnelLink": [
                                {
                                    "linkId": "4b62f1d4-9cef-4db2-8085-b4760042afe7"
                                },
                                {
                                    "linkId": "3095c1c7-5f87-4ffd-9122-992733046082"
            
                  },
                                {
                                    "linkId": "9735b71f-380d-4bf3-91e6-eba6e15902bb"
                                },
                                {
                                    "linkId": "6ba6a58c-54b5-40a6-9a20-812e5ad254b8"
                                }
                            ],
                            "number": 1
                        }
                    ]
                }
            },
            {
                "tunnelId": "23251b09-8001-4eb9-9c6c-fb6f65f1e8a2",
                "name": "Tunnel1",
                "destIp": "12.5.5.5",
                "deviceId": "3716b792-59ad-4035-87b5-6a10289fab7b",
                "application": [
                    {
                        "name": "DEFAULT"
                    },
                    {
                        "name": "3716b792-59ad-4035-87b5-6a10289fab7b"
                    }
                ],
                "tunnelType": False,
                "deviceName": "PE1",
                "mode": 0,
                "address": "30fef89d-3531-4d6c-8efe-37326bf550bc",
                "status": 1,
                "tpId": "23251b09-8001-4eb9-9c6c-fb6f65f1e8a2",
                "number": 1,
              "description": "ADWAN-Tunnel-1"
            }
        ]
    }
}
# 多隧道

sna_tunnel_info_data = {'output': {'totalSize': 6, 'tunnel': [{'tunnelId': '196ee30b-57e0-4ce5-9406-0e0ea107727a', 'mode': 0, 'name': 'Tunnel3', 'deviceName': 'VSR1', 'address': '0a1659af-1016-4709-9098-e933c99a04a4', 'ldp': True, 'description': 'ADWAN-Tunnel-3', 'deviceId': '5fc7e69a-709b-409d-b1e9-093c02394d5a', 'mpls': True, 'status': 1, 'tunnelType': False, 'application': [{'name': 'DEFAULT'}, {'name': '5fc7e69a-709b-409d-b1e9-093c02394d5a'}], 'areaId': '0.0.0.0', 'protocolType': 1, 'number': 3, 'destIp': '44.4.4.4', 'tpId': '196ee30b-57e0-4ce5-9406-0e0ea107727a', 'shortCutType': 1, 'processId': '1', 'collectionServiceClass': True}, {'tunnelId': 'e1cfff1e-0472-4b4d-9439-9b99dfef0ef5', 'mode': 0, 'deviceName': 'VSR1', 'serviceClass': 2, 'description': 'ADWAN-Tunnel-4', 'mpls': True, 'destIp': '44.4.4.4', 'tunnelPaths': {'tunnelPath': [{'number': 0, 'status': 1, 'tunnelLink': [{'linkId': '6308d6ad-eb76-41db-8e92-85672f533c32'}]}, {'number': 1, 'status': 1, 'tunnelLink': [{'linkId': '166eab8f-b8da-4b52-ad3f-104d1699ad17'}, {'linkId': '3b71a3a2-7bdf-4e31-92dd-948bd08c2b20'}]}]}, 'areaId': '0.0.0.0', 'protocolType': 1, 'number': 4, 'processId': '1', 'name': 'Tunnel4', 'tpId': 'e1cfff1e-0472-4b4d-9439-9b99dfef0ef5', 'ldp': True, 'collectionServiceClass': False, 'deviceId': '5fc7e69a-709b-409d-b1e9-093c02394d5a', 'address': '0a1659af-1016-4709-9098-e933c99a04a4', 'tunnelType': False, 'status': 1, 'application': [{'name': 'DEFAULT'}, {'name': '673fb267-41e0-4ea6-83fc-b93a24d48045'}], 'shortCutType': 1}, {'tunnelId': '8b5d91a2-bf3f-4261-82b9-d7ccf51ac793', 'mode': 0, 'deviceName': 'VSR1', 'serviceClass': 3, 'description': 'ADWAN-Tunnel-6', 'mpls': True, 'destIp': '66.1.1.1', 'tunnelPaths': {'tunnelPath': [{'number': 0, 'status': 1, 'tunnelLink': [{'linkId': '166eab8f-b8da-4b52-ad3f-104d1699ad17'}, {'linkId': '3490f918-c557-4d73-a283-91fe6779d417'}]}, {'number': 1, 'status': 1, 'tunnelLink': [{'linkId': '6308d6ad-eb76-41db-8e92-85672f533c32'}, {'linkId': '9d7bc3d2-b550-4e34-aca6-3891fbe5f254'}]}]}, 'areaId': '0.0.0.0', 'protocolType': 1, 'number': 6, 'processId': '1', 'name': 'Tunnel6', 'tpId': '8b5d91a2-bf3f-4261-82b9-d7ccf51ac793', 'ldp': True, 'collectionServiceClass': False, 'deviceId': '5fc7e69a-709b-409d-b1e9-093c02394d5a', 'address': '0a1659af-1016-4709-9098-e933c99a04a4', 'tunnelType': False, 'status': 1, 'application': [{'name': 'DEFAULT'}, {'name': '83dcd3b9-60af-427f-b4e1-50467f1d6be5'}], 'shortCutType': 1}, {'tunnelId': 'dc541fcd-a7bc-496c-9ab9-81db4281ef22', 'mode': 0, 'name': 'Tunnel5', 'deviceName': 'VSR1', 'address': '0a1659af-1016-4709-9098-e933c99a04a4', 'ldp': True, 'description': 'ADWAN-Tunnel-5', 'deviceId': '5fc7e69a-709b-409d-b1e9-093c02394d5a', 'mpls': True, 'status': 1, 'tunnelType': False, 'application': [{'name': 'DEFAULT'}, {'name': '5fc7e69a-709b-409d-b1e9-093c02394d5a'}], 'areaId': '0.0.0.0', 'protocolType': 1, 'number': 5, 'destIp': '66.1.1.1', 'tpId': 'dc541fcd-a7bc-496c-9ab9-81db4281ef22', 'shortCutType': 1, 'processId': '1', 'collectionServiceClass': True}, {'tunnelId': '1f2ceff8-e0a0-4630-af2c-71ef62a7506e', 'mode': 0, 'name': 'Tunnel1', 'deviceName': 'VSR1', 'address': '0a1659af-1016-4709-9098-e933c99a04a4', 'ldp': True, 'description': 'ADWAN-Tunnel-1', 'deviceId': '5fc7e69a-709b-409d-b1e9-093c02394d5a', 'mpls': True, 'status': 1, 'tunnelType': False, 'application': [{'name': 'DEFAULT'}, {'name': '5fc7e69a-709b-409d-b1e9-093c02394d5a'}], 'areaId': '0.0.0.0', 'protocolType': 1, 'number': 1, 'destIp': '55.5.5.5', 'tpId': '1f2ceff8-e0a0-4630-af2c-71ef62a7506e', 'shortCutType': 1, 'processId': '1', 'collectionServiceClass': True}, {'tunnelId': '26695822-5b20-4d67-9803-2a778ee4abec', 'mode': 0, 'deviceName': 'VSR1', 'serviceClass': 1, 'description': 'ADWAN-Tunnel-2', 'mpls': True, 'destIp': '55.5.5.5', 'tunnelPaths': {'tunnelPath': [{'number': 0, 'status': 1, 'tunnelLink': [{'linkId': 'e02d9152-a8c1-4b2a-a759-bd1401c31dba'}, {'linkId': '166eab8f-b8da-4b52-ad3f-104d1699ad17'}]}]}, 'areaId': '0.0.0.0', 'protocolType': 1, 'number': 2, 'processId': '1', 'name': 'Tunnel2', 'tpId': '26695822-5b20-4d67-9803-2a778ee4abec', 'ldp': True, 'collectionServiceClass': False, 'deviceId': '5fc7e69a-709b-409d-b1e9-093c02394d5a', 'address': '0a1659af-1016-4709-9098-e933c99a04a4', 'tunnelType': False, 'status': 1, 'application': [{'name': 'DEFAULT'}, {'name': '37a1af52-29bc-45f5-b96e-0fc82906d31d'}], 'shortCutType': 1}]}}

sna_tunnel_info_data_old = {
    "output": {
    "totalSize": 11,
    "tunnel": [
      {
        "tunnelId": "c257ff73-45b1-4b46-a103-d810a65bcf42",
        "name": "Tunnel6",
        "destIp": "12.4.4.4",
        "deviceId": "3716b792-59ad-4035-87b5-6a10289fab7b",
        "application": [
          {
            "name": "DEFAULT"
          },
          {
            "name": "1125a17c-d0a3-4057-a96e-22ffd308e0b4"
          }
        ],
        "tunnelType": False,
        "deviceName": "PE1",
        "mode": 0,
        "address": "30fef89d-3531-4d6c-8efe-37326bf550bc",
        "status": 1,
        "tpId": "498e1b07-952b-4a23-be62-02527a91c40c",
        "number": 6,
        "description": "ADWAN-Tunnel-6",
        "tunnelPaths": {
          "tunnelPath": [
            {
              "status": 1,
              "tunnelLink": [
                {
                  "linkId": "2594f424-89a5-4673-bb25-52a20d0b3dd6"
                },
                {
                  "linkId": "a323de9c-665d-4cdb-95e0-e69d3dd92e3a"
                },
                {
                  "linkId": "5a43e5c6-f99a-4217-b3cf-a76cb54c198e"
                }
              ],
          "number": 0
            }
          ]
        }
      },
      {
        "tunnelId": "508ba714-f279-4c05-b70e-3994dc161361",
        "name": "Tunnel5",
        "destIp": "12.4.4.4",
        "deviceId": "3716b792-59ad-4035-87b5-6a10289fab7b",
        "application": [
          {
            "name": "DEFAULT"
          },
          {
            "name": "3716b792-59ad-4035-87b5-6a10289fab7b"
          }
        ],
        "tunnelType": False,
        "deviceName": "PE1",
        "mode": 0,
        "address": "30fef89d-3531-4d6c-8efe-37326bf550bc",
        "status": 1,
        "tpId": "508ba714-f279-4c05-b70e-3994dc161361",
        "number": 5,
        "description": "ADWAN-Tunnel-5"
      },
      {
        "tunnelId": "1a459df0-4c35-45cc-9e91-7f20487dddfe",
        "name": "Tunnel2",
        "destIp": "12.5.5.5",
        "deviceId": "a835c187-7c1d-4452-8139-d8d6eecb9cc3",
        "application": [
          {
            "name": "DEFAULT"
          },
          {
            "name": "cd5696c8-a761-4fc0-9e05-32a46945c87e"
          }
        ],
        "tunnelType": False,
        "deviceName": "PE2",
        "mode": 0,
        "address": "e881849c-ae5a-486a-94db-dad09d6290bc",
        "status": 2,
        "tpId": "19a64558-3dce-49ef-b3e0-ea82ff60bec4",
        "number": 2,
        "description": "ADWAN-Tunnel-2",
        "tunnelPaths": {
          "tunnelPath": [
            {
              "status": 1,
              "tunnelLink": [
                {
                  "linkId": "6ba6a58c-54b5-40a6-9a20-812e5ad254b8"
                },
                {
                  "linkId": "5a43e5c6-f99a-4217-b3cf-a76cb54c198e"
                }
              ],
              "number": 0
            },
            {
              "status": 1,
              "tunnelLink": [
                {
                  "linkId": "b972ff48-5fbe-4514-8378-3388969ec032"
                },
                {
                  "linkId": "9db2814c-6751-4c13-b79a-3656fd5eaf94"
                }
              ],
              "number": 1
            }
          ]
        }
      },
      {
        "tunnelId": "9254f3b2-e3fb-4e08-ae34-e7fcc39e0de7",
        "name": "Tunnel4",
        "destIp": "12.6.6.6",
        "deviceId": "3716b792-59ad-4035-87b5-6a10289fab7b",
        "application": [
          {
            "name": "DEFAULT"
          },
          {
            "name": "f2d73b83-6481-47ed-80e3-c8688fd19d82"
          }
        ],
        "tunnelType": False,
        "deviceName": "PE1",
        "mode": 0,
        "address": "30fef89d-3531-4d6c-8efe-37326bf550bc",
        "status": 1,
        "tpId": "9254f3b2-e3fb-4e08-ae34-e7fcc39e0de7",
        "number": 4,
        "description": "ADWAN-Tunnel-4",
        "tunnelPaths": {
          "tunnelPath": [
            {
              "status": 1,
              "tunnelLink": [
                {
                  "linkId": "3095c1c7-5f87-4ffd-9122-992733046082"
                },
                {
                  "linkId": "2594f424-89a5-4673-bb25-52a20d0b3dd6"
                }
              ],
              "number": 0
            },
            {
              "status": 1,
              "tunnelLink": [
                {
                  "linkId": "00f0f007-9cf2-492b-8747-cac5035b81da"
                },
                {
                  "linkId": "b972ff48-5fbe-4514-8378-3388969ec032"
                },
                {
                  "linkId": "bdb460ba-c408-4693-b3ae-f8dcfd90d8a4"
                }
              ],
              "number": 1
            }
          ]
        }
      },
   
   {
        "tunnelId": "a0705aaf-c00c-4bb7-b3fd-b97e6e4d6505",
        "name": "Tunnel1",
        "destIp": "12.5.5.5",
        "deviceId": "a835c187-7c1d-4452-8139-d8d6eecb9cc3",
        "application": [
          {
            "name": "DEFAULT"
          },
          {
            "name": "a835c187-7c1d-4452-8139-d8d6eecb9cc3"
          }
        ],
        "tunnelType": False,
        "deviceName": "PE2",
        "mode": 0,
        "address": "e881849c-ae5a-486a-94db-dad09d6290bc",
        "status": 2,
        "tpId": "a0705aaf-c00c-4bb7-b3fd-b97e6e4d6505",
        "number": 1,
        "description": "ADWAN-Tunnel-1"
      },
      {
        "tunnelId": "5bbb0dc7-f8a4-4314-90c7-390e14904578",
        "name": "Tunnel3",
        "destIp": "12.6.6.6",
        "deviceId": "3716b792-59ad-4035-87b5-6a10289fab7b",
        "application": [
          {
            "name": "DEFAULT"
          },
          {
            "name": "3716b792-59ad-4035-87b5-6a10289fab7b"
          }
        ],
        "tunnelType": False,
        "deviceName": "PE1",
        "mode": 0,
        "address": "30fef89d-3531-4d6c-8efe-37326bf550bc",
        "status": 1,
        "tpId": "5bbb0dc7-f8a4-4314-90c7-390e14904578",
        "number": 3,
        "description": "ADWAN-Tunnel-3"
      },
      {
        "tunnelId": "1c4945c2-3862-4db0-b8b5-3fac7a3eb574",
        "name": "Tunnel4",
        "destIp": "12.6.6.6",
        "deviceId": "a835c187-7c1d-4452-8139-d8d6eecb9cc3",
        "application": [
          {
            "name": "DEFAULT"
          },
      {
            "name": "486e3d29-902e-415d-84a0-17ba9a128ac2"
          }
        ],
        "tunnelType": False,
        "deviceName": "PE2",
        "mode": 0,
        "address": "e881849c-ae5a-486a-94db-dad09d6290bc",
        "status": 2,
        "tpId": "1c4945c2-3862-4db0-b8b5-3fac7a3eb574",
        "number": 4,
        "description": "ADWAN-Tunnel-4",
        "tunnelPaths": {
          "tunnelPath": [
            {
              "status": 1,
              "tunnelLink": [
                {
                  "linkId": "3095c1c7-5f87-4ffd-9122-992733046082"
                },
                {
                  "linkId": "6ba6a58c-54b5-40a6-9a20-812e5ad254b8"
                }
              ],
              "number": 0
            },
            {
              "status": 1,
              "tunnelLink": [
                {
            "linkId": "b972ff48-5fbe-4514-8378-3388969ec032"
                },
                {
                  "linkId": "9db2814c-6751-4c13-b79a-3656fd5eaf94"
                },
                {
                  "linkId": "bdb460ba-c408-4693-b3ae-f8dcfd90d8a4"
                }
              ],
              "number": 1
            }
          ]
        }
      },
      {
        "tunnelId": "a643056b-4937-4990-b6b7-7886421c6782",
        "name": "Tunnel7",
        "destIp": "12.5.5.5",
        "deviceId": "3716b792-59ad-4035-87b5-6a10289fab7b",
        "application": [
          {
            "name": "DEFAULT"
          },
          {
            "name": "ad492bb6-b8ab-48a4-bfbb-64a16d9a1547"
          }
        ],
        "tunnelType": False,
        "deviceName": "PE1",
        "mode": 0,
        "address": "30fef89d-3531-4d6c-8efe-37326bf550bc",
        "status": 1,
        "tpId": "a643056b-4937-4990-b6b7-7886421c6782",
        "number": 7,
        "description": "ADWAN-Tunnel-7",
        "tunnelPaths": {
          "tunnelPath": [
            {
              "status": 1,
              "tunnelLink": [
                {
                  "linkId": "2594f424-89a5-4673-bb25-52a20d0b3dd6"
                },
                {
                  "linkId": "5a43e5c6-f99a-4217-b3cf-a76cb54c198e"
                }
              ],
              "number": 0
            },
            {
              "status": 1,
              "tunnelLink": [
                {
                  "linkId": "4b62f1d4-9cef-4db2-8085-b4760042afe7"
                },
                {
                  "linkId": "b972ff48-5fbe-4514-8378-3388969ec032"
                },
                {
                  "linkId": "9db2814c-6751-4c13-b79a-3656fd5eaf94"
                }
              ],
              "number": 1
            }
          ]
        }
      },
      {
        "tunnelId": "5acf6409-1724-4e76-941b-cb883980c62f",
        "name": "Tunnel3",
        "destIp": "12.6.6.6",
        "deviceId": "a835c187-7c1d-4452-8139-d8d6eecb9cc3",
        "application": [
          {
            "name": "DEFAULT"
          },
          {
            "name": "a835c187-7c1d-4452-8139-d8d6eecb9cc3"
          }
        ],
        "tunnelType": False,
        "deviceName": "PE2",
        "mode": 0,
        "address": "e881849c-ae5a-486a-94db-dad09d6290bc",
        "status": 2,
        "tpId": "5acf6409-1724-4e76-941b-cb883980c62f",

        "number": 3,
        "description": "ADWAN-Tunnel-3"
      },
      {
        "tunnelId": "c8fbc891-92c8-4fcb-868b-062a1c129f4f",
        "name": "Tunnel2",
        "deleting": False,
        "destIp": "12.5.5.5",
        "deviceId": "3716b792-59ad-4035-87b5-6a10289fab7b",
        "application": [
          {
            "name": "DEFAULT"
          },
          {
            "name": "ac7de5c6-6e90-4bf6-8f82-424b7da3411f"
          }
        ],
        "tunnelType": False,
        "deviceName": "PE1",
        "mode": 0,
        "address": "30fef89d-3531-4d6c-8efe-37326bf550bc",
        "status": 1,
        "tpId": "c8fbc891-92c8-4fcb-868b-062a1c129f4f",
        "number": 2,
        "description": "ADWAN-Tunnel-2",
        "tunnelPaths": {
          "tunnelPath": [
            {
              "status": 1,
              "tunnelLink": [
                {
                  "linkId": "2594f424-89a5-4673-bb25-52a20d0b3dd6"
                },
                {
                  "linkId": "5a43e5c6-f99a-4217-b3cf-a76cb54c198e"
                }
              ],
              "number": 0
            },
            {
              "status": 1,
              "tunnelLink": [
                {
                  "linkId": "4b62f1d4-9cef-4db2-8085-b4760042afe7"
                },
                {
                  "linkId": "b972ff48-5fbe-4514-8378-3388969ec032"
                },
                {
                  "linkId": "9db2814c-6751-4c13-b79a-3656fd5eaf94"
                }
              ],
              "number": 1
            }
          ]
        }
      },
      {
        "tunnelId": "23251b09-8001-4eb9-9c6c-fb6f65f1e8a2",
        "name": "Tunnel1",
        "deleting": False,
        "destIp": "12.5.5.5",
        "deviceId": "3716b792-59ad-4035-87b5-6a10289fab7b",
        "application": [
          {
            "name": "DEFAULT"
          },
          {
            "name": "3716b792-59ad-4035-87b5-6a10289fab7b"
          }
        ],
        "tunnelType": False,
        "deviceName": "PE1",
        "mode": 0,
        "address": "30fef89d-3531-4d6c-8efe-37326bf550bc",
        "status": 1,
        "tpId": "23251b09-8001-4eb9-9c6c-fb6f65f1e8a2",
        "number": 1,
        "description": "ADWAN-Tunnel-1"
      }
    ]
  }
}

sla_policy_data = {'output': {'slaPolicyInfo': [{'slaLevelId': '5dbcaf1b-f2a7-4839-825f-4f0bb0708eb9', 'pathNum': 1, 'maxBandwidth': 2000000000, 'policyId': 'ad2c53ef-f369-4a9d-a569-5a5d1efe5734', 'pathType': 1, 'policyName': 'base', 'maxHop': -1, 'minBandwidth': 10, 'enableRateLimit': False}]}}


sla_policy_data_old = {
    "output": {
        "slaPolicyInfo":[
        {
            "minBandwidth": 10,
            "maxBandwidth": 2000000000,
            "maxHop":-1,
            "pathType":1,
            "enableRateLimit": False,
            "slaLevelId": "613fc325-a0a0-460f-b7a3-548dc84dc4b7",
            "policyName": "ptest",
            "pathNum":1,
            "policyId": "6bbd7e7c-06e2-45f6-97e7-43b65592090c"
        }
        ]
    }
}

all_group_info_data = {'output': {'total': 3, 'flowGroupInstanceInfo': [{'pathStatus': 0, 'srcNode': '5fc7e69a-709b-409d-b1e9-093c02394d5a', 'dstNode': '04165eb6-48f0-4e7f-aa08-3e0967fda9a5', 'flowPaths': [{'collectId': '684c565c-4e00-4c94-b754-f9f663e8d588', 'defaultTunnelId': '196ee30b-57e0-4ce5-9406-0e0ea107727a', 'defaultCollectId': '0b9a98fb-8885-4baa-a2e2-d23df81b7543', 'paths': [{'linkList': [{'linkId': '6308d6ad-eb76-41db-8e92-85672f533c32'}], 'pathNumber': 0, 'strictStatus': 1}, {'linkList': [{'linkId': '166eab8f-b8da-4b52-ad3f-104d1699ad17'}, {'linkId': '3b71a3a2-7bdf-4e31-92dd-948bd08c2b20'}], 'pathNumber': 1, 'strictStatus': 1}], 'realPaths': [{'pathNumber': 0, 'strictStatus': 1, 'nodeTpPairs': [{'dstNodeName': 'VSR4', 'srcTpName': 'GigabitEthernet4/0', 'dstTpName': 'GigabitEthernet4/0', 'srcNodeName': 'VSR1'}]}, {'pathNumber': 1, 'strictStatus': 1, 'nodeTpPairs': [{'dstNodeName': 'VSR3', 'srcTpName': 'GigabitEthernet3/0', 'dstTpName': 'GigabitEthernet3/0', 'srcNodeName': 'VSR1'}, {'dstNodeName': 'VSR4', 'srcTpName': 'GigabitEthernet4/0', 'dstTpName': 'GigabitEthernet3/0', 'srcNodeName': 'VSR3'}]}], 'tunnelId': 'e1cfff1e-0472-4b4d-9439-9b99dfef0ef5'}], 'status': 0, 'flowGroupInstanceId': '673fb267-41e0-4ea6-83fc-b93a24d48045', 'flowGroupId': '4ac279d4-5bdf-41bd-b689-0420869c020c'}, {'pathStatus': 1, 'srcNode': '5fc7e69a-709b-409d-b1e9-093c02394d5a', 'dstNode': 'bb0e3e1d-7541-4a59-80e6-b55d9ae3d4ac', 'flowPaths': [{'collectId': '6e492b97-90db-41ec-9730-f99d2089de96', 'defaultTunnelId': '1f2ceff8-e0a0-4630-af2c-71ef62a7506e', 'defaultCollectId': 'e4bc4754-741e-4f09-b4f1-057781b780d1', 'paths': [{'linkList': [{'linkId': '166eab8f-b8da-4b52-ad3f-104d1699ad17'}, {'linkId': 'e02d9152-a8c1-4b2a-a759-bd1401c31dba'}], 'pathNumber': 0, 'strictStatus': 1}], 'realPaths': [{'pathNumber': 0, 'strictStatus': 1, 'nodeTpPairs': [{'dstNodeName': 'VSR3', 'srcTpName': 'GigabitEthernet3/0', 'dstTpName': 'GigabitEthernet3/0', 'srcNodeName': 'VSR1'}, {'dstNodeName': 'VSR5', 'srcTpName': 'GigabitEthernet5/0', 'dstTpName': 'GigabitEthernet3/0', 'srcNodeName': 'VSR3'}]}], 'tunnelId': '26695822-5b20-4d67-9803-2a778ee4abec'}], 'status': 0, 'flowGroupInstanceId': '37a1af52-29bc-45f5-b96e-0fc82906d31d', 'flowGroupId': '2461d0df-e668-4fe9-bb0a-a88e84280659', 'instancePaths': [{'pathNum': 'BACK', 'pathId': 'a92e557a-542e-445f-a38e-9d3cd438110b', 'sortNum': 0, 'pathType': 'NODE', 'constraintType': 'EXCLUDE'}, {'pathNum': 'BACK', 'pathId': '04165eb6-48f0-4e7f-aa08-3e0967fda9a5', 'sortNum': 0, 'pathType': 'NODE', 'constraintType': 'EXCLUDE'}]}, {'pathStatus': 0, 'srcNode': '5fc7e69a-709b-409d-b1e9-093c02394d5a', 'dstNode': '951b9eda-f804-4bfe-a4e1-a648dd7b4fe7', 'flowPaths': [{'collectId': 'f212838a-eb77-427a-839a-0340ffd13fba', 'defaultTunnelId': 'dc541fcd-a7bc-496c-9ab9-81db4281ef22', 'defaultCollectId': '8aa7e649-3445-432c-8e6a-22560acdd72a', 'calcPaths': [{'linkList': [{'linkId': '166eab8f-b8da-4b52-ad3f-104d1699ad17'}, {'linkId': '3490f918-c557-4d73-a283-91fe6779d417'}], 'pathNumber': 0, 'strictStatus': 1}, {'linkList': [{'linkId': '6308d6ad-eb76-41db-8e92-85672f533c32'}, {'linkId': '9d7bc3d2-b550-4e34-aca6-3891fbe5f254'}], 'pathNumber': 1, 'strictStatus': 1}], 'paths': [{'linkList': [{'linkId': '166eab8f-b8da-4b52-ad3f-104d1699ad17'}, {'linkId': '3490f918-c557-4d73-a283-91fe6779d417'}], 'pathNumber': 0, 'strictStatus': 1}, {'linkList': [{'linkId': '6308d6ad-eb76-41db-8e92-85672f533c32'}, {'linkId': '9d7bc3d2-b550-4e34-aca6-3891fbe5f254'}], 'pathNumber': 1, 'strictStatus': 1}], 'realPaths': [{'pathNumber': 0, 'strictStatus': 1, 'nodeTpPairs': [{'dstNodeName': 'VSR3', 'srcTpName': 'GigabitEthernet3/0', 'dstTpName': 'GigabitEthernet3/0', 'srcNodeName': 'VSR1'}, {'dstNodeName': 'VSR6', 'srcTpName': 'GigabitEthernet6/0', 'dstTpName': 'GigabitEthernet3/0', 'srcNodeName': 'VSR3'}]}, {'pathNumber': 1, 'strictStatus': 1, 'nodeTpPairs': [{'dstNodeName': 'VSR4', 'srcTpName': 'GigabitEthernet4/0', 'dstTpName': 'GigabitEthernet4/0', 'srcNodeName': 'VSR1'}, {'dstNodeName': 'VSR6', 'srcTpName': 'GigabitEthernet6/0', 'dstTpName': 'GigabitEthernet4/0', 'srcNodeName': 'VSR4'}]}], 'tunnelId': '8b5d91a2-bf3f-4261-82b9-d7ccf51ac793'}], 'status': 0, 'flowGroupInstanceId': '83dcd3b9-60af-427f-b4e1-50467f1d6be5', 'flowGroupId': '3bdb0333-b838-4384-8778-f16d0e5df67f'}], 'totalPage': 1, 'currentPageNo': 1}}


group_info_data = {'output': {'flowGroupsInfo': [{'enableStatus': False, 'flowIds': ['f69f4980-ab1a-4a1f-8c65-c139b1321bb4'], 'flowGroupStatus': 0, 'flowGroupName': '1-6', 'ecmp': 1, 'serviceClass': 3, 'bandwidth': 2000000000, 'vpUpdateTime': 0, 'enableQosExp': False, 'pathNum': 2, 'isAction': 1, 'pathMode': 0, 'configStatus': 'DISABLE', 'pathManage': 1, 'networkScopeId': '70a6c4ae-6f39-44d6-86bd-519826623870', 'tunnelMode': 0, 'backupBandwidthPercent': 100, 'schedulePolicyIds': [{'scheduleId': 'ead67f0b-8c64-4122-9af0-50d94e0bc3f0', 'slaPolicyIds': [{'policyId': 'ad2c53ef-f369-4a9d-a569-5a5d1efe5734'}]}], 'scheduleMode': 0, 'flowGroupId': '3bdb0333-b838-4384-8778-f16d0e5df67f', 'comment': ''}, {'enableStatus': False, 'flowIds': ['f69f4980-ab1a-4a1f-8c65-c139b1321bb4'], 'flowGroupStatus': 0, 'flowGroupName': '1-5', 'ecmp': 1, 'serviceClass': 1, 'bandwidth': 2000000000, 'vpUpdateTime': 0, 'enableQosExp': False, 'pathNum': 2, 'isAction': 1, 'pathMode': 0, 'configStatus': 'DISABLE', 'pathManage': 1, 'networkScopeId': '274f1780-3949-4657-8c5e-455991cf4f6b', 'tunnelMode': 0, 'backupBandwidthPercent': 100, 'schedulePolicyIds': [{'scheduleId': 'ead67f0b-8c64-4122-9af0-50d94e0bc3f0', 'slaPolicyIds': [{'policyId': 'ad2c53ef-f369-4a9d-a569-5a5d1efe5734'}]}], 'scheduleMode': 0, 'flowGroupId': '2461d0df-e668-4fe9-bb0a-a88e84280659', 'comment': 'vsr1-vsr5'}, {'enableStatus': False, 'flowIds': ['f69f4980-ab1a-4a1f-8c65-c139b1321bb4'], 'flowGroupStatus': 0, 'flowGroupName': 'test', 'ecmp': 1, 'serviceClass': 2, 'bandwidth': 2000000000, 'vpUpdateTime': 0, 'enableQosExp': False, 'pathNum': 2, 'isAction': 1, 'pathMode': 0, 'configStatus': 'DISABLE', 'pathManage': 1, 'networkScopeId': 'e35e75f1-999d-4c1b-9b32-e21b9bd845a9', 'tunnelMode': 0, 'backupBandwidthPercent': 100, 'schedulePolicyIds': [{'scheduleId': 'ead67f0b-8c64-4122-9af0-50d94e0bc3f0', 'slaPolicyIds': [{'policyId': 'ad2c53ef-f369-4a9d-a569-5a5d1efe5734'}]}], 'scheduleMode': 0, 'flowGroupId': '4ac279d4-5bdf-41bd-b689-0420869c020c', 'comment': ''}]}}


group_info_data_old = {
    "output": {
        "flowGroupsInfo": [
        {
            "flowGroupStatus": 0,
            "pathMode": 0,
            "enableQosExp": False,
            "networkScopeId": "e0f64987-9be3-4e71-bab6-f062ce3f868f",
            "ecmp": 1,
            "configStatus": "DISABLE",
            "pathManage": 1,
            "schedulePolicyIds": [
            {
                "scheduleId": "c9060c64-63d9-4efa-a934-a544aef4eb08",
                "slaPolicyIds": [
                {
                    "policyId": "6bbd7e7c-06e2-45f6-97e7-43b65592090c"
                }
                ]
            }
            ],
            "backupBandwidthPercent": 100,
            "tunnelMode": 0,
            "serviceClass": 1,
            "enableStatus": False,
            "isAction": 1,
            "bandwidth": 2000000000,
            "pathNum": 2,
            "flowGroupId": "a83e9500-d589-4bb5-aecf-fc3481474f71",
            "scheduleMode": 0,
            "flowGroupName": "tunnel1",
            "vpUpdateTime": 0,
            "flowIds": [
                "1e091482-8246-4e37-b782-2a7f608b01ac"
            ]
        }
        ]
    }
}


ins_with_tun_data = {'output': {'total': 3, 'flowGroupInstanceInfoView': [{'mainSlaStatus': '1', 'pathStatus': 0, 'pathNum': 2, 'desNodeName': 'VSR4', 'dstNode': '04165eb6-48f0-4e7f-aa08-3e0967fda9a5', 'flowGroupName': 'test', 'status': 0, 'srcNodeName': 'VSR1', 'bandwidth': -1, 'pathMode': 0, 'flowPaths': [{'collectId': '684c565c-4e00-4c94-b754-f9f663e8d588', 'defaultTunnelId': '196ee30b-57e0-4ce5-9406-0e0ea107727a', 'defaultCollectId': '0b9a98fb-8885-4baa-a2e2-d23df81b7543', 'paths': [{'linkList': [{'linkId': '6308d6ad-eb76-41db-8e92-85672f533c32'}], 'pathNumber': 0, 'strictStatus': 1}, {'linkList': [{'linkId': '166eab8f-b8da-4b52-ad3f-104d1699ad17'}, {'linkId': '3b71a3a2-7bdf-4e31-92dd-948bd08c2b20'}], 'pathNumber': 1, 'strictStatus': 1}], 'realPaths': [{'pathNumber': 0, 'strictStatus': 1, 'nodeTpPairs': [{'dstNodeName': 'VSR4', 'srcTpName': 'GigabitEthernet4/0', 'dstTpName': 'GigabitEthernet4/0', 'srcNodeName': 'VSR1'}]}, {'pathNumber': 1, 'strictStatus': 1, 'nodeTpPairs': [{'dstNodeName': 'VSR3', 'srcTpName': 'GigabitEthernet3/0', 'dstTpName': 'GigabitEthernet3/0', 'srcNodeName': 'VSR1'}, {'dstNodeName': 'VSR4', 'srcTpName': 'GigabitEthernet4/0', 'dstTpName': 'GigabitEthernet3/0', 'srcNodeName': 'VSR3'}]}], 'tunnelId': 'e1cfff1e-0472-4b4d-9439-9b99dfef0ef5'}], 'process': 100, 'srcNode': '5fc7e69a-709b-409d-b1e9-093c02394d5a', 'tunnelMode': 0, 'tunnelInfo': [{'tunnelName': 'Tunnel4', 'defaultTunnelId': '196ee30b-57e0-4ce5-9406-0e0ea107727a', 'tunnelId': 'e1cfff1e-0472-4b4d-9439-9b99dfef0ef5', 'defaultTunnelName': 'Tunnel3'}], 'flowGroupInstanceId': '673fb267-41e0-4ea6-83fc-b93a24d48045', 'srcNodeIp': '10.99.211.211', 'scheduleMode': 0, 'flowGroupId': '4ac279d4-5bdf-41bd-b689-0420869c020c', 'desNodeIp': '10.99.211.214'}, {'mainSlaStatus': '1', 'pathStatus': 1, 'pathNum': 2, 'desNodeName': 'VSR5', 'dstNode': 'bb0e3e1d-7541-4a59-80e6-b55d9ae3d4ac', 'flowGroupName': '1-5', 'status': 0, 'srcNodeName': 'VSR1', 'bandwidth': -1, 'pathMode': 0, 'flowPaths': [{'collectId': '6e492b97-90db-41ec-9730-f99d2089de96', 'defaultTunnelId': '1f2ceff8-e0a0-4630-af2c-71ef62a7506e', 'defaultCollectId': 'e4bc4754-741e-4f09-b4f1-057781b780d1', 'paths': [{'linkList': [{'linkId': '166eab8f-b8da-4b52-ad3f-104d1699ad17'}, {'linkId': 'e02d9152-a8c1-4b2a-a759-bd1401c31dba'}], 'pathNumber': 0, 'strictStatus': 1}], 'realPaths': [{'pathNumber': 0, 'strictStatus': 1, 'nodeTpPairs': [{'dstNodeName': 'VSR3', 'srcTpName': 'GigabitEthernet3/0', 'dstTpName': 'GigabitEthernet3/0', 'srcNodeName': 'VSR1'}, {'dstNodeName': 'VSR5', 'srcTpName': 'GigabitEthernet5/0', 'dstTpName': 'GigabitEthernet3/0', 'srcNodeName': 'VSR3'}]}], 'tunnelId': '26695822-5b20-4d67-9803-2a778ee4abec'}], 'process': 85, 'srcNode': '5fc7e69a-709b-409d-b1e9-093c02394d5a', 'flowGroupId': '2461d0df-e668-4fe9-bb0a-a88e84280659', 'tunnelMode': 0, 'tunnelInfo': [{'tunnelName': 'Tunnel2', 'defaultTunnelId': '1f2ceff8-e0a0-4630-af2c-71ef62a7506e', 'tunnelId': '26695822-5b20-4d67-9803-2a778ee4abec', 'defaultTunnelName': 'Tunnel1'}], 'flowGroupInstanceId': '37a1af52-29bc-45f5-b96e-0fc82906d31d', 'srcNodeIp': '10.99.211.211', 'scheduleMode': 0, 'instancePaths': [{'pathNum': 'BACK', 'pathId': 'a92e557a-542e-445f-a38e-9d3cd438110b', 'sortNum': 0, 'pathType': 'NODE', 'constraintType': 'EXCLUDE'}, {'pathNum': 'BACK', 'pathId': '04165eb6-48f0-4e7f-aa08-3e0967fda9a5', 'sortNum': 0, 'pathType': 'NODE', 'constraintType': 'EXCLUDE'}], 'desNodeIp': '10.99.211.215'}, {'mainSlaStatus': '1', 'pathStatus': 0, 'pathNum': 2, 'desNodeName': 'VSR6', 'dstNode': '951b9eda-f804-4bfe-a4e1-a648dd7b4fe7', 'flowGroupName': '1-6', 'status': 0, 'srcNodeName': 'VSR1', 'bandwidth': -1, 'pathMode': 0, 'flowPaths': [{'collectId': 'f212838a-eb77-427a-839a-0340ffd13fba', 'defaultTunnelId': 'dc541fcd-a7bc-496c-9ab9-81db4281ef22', 'defaultCollectId': '8aa7e649-3445-432c-8e6a-22560acdd72a', 'calcPaths': [{'linkList': [{'linkId': '166eab8f-b8da-4b52-ad3f-104d1699ad17'}, {'linkId': '3490f918-c557-4d73-a283-91fe6779d417'}], 'pathNumber': 0, 'strictStatus': 1}, {'linkList': [{'linkId': '6308d6ad-eb76-41db-8e92-85672f533c32'}, {'linkId': '9d7bc3d2-b550-4e34-aca6-3891fbe5f254'}], 'pathNumber': 1, 'strictStatus': 1}], 'paths': [{'linkList': [{'linkId': '166eab8f-b8da-4b52-ad3f-104d1699ad17'}, {'linkId': '3490f918-c557-4d73-a283-91fe6779d417'}], 'pathNumber': 0, 'strictStatus': 1}, {'linkList': [{'linkId': '6308d6ad-eb76-41db-8e92-85672f533c32'}, {'linkId': '9d7bc3d2-b550-4e34-aca6-3891fbe5f254'}], 'pathNumber': 1, 'strictStatus': 1}], 'realPaths': [{'pathNumber': 0, 'strictStatus': 1, 'nodeTpPairs': [{'dstNodeName': 'VSR3', 'srcTpName': 'GigabitEthernet3/0', 'dstTpName': 'GigabitEthernet3/0', 'srcNodeName': 'VSR1'}, {'dstNodeName': 'VSR6', 'srcTpName': 'GigabitEthernet6/0', 'dstTpName': 'GigabitEthernet3/0', 'srcNodeName': 'VSR3'}]}, {'pathNumber': 1, 'strictStatus': 1, 'nodeTpPairs': [{'dstNodeName': 'VSR4', 'srcTpName': 'GigabitEthernet4/0', 'dstTpName': 'GigabitEthernet4/0', 'srcNodeName': 'VSR1'}, {'dstNodeName': 'VSR6', 'srcTpName': 'GigabitEthernet6/0', 'dstTpName': 'GigabitEthernet4/0', 'srcNodeName': 'VSR4'}]}], 'tunnelId': '8b5d91a2-bf3f-4261-82b9-d7ccf51ac793'}], 'process': 100, 'srcNode': '5fc7e69a-709b-409d-b1e9-093c02394d5a', 'tunnelMode': 0, 'tunnelInfo': [{'tunnelName': 'Tunnel6', 'defaultTunnelId': 'dc541fcd-a7bc-496c-9ab9-81db4281ef22', 'tunnelId': '8b5d91a2-bf3f-4261-82b9-d7ccf51ac793', 'defaultTunnelName': 'Tunnel5'}], 'flowGroupInstanceId': '83dcd3b9-60af-427f-b4e1-50467f1d6be5', 'srcNodeIp': '10.99.211.211', 'scheduleMode': 0, 'flowGroupId': '3bdb0333-b838-4384-8778-f16d0e5df67f', 'desNodeIp': '10.99.211.216'}], 'totalPage': 1, 'currentPageNo': 1}}

ins_with_tun_data_old = {
    "output": {
        "flowGroupInstanceInfoView": [
        {
            "pathMode": 0,
            "flowGroupInstanceId": "ac7de5c6-6e90-4bf6-8f82-424b7da3411f",
            "tunnelInfo": [
            {
                "tunnelName": "Tunnel2",
                "defaultTunnelName": "Tunnel1",
                "tunnelId": "c8fbc891-92c8-4fcb-868b-062a1c129f4f",
                "defaultTunnelId": "23251b09-8001-4eb9-9c6c-fb6f65f1e8a2"
            }
            ],
            "status": 0,
            "desNodeIp": "172.100.1.54",
            "flowPaths": [
            {
                "tunnelId": "c8fbc891-92c8-4fcb-868b-062a1c129f4f",
                "paths": [
                {
                    "linkList": [
                    {
                        "linkId": "2594f424-89a5-4673-bb25-52a20d0b3dd6"
                    },
                    {
                    "linkId": "5a43e5c6-f99a-4217-b3cf-a76cb54c198e"
                    }
                    ],
                    "strictStatus": 1,
                    "pathNumber": 0
                },
                {
                    "linkList": [
                    {
                        "linkId": "4b62f1d4-9cef-4db2-8085-b4760042afe7"
                    },
                    {
                        "linkId": "6ba6a58c-54b5-40a6-9a20-812e5ad254b8"
                    },
                    {
                        "linkId": "bc16d72f-c284-4e48-96fb-5e9eb4894efe"
                    },
                    {
                        "linkId": "b972ff48-5fbe-4514-8378-3388969ec032"
                    }
                    ],
                    "strictStatus": 1,
                    "pathNumber": 1
                }
                ],
                "defaultTunnelId": "23251b09-8001-4eb9-9c6c-fb6f65f1e8a2",
                "collectId": "6ea66cdb-77d6-41e4-a294-3c43d6c3a10b",
                "defaultCollectId": "6670bc0e-d65c-4919-ad86-4c7c8fe1b63d",
                "realPaths": [
                {
                    "strictStatus": 1,
                    "nodeTpPairs": [
                    {
                        "dstTpName": "GigabitEthernet3/2/2",
                        "srcTpName": "GigabitEthernet3/2/2",
                        "dstNodeName": "P1",
                        "srcNodeName": "PE1"
                    },
                    {
                        "dstTpName": "GigabitEthernet3/1/2",
                        "srcTpName": "GigabitEthernet3/2/3",
                        "dstNodeName": "PE3",
                        "srcNodeName": "P1"
                    }
                    ],
                    "pathNumber": 0
                },
                {
                    "strictStatus": 1,
                    "nodeTpPairs": [
                    {
                        "dstTpName": "GigabitEthernet3/2/1",
                        "srcTpName": "GigabitEthernet3/2/1",
                        "dstNodeName": "PE2",
                        "srcNodeName": "PE1"
                    },
                    {
                        "dstTpName": "GigabitEthernet3/2/4",
                        "srcTpName": "GigabitEthernet3/2/3",
                        "dstNodeName": "P1",
                        "srcNodeName": "PE2"
                    },
                    {
                        "dstTpName": "GigabitEthernet3/2/1",
                        "srcTpName": "GigabitEthernet3/2/1",
                        "dstNodeName": "P2",
                        "srcNodeName": "P1"
                    },
                    {
                        "dstTpName": "GigabitEthernet3/1/3",
                        "srcTpName": "GigabitEthernet3/2/5",
                        "dstNodeName": "PE3",
                        "srcNodeName": "P2"
                    }
                    ],
                    "pathNumber": 1
                }
                ]
            }
            ],
            "srcNode": "3716b792-59ad-4035-87b5-6a10289fab7b",
            "mainSlaStatus": "1",
            "srcNodeName": "PE1",
            "tunnelMode": 0,
            "dstNode": "d3501601-faed-4d5d-b57b-e528dc1e266e",
            "pathStatus": 0,
            "desNodeName": "PE3",
            "bandwidth": -1,
            "srcNodeIp": "172.100.1.50",
            "pathNum": 2,
            "flowGroupId": "a83e9500-d589-4bb5-aecf-fc3481474f71",
            "scheduleMode": 0,
            "flowGroupName": "tunnel1",
            "process": 100
        }
        ],
        "currentPageNo": 1,
        "totalPage": 1,
        "total": 1
    }
}

sla_level_data = {'output': {'slaLevelInfo': [{'expRange': [2], 'maxPacketLossRate': 15, 'maxDelay': 300, 'maxJitter': 5, 'slaLevelId': '401c1d52-5d86-47e7-9b30-0fd978d00ad3', 'slaLevelName': 'Immediate', 'dscpRange': [16, 18, 20, 22], 'priority': 2}, {'expRange': [5], 'maxPacketLossRate': 5, 'maxDelay': 50, 'maxJitter': 3, 'slaLevelId': '5dbcaf1b-f2a7-4839-825f-4f0bb0708eb9', 'slaLevelName': 'Critic', 'dscpRange': [40, 46], 'priority': 5}, {'expRange': [3], 'maxPacketLossRate': 10, 'maxDelay': 150, 'maxJitter': 5, 'slaLevelId': '0fbd74e3-6cb1-4436-bba3-50902c2af933', 'slaLevelName': 'Flash', 'dscpRange': [24, 26, 28, 30], 'priority': 3}, {'expRange': [4], 'maxPacketLossRate': 5, 'maxDelay': 100, 'maxJitter': 5, 'slaLevelId': '99eafd95-370c-4674-8258-8a52db406670', 'slaLevelName': 'FlashOverride', 'dscpRange': [32, 34, 36, 38], 'priority': 4}, {'expRange': [1], 'maxPacketLossRate': 25, 'maxDelay': 500, 'maxJitter': 10, 'slaLevelId': '6e347f24-7c34-44d4-b2e1-e2f526f5bc47', 'slaLevelName': 'Priority', 'dscpRange': [8, 10, 12, 14], 'priority': 1}]}}

sla_level_data_old = {
    "output": {
        "slaLevelInfo": [
            {
                "maxPacketLossRate": 15,
                "maxJitter": 5,
                "maxDelay": 300,
                "slaLevelName": "Immediate",
                "expRange": [
                    2
                ],
                "slaLevelId": "a797320b-df28-4a62-9679-899e4b24dcaf",
                "priority": 2,
                "dscpRange": [
                    16,
                    18,
                    20,
                    22
                ]
            },
            {
                "maxPacketLossRate": 10,
                "maxJitter": 5,
                "maxDelay": 150,
                "slaLevelName": "Flash",
                "expRange": [
                    3
                ],
                "slaLevelId": "b083f1e6-48fd-4122-b27a-24f7478695d0",
                "priority": 3,
                "dscpRange": [
                    24,
                    26,
                    28,
                    30
                ]
            },
            {
                "maxPacketLossRate": 5,
                "maxJitter": 5,
                "maxDelay": 100,
                "slaLevelName": "FlashOverride",
                "expRange": [
                    4
                ],
                "slaLevelId": "588a6da9-7fae-477a-8534-d075a26100f5",
                "priority": 4,
                "dscpRange": [
                    32,
                    34,
                    36,
                    38
                ]
            },
            {
                "maxPacketLossRate": 5,
                "maxJitter": 3,
                "maxDelay": 50,
                "slaLevelName": "Critic",
                "expRange": [
                    5
                ],
                "slaLevelId": "844608f1-77bc-4c64-9636-abce51765a64",
                "priority": 5,
                "dscpRange": [
                    40,
                    46
                ]
            },
            {
                "maxPacketLossRate": 25,
                "maxJitter": 10,
                "maxDelay": 500,
                "slaLevelName": "Priority",
                "expRange": [
                    1
                ],
                "slaLevelId": "201051ad-5cb9-4ba0-b809-811e815df30b",
                "priority": 1,
                "dscpRange": [
                    8,
                    10,
                    12,
                    14
                ]
            }
        ]
    }
}
