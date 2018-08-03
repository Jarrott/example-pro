# -*- encoding:utf-8 -*-
"""
@ Created by Seven on  2018/07/30 
"""
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