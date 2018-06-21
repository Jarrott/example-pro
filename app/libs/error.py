# -*- encoding:utf-8 -*-
"""
@ Created by Seven on  2018/06/21 
"""
from flask import request, json
from werkzeug.exceptions import HTTPException


def res_code(code):
    code_map = {
        200: {'code': 0, 'msg': u"请求成功"},
        201: {'code': 0, 'msg': u"操作成功"},
        202: {'code': 0, 'msg': u"数据接收成功"},
        204: {'code': 0, 'msg': u"重复请求"},
        222: {'code': 0, 'msg': u"删除模版含有关联数据"},
        400: {'code': 10008, 'msg': u"请求参数错误"},
        401: {'code': 10005, 'msg': u"无权限访问系统"},
        403: {'code': 10002, 'msg': u"禁止访问"},
        404: {'code': 10013, 'msg': u"未匹配到数据"},
        405: {'code': 10021, 'msg': u"请求方法不支持"},
        406: {'code': 10015, 'msg': u"请求不予接受"},
        412: {'code': 10017, 'msg': u"参数类型错误"},
        413: {'code': 10018, 'msg': u"API请求频率超出限制"},
        414: {'code': 10019, 'msg': u"开始时间早于结束时间"},
        416: {'code': 10013, 'msg': u"数据不允许修改"},
        421: {'code': 10051, 'msg': u"字段user和course必须能构成唯一集合"},
        500: {'code': 10001, 'msg': u"服务器异常"},
        712: {'code': 10712, 'msg': u"删除操作成功"}

    }
    try:
        return code_map[code]
    except KeyError:
        return {'code': code, 'msg': ""}


class JsonTypeException(HTTPException):
    code = 500
    message = '遇到未知错误 ~  ╮(╯▽╰)╭ '
    error_code = 999

    def __init__(self, message=None, code=None, error_code=None, heardes=None):
        if code:
            self.code = code
        if message:
            self.message = message
        if error_code:
            self.error_code = res_code(error_code)['code']
        super(JsonTypeException, self).__init__(message, None)

    def get_body(self, environ=None):
        body = dict(
            message=self.message,
            error_code=self.error_code,
            request=request.method + ' ' + self.get_url_no_param()
        )
        response = json.dumps(body)
        return response

    def get_headers(self, environ=None):
        """
        重写HTTPException,返回格式为json格式
        :param environ:
        :return:
        """
        return [('Content-Type', 'application/json')]

    @staticmethod
    def get_url_no_param():
        """
        获取客户端请求的API接口
        :return:
        """
        full_path = str(request.full_path)
        main_path = full_path.split('?')
        return main_path[0]
