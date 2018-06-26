# -*- encoding:utf-8 -*-
"""
@ Created by Seven on  2018/06/20 
"""
from flask import g
from werkzeug.security import generate_password_hash, check_password_hash

from app.libs.error_code import NotFound, AuthFailed
from app.libs.model_base import (db, Base,
                                 MixinModelJSONSerializer)


class User(Base, MixinModelJSONSerializer):
    id = db.Column(db.Integer, primary_key=True, doc="用户自增ID")
    username = db.Column(db.String(24), unique=True, nullable=True, doc="用户名")
    nickname = db.Column(db.String(24), unique=True, nullable=False, doc="用户昵称")
    auth = db.Column(db.SmallInteger, default=1)
    _password = db.Column('password', db.String(100), nullable=True, doc="用户密码")

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
            raise NotFound(message="用户没有找到 ~ !")
        if not user.check_password(password):
            raise AuthFailed()
        scope = 'AdminScope' if user.auth == 777 else 'UserScope'
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
