# -*- encoding: utf-8 -*-
"""
@File    : digitaltwin.py
@Time    : 2019/05/29 10:56:59
@Author  : 
@License : Copyright (c) 2004-2019 New H3C Tech. Co., Ltd. All rights reserved.
@Desc    : 创建flask应用，启用应用
"""

from flask import Flask
from flask import jsonify
from flask_cors import CORS
from apps import register_blueprints
from apps.util import init_logger
from apps.errcode import ErrCode
from apps.v1_0.test import *

def create_app():
    """创建应用."""
    app = Flask(__name__, static_url_path="/digitalTwins/static")
    CORS(app, supports_credentials=True)

    return app

def init_app(app):
    """初始化app."""

    init_logger(app)
    register_blueprints(app)

	
# 创建应用
app = create_app()
init_app(app)

@app.errorhandler(404)
def handle_not_found(e):
    """自定义404的回应信息."""

    response = jsonify({
        "status":"fail",
        "errorCode":ErrCode.RESOURCE_NOT_FOUND,
        "errorInfo":ErrCode.ERR_MSG[ErrCode.RESOURCE_NOT_FOUND]})
    response.status_code = 404

    return response

if __name__ == '__main__':
    if debug_postman:
        app.run(threaded=True, debug=True, host='0.0.0.0', port=port_id)
    else:
        app.run(threaded=True, debug=False, host='0.0.0.0', port=9025)