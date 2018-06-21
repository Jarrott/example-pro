# -*- encoding:utf-8 -*-
"""
@ Created by Seven on  2018/06/20 
"""
from datetime import datetime
from contextlib import contextmanager
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery


class SQLAlchemy(_SQLAlchemy):
    """
    简化每次提交数据需要commit的问题
    """

    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e


class Query(BaseQuery):

    def filter_by(self, **kwargs):
        """
        重写此方法，解决"软删除"能多次删除的问题
        :param kwargs:
        :return:
        """
        if 'deleted' not in kwargs.keys():
            kwargs['deleted'] = 0
        return super(Query, self).filter_by(**kwargs)

    def get_or_404(self, ident):
        """
        重写此方法，实现出错时可以抛出异常
        :param ident:
        :return:
        """
        rv = self.get(ident)
        if rv is None:
            pass
        return rv


db = SQLAlchemy(query_class=Query)


class Base(db.Model):
    __abstract__ = True
    deleted = db.Column(db.Integer, default=0, doc="软删除")
    create_time = db.Column(db.Integer)
    active = db.Column(db.Integer, default=0, doc="用户是否被禁用")

    def __init__(self):
        self.create_time = int(datetime.now().timestamp())

    def __getitem__(self, item):
        return getattr(self, item)

    @property
    def create_datetime(self):
        if self.create_time:
            return datetime.fromtimestamp(self.create_time)
        else:
            return None

    def set_attrs(self, attrs_dict):
        for key, value in attrs_dict.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)

    def delete(self):
        self.deleted = 1


def append(self, *keys):
    for key in keys:
        self.fields.append(key)
    return self
