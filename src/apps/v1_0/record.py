# -*- encoding: utf-8 -*-
# -*- encoding: utf-8 -*-
"""
@File    : record.py
@Time    : 2019/11/19 11:16:55
@Author  : 
@License : Copyright (c) 2004-2019 New H3C Tech. Co., Ltd. All rights reserved.
@Desc    : 
"""
import threading
import os
import sys
import stat
import zipfile 
import shutil
import xlsxwriter
import time
from flask import request, json
from flask import make_response
from flask_restful import Resource

from apps.errcode import ErrCode
from apps.util import g_ana, g_sim,  g_tunrec
from apps.util import get_start_end_time
from apps.util import info_logger,error_logger

from apps.v1_0.bginterface import *

from apps.v1_0.analyse import get_summary_info, get_fault_def, get_flows_and_path_info, get_tunnels_info

class LoadStatisticInfo():
    def __init__(self):
        self.overload_num = 0
        self.change_num =0
        self.other_num = 0

        self.overload_percent = 0
        self.other_percent = 0  

        # 仿真类型 复选
        self.overload_data = []
        self.changed_data = []


def exchange(input):
    try:
        if input == 'Unchange':
            return '未变化'
        elif input == 'Change':
            return '变化'
        elif input == 'Interrupt':
            return '中断'
        elif input == 'Reachable':
            return '可达'
        elif input == 'Unreachable':
            return '不可达'
        elif input == 'Overload':
            return '过载'
        elif input == 'Router':
            return '路由器'
        elif input == 'Link Fault':
            return '链路故障'
        elif input == 'Node Fault':
            return '网元故障'
        elif input == 'Before Definition':
            return '定义前故障'
        elif input == 'After Definition':
            return '定义后故障'
        elif input == 'Before & After Definition':
            return '定义前,定义后均故障'
        elif input == 'UP':
            return '可达'
        elif input == 'DOWN':
            return '不可达'            
        else:
            return 'N/A'
    except Exception as e:
        info_logger.error(e)
        error_logger.error(e)
        print("exchange Exception:", e)
        return 0        

# 5.1.2	子函数
def get_rate_stage(rate):
    try:
        # 阈值获取
        firstStepEnd = g_ana.analyse_firstStepEnd 
        secondStepEnd = g_ana.analyse_secondStepEnd 
        thirdStepEnd = g_ana.analyse_thirdStepEnd 

        if firstStepEnd > secondStepEnd or secondStepEnd > thirdStepEnd:
            # 错误情况，暂定返回最高阶段
            return 4

        if rate >= 0 and rate < firstStepEnd:
            stage = 1
        elif rate >= firstStepEnd and rate < secondStepEnd:
            stage = 2
        elif rate >= secondStepEnd and rate < thirdStepEnd:
            stage = 3
        else:
            stage = 4
        
        return stage
    except Exception as e:
        info_logger.error(e)
        error_logger.error(e)
        print("get_rate_stage Exception:", e)
        return 0

def insert_one_chart(workbook, worksheet, categories, values,chart_name, position):
    try:
        # --------生成图表并插入到excel---------------
        # 创建一个柱状图(pie chart)
        chart_col = workbook.add_chart({'type': 'pie'})
        # 配置第一个系列数据
        chart_col.add_series({
            'name': chart_name,
            'categories': categories,
            'values': values,
            'points': [
                {'fill': {'color': 'B8B8B8'}},  # green  #00CD00
                {'fill': {'color': 'FF9900'}},   # blue
                {'fill': {'color': 'CA0001'}},  # yellow
                {'fill': {'color': 'gray'}},   # 黄色 FF9900  灰色 B8B8B8  红色 CA0001 
            ],
        })
        # 设置大小
        chart_col.set_size({'width': 356, 'height': 257})
        # 设置图表的title 和 x，y轴信息
        chart_col.set_title({'name': chart_name})
        # 设置图表的风格
        chart_col.set_style(10)
        # 把图表插入到worksheet以及偏移
        worksheet.insert_chart(position, chart_col, {'x_offset': 0, 'y_offset': 0})
    except Exception as e:
        info_logger.error(e)
        error_logger.error(e)
        print("insert_one_chart Exception:", e)
 
