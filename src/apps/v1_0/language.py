# -*- encoding: utf-8 -*-
"""
@File    : language.py
@Time    : 2019/06/22 14:07:21
@Author  : 
@License : Copyright (c) 2004-2019 New H3C Tech. Co., Ltd. All rights reserved.
@Desc    : 
"""
import os
import threading
from flask import request, json
from flask import make_response
from flask_restful import Resource

from apps.errcode import ErrCode
from apps.datacode import FlowLoadDetailCode,SyncModCode
from apps.util import info_logger, error_logger


language_save_info = {
}


language_file_name = 'i18n.conf'
language_file_path = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir,'data','language','i18n.conf')
language_dir_path = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir,'data','language')


def get_session_id():
    return 'h3c'

def get_language_from_file():
    b_read_success = 0
    language_dir = language_dir_path
    if not os.path.exists(language_dir):
        return ErrCode.FAILED
    elif not os.path.exists(language_file_path):
        return ErrCode.FAILED
    else:
        with open(language_file_path,'r') as conf:
            try:
                config = json.load(conf)
                if 'language_setting' in config.keys():
                    language = config['language_setting']
                    # 把所有的已经存在的信息进行读取
                    if isinstance(language,dict):
                        for key in language:
                            b_read_success = 1
                            language_save_info[key] = language[key]
                
                if b_read_success == 1:
                    return ErrCode.SUCCESS
                else:
                    return ErrCode.FAILED
            except Exception as e:
                return ErrCode.FAILED 

def save_language(language_index, ses_id):
    b_need_rewrite = 0
    get_id = get_session_id()
    if ses_id == None:
        session_id = get_id
    else:
        session_id = ses_id
    language_file_name = 'i18n.conf'
    
    info = '{"language_setting":{"%s":"%s"}}'%(session_id,language_index)
    
    language_dir = language_dir_path
    # 新建第一次的static\language文件夹
    if not os.path.exists(language_dir):
        language_save_info[session_id] = language_index
        os.makedirs(language_dir)
        file_path = language_dir +'/'+ language_file_name
        with open(file_path,"w") as conf:        
            conf.write(info)                   
    else:
        #如果文件夹存在，则判断文件是否存在
        if not os.path.exists(language_file_path):
            # 文件不存在时，直接把文件创建，把信息写入即可
            with open(language_file_path,"w") as conf:
                language_save_info[session_id] = language_index
                conf.write(info)
        else:
                # 文件存在时，查看里面的内容
                with open(language_file_path,'r') as conf:
                    try:
                        config = json.load(conf)
                        if 'language_setting' in config.keys():
                            language = config['language_setting']

                            # 这里无需判断此session_id是否存在,如下语句是有就替换，无就添加
                            language[session_id] = language_index

                            # 把所有的已经存在的信息进行读取
                            if isinstance(language,dict):
                                for key in language:
                                    language_save_info[key] = language[key]
                            
                            b_need_rewrite = 1
                            info = '{"language_setting":%s}'%(json.dumps(language))
                        else:
                            language_save_info[session_id] = language_index
                            # 如果连language_setting这个关键字都没有，直接添加即可
                            b_need_rewrite = 1    
                    except Exception as e:
                        info_logger.error(e)
                        error_logger.error(e)
                        language_save_info[session_id] = language_index
                        # 如果读取失败，直接写
                        b_need_rewrite = 1  

                if b_need_rewrite == 1:
                    with open(language_file_path,"w") as conf:
                        conf.write(info)

def set_lange(lang):
    session_id = get_session_id()
    save_language(lang, session_id)
    if lang == 'CHS':
        data = {"i_18n": "中文"}
    else:
        data = {"i_18n": lang} 
    return ErrCode.SUCCESS,data

# [debug]session会越来越多
def get_language_setting_index():
    if not language_save_info:
        save_language('CHS',get_session_id())
    
    session_id = get_session_id()

    if session_id in language_save_info:
        language = language_save_info[session_id]
    else:
        # 避免集群的时候，切换后，数据未同步，先从配置文件中读取一下
        result = get_language_from_file() 
        if result == ErrCode.SUCCESS:
            if session_id in language_save_info:
                language = language_save_info[session_id]
            else:
                save_language('EN',get_session_id())
        else:
            save_language('EN',get_session_id())
            
    if language == 'CHS':
        index = 1
    else:
        index = 0
    return index

def get_err_lang_str(code):
    """获取err模块的页面显示字符串"""
    
    index = get_language_setting_index()
    return ErrCode.ERR_MSG[code][index]

def get_flow_lang_str(code):
    """获取flow模块的页面显示字符串"""

    index = get_language_setting_index()
    return FlowLoadDetailCode.FLOW_LOAD_MSG[code][index]

def get_sync_lang_str(code):
    """获取sync模块的页面显示字符串"""

    index = get_language_setting_index()
    return SyncModCode.SYNC_MSG[code][index]