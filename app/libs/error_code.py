# -*- encoding:utf-8 -*-
"""
@ Created by Seven on  2018/06/21 
"""
from .error import JsonTypeException


class Success(JsonTypeException):
    """
    操作成功
    """
    code = 201
    message = 'ok'
    error_code = 0


class DeleteSuccess(JsonTypeException):
    """
    删除成功
    因为204是 not content
    所以稍微违背rest开发原则
    采用202
    """
    code = 202
    message = '删除成功'
    error_code = 1


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
    message = '服务器异常！'
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
    message = '找不到当前资源 ~ '
    error_code = 10013


class UserNotExistException(JsonTypeException):
    """
    400 用户不存在
    """
    code = 400
    message = "用户不存在 ~！"
    error_code = 20001


class AuthFailed(JsonTypeException):
    """
    授权失败
    """
    code = 401
    message = '授权出错 ~'
    error_code = 10005


class Forbidden(JsonTypeException):
    """
    无权限操作
    """
    code = 403
    message = '您没有访问此功能的权限 ~'
    error_code = 10004


class Failed(JsonTypeException):
    code = 404
    message = '失败的动作 ~'
    error_code = 10012


class ImagesError(JsonTypeException):
    code = 400
    message = '图片上传失败'
    error_code = 20001


class EditError(JsonTypeException):
    code = 404
    message = '内容已存在'
    error_code = 10014
