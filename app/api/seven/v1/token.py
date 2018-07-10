# -*- encoding:utf-8 -*-
"""
@ Created by Seven on  2018/06/22 
"""
from flask import current_app, jsonify
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer)

from app.api.seven.models import User
from app.libs.enums import ClientTypeEnum
from app.libs.redprint import Redprint
from app.validators.forms import ClientForm

__author__ = 'Little Seven'

api = Redprint('token')


@api.route('', methods=['post'])
def get_token():
    """
    用户登录
            ---
            tags:
              - 用户模块
            parameters:
              - name: username
                in: body
                type: string
                required: true
                example: simple
              - name: password
                in: body
                type: string
                required: true
                example: 123456
              - name: type
                in: body
                type: int
                required: true
                example: 100
            responses:
              200:
                description: 返回信息
                examples:
                  success : {"error_code": 0,"msg": "ok","request": "POST /seven/v1/token"}
    """
    form = ClientForm().validate_for_api()
    promise = {
        ClientTypeEnum.USER_NAME: User.verify,
    }
    identity = promise[form.type.data](
        form.username.data,
        form.password.data
    )

    # 从配置文件读取token过期时间
    expiration = current_app.config['JWT_TOKEN_EXPIRES']

    token = generate_auth_token(
        identity['uid'],
        form.type.data,
        identity['scope'],
        expiration
    )
    res_token = {
        'error_code': 0,
        'success_token': token.decode('ascii')
    }
    return jsonify(res_token), 201


def generate_auth_token(uid, ac_type, scope=None,
                        expiration=7200):
    """
    生成token的方法
    :param uid:
    :param ac_type:
    :param scope:
    :param expiration:
    :return:
    """
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
    return s.dumps({
        'uid': uid,
        'type': ac_type.value,
        'scope': scope
    })
