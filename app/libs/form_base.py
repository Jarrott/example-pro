# -*- encoding:utf-8 -*-
"""
@ Created by Seven on  2018/06/20 
"""
from flask import request
from wtforms import Form

from app.libs.error_code import ParameterException


class BaseForm(Form):
    """
    重写Form，实现是指验证api参数
    """
    def __init__(self):
        # 静默模式接受json参数
        data = request.get_json(silent=True)
        args = request.args.to_dict()
        super(BaseForm, self).__init__(data=data, **args)

    def validate_for_api(self):
        valid = super(BaseForm, self).validate()
        if not valid:
            raise ParameterException(message=self.errors)
        return self