def write_summary_xls_data(summary_data,sum_list,workbook,worksheet,cur_time):
    try:
    
        bold = workbook.add_format({'bold': 1,'top':1, 'left':1, 'right':1, 'bottom':1,'bg_color':'#DAEEF3','align' : 'center'})
        center = workbook.add_format({'align' : 'center','top':1, 'left':1, 'right':1, 'bottom':1})
        center_time = workbook.add_format({'align' : 'center','bg_color':'#E6B8B7'})

        # 向excel中写入数据，建立图标时要用到
        summary_flow = ['数量',summary_data['summary']['flows']['flow_unchanged'],
                        summary_data['summary']['flows']['flow_changed'],
                        summary_data['summary']['flows']['flow_interrupted']]
        summary_tunnel = ['数量',summary_data['summary']['tunnels']['tunnel_unchanged'],
                        summary_data['summary']['tunnels']['tunnel_changed'],
                        summary_data['summary']['tunnels']['tunnel_interrupted']]
        summary_load = ['数量',summary_data['summary']['loads']['other_num'],
                        summary_data['summary']['loads']['overload_num']]
        outlookTime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(int(cur_time)/1000))
        time1 = outlookTime.split(' ')[0]
        time2 = outlookTime.split(' ')[1]
        row0 = ['时刻',time1,time2,'','','','','','','','','','','']
        center_first = workbook.add_format({'align' : 'center','bg_color':'#E6B8B7'})
        worksheet.write_row('A'+str(sum_list), row0, center_time)
        sum_list+= 1

        # 写入数据 
        row0 = ['Flow', '未变化', '变化', '中断']
        worksheet.write_row('A'+str(sum_list), row0, bold)
        worksheet.write_row('A'+str(sum_list+1), summary_flow,center)

        row4 = ['Tunnel', '未变化', '变化', '中断']
        worksheet.write_row('F'+str(sum_list), row4, bold)
        worksheet.write_row('F'+str(sum_list+1), summary_tunnel, center)

        row7 = ['Load', '其他', '过载']
        worksheet.write_row('K'+str(sum_list), row7, bold)
        worksheet.write_row('K'+str(sum_list+1), summary_load, center)

        # 画出饼状图 1
        flow_change_num = summary_data['summary']['flows']['flow_unchanged'] 
        flow_unchange_num = summary_data['summary']['flows']['flow_changed']
        flow_interrupt_num = summary_data['summary']['flows']['flow_interrupted']
        categories1 = '=Sheet1!$B$'+ str(sum_list) + ':$D$' + str(sum_list)
        if flow_change_num == 0 and flow_unchange_num == 0 and flow_interrupt_num == 0:
            values2 = '={1,1,1}'
        else:
            values2 = '=Sheet1!$B$'+ str(sum_list+1) + ':$D$' + str(sum_list+1)
        insert_one_chart(workbook, worksheet, categories1, values2, '流量信息', 'A'+str(sum_list+3))
        # 画出饼状图 2
        tun_change_num = summary_data['summary']['tunnels']['tunnel_unchanged']
        tun_unchange_num = summary_data['summary']['tunnels']['tunnel_changed']
        tun_interrupt_num = summary_data['summary']['tunnels']['tunnel_interrupted']
        categories1 = '=Sheet1!$G$'+ str(sum_list) + ':$I$' + str(sum_list)
        if tun_change_num == 0 and tun_unchange_num == 0 and tun_interrupt_num == 0:
            values2 = '={1,1,1}'
        else:
            values2 = '=Sheet1!$G$'+ str(sum_list+1) + ':$I$' + str(sum_list+1)
        insert_one_chart(workbook, worksheet, categories1, values2, '隧道信息', 'F'+str(sum_list+3))
        # 画出饼状图 3
        load_other_num = summary_data['summary']['loads']['other_num']
        load_overload_num = summary_data['summary']['loads']['overload_num']
        categories1 = '=Sheet1!$L$'+ str(sum_list) + ':$M$' + str(sum_list)
        if load_overload_num == 0 and load_other_num == 0 :
            values2 = '={1,1}'
        else:
            values2 = '=Sheet1!$L$'+ str(sum_list+1) + ':$M$' + str(sum_list+1)
        #print('categories1 = ',categories1)
        #print('values2 = ',values2)
        insert_one_chart(workbook, worksheet,  categories1, values2, '负载信息', 'K'+str(sum_list+3))
    except Exception as e:
        info_logger.error(e)
        error_logger.error(e)
        #print("write_summary_xls_data Exception:", e)

def report_summary_data(cur_time, get_type):
    try:
        if get_type == 'current':
            data_path = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir,'data', 'report_cur')
            # 删除旧报表
            dirs = os.listdir(data_path)
            for cur in dirs:
                if 'summary_report' in cur:
                    os.remove(data_path+'/' + cur)
            workbook = xlsxwriter.Workbook(data_path+'/summary_report_cur_time.xlsx')
        else:
            data_path = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir,'data', 'report_all')
            # 删除旧报表
            dirs = os.listdir(data_path)
            for cur in dirs:
                if 'summary_report' in cur:
                    os.remove(data_path+'/' + cur)
            workbook = xlsxwriter.Workbook(data_path+'/summary_report_all_time.xlsx')

        worksheet = workbook.add_worksheet()

        # 自定义xls内容格式
        worksheet.set_column('A:D', 12)
        worksheet.set_column('F:I', 12)
        worksheet.set_column('K:N', 12)

        # test
        _, summary_data = get_summary_info(cur_time)

        #获取数据 
        if get_type == 'current':
            #_, summary_data = get_summary_info(cur_time)
            sum_list = 1
            write_summary_xls_data(summary_data,sum_list,workbook,worksheet,cur_time)
        else:
            dic_sort_key = sorted(g_sim.statis_flow)
            sum_list = 1
            for start_time in dic_sort_key:
                #print(start_time)
                _, summary_data = get_summary_info(start_time)
                write_summary_xls_data(summary_data,sum_list,workbook,worksheet,start_time)
                sum_list += 18

        # 关闭workbook 
        workbook.close()

    except Exception as e:
        print("report_summary_data Exception:", e)
        info_logger.error(e)
        error_logger.error(e)

