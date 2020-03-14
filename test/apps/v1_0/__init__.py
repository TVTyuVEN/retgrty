from flask import Blueprint
from flask_restful import Api
from apps.v1_0.api import *


def register_views(app):
    api = Api(app)
    api.add_resource(testApi,"/testApi")

def creat_blueprint_v1_0():
    """创建蓝图v1.0版本"""
    bp_v1_0 = Blueprint("v1.0",__name__)
    register_views(bp_v1_0)
