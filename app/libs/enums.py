# -*- encoding:utf-8 -*-
"""
@ Created by Seven on  2018/06/20 
"""

from enum import Enum


class ClientTypeEnum(Enum):

    USER_EMAIL = 100
    USER_MOBILE = 101

    # 微信小程序
    USER_MINA = 200
    # 微信公众号
    USER_WX = 201

    # 第三方
    USER_QQ = 300
