# -*- encoding:utf-8 -*-
"""
@ Created by Seven on  2018/07/26 
"""
from flask import current_app
from redis import StrictRedis
from redis import ConnectionPool

from app.libs.error_code import NotFound


class Reids:
    def __init__(self):
        self.cli = None

    def connect(self):
        pool = ConnectionPool(
            host=current_app.config['REDIS_HOST'],
            port=current_app.config['REDIS_PORT'],
            db=current_app.config['REDIS_DB'],
            password=current_app.config['REDIS_PASSWORD']
        )
        return StrictRedis(connection_pool=pool)

    def get_uid_by_key(self, key):
        try:
            ruid = int(self.connection.hget(key, 'uid').decode('ascii'))
        except Exception:
            raise NotFound()
        return ruid

    @property
    def connection(self):
        if self.cli:
            return self.cli
        else:
            self.cli = self.connect()
            return self.cli


redis = Reids()
