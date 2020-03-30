# -*- encoding:utf-8 -*-
"""
@ Created by Seven on  2018/07/12 
"""
import base64
import datetime
import os
import time
import uuid
import random

from flask import json, jsonify

from app.libs.redis import redis


def change_filename(filename):
    """
    修改文件名称
    :param filename:
    :return:
    """
    fileinfo = os.path.splitext(filename)
    filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + \
               str(uuid.uuid4().hex) + fileinfo[-1]
    return filename


def get_timestamp(dt, fmt="%Y-%m-%d"):
    """将 年-月-日格式数据转换为'1531881731'
    "
    :param dt: 指 datetime.now()
    :param fmt: 格式化的类型
    
    :doc : 当然可以采用datetime库
    
    :code:   from datetime import datetime
             dt = datetime.now()
             dt.strftime("%c") # 显示格式 年/月/日/ 时：分：秒
    
    """
    if dt is not None:
        time_array = time.strptime(dt, fmt)
        return int(time.mktime(time_array))
    return None


def str_timestamp(dt, fmt="%Y-%m-%d"):
    """将1531881731类型转换为'年-月-日'
    """
    __time = time.localtime(dt)
    time_array = time.strftime(fmt, __time)
    return time_array


def encode_base64(data):
    """对字典进行base64加密"""
    res_data = base64.b64encode(json.dumps(data).encode()).decode()
    return res_data


def decode_base64(data):
    """对base64解密"""
    data = base64.b64decode(data).decode('utf-8')
    res_data = json.loads(data)
    return res_data


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
