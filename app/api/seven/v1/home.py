# -*- encoding:utf-8 -*-
"""
@ Created by Seven on  2018/06/20 
"""
from app.libs.redprint import Redprint

__author__ = 'Little Seven'

# 前台路由
api = Redprint('home')


@api.route('')
def index():
    return "1"