def report_flow_data(cur_time, get_type):
    # 创建一个excel
    try:
        if get_type == 'current':
            data_path = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir,'data', 'report_cur')
            # 删除旧报表
            dirs = os.listdir(data_path)
            for cur in dirs:
                if 'flow_report' in cur:
                    os.remove(data_path+'/' + cur)
            workbook = xlsxwriter.Workbook(data_path+'/flow_report_cur_time.xlsx')
        else:
            data_path = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir,'data', 'report_all')
            # 删除旧报表
            dirs = os.listdir(data_path)
            for cur in dirs:
                if 'flow_report' in cur:
                    os.remove(data_path+'/' + cur)
            workbook = xlsxwriter.Workbook(data_path+'/flow_report_all_time.xlsx')
        worksheet = workbook.add_worksheet()

        # 自定义样式，加粗
        bold = workbook.add_format({'bold': 1,'top':1, 'left':1, 'right':1, 'bottom':1,'bg_color':'#FAEBD7','align' : 'center'})
        center_first = workbook.add_format({'align' : 'center','top':1, 'left':1, 'right':1, 'bottom':1,'bg_color':'#D5F3F4'})
        center = workbook.add_format({'align' : 'center','top':1, 'left':1, 'right':1, 'bottom':1})
        center_time = workbook.add_format({'align' : 'center','bg_color':'#E6B8B7'})
        worksheet.set_column('A:F', 18)
        
        row_num = 1
        if get_type == 'current':
            # 单时刻报表打印            
            _, flow_data = get_flows_and_path_info(cur_time,'all')
            outlookTime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(int(cur_time)/1000))
            if flow_data:
                flows = flow_data['flowsInfo']
            else:
                flows = {}

            # 下面的内容 按照这个排序 
            row0 = ['时刻',outlookTime,"", "", "", ""]
            worksheet.write_row('A'+str(row_num), row0, center_time)
            row_num += 1

            row1 = ['序号','Flow名称',"跳数", "路径时延(ms)", "状态", ""]
            worksheet.write_row('A'+str(row_num), row1, bold)
            row_num += 1
            # 一条flow 一个list
            list_num = 1

            for flow in flows:
                row_next = [list_num, flow['name'], flow['hopCount'], flow['pathDelay'], exchange(flow['staus']), '']
                worksheet.write_row('A'+str(row_num), row_next,center_first)
                row_num += 1
                # 显示具体的path信息 
                row_next = ['','仿真定义前(后)','流量名称','路径时延(ms)','跳数','可达']
                worksheet.write_row('A'+str(row_num), row_next,center)
                row_num += 1
                # 显示故障前的path信息 
                path_before = flow['pathInfo']['beforeFault']
                row_next = ['','仿真定义前',path_before['flowInfo']['flowName'],path_before['flowInfo']['flowDelay'],
                            path_before['flowInfo']['flowHopNum'],exchange(path_before['flowInfo']['flowIsReach'])]
                worksheet.write_row('A'+str(row_num), row_next,center)
                row_num += 1
                # 显示故障后的path信息 
                path_after = flow['pathInfo']['afterFault']
                row_next = ['','仿真定义后',path_after['flowInfo']['flowName'],path_after['flowInfo']['flowDelay'],
                path_after['flowInfo']['flowHopNum'],exchange(path_after['flowInfo']['flowIsReach'])]
                worksheet.write_row('A'+str(row_num), row_next,center)
                row_num += 1
                list_num += 1
        else:
            # 所有时刻报表打印  
            dic_sort_key = sorted(g_sim.statis_flow)
            for cur_time in dic_sort_key:
                _, flow_data = get_flows_and_path_info(cur_time,'all')
                outlookTime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(int(cur_time)/1000))
                if flow_data:
                    flows = flow_data['flowsInfo']
                else:
                    flows = {}

                # 下面的内容 按照这个排序 
                row0 = ['时刻',outlookTime,"", "", "",  ""]
                worksheet.write_row('A'+str(row_num), row0, center_time)
                row_num += 1

                row1 = ['序号','Flow名称',"跳数", "路径时延(ms)", "状态", ""]
                worksheet.write_row('A'+str(row_num), row1, bold)
                row_num += 1
                # 一条flow 一个list
                list_num = 1

                for flow in flows:
                    row_next = [list_num, flow['name'], flow['hopCount'], flow['pathDelay'], exchange(flow['staus']), '']
                    worksheet.write_row('A'+str(row_num), row_next,center_first)
                    row_num += 1
                    # 显示具体的path信息 
                    row_next = ['','仿真定义前(后)','流量名称','路径时延(ms)','跳数','可达']
                    worksheet.write_row('A'+str(row_num), row_next,center)
                    row_num += 1
                    # 显示故障前的path信息 
                    path_before = flow['pathInfo']['beforeFault']
                    row_next = ['','仿真定义前',path_before['flowInfo']['flowName'],path_before['flowInfo']['flowDelay'],
                                path_before['flowInfo']['flowHopNum'],exchange(path_before['flowInfo']['flowIsReach'])]
                    worksheet.write_row('A'+str(row_num), row_next,center)
                    row_num += 1
                    # 显示故障后的path信息 
                    path_after = flow['pathInfo']['afterFault']
                    row_next = ['','仿真定义后',path_after['flowInfo']['flowName'],path_after['flowInfo']['flowDelay'],
                    path_after['flowInfo']['flowHopNum'],exchange(path_after['flowInfo']['flowIsReach'])]
                    worksheet.write_row('A'+str(row_num), row_next,center)
                    row_num += 1
                    list_num += 1

                # 最后空一行    
                row_num += 1
            
        workbook.close()
    
    except Exception as e:
        print("report_flow_data Exception:", e)
        info_logger.error(e)
        error_logger.error(e)

