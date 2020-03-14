from flask import json
from werkzeug.exceptions import HTTPException


class ErrCode:
    """自定义错误码和错误信息"""

    #自定义错误码
    SUCCESS = 0
    FAILED = 1000

    #基本错误码



