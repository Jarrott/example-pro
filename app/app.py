# -*- encoding:utf-8 -*-
"""
@ Created by Seven on  2018/06/20 
"""
from datetime import date
from flask import Flask as _Flask
from flask.json import JSONEncoder as _JsonEncoder

from app.libs.error_code import ServerError


class JsonEncoder(_JsonEncoder):
    def default(self, o):
        """
        重写Flask JsonEncoder
        实现支持对象序列化
        :param o:
        :return:
        """
        if hasattr(o, 'keys') and hasattr(o, '__getitem__'):
            return dict(o)
        if isinstance(o, date):
            return o.strftime('%Y-%m-%d')
        raise ServerError()


class Flask(_Flask):
    """
    重写Flask
    """
    json_encoder = JsonEncoder
