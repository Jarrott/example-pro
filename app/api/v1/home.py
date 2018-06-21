# -*- encoding:utf-8 -*-
"""
@ Created by Seven on  2018/06/20 
"""
from flask import jsonify

from app.libs.redprint import Redprint

# 前台路由
api = Redprint('home')


@api.route('/')
def index():
    return jsonify({"username": "test"})
