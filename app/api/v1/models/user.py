# -*- encoding:utf-8 -*-
"""
@ Created by Seven on  2018/06/20 
"""
from werkzeug.security import generate_password_hash, check_password_hash
from app.libs.model_base import db, Base


class User(Base):
    id = db.Column(db.Integer, primary_key=True, doc="用户自增ID")
    username = db.Column(db.String(24), unique=True, nullable=True, doc="用户名")
    _password = db.Column('password', db.String(100), nullable=True, doc="用户密码")

    def __repr__(self):
        return '<Admin:{}>'.format(self.username)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, orig_password):
        self._password = generate_password_hash(orig_password)

    def check_password(self, password):
        return check_password_hash(self._password, password)

    @staticmethod
    def register_by_username(username, password):
        with db.auto_commit():
            user = User()
            user.username = username
            user.password = password
            db.session.add(user)
