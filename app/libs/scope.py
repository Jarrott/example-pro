# -*- encoding:utf-8 -*-
"""
@ Created by Seven on  2018/06/22 
"""


class Scope:
    """
    权限控制的基类
    """
    allow_api = []
    allow_module = []
    forbidden = []

    def __add__(self, other):
        self.allow_api = self.allow_api + other.allow_api
        self.allow_api = list(set(self.allow_api))
        # 运算符重载

        self.allow_module = self.allow_module + \
                            other.allow_module
        self.allow_module = list(set(self.allow_module))

        self.forbidden = self.forbidden + other.forbidden
        self.forbidden = list(set(self.forbidden))

        return self


class AdminScope(Scope):
    """
    管理员访问的接口
    auth:777
    """
    allow_module = ['seven_v1.user']


class UserScope(Scope):
    """
    用户访问的接口
    auth:1
    """
    allow_api = ['seven_v1.user+delete_user']

    # def __init__(self):
    #     self + AdminScope


def is_in_scope(scope, endpoint):
    """
    验证权限作用域
    :param scope:
    :param endpoint:
    :return:
    """
    scope = globals()[scope]()
    splits = endpoint.split('+')
    red_name = splits[0]
    if endpoint in scope.forbidden:
        return False
    if endpoint in scope.allow_api:
        return True
    if red_name in scope.allow_module:
        return True
    else:
        return False
