from apps.util import *
from apps.errcode import ErrCode


from flask import make_response











def error_response(error_code,status_code):
    """操作失败, response信息返回。

    Args:
        error_code: 自定义的错误码
        status_code: 返回的http状态码
    Returns:
        返回response信息和状态码
    Raise:
        none
    """
    response = make_response()
    response.headers.set("Content-Type","application/json")

    response = {
        "status":"fail",
        "errorCode":error_code,
        # "errorInfo":get_err_lang_str(error_code)
    }

    return response,status_code


def success_response():
    """操作成功, response信息返回。

    Args:
        none
    Returns:
        返回response信息和状态码
    Raise:
        none
    """

    response = make_response()
    response.headers.set('Content-Type', 'application/json')

    response = {
        "status": "success",
        "errorCode": ErrCode.SUCCESS,
        "errorInfo": get_err_lang_str(ErrCode.SUCCESS)}
    # print(response)
    return response, 200

def

