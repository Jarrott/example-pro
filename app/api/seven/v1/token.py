# -*- encoding:utf-8 -*-
"""
@ Created by Seven on  2018/06/22 
"""
from flask import current_app, jsonify
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from app.api.seven.models import User
from app.libs.enums import ClientTypeEnum
from app.libs.redprint import Redprint
from app.validators.forms import ClientForm

api = Redprint('token')


@api.route('', methods=['post'])
def get_token():
    """
    用户可以获取token的接口
    :return:
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
