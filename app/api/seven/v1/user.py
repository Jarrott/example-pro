# -*- encoding:utf-8 -*-
"""
@ Created by Seven on  2018/06/20 
"""
from flask import jsonify, g

from app.api.seven.models import User, db
from app.libs.error_code import DeleteSuccess, Success, Failed
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.validators.forms import ChangePasswordForm

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
                examples:
                  success : {"error_code": 0,"msg": "ok","request": "GET /seven/v1/<id>","data":"$user"}
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
                  success : {"error_code": 0,"msg": "ok","request": "DELETE /seven/v1/<id>","data":"$user"}
        """
    with db.auto_commit():
        user = User.query.filter_by(id=int(uid)).first_or_404()
        user.delete()
    return DeleteSuccess()


@api.route('/clear_myself', methods=['DELETE'])
@auth.login_required
def delete_user():
    """
    用户清除自己的账号
    :return:
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
    :return:
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
