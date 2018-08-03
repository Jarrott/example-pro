# -*- encoding:utf-8 -*-
"""
@ Created by Seven on  2018/06/20 
"""
from flask import g
from werkzeug.security import generate_password_hash, check_password_hash

from app.libs.data_scope import (admin_scope, company_scope, user_scope,
                                 literacy_scope, property_scope, merchants_cope,
                                 get_defualt)
from app.libs.error_code import AuthFailed, UserNotExistException
from app.libs.model_base import (db, Base,
                                 MixinModelJSONSerializer)


class User(Base, MixinModelJSONSerializer):
    id = db.Column(db.Integer, primary_key=True, doc="用户自增ID")
    auth = db.Column(db.SmallInteger, default=100, doc="默认组")
    username = db.Column(db.String(24), unique=True, nullable=True, doc="用户名")
    nickname = db.Column(db.String(24), unique=True, nullable=False, doc="用户昵称")
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), doc="用户权限组")
    _image = db.Column('image', db.String(50))
    _password = db.Column('password', db.String(100), nullable=True, doc="用户密码")

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, filename):
        self._image = filename

    def _set_fields(self):
        """
        数据序列化要隐藏的字段
        :return:
        """
        self._exclude = ['password']

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    def check_password(self, raw):
        if not self._password:
            return False
        return check_password_hash(self._password, raw)

    @staticmethod
    def register_by_username(username, password, nickname):
        with db.auto_commit():
            user = User()
            user.nickname = nickname
            user.username = username
            user.password = password
            db.session.add(user)

    @staticmethod
    def verify(username, password):
        """
        验证用户的作用域
        :param username:
        :param password:
        :return:
        """
        user = User.query.filter_by(username=username).first_or_404()
        if not user:
            raise UserNotExistException(message="当前用户不存在 ~ !")
        if not user.check_password(password):
            raise AuthFailed()
        is_auth = {
            777: admin_scope,
            755: company_scope,
            707: merchants_cope,
            706: property_scope,
            705: literacy_scope,
            100: user_scope
        }
        scope = is_auth.get(user.auth, get_defualt)()
        return {'uid': user.id, 'scope': scope}

    @staticmethod
    def change_password(old_password, new_password):
        """
        修改密码
        :param old_password:
        :param new_password:
        :return:
        """
        uid = g.user.uid
        with db.auto_commit():
            user = User.query.get(uid)
            if not user:
                return False
            if user.check_password(old_password):
                user.password = new_password
                return True
            return False


class AdminAuth(Base, MixinModelJSONSerializer):
    """权限模快"""
    id = db.Column(db.Integer, primary_key=True)
    auth_name = db.Column(db.String(100), unique=True)
    url = db.Column(db.String(255), unique=True)


class Role(Base, MixinModelJSONSerializer):
    """角色模块"""
    id = db.Column(db.Integer, primary_key=True, doc="自增ID")
    name = db.Column(db.String(100), unique=True, doc="角色名")
    auths = db.Column(db.String(600), doc="权限列表")
    role = db.relationship("User", backref='role')
