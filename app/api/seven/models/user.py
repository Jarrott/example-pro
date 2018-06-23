# -*- encoding:utf-8 -*-
"""
@ Created by Seven on  2018/06/20 
"""
from app.libs.error_code import NotFound, AuthFailed
from app.libs.model_base import (db, Base, orm,
                                 MixinModelJSONSerializer)


class User(Base, MixinModelJSONSerializer):
    id = db.Column(db.Integer, primary_key=True, doc="用户自增ID")
    username = db.Column(db.String(24), unique=True, nullable=True, doc="用户名")
    nickname = db.Column(db.String(24), unique=True, nullable=False, doc="用户昵称")
    auth = db.Column(db.SmallInteger, default=1)
    _password = db.Column('password', db.String(100), nullable=True, doc="用户密码")

    # 特殊场景设置，有的地方如果不需要nickname 在视图逻辑层调用hide
    @orm.reconstructor
    def __init__(self):
        self.fields = ['id', 'username', 'nickname', 'auth']

    def _set_fields(self):
        """
        数据序列化要隐藏的字段
        :return:
        """
        self._exclude = ['password']

    @staticmethod
    def verify(username, password):
        user = User.query.filter_by(username=username).first_or_404()
        if not user:
            raise NotFound(message="用户没有找到 ~ !")
        if not user.check_password(password):
            raise AuthFailed()
        scope = 'AdminScope' if user.auth == 777 else 'UserScope'
        return {'uid': user.id, 'scope': scope}