def report_load_data(curTime, get_type):

    try:
        if get_type == 'current':
            data_path = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir,'data', 'report_cur')
            # 删除旧报表
            dirs = os.listdir(data_path)
            for cur in dirs:
                if 'load_report' in cur:
                    os.remove(data_path+'/' + cur)
            workbook = xlsxwriter.Workbook(data_path+'/load_report_cur_time.xlsx')
        else:
            data_path = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir,'data', 'report_all')
            # 删除旧报表
            dirs = os.listdir(data_path)
            for cur in dirs:
                if 'load_report' in cur:
                    os.remove(data_path+'/' + cur)
            workbook = xlsxwriter.Workbook(data_path+'/load_report_all_time.xlsx')

        # 创建一个sheet
        worksheet = workbook.add_worksheet()
        # 自定义样式，加粗
        bold = workbook.add_format({'bold': 1,'top':1, 'left':1, 'right':1, 'bottom':1,'bg_color':'#FAEBD7','align' : 'center'})
        center = workbook.add_format({'align' : 'center','top':1, 'left':1, 'right':1, 'bottom':1})
        center_time = workbook.add_format({'align' : 'center','bg_color':'#E6B8B7'})
        center_yellow = workbook.add_format({'align' : 'center','top':1, 'left':1, 'right':1, 'bottom':1, 'bg_color':'#FFFF00'})
        worksheet.set_column('A:H', 18.5)

        row_num = 1
        step = g_ana.analyse_thirdStepEnd
        step_str = str(step)+'%'
        row0 = ['带宽利用率正常范围:','小于'+step_str,'带宽利用率过载范围:','大于或等于'+step_str]
        worksheet.write_row('A'+str(row_num), row0, center_yellow)
        
        row_num+=1
        if get_type == 'current':
            # 当前时刻报表
            start_time,_ = get_start_end_time(curTime)
            # 重新根据左侧的阈值栏 计算load数据 
            cal_load_info_by_threshold(start_time, g_ana.analyse_thirdStepEnd)

            try:
                overloadData = g_sim.statis_load.overload_data
                overloadNum = g_sim.statis_load.overload_num
            except Exception as e:
                print("report_load_data Exception:", e)
                overloadData = []
                overloadNum = 0

            load_data = {'overloadData':overloadData, 'overloadNum': overloadNum}
            outlookTime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(int(curTime)/1000))
            row0 = ['时刻',outlookTime,'','','','','','']
            worksheet.write_row('A'+str(row_num), row0, center_time)
            row_num += 1
            # 下面的内容 按照这个排序 
            row1 = ['序号','网元名称', "接口名称", "接口类型", "带宽(Mbps)", "带宽利用率(前)", "带宽利用率(后)", "状态"]
            worksheet.write_row('A'+str(row_num), row1, bold)
            row_num += 1

            list_num = 1
            for load in load_data['overloadData']:
                row_next = [list_num, load['assetName'], load['apiName'], load['apiType'], load['bandWidth'],str(load['ratioBefore'])+'%',str(load['ratioLater'])+'%',exchange(load['loadStatus'])]
                worksheet.write_row('A'+str(row_num), row_next,center)
                row_num += 1
                list_num += 1     
        else:
            # 所有时刻报表
            dic_sort_key = sorted(g_sim.before_fault_link_info)
            for st_time in dic_sort_key:
                start_time,_ = get_start_end_time(st_time)
                cal_load_info_by_threshold(start_time, g_ana.analyse_thirdStepEnd)
                try:
                    overloadData = g_sim.statis_load.overload_data
                    overloadNum = g_sim.statis_load.overload_num
                except Exception as e:
                    print("report_load_data 2 Exception:", e)
                    overloadData = []
                    overloadNum = 0

                load_data = {'overloadData':overloadData, 'overloadNum': overloadNum}
                #write_load_xls_data(load_data,row_num,workbook,worksheet)
                
                outlookTime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(int(st_time)/1000))
                row0 = ['时刻',outlookTime,'','','','','','']
                worksheet.write_row('A'+str(row_num), row0, center_time)
                row_num += 1
                # 下面的内容 按照这个排序 
                row1 = ['序号','网元名称', "接口名称", "接口类型", "带宽(Mbps)", "带宽利用率(前)", "带宽利用率(后)", "状态"]
                worksheet.write_row('A'+str(row_num), row1, bold)
                row_num += 1

                list_num = 1
                for load in load_data['overloadData']:
                    row_next = [list_num, load['assetName'], load['apiName'], load['apiType'], load['bandWidth'],str(load['ratioBefore'])+'%',str(load['ratioLater'])+'%',exchange(load['loadStatus'])]
                    worksheet.write_row('A'+str(row_num), row_next,center)
                    row_num += 1
                    list_num += 1    

                # 两时刻之间 空一个行    
                row_num += 1
                
        workbook.close()
    except Exception as e:
        print("report_load_data Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
    
def report_fault_data(get_type):
    # 创建一个excel
    try: 
        if get_type == 'current':
            xls_file_name = 'fault_report_cur_time.xlsx'

            data_path = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir,'data', 'report_cur')

            # 将已存在的信息删除
            dirs = os.listdir(data_path)
            #print('dir = ', dirs)
            for cur in dirs:
                if 'fault_report' in cur:
                    os.remove(data_path+'/' + cur)
            
        else:
            xls_file_name = 'fault_report_all_time.xlsx'

            data_path = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir,'data', 'report_all')

            # 将已存在的信息删除
            dirs = os.listdir(data_path)
            #print('dir = ', dirs)
            for cur in dirs:
                if 'fault_report' in cur:
                    os.remove(data_path+'/' + cur)

        workbook = xlsxwriter.Workbook(data_path+'/'+xls_file_name)
        
        # 创建一个sheet
        worksheet = workbook.add_worksheet()
        # 自定义样式，加粗
        bold = workbook.add_format({'bold': 1,'top':1, 'left':1, 'right':1, 'bottom':1,'bg_color':'#FAEBD7','align' : 'center'})
        center = workbook.add_format({'align' : 'center','top':1, 'left':1, 'right':1, 'bottom':1})
        worksheet.set_column('A:E', 14)
        # 下面的内容 按照这个排序 
        row0 = ['序号','故障类型', "故障名称", "故障描述", "故障阶段"]
        worksheet.write_row('A1', row0, bold)
        row_num = 2
        list_num = 1

        # 获取故障数据 
        fault_data = get_fault_def()

        if 'faultDef' in fault_data:
            if len(fault_data['faultDef']) > 0:
                faults = fault_data['faultDef'] 
                for fault in faults:
                    row_next = [list_num, fault['faultType'],fault['name'], exchange(fault['describe']),exchange(fault['message'])]
                    worksheet.write_row('A'+str(row_num), row_next,center)
                    row_num += 1
                    list_num += 1
        workbook.close()

    except Exception as e:
        print("report_fault_data Exception:", e)
        info_logger.error(e)
        error_logger.error(e)

