# -*- encoding:utf-8 -*-
"""
@ Created by Seven on  2018/06/20 
"""
from flask import Blueprint
from app.api.seven.v1 import (home, client,
                              user, park)
from app.api.seven.v1 import token


def create_blueprint():
    """
    版本号为v1
    将宏图注册到蓝图当中
    :return: 视图路由
    """
    bp_v1 = Blueprint('seven_v1', __name__)
    home.api.register(bp_v1)
    client.api.register(bp_v1)
    user.api.register(bp_v1)
    token.api.register(bp_v1)
    park.api.register(bp_v1)
    return bp_v1
