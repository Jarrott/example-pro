# -*- encoding:utf-8 -*-
"""
@ Created by Seven on  2018/06/20 
"""
from flask import jsonify, g

from app.api.seven.v1.scope import get_scope
from app.libs.helper import verify_code
from app.libs.token_auth import auth
from app.libs.redprint import Redprint
from app.api.seven.models import User, db
from app.libs.error_code import (DeleteSuccess, Success, Failed)
from app.validators.forms import ChangePasswordForm, UserTypeForm, PhoneCodeForm, EmailForm, ResetPasswordForm

__author__ = 'Little Seven'

api = Redprint('user')


@api.route('/<int:uid>', methods=['GET'])
@auth.login_required
def super_get_user(uid):
    """ 查询用户
            重写了sqlalchemy中的get_or_404
            出错可以返回想要的报错信息
            filter_by 过滤了软删除的用户
            所以filter_by 也是必不可少的
            ---
            tags:
              - 超级管理员模块
            parameters:
              - name: id
                in: body
                type: int
                required: true
                example: 1
            responses:
              200:
                description: 返回信息
                schema:
                    id: User
                    type: object
                examples:
                  success : {"error_code": 0,"msg": "ok","request": "GET /seven/v1/<id>"}
        """
    user = User.query.filter_by(id=int(uid)).first_or_404()
    return jsonify(user)


@api.route('/get_user', methods=['GET'])
@auth.login_required
def super_get_all_user():
    """ 查询用户
            重写了sqlalchemy中的get_or_404
            出错可以返回想要的报错信息
            filter_by 过滤了软删除的用户
            所以filter_by 也是必不可少的
            ---
            tags:
              - 超级管理员模块
            parameters:
              - name: id
                in: body
                type: int
                required: true
                example: 1
            responses:
              200:
                description: 返回信息
                schema:
                    id: User
                    type: object
                examples:
                  success : {"error_code": 0,"msg": "ok","request": "GET /seven/v1/<id>"}
        """
    uid = g.user.uid
    user = User.query.filter_by(id=int(uid)).first_or_404()
    all_user = User.query.all()
    if user:
        return jsonify(all_user)
    return jsonify(user)


@api.route('/<int:uid>', methods=['DELETE'])
@auth.login_required
def super_delete_user(uid):
    """ 删除用户
            ---
            tags:
              - 超级管理员模块
            parameters:
              - name: id
                in: body
                type: int
                required: true
                example: 1
            responses:
              200:
                description: 返回信息
                examples:
                  success : {"error_code": 0,"msg": "ok","request": "DELETE /seven/v1/<id>"}
        """
    with db.auto_commit():
        user = User.query.filter_by(id=int(uid)).first_or_404()
        user.delete()
    return DeleteSuccess()


@api.route('/int:<uid>', methods=['POST'])
@auth.login_required
def super_edit_user(uid):
    with db.auto_commit():
        user = User.query.filter_by(id=int(uid)).first_or_404()
        """
        权限编辑添加写在这些接口中
        """
        pass


@api.route('/clear_myself', methods=['DELETE'])
@auth.login_required
def delete_user():
    """
    清空账号
        ---
        tags:
          - 用户模块
        parameters:
          - name: id
            in: body
            type: int
            required: true
            example: 1
        responses:
          200:
            description: 返回信息
            examples:
              success : {"error_code": 0,"msg": "ok","request": "DELETE /seven/v1/clear_myself"}
    """
    uid = g.user.uid
    with db.auto_commit():
        user = User.query.filter_by(id=int(uid)).first_or_404()
        user.delete()
        return DeleteSuccess()


@api.route('/get_myself', methods=['GET'])
@auth.login_required
def get_user():
    """
    查看自己的资料
    :return:
    """
    uid = g.user.uid
    user = User.query.filter_by(id=int(uid)).first_or_404()
    role = get_scope(uid)
    try:
        auths = {
            'user': user,
            'role': role
        }
        return jsonify(auths)
    except AttributeError:
        return jsonify(user)


@api.route('/change/password', methods=['POST'])
@auth.login_required
def change_password():
    """
    修改密码
        ---
        tags:
          - 用户模块
        parameters:
          - name: id
            in: body
            type: int
            required: true
            example: 1
        responses:
          200:
            description: 返回信息
            examples:
              success : {"error_code": 0,"msg": "ok","request": "POST /seven/v1/change/password"}
    """
    form = ChangePasswordForm().validate_for_api()
    ok = User.change_password(form.old_password.data, form.new_password.data)
    if ok:
        return Success(message="密码修改成功!")
    else:
        return Failed(message="密码修改失败!")


@api.route('/<int:id>', methods=['POST'])
@auth.login_required
def user_type(id):
    """
    用户类型
    企业用户 普通用户..
    """
    form = UserTypeForm().validate_for_api()
    with db.auto_commit():
        data = User.query.filter_by(id=id).first()
        data.role_id = form.role.data
        db.session.add(data)
    return Success(message="用户类型修改成功！")


@api.route('/get_code', methods=['GET'])
def get_code():
    code = verify_code()
    return code


@api.route('/phone_code', methods=['POST'])
@auth.login_required
def get_phone_code():
    from app.libs.sms import send_sms
    params = {'number': 1024}
    form = PhoneCodeForm().validate_for_api()
    phone = form.phone.data
    send_sms(phone, params)
    return Success(message="短信已发送！")


@api.route('/forget/password', methods=['POST'])
def forget_password_request():
    """ 密码重置请求
        发送注册邮箱
        ---
        parameters:
          - name: email
            in: body
            type: string
            required: true
            example: 123456@qq.com
        responses:
          200:
            description: 返回
            examples:
              success: {"error_code": 0,"msg": "请前往邮箱重置你的密码","request": "POST /persona/v1/user/reset/password"}
    """
    form = EmailForm().validate_for_api()
    reset_email = form.email.data
    user = User.query.filter_by(email=reset_email).first_or_404()
    from app.libs.email import send_reset_password_email
    send_reset_password_email(email_address=form.email.data, email_title='[重置密码]',
                              user_name=user.nickname,
                              token=user.generate_token(),
                              template='email/reset_password.html')
    return Success(message="请前往邮箱重置你的密码")


@api.route('/reset/password/<token>', methods=['POST'])
def forget_password(token):
    """ 密码重置
        接受密码重置
        ---
        parameters:
          - name: token
            in: path
            type: string
            required: true
            example: nkkhknkajkhsdljiodaojaiojdoi
          - name: new_password
            type: string
            required: true
            example: 147258
          - name: confirm_password
            type: string
            required: true
            example: 147258
        responses:
          200:
            description: 个人信息
            examples:
              user: {'red', 'green', 'blue'}
    """
    form = ResetPasswordForm().validate_for_api()
    ok = User.reset_password(token, form.new_password.data)
    if ok:
        return Success(message='密码重置成功')
    else:
        return Failed(message="密码重置失败，请输入正确密码")


@api.route('/email_code', methods=['POST'])
def send_email():
    from app.libs.email import send_code_email
    form = EmailForm().validate_for_api()
    try:
        send_code_email(email_address=form.email.data,
                        email_title="[激活账户]",
                        template="email/code.html",
                        user_name="seven",
                        code="1024")

        return Success(message="邮件发送成功！")
    except Exception as e:
        return e
