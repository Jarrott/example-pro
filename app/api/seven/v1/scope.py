# -*- encoding:utf-8 -*-
"""
@ Created by Seven on  2018/08/05 
"""
from flask import jsonify

from app.libs.scope import *
from app.libs.data_scope import *
from app.libs.model_base import db
from app.libs.token_auth import auth
from app.libs.redprint import Redprint
from app.libs.error_code import Success
from app.validators.forms import RoleForm, RoleGroupForm
from app.api.seven.models.user import User, AdminAuth, Role

api = Redprint('scope')


@api.route('', methods=['GET'])
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
    auth_name = [v.auth_name for v in auth_list for val in auths if val == v.id]
    append_scope = {
        777: add_admin_scope(AdminScope),
        755: add_company_scope(CompanyScope),
        707: add_merchants_cope(MerchantsScope),
        706: add_property_scope(PropertyScope),
        705: add_literacy_scope(LiteracyScope),
        100: add_user_scope(UserScope)
    }
    key = data.auth
    scope = append_scope.get(key, None)
    urls = [v.url for v in auth_list for val in auths if val == v.id if v.url not in scope.allow_api]
    for num in range(len(urls)):
        scope.allow_api.append(urls[num])
    return jsonify({
        'rule': data.role_id,
        'auth_name': auth_name
    })


@api.route('', methods=['POST'])
@auth.login_required
def role_add():
    """
    添加角色
    """
    form = RoleForm().validate_for_api()
    with db.auto_commit():
        data = Role()
        data.name = form.name.data
        data.auths = form.auths.data
        db.session.add(data)
    return Success(message="角色添加成功！")


@api.route('/<int:id>', methods=['POST'])
@auth.login_required
def update_role(id):
    """
    用户关联用户组
    """
    form = RoleGroupForm().validate_for_api()
    with db.auto_commit():
        data = User.query.filter_by(id=id).first()
        data.role_id = form.role.data
        db.session.add(data)
    return Success(message="用户组修改成功！")


@api.route('/list', methods=['GET'])
@auth.login_required
def auth_list():
    """
    权限列表
    """
    data = AdminAuth.query.all()
    _list = {
        'auth_list': data
    }
    return jsonify(_list)
