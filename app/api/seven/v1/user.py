# -*- encoding:utf-8 -*-
"""
@ Created by Seven on  2018/06/20 
"""
from flask import jsonify, g

from app.libs.scope import *
from app.libs.data_scope import *
from app.api.seven.models import User, db
from app.api.seven.models.user import Role, AdminAuth
from app.libs.error_code import (DeleteSuccess, Success, Failed)
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.validators.forms import ChangePasswordForm, RoleForm

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


@api.route('/flash/message', methods=['POST'])
@auth.login_required
def show_message():
    """
    消息提醒
    :return:
    """
    pass


@api.route('/role', methods=['POST'])
@auth.login_required
def role_add():
    """
    添加角色
    :return:
    """
    form = RoleForm().validate_for_api()
    with db.auto_commit():
        data = Role()
        data.name = form.name.data
        data.auths = form.auths.data
    return Success(message="角色添加成功！")


@api.route('/scope', methods=['GET'])
@auth.login_required
def get_scope():
    """
    将用户拥有的权限
    注入到scope中
    """
    data = User.query.join(
        Role
    ).filter(
        Role.id == User.role_id
    ).first()
    auths = data.role.auths
    auths = list(map(lambda v: int(v), auths.split(",")))
    auth_list = AdminAuth.query.all()
    urls = [v.url for v in auth_list for val in auths if val == v.id]
    auth_name = [v.auth_name for v in auth_list for val in auths if val == v.id]
    append_scope = {
        777: add_admin_scope(AdminScope),
        755: add_company_scope(CompanyScope),
        707: add_merchants_cope(MerchantsScope),
        706: add_property_scope(PropertyScope),
        705: add_literacy_scope(LiteracyScope),
        100: add_user_scope(UserScope)
    }
    scope = append_scope.get(data.auth, None)

    scope.allow_api.append(','.join(urls))

    return jsonify({
        'rule': data.role_id,
        'auth_name': auth_name
    })
