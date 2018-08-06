# -*- encoding:utf-8 -*-
"""
@ Created by Seven on  2018/07/30 
"""
import random

from flask import jsonify

from app.libs.redis import redis


def add_data_cache(up, down, obj):
    """定时上下架功能
    """
    redis.connection.set(up, obj)
    redis.connection.expireat(up, down)

    return 200


def get_data_cache(up):
    ss = redis.connection.get(up)
    return ss


def verify_code():
    """验证码"""
    """
    登录验证码
    每循环一次,从a到z中随机生成一个字母或数字
    65到90为字母的ASCII码,使用chr把生成的ASCII码转换成字符
    str把生成的数字转换成字符串
    """
    code = ''
    for i in range(4):
        v_code = random.choice([chr(random.randint(65, 90)), str(random.randint(0, 9))])
        code += v_code
    s_data = code.lower()
    if s_data:
        redis.connection.setex(s_data, 30, s_data)
        verify_code = {
            'error_code': 0,
            'code': code
        }

        return jsonify(verify_code)
