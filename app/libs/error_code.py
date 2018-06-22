# -*- encoding:utf-8 -*-
"""
@ Created by Seven on  2018/06/21 
"""
from .error import JsonTypeException


class ClientTypeError(JsonTypeException):
    """
    用户注册相关异常
    """
    code = 400
    message = '请求参数错误 ~ ！ ╮(╯▽╰)╭ '
    error_code = 10008


class ServerError(JsonTypeException):
    """
    服务器异常
    """
    code = 500
    message = "服务器异常！"
    error_code = 10001


class ParameterException(JsonTypeException):
    """
    全局异常
    """
    code = 400
    message = '非法参数 ~ ！ ╮(╯▽╰)╭ '
    error_code = 10008


class NotFound(JsonTypeException):
    """
    404错误
    """
    code = 404
    message = "找不到当前资源 ~ "
    error_code = 10013


class AuthFailed(JsonTypeException):
    """
    授权失败
    """
    code = 401
    message = "无权限访问"
    error_code = 10005


class Success(JsonTypeException):
    """
    操作成功
    """
    code = 201
    message = 'ok'
    error_code = 0