def report_tunnel_data(curTime, get_type):
    # 创建一个excel
    try:

        if get_type == 'current':
            data_path = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir,'data', 'report_cur')
            # 删除旧报表
            dirs = os.listdir(data_path)
            for cur in dirs:
                if 'tunnel_report' in cur:
                    os.remove(data_path+'/' + cur)
            workbook = xlsxwriter.Workbook(data_path+'/tunnel_report_cur_time.xlsx')
        else:
            data_path = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir,'data', 'report_all')
            # 删除旧报表
            dirs = os.listdir(data_path)
            for cur in dirs:
                if 'tunnel_report' in cur:
                    os.remove(data_path+'/' + cur)
            workbook = xlsxwriter.Workbook(data_path+'/tunnel_report_all_time.xlsx')

        # 创建一个sheet
        worksheet = workbook.add_worksheet()
        # 自定义样式，加粗
        bold = workbook.add_format({'bold': 1,'top':1, 'left':1, 'right':1, 'bottom':1,'bg_color':'#FAEBD7','align' : 'center'})
        center = workbook.add_format({'align' : 'center','top':1, 'left':1, 'right':1, 'bottom':1})
        center_first = workbook.add_format({'align' : 'center','top':1, 'left':1, 'right':1, 'bottom':1,'bg_color':'#D5F3F4'})
        center_time = workbook.add_format({'align' : 'center','bg_color':'#E6B8B7'})
        worksheet.set_column('A:J', 14)
        
        row_num = 1
        if get_type == 'current':
            # 获取数据 
            _, tunnel_data = get_tunnels_info(curTime, 'all')
            if 'tunnels' in tunnel_data:
                if len(tunnel_data['tunnels']) > 0:
                    tuns = tunnel_data['tunnels'] 
                    outlookTime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(int(curTime)/1000))
                    time1 = outlookTime.split(' ')[0]
                    time2 = outlookTime.split(' ')[1]
                    row0 = ['时刻',time1,time2,'','','','','','','']
                    worksheet.write_row('A'+str(row_num), row0, center_time)
                    row_num += 1
                    row1 = ['序号','网元名称', "隧道名称",'调度隧道路径', "源IP", "目的IP", "隧道类型", "跳数", "路径时延(ms)", "状态"]
                    worksheet.write_row('A'+str(row_num), row1, bold)
                    row_num += 1
                    list_num = 1
                    for tunnel in tuns:
                        if tunnel['pathNum'] == 1:
                            row_next = [list_num, tunnel['assetName'],tunnel['tunnelName'],'单路径',tunnel['SIP'],tunnel['DIP'],tunnel['tunnelType'],tunnel['hopNum'],tunnel['dalay'],exchange(tunnel['tunnelsStatus'])]
                        else:
                            row_next = [list_num, tunnel['assetName'],tunnel['tunnelName'],'主备路径',tunnel['SIP'],tunnel['DIP'],tunnel['tunnelType'],tunnel['hopNum'],tunnel['dalay'],exchange(tunnel['tunnelsStatus'])]
                        worksheet.write_row('A'+str(row_num), row_next,center_first)
                        row_num += 1
                        # 显示具体的path信息 
                        row_next = ['','仿真定义前(后)','主(备)路径','路径状态','跳数','路径时延(ms)','Tunnel状态','','','']
                        worksheet.write_row('A'+str(row_num), row_next,center)
                        row_num += 1
                        # 显示故障前的path信息 
                        info = tunnel['pathInfo']['beforeFault']['primary']

                        if info:
                            row_next = ['','仿真定义前', '主路径',info["tunnelInfo"]["tunnelStrict"],info["tunnelInfo"]["tunnelHopNum"],info["tunnelInfo"]["tunnelDelay"],exchange(info["tunnelInfo"]["tunnelStatus"]),'','','']
                        else:
                            row_next = ['','仿真定义前', '主路径','','','','','','','']

                        worksheet.write_row('A'+str(row_num), row_next,center)
                        row_num += 1
                        if tunnel['pathNum'] == 2:
                            info = tunnel['pathInfo']['beforeFault']['standby']
                            if info:
                                row_next = ['','仿真定义前', '备路径',info["tunnelInfo"]["tunnelStrict"],info["tunnelInfo"]["tunnelHopNum"],info["tunnelInfo"]["tunnelDelay"],exchange(info["tunnelInfo"]["tunnelStatus"]),'','','']
                            else:
                                row_next = ['','仿真定义前', '备路径','','','','','','','']
                        
                            worksheet.write_row('A'+str(row_num), row_next,center)
                            row_num += 1
                        # 显示故障后的path信息 
                        info = tunnel['pathInfo']['afterFault']['primary']
                        if info:
                            row_next = ['','仿真定义后', '主路径',info["tunnelInfo"]["tunnelStrict"],info["tunnelInfo"]["tunnelHopNum"],info["tunnelInfo"]["tunnelDelay"],exchange(info["tunnelInfo"]["tunnelStatus"]),'','','']
                        else:
                            row_next = ['','仿真定义后', '主路径','','','','','','','']
                        worksheet.write_row('A'+str(row_num), row_next,center)
                        row_num += 1
                        if tunnel['pathNum'] == 2:
                            info = tunnel['pathInfo']['afterFault']['standby']
                            if info:
                                row_next = ['','仿真定义后', '备路径',info["tunnelInfo"]["tunnelStrict"],info["tunnelInfo"]["tunnelHopNum"],info["tunnelInfo"]["tunnelDelay"],exchange(info["tunnelInfo"]["tunnelStatus"]),'','','']
                            else:
                                row_next = ['','仿真定义后', '备路径','','','','','','','']
                            worksheet.write_row('A'+str(row_num), row_next,center)
                            row_num += 1
                        list_num += 1
                else:
                    outlookTime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(int(curTime)/1000))
                    time1 = outlookTime.split(' ')[0]
                    time2 = outlookTime.split(' ')[1]
                    row0 = ['时刻',time1,time2,'','','','','','','']                    
                    worksheet.write_row('A'+str(row_num), row0, center_time)
                    row_num += 1
                    row1 = ['序号','网元名称', "隧道名称", '调度隧道路径',"源IP", "目的IP", "隧道类型", "跳数", "路径时延(ms)", "状态"]
                    worksheet.write_row('A'+str(row_num), row1, bold)
                    row_num += 1
        else:
            dic_sort_key = sorted(g_tunrec.sim_b4tuns)
            for cur_time in dic_sort_key:
                # 获取数据 
                _, tunnel_data = get_tunnels_info(cur_time, 'all')
                #print('tunnel_data===',tunnel_data)
                if 'tunnels' in tunnel_data:
                    if len(tunnel_data['tunnels']) > 0:
                        tuns = tunnel_data['tunnels'] 
                        outlookTime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(int(cur_time)/1000))
                        time1 = outlookTime.split(' ')[0]
                        time2 = outlookTime.split(' ')[1]
                        row0 = ['时刻',time1,time2,'','','','','','','']
                        worksheet.write_row('A'+str(row_num), row0, center_time)
                        row_num += 1
                        row1 = ['序号','网元名称', "隧道名称", '调度隧道路径',"源IP", "目的IP", "隧道类型", "跳数", "路径时延(ms)", "状态"]
                        worksheet.write_row('A'+str(row_num), row1, bold)
                        row_num += 1 
                        list_num = 1 
                        for tunnel in tuns:
                            if tunnel['pathNum'] == 1:
                                row_next = [list_num, tunnel['assetName'],tunnel['tunnelName'],'单路径',tunnel['SIP'],tunnel['DIP'],tunnel['tunnelType'],tunnel['hopNum'],tunnel['dalay'],exchange(tunnel['tunnelsStatus'])]
                            else:
                                row_next = [list_num, tunnel['assetName'],tunnel['tunnelName'],'主备路径',tunnel['SIP'],tunnel['DIP'],tunnel['tunnelType'],tunnel['hopNum'],tunnel['dalay'],exchange(tunnel['tunnelsStatus'])]
                            worksheet.write_row('A'+str(row_num), row_next,center_first)
                            row_num += 1
                            # 显示具体的path信息 
                            row_next = ['','仿真定义前(后)','主(备)路径','路径状态','跳数','路径时延(ms)','Tunnel状态','','','']
                            worksheet.write_row('A'+str(row_num), row_next,center)
                            row_num += 1
                            # 显示故障前的path信息 
                            info = tunnel['pathInfo']['beforeFault']['primary']
                            #print('!! info 1 ===',info)
                            if info:
                                row_next = ['','仿真定义前', '主路径',info["tunnelInfo"]["tunnelStrict"],info["tunnelInfo"]["tunnelHopNum"],info["tunnelInfo"]["tunnelDelay"],exchange(info["tunnelInfo"]["tunnelStatus"]),'','','']
                            else:
                                row_next = ['','仿真定义前', '主路径','','','','','','','']
                            worksheet.write_row('A'+str(row_num), row_next,center)
                            row_num += 1
                            if tunnel['pathNum'] == 2:
                                info = tunnel['pathInfo']['beforeFault']['standby']
                                #print('!! info 2 ===',info)
                                if info:                          
                                    row_next = ['','仿真定义前', '备路径',info["tunnelInfo"]["tunnelStrict"],info["tunnelInfo"]["tunnelHopNum"],info["tunnelInfo"]["tunnelDelay"],exchange(info["tunnelInfo"]["tunnelStatus"]),'','','']
                                else:
                                    row_next = ['','仿真定义前', '备路径','','','','','','','']
                                worksheet.write_row('A'+str(row_num), row_next,center)
                                row_num += 1
                            # 显示故障后的path信息 
                            info = tunnel['pathInfo']['afterFault']['primary']
                            #print('!! info 3 ===',info)
                            if info:
                                row_next = ['','仿真定义后', '主路径',info["tunnelInfo"]["tunnelStrict"],info["tunnelInfo"]["tunnelHopNum"],info["tunnelInfo"]["tunnelDelay"],exchange(info["tunnelInfo"]["tunnelStatus"]),'','','']
                            else:
                                row_next = ['','仿真定义后', '主路径','','','','','','','']
                                worksheet.write_row('A'+str(row_num), row_next,center)
                                row_num += 1
                            if tunnel['pathNum'] == 2:
                                info = tunnel['pathInfo']['afterFault']['standby']
                                #print('!! info 4 ===',info)
                                if info:
                                    row_next = ['','仿真定义后', '备路径',info["tunnelInfo"]["tunnelStrict"],info["tunnelInfo"]["tunnelHopNum"],info["tunnelInfo"]["tunnelDelay"],exchange(info["tunnelInfo"]["tunnelStatus"]),'','','']
                                else:
                                    row_next = ['','仿真定义后', '主路径','','','','','','','']
                                worksheet.write_row('A'+str(row_num), row_next,center)
                                row_num += 1
                            list_num += 1
                    else:
                        outlookTime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(int(cur_time)/1000))
                        time1 = outlookTime.split(' ')[0]
                        time2 = outlookTime.split(' ')[1]
                        row0 = ['时刻',time1,time2,'','','','','','','']
                        worksheet.write_row('A'+str(row_num), row0, center_time)
                        row_num += 1
                        row1 = ['序号','网元名称', "隧道名称", '调度隧道路径',"源IP", "目的IP", "隧道类型", "跳数", "路径时延(ms)", "状态"]
                        worksheet.write_row('A'+str(row_num), row1, bold)
                        row_num += 1
                #最后空一行
                row_num += 1
        workbook.close()

    except Exception as e:
        print("report_tunnel_data Exception:", e)
        info_logger.error(e)
        error_logger.error(e)

