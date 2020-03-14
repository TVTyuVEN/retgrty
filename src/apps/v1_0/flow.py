# -*- encoding: utf-8 -*-
"""
@File    : flow.py
@Time    : 2019/05/29 13:56:58
@Author  : leijuyan 11389
@License : Copyright (c) 2004-2019 New H3C Tech. Co., Ltd. All rights reserved.
@Desc    : 流量管理
"""
import threading
import os
import xlrd
import time
import copy
from flask import request

from apps.errcode import ErrCode
from apps.datacode import FlowLoadDetailCode

from apps.util import FLOW_IMPORT_LOCK
from apps.util import g_allFlows,g_tunrec, g_sim, g_dt
from apps.util import info_logger, error_logger
from apps.util import get_current_time
from apps.util import generate_uuid, parse_flow_to_kbps

from apps.v1_0.language import get_language_setting_index

FLOW_SAVE_PATH = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir,'data','flow')
FLOW_SAVE_NAME = "flow.xlsx"
#FLOW_TEMPLATE_PATH = "template"

# 把流量文件里的第一行的索引对应成key，以防次序被弄乱仍能正确解析
flowFileToFlowJson = {'flow_name':'flow_name',
                    'source_node_name':'source_node_name', 		
                    'destination_node_name':'des_node_name', 
                    'source_ip': 'sourceIp',						
                    'destination_ip':'desIp',
                    'source_node_ip': 'sourceIp',  #为了避免有人拿着老模板，source_ip也报留了.						
                    'destination_node_ip':'desIp',				
                    'start_time':'start_time',  					
                    'end_time':'end_time',   					
                    'band_width(Mbps)':'band_width', 	
                    'band_width(bit/s)':'band_width',  #为了避免有人拿着老模板，band_width(bit/s)也报留了.		
                    'flow_type':'flow_type',								
                    'tunnel_name':'tunnel_name'                   
                    }

class FlowObj(object):
    """Class for Flow.
    
    Attributes:
        none
    """
    
    def __init__(self, id=None):
        if id == None:
            self.id = generate_uuid()
        else:
            self.id = id

        self.flow_name = 'N/A'      # sdn 有，大数据没有
        self.src_name = ''
        self.des_name = ''
        self.src_ip = 'N/A'    # sdn 有， 大数据有
        self.des_ip = 'N/A'   # sdn 有， 大数据有
        self.src_id = ''  # 对应二层topo的节点ID，自己对应
        self.des_id = ''  # 对应二层topo的节点ID，自己对应
        self.start_time = ''
        self.end_time = ''
        self.flow_type =''
        self.tun_name = ''  # 有无tunnel name
        self.orgin = ''  # 'model',表示用户从流量模板导入的流;'tunnel_build',表示基于隧道自动创建的流量
        #self.jump = 0
        self.b4_jump = {}   # 各个时刻的跳数信息, tunnel流{"t1":5, "t2":2},普通流{"all":5}
        self.af_jump = {}
        self.org_path = {}
        self.b4_path = {}   # 各个时刻的路径具体信息：tunnel流{t1:[], t2:[], t3:[]}, 普通流{"all":[]}
        self.af_path = {}
        self.b4_delay = {}  # 各个时刻的延时信息
        self.af_delay = {}
        #self.throughput = 0    # sdn 没有，大数据有,默认修改为-1，用于删除有误的隧道信息
        self.bandwidth = {}   # 各个时刻的流量大小 tunnel流{"t1":500, "t2":800},普通流{"all":200}

        
