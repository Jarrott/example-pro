# -*- encoding:utf-8 -*-
"""
@ Created by Seven on  2018/06/20 
"""
from flask import jsonify, g

from app.libs.token_auth import auth
from app.libs.redprint import Redprint
from app.api.seven.models import User, db
from app.validators.forms import ChangePasswordForm, UserTypeForm
from app.libs.error_code import (DeleteSuccess, Success, Failed)

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
