# -*- encoding:utf-8 -*-
"""
@ Created by Seven on  2018/06/22 
"""
from flask import current_app, g, request
from collections import namedtuple
from flask_httpauth import HTTPBasicAuth
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
                          BadSignature, SignatureExpired)

from app.libs.error_code import AuthFailed, Forbidden
from app.libs.scope import is_in_scope

auth = HTTPBasicAuth()
User = namedtuple('User', ['uid', 'ac_type', 'scope'])


@auth.verify_password
def verify_password(token, password):
    """
    装饰器
    验证token是否合法
    :param username:
    :param password:
    :return:
    """
    user_info = verify_auth_token(token=token)
    if not user_info:
        return False
    else:
        g.user = user_info
        return True


def verify_auth_token(token):
    """
    验证token信息和所拥有的权限
    :param token:
    :return:
    """
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except BadSignature:
        raise AuthFailed(message="无效的Token",
                         error_code=10008)
    except SignatureExpired:
        raise AuthFailed(message="Token已过期",
                         error_code=10002)
    uid = data['uid']
    ac_type = data['type']
    scope = data['scope']
    allow = is_in_scope(scope, request.endpoint)
    if not allow:
        raise Forbidden()
    return User(uid, ac_type, scope)