class FlowImportInfo():
    """流量导入
    
    Attributes:
        flow_import_status: 流量导入状态
    """

    def __init__(self):
        self.flow_importing = False
        self.flow_file_name = ''
        self.flow_import_status = "文件读取完成"
        self.flow_import_progress = 0
        self.flow_import_infoNum = 0
        self.flow_import_detail_english = []
        self.flow_import_detail_chinese = []
     
    def init_import_flow_status(self, file_name):
        self.flow_file_name = file_name
        self.flow_import_status = "文件读取完成"
        self.flow_import_progress = 0
        self.flow_import_infoNum = 0
        self.flow_import_detail_english = []
        self.flow_import_detail_chinese = []
    def to_json(self, file_name):
        if self is None:
            ret = ErrCode.FLOW_FILE_IS_NOT_EXIST
        elif self.flow_file_name == file_name:
            lang = get_language_setting_index()
            if lang == 1:
                data = {
                        "progress": self.flow_import_progress,
                        "infonum":self.flow_import_infoNum,
                        "flowInfo": self.flow_import_detail_chinese,
                }
            else:
                data = {
                        "progress": self.flow_import_progress,
                        "infonum":self.flow_import_infoNum,
                        "flowInfo": self.flow_import_detail_english,
                }
            ret = ErrCode.SUCCESS
        else:
            data = {''}
            ret = ErrCode.FLOW_IS_NOT_ANALYZING
        return ret, data
    

fii = FlowImportInfo()

def get_flow_xlxs_time(value,value_type):
    try:
        if value_type == 1:
            #ctype : 0 empty, 1 string, 2 number, 3 date, 4 boolean, 5 error                 
            timeArray = time.strptime(value, "%Y/%m/%d %H:%M:%S")
            result = int(1000 * time.mktime(timeArray))
        else:
            table_value = '%s' % value
            add_time = xlrd.xldate_as_datetime(float(table_value),0) 
            result = int(1000 * time.mktime(add_time.timetuple()))
        return result
    except Exception as e:
        result = ''
        info_logger.error(e)
        return result

def is_number(value):
    try:
        float(value)
        return True
    except Exception as e:
        info_logger.error(e)
        return False   