def get_all_xlsx_report_data(cur_time, get_type):

    try:
        if get_type == 'all':
            # Load 
            report_load_data(cur_time, get_type)
            # summary 
            report_summary_data(cur_time, get_type)
        else:
            report_flow_data(cur_time, get_type)
            # tunnel 
            report_tunnel_data(cur_time, get_type)
            # Fault 无需时间段处理
            report_fault_data(get_type)
            # Load 
            report_load_data(cur_time, get_type)
            # summary 
            report_summary_data(cur_time, get_type)
        return ErrCode.SUCCESS
    except Exception as e:
        print("get_all_xlsx_report_data Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return ErrCode.FAILED

def generate_zip_file(get_type):
    try:
        data_path = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
        run_path = os.getcwd()
        dirs = os.listdir(data_path+'/static/flow/')
        # 获取系统时间，用于zip文件名一部分
        cur_time =  time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        
        if get_type == 'current':
            # 删除之前的旧报表zip文件 
            for cur in dirs:
                if 'report_cur' in cur:
                    os.remove(data_path+'/static/flow/' + cur)
            # 输出文件名
            file_name = 'Report_cur_' + cur_time + '.zip'
            startdir = data_path+"/data/report_cur/"
            zip_path = '/digitalTwins/static/flow/' + file_name

        else:
            # 删除之前的旧报表zip文件 
            for cur in dirs:
                if 'report_all' in cur:
                    os.remove(data_path+'/static/flow/' + cur)
            # 输出文件名
            file_name = 'report_all' + '_' + cur_time + '.zip'
            startdir = data_path+"/data/report_all/"
            zip_path = '/digitalTwins/static/flow/' + file_name

        files = os.listdir(startdir)
        # 打包文件 
        f = zipfile.ZipFile(file_name, 'w', zipfile.ZIP_DEFLATED)
        for fil in files:
            fileFullPath = os.path.join(startdir, fil)
            f.write(fileFullPath,fil)

        f.close() 
        
        # 将文件移动到static/flow下 
        shutil.move(run_path+'/'+file_name, data_path+'/static/flow')

        return zip_path

    except Exception as e:
        print("generate_zip_file Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return 'Null'

def report_analyse_data(input_time, get_type):
    try:
        # 先生成所有的excl文件
        ret = get_all_xlsx_report_data(input_time, get_type)

        if ret != ErrCode.SUCCESS:
            return 'Get report fail'

        # 然后打包为压缩文件，将路径返回给前台
        zip_file_path = generate_zip_file(get_type)

        return zip_file_path
    except Exception as e:
        print("report_analyse_data Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
        return 'Null zip file'

def report_xls_in_advance():
    try:
        # 生成所有时刻的xls文件，由于以下内容较多且固定，因此在仿真阶段先保存好文件
        # Flow 
        report_flow_data(0, 'all')
        # tunnel 
        report_tunnel_data(0, 'all')
        # Fault 无需时间段处理
        report_fault_data('all')
    except Exception as e:
        print("report_xls_in_advance Exception:", e)
        info_logger.error(e)
        error_logger.error(e)

def cal_load_info_by_threshold(start_time, thirdstepend):
    try:
        """根据查看时，设置的时间，及阈值，进行负载这个设置时间的负载分析
        把负载的统计信息，保存到sim.statis_load里
        把链路的阈值信息，保存到sim.topo.link里
        
        Args:
            none
        Returns:
            none
        Raise:
            none
        """ 
        # 统计仿真故障前后超过阈值负载信息和其它负载信息
        g_sim.statis_load = LoadStatisticInfo()
        overloaddata_info = g_sim.statis_load.overload_data
        changeddata_info = g_sim.statis_load.changed_data

        if start_time not in g_sim.before_fault_link_info or start_time not in g_sim.after_fault_link_info:
            return ErrCode.FAILED

        # 获取start_time 
        period_link_before = g_sim.before_fault_link_info[start_time].link_info
        period_link_after = g_sim.after_fault_link_info[start_time].link_info

        # 获取链路信息
        for linkid, value in period_link_before.items():
            linkInfo_before = value
            linkInfo_after = period_link_after[linkid]

            # 获取带宽利用率 
            rate_a2b_before = linkInfo_before.a_to_b.out_use_ratio
            rate_b2a_before = linkInfo_before.b_to_a.out_use_ratio
            rate_a2b_after = linkInfo_after.a_to_b.out_use_ratio         
            rate_b2a_after = linkInfo_after.b_to_a.out_use_ratio

            #print('rate_a2b_before:',rate_a2b_before,rate_b2a_before,rate_a2b_after,rate_b2a_after)
            #print('ana_step:', g_ana.analyse_firstStepEnd, g_ana.analyse_secondStepEnd, g_ana.analyse_thirdStepEnd)

            # 计算得到带宽利用率对应的阈值
            stage_a2b_before = get_rate_stage(rate_a2b_before)
            stage_a2b_after = get_rate_stage(rate_a2b_after)
            stage_b2a_before = get_rate_stage(rate_b2a_before)
            stage_b2a_after = get_rate_stage(rate_b2a_after)

            if period_link_before[linkid].asset_a == g_sim.topo.links[linkid].nodeid1:
                # 记录a_to_b 和 b_to_a 的带宽利用阈值区间,
                g_sim.topo.links[linkid].bandwidthStage1to2 = stage_a2b_before 
                g_sim.topo.links[linkid].bandwidthStage2to1 = stage_b2a_before 
    
                g_sim.af_topo.links[linkid].bandwidthStage1to2 = stage_a2b_after
                g_sim.af_topo.links[linkid].bandwidthStage2to1 = stage_b2a_after
            else:
                # 如果topo上的assid_1与node2才匹配，需要换一下顺序,
                g_sim.topo.links[linkid].bandwidthStage1to2 = stage_b2a_before 
                g_sim.topo.links[linkid].bandwidthStage2to1 = stage_a2b_before 

                g_sim.af_topo.links[linkid].bandwidthStage1to2 = stage_b2a_after
                g_sim.af_topo.links[linkid].bandwidthStage2to1 = stage_a2b_after

        # 把kbps改成mbps , 保留两位小数
            a_b_m_bps = round(linkInfo_after.a_to_b.band_width / 1000, 2)
            b_a_m_bps = round(linkInfo_after.b_to_a.band_width / 1000, 2)

            if rate_a2b_after >= thirdstepend: # 如果仿真故障后的带宽利用率大于阈值，则超过阈值的个数加1并保存overloaded信息
                overload_info = {'assetName':linkInfo_after.a_to_b.asset_net_name,\
                                'apiName':linkInfo_after.a_to_b.asset_port,\
                                'apiType':linkInfo_after.a_to_b.interface_type,\
                                'bandWidth':('%.2f'%(a_b_m_bps)),\
                                'ratioBefore':('%.2f'%(rate_a2b_before)),\
                                'ratioLater':('%.2f'%(rate_a2b_after)),\
                                'loadStatus':'Overload'}
                overloaddata_info.append(overload_info)
                g_sim.statis_load.overload_num += 1
            else:
                g_sim.statis_load.other_num += 1        
                if rate_a2b_after != rate_a2b_before: # 如果仿真故障后的带宽利用率小于阈值，且不等于仿真故障前的带宽利用率，则保存changed信息
                    changed_info = {'assetName':linkInfo_after.a_to_b.asset_net_name,\
                                    'apiName':linkInfo_after.a_to_b.asset_port,\
                                    'apiType':linkInfo_after.a_to_b.interface_type,\
                                    'bandWidth':('%.2f'%(a_b_m_bps)),\
                                    'ratioBefore':('%.2f'%(rate_a2b_before)),\
                                    'ratioLater':('%.2f'%(rate_a2b_after)),\
                                    'loadStatus':'Change'}
                    changeddata_info.append(changed_info)
                    g_sim.statis_load.change_num += 1 

            if rate_b2a_after >= thirdstepend: # 同理
                overload_info ={'assetName':linkInfo_after.b_to_a.asset_net_name,\
                                'apiName':linkInfo_after.b_to_a.asset_port,\
                                'apiType':linkInfo_after.b_to_a.interface_type,\
                                'bandWidth':('%.2f'%(b_a_m_bps)),\
                                'ratioBefore':('%.2f'%(rate_b2a_before)),\
                                'ratioLater':('%.2f'%(rate_b2a_after)),\
                                'loadStatus':'Overload'}
                overloaddata_info.append(overload_info)
                g_sim.statis_load.overload_num += 1
            else:
                g_sim.statis_load.other_num += 1       
                if rate_b2a_after != rate_b2a_before:
                    changed_info = {'assetName':linkInfo_after.b_to_a.asset_net_name,\
                                    'apiName':linkInfo_after.b_to_a.asset_port,\
                                    'apiType':linkInfo_after.b_to_a.interface_type,\
                                    'bandWidth':('%.2f'%(b_a_m_bps)),\
                                    'ratioBefore':('%.2f'%(rate_b2a_before)),\
                                    'ratioLater':('%.2f'%(rate_b2a_after)),\
                                    'loadStatus':'Change'}
                    changeddata_info.append(changed_info)
                    g_sim.statis_load.change_num += 1 
            
        sum_num = g_sim.statis_load.overload_num + g_sim.statis_load.other_num
        g_sim.statis_load.overload_percent = 100 * g_sim.statis_load.overload_num / sum_num
        g_sim.statis_load.other_percent = 100 * g_sim.statis_load.other_num / sum_num

    except Exception as e:
        print("cal_load_info_by_threshold Exception:", e)
        info_logger.error(e)
        error_logger.error(e)
