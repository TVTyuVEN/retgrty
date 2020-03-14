from flask import Flask
from flask import jsonify
from flask_cors import CORS
from apps import register_blueprints
from apps.util import init_logger
from apps.errcode import ErrCode
from apps.v1_0.test import *