"""
@funName    : read_flow_file
@function   : 导入流量
@Author     : leijuyan 11389
@注意事项    : 无.
"""    
def read_flow_file(file_dir):
    #读取excel表的数据
    try:
        workbook = xlrd.open_workbook(file_dir)
        #选取需要读取数据的那一页
        sheet = workbook.sheet_by_index(0)

        #获得行数和列数
        rows =sheet.nrows
        cols =sheet.ncols

        tun_flow_failed = 0 # 记录有多少条tunnel流，因为导入的flow填写的目的地址和实际的tunnel的目的地址不一样，而把目的地址改成tunnel的目的地址
        
        flows_num = 0
        if rows == 1:    
            return ErrCode.FAILED, flows_num,flows_num, tun_flow_failed
        
        if g_dt.phy_topo == None:
            return ErrCode.FAILED, flows_num,flows_num, tun_flow_failed
        
        index_list = []
        flow_unit = 'Mbps'

        for k in range(0,cols):
            cols_value = sheet.cell(0,k).value.strip()  
            if cols_value in  flowFileToFlowJson.keys():
                index_value = '%s' % flowFileToFlowJson[cols_value]
                if cols_value == 'band_width(bit/s)':
                    flow_unit = 'bps'
            else:
                index_value = ''
            index_list.append(index_value)

        if ('start_time' not in index_list or
            'end_time' not in index_list or
            'source_node_name' not in index_list or
            'des_node_name' not in index_list or
            'band_width' not in index_list or
            'desIp' not in index_list or
            'sourceIp' not in index_list):
            return ErrCode.FAILED, flows_num,flows_num, tun_flow_failed

        for i in range(1,rows):
            d={}
            for j in range(0,cols):
                q = index_list[j]  
                if q == '':
                    continue
                if isinstance(sheet.cell(i,j).value,str):
                    if q == 'start_time' or q == 'end_time':
                        if sheet.cell(i,j).value != '':
                            d[q] = get_flow_xlxs_time(sheet.cell(i,j).value, value_type = 1) 
                        else:
                            d[q] = ''
                    else:
                        d[q] = '%s' % sheet.cell(i,j).value.strip()
                else:
                    if q == 'start_time' or q == 'end_time':
                        if sheet.cell(i,j).value != '':
                            d[q] = get_flow_xlxs_time(sheet.cell(i,j).value, value_type = 2)
                        else:
                            d[q] = ''
                    else:
                        d[q] = '%s' % sheet.cell(i,j).value
    
            if (d['start_time'] == '' or d['end_time'] == '' 
                or d['source_node_name'] == '' or d['des_node_name'] == '' 
                or d['band_width'] == 0 or d['band_width']==''
                or d['desIp']== '' or d['sourceIp'] == ''
                or d['flow_name'] == ''
                or d['sourceIp'] == d['desIp']):  # 源和目的相同的流量，默认其为错误流量，不添加
                continue
            
            # 流量大小不是数字，这条流量不要
            if is_number(d['band_width']) == False:
                continue

            a_flow = FlowObj()
            a_flow.flow_name = d['flow_name']
            a_flow.src_name = d['source_node_name']
            a_flow.des_name = d['des_node_name']
            a_flow.src_ip = d['sourceIp']
            a_flow.des_ip = d['desIp']
            a_flow.start_time = d['start_time']
            a_flow.end_time = d['end_time']
            
            # flow文件是按照Mbps导入的，所以这里要做转化
            a_flow.bandwidth["all"] = parse_flow_to_kbps(flow_unit, float(d['band_width'])) 

            if d['flow_type'] == '':  #如果没有填写类型，就写成undefine类型
                a_flow.flow_type = 'undefine'
            else:
                a_flow.flow_type = d['flow_type']

            des_mate = 0
            source_mate = 0

            # 如果客户用的是老的模板，没有tunnel_name的选项,则把tunnel_name这一项填成空的
            if 'tunnel_name' not in d.keys():
                d['tunnel_name'] = ''
            
            a_flow.tun_name = d['tunnel_name']

            #'model',表示用户从流量模板导入的流
            a_flow.orgin = 'model'

            for key in g_dt.phy_topo.nodes.keys():
                if source_mate == 0:
                    if g_dt.phy_topo.nodes[key].name == a_flow.src_name and g_dt.phy_topo.nodes[key].mgrip == a_flow.src_ip:
                        a_flow.src_id = g_dt.phy_topo.nodes[key].id
                        source_mate = 1

                if des_mate == 0:
                    if g_dt.phy_topo.nodes[key].name == a_flow.des_name and g_dt.phy_topo.nodes[key].mgrip == a_flow.des_ip:
                        a_flow.des_id = g_dt.phy_topo.nodes[key].id
                        des_mate = 1

                if source_mate == 1 and des_mate == 1:
                    if a_flow.tun_name != '':
                        tunid = a_flow.src_id + a_flow.tun_name
                        if tunid in g_tunrec.org_tuns.keys():
                            if g_tunrec.org_tuns[tunid].src_id == a_flow.src_id and g_tunrec.org_tuns[tunid].des_id == a_flow.des_id:
                                flows_num += 1
                                flowid = a_flow.id
                                a_flow.flow_name += ("_" + g_tunrec.org_tuns[tunid].name)
                                a_flow.flow_type = "tunnel_flow"
                                g_allFlows[flowid] = copy.deepcopy(a_flow)
                            else:
                                tun_flow_failed += 1
                        else:
                            tun_flow_failed += 1
                    else:
                        flows_num += 1
                        flowid = a_flow.id
                        g_allFlows[flowid] = copy.deepcopy(a_flow)

                    break              
        parser_failed = (rows - 1) - flows_num
        return ErrCode.SUCCESS, flows_num, parser_failed, tun_flow_failed                
    except Exception as e:
        print("read_flow_file 2 Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.FAILED,0,0, 0    

"""
@funName    : import_flow_data
@function   : 导入流量
@Author     : leijuyan 11389
@注意事项    : 无.
"""    
def import_flow_data(file_dir, file_name):
    """同步topo数据。"""
    try:
        fii.init_import_flow_status(file_name)

        fii.flow_import_progress = 5 
        fii.flow_import_status = 'success'  
        step =  FlowLoadDetailCode.TOPO_FINISH_SEARCH_FLOW

        curtime = get_current_time()
        detail = {"time":curtime, "status":"sucess","info":FlowLoadDetailCode.FLOW_LOAD_MSG[step][0]}
        detailchinese = {"time":curtime, "status":"sucess","info":FlowLoadDetailCode.FLOW_LOAD_MSG[step][1] }
        fii.flow_import_infoNum += 1
        fii.flow_import_detail_english.append(detail)  
        fii.flow_import_detail_chinese.append(detailchinese)  
    

        fii.flow_import_progress = 20
        step = FlowLoadDetailCode.FIND_THE_FLOW_FILE

        curtime = get_current_time()
        detail = {"time":curtime, "status":"sucess","info":FlowLoadDetailCode.FLOW_LOAD_MSG[step][0]}
        detailchinese = {"time":curtime, "status":"sucess","info":FlowLoadDetailCode.FLOW_LOAD_MSG[step][1]}
        fii.flow_import_infoNum += 1
        fii.flow_import_detail_english.append(detail)   
        fii.flow_import_detail_chinese.append(detailchinese) 

        parser_success_num = 0
        parser_fail_num = 0
        tun_flow_failed = 0
        resp, parser_success_num, parser_fail_num,tun_flow_failed = read_flow_file(file_dir)
        if resp == ErrCode.FAILED:
            step = FlowLoadDetailCode.FILE_PARSNG_FAILED
            curtime = get_current_time()    
            detail = {"time":curtime, "status":"sucess","info":FlowLoadDetailCode.FLOW_LOAD_MSG[step][0]}
            detailchinese = {"time":curtime, "status":"sucess","info":FlowLoadDetailCode.FLOW_LOAD_MSG[step][1] }
            fii.flow_import_infoNum += 1
            fii.flow_import_detail_english.append(detail)   
            fii.flow_import_detail_chinese.append(detailchinese)

            fii.flow_import_progress = 100
            
            fii.flow_import_status = "fail"
            FLOW_IMPORT_LOCK.acquire()
            fii.flow_importing = False
            FLOW_IMPORT_LOCK.release()
            return ErrCode.FAILED

        if parser_fail_num == 0:
            step = FlowLoadDetailCode.FILE_PARSNG_FINISH_SUCCESS

            curtime = get_current_time()
            # '完成文件解析，解析成功 %d 条流量 (parser_success_num)
            detail = {"time":curtime, "status":"sucess","info":FlowLoadDetailCode.FLOW_LOAD_MSG[step][0] %(parser_success_num)} 
            detailchinese = {"time":curtime, "status":"sucess","info":FlowLoadDetailCode.FLOW_LOAD_MSG[step][1] %(parser_success_num)}
            fii.flow_import_infoNum += 1
            fii.flow_import_detail_english.append(detail)
            fii.flow_import_detail_chinese.append(detailchinese) 
            fii.flow_import_progress = 100
            
        
        else: 
            step = FlowLoadDetailCode.FILE_PARSNG_FINISH_HAS_FAILED_DETAIL

            curtime = get_current_time()
            # '完成文件解析，解析成功 %d 条流量, 解析失败 %d 条流量-流量未能匹配topo节点' % (parser_success_num, parser_fail_num)
            detail = {"time":curtime, "status":"sucess","info":FlowLoadDetailCode.FLOW_LOAD_MSG[step][0] %(parser_success_num, parser_fail_num)}
            detailchinese = {"time":curtime, "status":"sucess","info":FlowLoadDetailCode.FLOW_LOAD_MSG[step][1] %(parser_success_num, parser_fail_num)}
            fii.flow_import_infoNum += 1
            fii.flow_import_detail_english.append(detail)
            fii.flow_import_detail_chinese.append(detailchinese) 
            fii.flow_import_progress = 100
            

        FLOW_IMPORT_LOCK.acquire()
        fii.flow_importing = False
        FLOW_IMPORT_LOCK.release()

        return ErrCode.SUCCESS
    except Exception as e:
        print("import_flow_data 2 Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.FAILED

"""
@funName    : get_flow_import_progress
@function   : 获得导入流量文件的解析进度
@Author     : leijuyan 11389
@注意事项    : 无.
"""       
def get_flow_import_progress(flow_file_name):
    ret, msg = fii.to_json(FLOW_SAVE_NAME)
    return ret, msg        

"""
@funName    : import_flow_file
@function   : 把流量文件进行下载，保存到src/saveFlowPath路径下
@Author     : leijuyan 11389
@注意事项    : 无.
"""        
def import_flow_file():
    body_content = request.headers.get('Content-Type', 'None')            
    if 'multipart/form-data' in body_content :                               
        excel_file = request.files.get('cover', None)
        
        if excel_file is None:
            return ErrCode.FLOW_FILE_IS_NOT_EXIST
        if os.path.splitext(excel_file.filename)[1] != '.xlsx':
            return ErrCode.SAVE_FILENAME_ERROR

        FLOW_IMPORT_LOCK.acquire()
        if fii.flow_importing == False:
            fii.flow_importing = True
        else:
            FLOW_IMPORT_LOCK.release()
            return ErrCode.FLOW_IMPORTING
        FLOW_IMPORT_LOCK.release()

        file_dir = os.path.join(FLOW_SAVE_PATH, FLOW_SAVE_NAME)
        try:
            excel_file.save(file_dir)
        except Exception as e:
            print("import_flow_file Exception:", e)
            info_logger.error(e)
            error_logger.error(e)
            FLOW_IMPORT_LOCK.acquire()
            fii.flow_importing = False
            FLOW_IMPORT_LOCK.release()
            return ErrCode.FAILED

        # 创建线程
        # 注：不能把excel_file传到线程参数里，直接保存文件,因为退出这个文件后，excel_file已经被关闭了,无法成功写入，除非再重新打开。
        # 尝试过保存比较大的文件，也非常快,所以在这里直接处理
        flow_import_thd = threading.Thread(target=import_flow_data, args=(file_dir, FLOW_SAVE_NAME))
        flow_import_thd.start()             
    else:
        return ErrCode.FLOW_FILE_FORMAT_ERROR          
    return ErrCode.SUCCESS


def get_flow_Info_by_flowid(flow_id):
    """根据flowid获取导入流量的详细信息
    
    Args:
        flow_id:流ID
    Returns:
        none
    Raise:
        none
    """
    try:
        data ={}
        #print('g_allFlows ===',g_allFlows)
        if flow_id in g_allFlows.keys():
            flow_info = g_allFlows[flow_id]
            bandwidth = round(float((flow_info.bandwidth['all']) / 1000), 2)
            data = {
                        "flowName":flow_info.flow_name,
                        "sourceIp":flow_info.src_ip,
                        "destIp":flow_info.des_ip,
                        "startTime":flow_info.start_time,
                        "endTime":flow_info.end_time,
                        "bandwidth":('%.2f'%(bandwidth))
                    }
            #print('flow_info data ===',data)
            ret = ErrCode.SUCCESS
        else:
            ret = ErrCode.FLOW_IS_NOT_EXIST
        return ret, data

    except Exception as e:
        print("get_flow_Info_by_flowid Exception:", e)
        error_logger.error(e)
        ret = ErrCode.FAILED
        data ={}
        return ret, data

def get_all_loaded_flow():
    """获取所有的流量信息，以流量左树的方式发给前台
    
    Args:
        none
    Returns:
        none
    Raise:
        none
    """

    data = {}
    flow_name = ''
    flow_type = ''
    flow_source = ''
    flow_dest =''
    type_num = 0

    all_type_info = []

    if not bool(g_allFlows):
        #无流量的时候，直接返回为空,这样前台不会显示错误，以便界面更合理
        data ={}
        ret = ErrCode.SUCCESS
        return ret, data
    try:
        for _, value in g_allFlows.items():
            b_add = 0
            flow_name = value.flow_name
            flow_type = value.flow_type
            flow_source = value.src_name
            flow_dest = value.des_name
            flow_id = value.id       
            flow_desnode_id = value.des_id
            flow_sourcenode_id = value.src_id
            exit_flag = False

            for all_type_item in all_type_info:
                if all_type_item['flow_type'] == flow_type:                    
                    flow_detail = all_type_item['flowsDetail']
                    for flow_detail_item in  flow_detail:
                        if flow_detail_item['sourceFlow'] == flow_source:
                            flows = flow_detail_item['flows']
                            for flows_item in  flows:
                                if flows_item['desFlow'] == flow_dest:
                                    b_add = 1
                                    flows_item['flowNum'] += 1                                                
                                    new_dic_msg = {'flowId':flow_id, 'flowName':flow_name,'flowSourceNodeId':flow_sourcenode_id,'flowDesNodeId':flow_desnode_id}
                                    flows_item['flow_info'].append(new_dic_msg)
                                    exit_flag = True
                                    break # 退出for flows_item in  flows 循环
                            if b_add == 0: # source 相同，但是目的地址没有相同的，新加一条
                                b_add = 1
                                new_dic_msg ={'desFlow': flow_dest, 'flowNum':1, 'flow_info':[{'flowId':flow_id, 'flowName':flow_name,'flowSourceNodeId':flow_sourcenode_id,'flowDesNodeId':flow_desnode_id}]}
                                flow_detail_item['desFlowNum'] += 1
                                flows.append(new_dic_msg)
                                exit_flag = True

                            if exit_flag:# 退出flow_detail_item in  flow_detail
                                break
                    if b_add == 0: #flow type 相同，但是源不相同
                        b_add = 1
                        new_dic_msg ={'sourceFlow':flow_source, 'desFlowNum':1, 'flows':[{'desFlow': flow_dest, 'flowNum':1, 'flow_info':[{'flowId':flow_id, 'flowName':flow_name,'flowSourceNodeId':flow_sourcenode_id,'flowDesNodeId':flow_desnode_id}]}]}
                        all_type_item['thisTypeSurceNum'] += 1
                        flow_detail.append(new_dic_msg)    
                        exit_flag = True
                    if exit_flag:# 退出all_type_item in all_type_info:
                        break
            if  b_add == 0:
                new_dic_msg ={'flow_type':flow_type, 'thisTypeSurceNum':1, 'flowsDetail':[{'sourceFlow':flow_source, 'desFlowNum':1, 'flows':[{'desFlow': flow_dest, 'flowNum':1, 'flow_info':[{'flowId':flow_id, 'flowName':flow_name,'flowSourceNodeId':flow_sourcenode_id,'flowDesNodeId':flow_desnode_id}]}]}]}
                all_type_info.append(new_dic_msg)
                type_num += 1       
            
        data = {
                'typeNum':type_num,
                'allFlowInfo':all_type_info              
                }
        ret = ErrCode.SUCCESS
        return ret, data

    except Exception as e:
        print("get_all_loaded_flow Exception:", e)
        data = {
                'typeNum':0,
                'allFlowInfo':[]              
                }
        error_logger.error(e)
        return ErrCode.FAILED, data   

def del_flow(del_num, flow_info):
    try:
        del_result = []
        cal_flow_num = 0
        success_del_flow = 0
        if not g_allFlows:
            data = {}
            return ErrCode.NO_FLOWS,data

        if isinstance (flow_info, list):
            for flow_item in flow_info:
                cal_flow_num += 1
                flowId = flow_item['flowId']
                if flowId in g_allFlows.keys():
                    del g_allFlows[flowId]
                    success_del_flow += 1
                    msg = {flowId:'删除流量成功'}
                    del_result.append(msg)
                else:
                    msg = {flowId:'流量不存在，未进行删除'}
                    del_result.append(msg)
        if success_del_flow == 0:
            ret = ErrCode.ALL_FLOWS_YOU_WANT_DEL_NOT_EXIST
            data = {}
        else:
            data = {
                'delFlowNum':cal_flow_num,
                'delInfo':del_result
                }

            ret = ErrCode.SUCCESS
        return ret, data
    except Exception as e:
        print("del_flow Exception:", e)
        data = {
                'delFlowNum':0,
                'delInfo':[]            
                }
        error_logger.error(e)
        return ErrCode.FAILED, data 

def search_flow_Info_at_flow_list(search_type,search_info,content):
    try:
        if content == None:
            data = {}
            return ErrCode.SUCCESS,data

        all_type_info = []
        type_num = 0
        b_add = 0

        for value in content:
            b_found = False
            key_get_info = []
            if search_type == 'flowName':      
                key_get_info.append(value["flow_name"])
            elif search_type == 'sourceNode':
                key_get_info.append(value["source_node_name"])
            elif search_type == 'desNode':
                key_get_info.append(value["des_node_name"])
            else:
                key_get_info.append(value["flow_name"])
                key_get_info.append(value["source_node_name"])
                key_get_info.append(value["des_node_name"])
            
            for info in key_get_info:
                if search_info in info:
                    b_found = True
                    break

            if b_found:
                b_add = 0
                flow_name= value["flow_name"]
                flow_type = value["flow_type"]
                flow_source = value["source_node_name"]
                flow_dest = value["des_node_name"]
                flow_id = value["flowId"]
                flow_desnode_id = value["des_node_id"]
                flow_sourcenode_id = value["source_node_id"]

                for all_type_item in all_type_info:
                    if all_type_item['flow_type'] == flow_type:                    
                        flow_detail = all_type_item['flowsDetail']
                        for flow_detail_item in  flow_detail:
                            if flow_detail_item['sourceFlow'] == flow_source:
                                flows = flow_detail_item['flows']
                                for flows_item in  flows:
                                    if flows_item['desFlow'] == flow_dest:
                                        b_add = 1
                                        flows_item['flowNum'] += 1                                                
                                        new_dic_msg = {'flowId':flow_id, 'flowName':flow_name,'flowSourceNodeId':flow_sourcenode_id,'flowDesNodeId':flow_desnode_id}
                                        flows_item['flow_info'].append(new_dic_msg)
                                        continue # 退出for flows_item in  flows 循环
                                if b_add == 0: # source 相同，但是目的地址没有相同的，新加一条
                                    b_add = 1
                                    new_dic_msg ={'desFlow': flow_dest, 'flowNum':1, 'flow_info':[{'flowId':flow_id, 'flowName':flow_name,'flowSourceNodeId':flow_sourcenode_id,'flowDesNodeId':flow_desnode_id}]}
                                    flow_detail_item['desFlowNum'] += 1
                                    flows.append(new_dic_msg)
                                    continue # 退出flow_detail_item in  flow_detail
                        if b_add == 0: #flow type 相同，但是源不相同
                            b_add = 1
                            new_dic_msg ={'sourceFlow':flow_source, 'desFlowNum':1, 'flows':[{'desFlow': flow_dest, 'flowNum':1, 'flow_info':[{'flowId':flow_id, 'flowName':flow_name,'flowSourceNodeId':flow_sourcenode_id,'flowDesNodeId':flow_desnode_id}]}]}
                            all_type_item['thisTypeSurceNum'] += 1
                            flow_detail.append(new_dic_msg)    
                            continue
                if  b_add == 0:
                    new_dic_msg ={'flow_type':flow_type, 'thisTypeSurceNum':1, 'flowsDetail':[{'sourceFlow':flow_source, 'desFlowNum':1, 'flows':[{'desFlow': flow_dest, 'flowNum':1, 'flow_info':[{'flowId':flow_id, 'flowName':flow_name,'flowSourceNodeId':flow_sourcenode_id,'flowDesNodeId':flow_desnode_id}]}]}]}
                    all_type_info.append(new_dic_msg)
                    type_num += 1   
                        
        if type_num > 0:       
            data = {
                    'typeNum':type_num,
                    'allFlowInfo':all_type_info              
                    }
            ret = ErrCode.SUCCESS
            return ret, data
        else:
            data = {}
            return ErrCode.SUCCESS,data 
    except Exception as e:
        print("search_flow_Info_at_flow_list Exception:", e)
        data = {}
        error_logger.error(e)
        return ErrCode.FAILED, data 


def search_flow_Info_at_gallflow(search_type,search_info):
    try:
        all_type_info = []
        type_num = 0
        b_add = 0

        for value in g_allFlows.values():
            b_found = False
            key_get_info = []
            if search_type == 'flowName':      
                key_get_info.append(value.flow_name)
            elif search_type == 'sourceNode':
                key_get_info.append(value.src_name)
            elif search_type == 'desNode':
                key_get_info.append(value.des_name)
            else:
                key_get_info.append(value.flow_name)
                key_get_info.append(value.src_name)
                key_get_info.append(value.des_name)
            
            for info in key_get_info:
                if search_info in info:
                    b_found = True
                    break

            if b_found:
                b_add = 0
                flow_name= value.flow_name
                flow_type = value.flow_type
                flow_source = value.src_name
                flow_dest = value.des_name
                flow_id = value.id
                flow_desnode_id = value.des_id
                flow_sourcenode_id = value.src_id

                for all_type_item in all_type_info:
                    if all_type_item['flow_type'] == flow_type:                    
                        flow_detail = all_type_item['flowsDetail']
                        for flow_detail_item in  flow_detail:
                            if flow_detail_item['sourceFlow'] == flow_source:
                                flows = flow_detail_item['flows']
                                for flows_item in  flows:
                                    if flows_item['desFlow'] == flow_dest:
                                        b_add = 1
                                        flows_item['flowNum'] += 1                                                
                                        new_dic_msg = {'flowId':flow_id, 'flowName':flow_name,'flowSourceNodeId':flow_sourcenode_id,'flowDesNodeId':flow_desnode_id}
                                        flows_item['flow_info'].append(new_dic_msg)
                                        continue # 退出for flows_item in  flows 循环
                                if b_add == 0: # source 相同，但是目的地址没有相同的，新加一条
                                    b_add = 1
                                    new_dic_msg ={'desFlow': flow_dest, 'flowNum':1, 'flow_info':[{'flowId':flow_id, 'flowName':flow_name,'flowSourceNodeId':flow_sourcenode_id,'flowDesNodeId':flow_desnode_id}]}
                                    flow_detail_item['desFlowNum'] += 1
                                    flows.append(new_dic_msg)
                                    continue # 退出flow_detail_item in  flow_detail
                        if b_add == 0: #flow type 相同，但是源不相同
                            b_add = 1
                            new_dic_msg ={'sourceFlow':flow_source, 'desFlowNum':1, 'flows':[{'desFlow': flow_dest, 'flowNum':1, 'flow_info':[{'flowId':flow_id, 'flowName':flow_name,'flowSourceNodeId':flow_sourcenode_id,'flowDesNodeId':flow_desnode_id}]}]}
                            all_type_item['thisTypeSurceNum'] += 1
                            flow_detail.append(new_dic_msg)    
                            continue
                if  b_add == 0:
                    new_dic_msg ={'flow_type':flow_type, 'thisTypeSurceNum':1, 'flowsDetail':[{'sourceFlow':flow_source, 'desFlowNum':1, 'flows':[{'desFlow': flow_dest, 'flowNum':1, 'flow_info':[{'flowId':flow_id, 'flowName':flow_name,'flowSourceNodeId':flow_sourcenode_id,'flowDesNodeId':flow_desnode_id}]}]}]}
                    all_type_info.append(new_dic_msg)
                    type_num += 1   
                        
        if type_num > 0:       
            data = {
                    'typeNum':type_num,
                    'allFlowInfo':all_type_info              
                    }
            ret = ErrCode.SUCCESS
            return ret, data
        else:
            data = {}
            return ErrCode.SUCCESS,data 
    except Exception as e:
        print("search_flow_Info_at_flow_list Exception:", e)
        data = {}
        error_logger.error(e)
        return ErrCode.FAILED, data 
