# -*- encoding: utf-8 -*-
"""
@File    : __init__.py
@Time    : 2019/05/29 11:08:10
@Author  : 
@License : Copyright (c) 2004-2019 New H3C Tech. Co., Ltd. All rights reserved.
@Desc    : 注册蓝图
"""

from apps.v1_0 import creat_blueprint_v1_0


def register_blueprints(app):
    """注册蓝图版本到应用."""
    app.register_blueprint(creat_blueprint_v1_0(), url_prefix='/digitalTwins/v1.0')