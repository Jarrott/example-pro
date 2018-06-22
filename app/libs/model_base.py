# -*- encoding:utf-8 -*-
"""
@ Created by Seven on  2018/06/20 
"""
from datetime import datetime
from contextlib import contextmanager
from flask_sqlalchemy import (SQLAlchemy as _SQLAlchemy,
                              BaseQuery, orm, inspect)

from app.libs.error_code import NotFound


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
            raise NotFound()
        return rv

    def first_or_404(self):
        """
        重写此方法，实现出错时可以抛出异常
        :return:
        """
        rv = self.first()
        if not rv:
            raise NotFound()
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


class MixinModelJSONSerializer:
    """
    序列化模型
    """

    @orm.reconstructor
    def init_on_load(self):
        self._fields = []
        self._exclude = []

        self._set_fields()
        self.__prune_fields()

    def _set_fields(self):
        pass

    def __prune_fields(self):
        columns = inspect(self.__class__).columns
        if not self._fields:
            all_columns = set([column.name for column in columns])
            self._fields = list(all_columns - set(self._exclude))

    def hide(self, *args):
        for key in args:
            self._fields.remove(key)
        return self

    def keys(self):
        return self._fields

    def __getitem__(self, key):
        return getattr(self, key)


class MixinJSONSerializer:
    _fields = []
    _exclude = []

    def __init__(self):
        self._set_fields()
        self._prune_fields()

    def _set_fields(self):
        pass

    def _prune_fields(self):
        if not self._fields:
            self.__init_subclass__()
            all_columns = set(self.__dict__.keys())
            self._fields = list(all_columns - set(self._exclude))

    def hide(self, *args):
        for key in args:
            self._fields.remove(key)
        return self

    def keys(self):
        return self._fields

    def __getitem__(self, key):
        return getattr(self, key)
