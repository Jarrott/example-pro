# -*- encoding:utf-8 -*-
"""
@ Created by Seven on  2018/06/20 
"""
from app.libs.error_code import Success
from app.libs.redprint import Redprint
from app.libs.enums import ClientTypeEnum
from app.validators.forms import ClientForm, UserForm
from .models.user import User

api = Redprint('client')


@api.route('/register', methods=['POST'])
def create_client():
    """ 用户注册
            发送json数据进行注册(注册为开发者的type为300)
            ---
            tags:
              - 后台登录权限相关
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
                  success : {"error_code": 0,"msg": "ok","request": "POST /v1/client/register"}
        """
    form = ClientForm().validate_for_api()
    promise = {
        ClientTypeEnum.USER_NAME: __register_user_by_username,
    }
    promise[form.type.data]()
    return Success()


@api.route('/register/by_mobile')
def create_mobile():
    """
    手机格式注册
    :return:
    """
    pass


@api.route('/register/by_wx')
def create_wx():
    """
    第三方注册
    :return:
    """
    pass


def __register_user_by_username():
    form = UserForm().validate_for_api()
    User.register_by_username(form.username.data,
                              form.password.data,
                              form.nickname.data)
