# -*- encoding:utf-8 -*-
"""
@ Created by Seven on  2018/06/20 
"""
from flask import jsonify, g

from app.api.v1.models import User, db
from app.libs.error_code import DeleteSuccess
from app.libs.redprint import Redprint
from app.libs.token_auth import auth

api = Redprint('user')


@api.route('/<int:uid>', methods=['GET'])
@auth.login_required
def super_get_user(uid):
    """
    重写了sqlalchemy中的get_or_404
    出错可以返回想要的报错信息
    filter_by 过滤了软删除的用户
    所以filter_by 也是必不可少的
    """
    user = User.query.filter_by(id=int(uid)).first_or_404()
    return jsonify(user)


@api.route('/<int:uid>', methods=['DELETE'])
@auth.login_required
def super_delete_user(uid):
    """
    删除用户
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
