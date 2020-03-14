# -*- encoding: utf-8 -*-
"""
@File    : param.py
@Time    : 
@Author  : 
@License : Copyright (c) 2004-2019 New H3C Tech. Co., Ltd. All rights reserved.
@Desc    : 创建flask应用，启用应用
"""

debug_postman = 1       # 用postman调试版本时置1，所有接口会切换为postman,正式版本置为0
test_debug = 1          # 使用假数据时置1（如传给前端用的调试版本）,正式版本置为0，
log_print_debug = 1     # 调试时置为1，打印代码中的err信息到log文件中，正式版本置为0
port_id = 5888          # 填写自己在postMan下测试的端口号
token = 'pUpxxoF2HDH7F4+NOkxThw=='  # token根据自己网页的URL上进行修改  服务器重启后会改变
