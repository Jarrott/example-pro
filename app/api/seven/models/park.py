# -*- encoding:utf-8 -*-
"""
@ Created by Seven on  2018/06/26 
@ 园区综合管理
"""
from flask import url_for

from app.libs.model_base import (db, Base,
                                 MixinModelJSONSerializer)

__all__ = ['ParkPush', 'ParkBreaking',
           'ParkNews', 'ParkEduNotices',
           'ParkPolicy', 'ParkCircum',
           'ParkIndustry', 'ParkMerchant', 'ParkIndustryShow',
           'ParkIndustrialPark', 'ParkEnterprise', 'ParkPersonal']


class ParkPush(Base, MixinModelJSONSerializer):
    """
    需求推送
    """
    __tablename__ = 'park_push'
    id = db.Column(db.Integer, primary_key=True, doc="需求推送自增ID")
    company = db.Column(db.String(20))
    type = db.Column(db.SmallInteger)
    content = db.Column(db.Text)


class ParkNews(Base, MixinModelJSONSerializer):
    """
    新闻动态
    """
    __tablename__ = 'park_news'
    id = db.Column(db.Integer, primary_key=True, doc="新闻动态自增ID")
    title = db.Column(db.String(20))
    _image = db.Column('image', db.String(32))
    content = db.Column(db.Text)

    @property
    def image(self):
        return url_for('/', filename=self.image)

    @image.setter
    def image(self, filename):
        self._image = filename


class ParkEduNotices(Base, MixinModelJSONSerializer):
    """
    园区&政府动态
    """
    __tablename__ = 'park_notices'
    id = db.Column(db.Integer, primary_key=True, doc="园区动态自增ID")
    title = db.Column(db.String(20))
    _image = db.Column('image', db.String(32))
    type = db.Column(db.String(20))
    content = db.Column(db.Text)

    @property
    def image(self):
        return url_for('/', filename=self._image)

    @image.setter
    def image(self, filename):
        self._image = filename


class ParkPolicy(Base, MixinModelJSONSerializer):
    """
    园区政策
    """
    __tablename__ = 'park_policy'
    id = db.Column(db.Integer, primary_key=True, doc="政策动态自增ID")
    title = db.Column(db.String(20))
    _image = db.Column('image', db.String(32))
    _file = db.Column('file', db.String(32))
    type = db.Column(db.String(20))
    content = db.Column(db.Text)

    @property
    def image(self):
        """
        处理图片
        :return:
        """
        return url_for('/', filename=self._image)

    @image.setter
    def image(self, filename):
        self._image = filename

    @property
    def file(self):
        """
        处理文件
        :return:
        """
        return url_for('/', filename=self._file)

    @file.setter
    def file(self, filename):
        self._file = filename


class ParkBreaking(Base, MixinModelJSONSerializer):
    """
    大事件
    """
    __tablename__ = 'park_breaking'
    id = db.Column(db.Integer, primary_key=True, doc="大事件自增ID")
    title = db.Column(db.String(20))
    note = db.Column(db.Text)


class ParkCircum(Base, MixinModelJSONSerializer):
    """
    周边园区
    """
    __tablename__ = 'park_circum'
    id = db.Column(db.Integer, primary_key=True, doc="周边自增ID")
    title = db.Column(db.String(20))
    _image = db.Column(db.String(20))
    city = db.Column(db.String(20))
    url = db.Column(db.String(20))
    mobile = db.Column(db.String(20))
    content = db.Column(db.Text)

    @property
    def image(self):
        return url_for('/', filename=self.image)

    @image.setter
    def image(self, filename):
        self._image = filename


class ParkIndustry(Base, MixinModelJSONSerializer):
    """
    行业资讯
    """
    __tablename__ = 'park_industry'
    id = db.Column(db.Integer, primary_key=True, doc="行业资讯自增ID")
    title = db.Column(db.String(20))
    type = db.Column(db.String(20))
    _image = db.Column(db.String(20))
    content = db.Column(db.String(20))
    remark = db.Column(db.String(20))

    @property
    def image(self):
        return url_for('/', filename=self.image)

    @image.setter
    def image(self, filename):
        self._image = filename


class ParkMerchant(Base, MixinModelJSONSerializer):
    """
    招商资讯
    """
    __tablename__ = 'park_merchant'
    id = db.Column(db.Integer, primary_key=True, doc="招商资讯自增ID")
    title = db.Column(db.String(20))
    content = db.Column(db.String(20))


class ParkIndustryShow(Base, MixinModelJSONSerializer):
    """
    资讯分类
    """
    __tablename__ = 'park_ind_show'
    id = db.Column(db.Integer, primary_key=True, doc="资讯分类自增ID")
    type = db.Column(db.String(20))
    active = db.Column(db.SmallInteger, default=0)


"↓ 园区形象 ↓"


class ParkInfo(Base, MixinModelJSONSerializer):
    """城南新区信息"""
    __tablename__ = 'park_info'
    id = db.Column(db.Integer, primary_key=True, doc="资讯分类自增ID")
    name = db.Column(db.String(20), unique=True, nullable=False)
    url = db.Column(db.String(20))
    dec = db.Column(db.Text)


class ParkSmallTown(Base, MixinModelJSONSerializer):
    """数梦小镇"""
    __tablename__ = 'park_smalltown'
    id = db.Column(db.Integer, primary_key=True, doc="行业资讯自增ID")
    name = db.Column(db.String(20), unique=True, nullable=False)
    _image = db.Column(db.String(20))
    dec = db.Column(db.Text)
    content = db.Column(db.Text)

    @property
    def image(self):
        return url_for('/', filename=self.image)

    @image.setter
    def image(self, filename):
        self._image = filename


class ParkIndustrialPark(Base, MixinModelJSONSerializer):
    """园区实景"""
    __tablename__ = 'park_indupark'
    id = db.Column(db.Integer, primary_key=True, doc="行业资讯自增ID")
    type = db.Column(db.SmallInteger)
    name = db.Column(db.String(20), unique=True, nullable=False)
    _image = db.Column(db.String(20))

    @property
    def image(self):
        return url_for('/', filename=self.image)

    @image.setter
    def image(self, filename):
        self._image = filename


class ParkEnterprise(Base, MixinModelJSONSerializer):
    """企业风采"""
    __tablename__ = 'park_enterprise'
    id = db.Column(db.Integer, primary_key=True, doc="行业资讯自增ID")
    name = db.Column(db.String(20))
    _image = db.Column(db.String(20))
    content = db.Column(db.Text)

    @property
    def image(self):
        return url_for('/', filename=self.image)

    @image.setter
    def image(self, filename):
        self._image = filename


class ParkPersonal(Base, MixinModelJSONSerializer):
    """个人风采"""
    __tablename__ = 'park_personal'
    id = db.Column(db.Integer, primary_key=True, doc="行业资讯自增ID")
    company = db.Column(db.String(20))
    job = db.Column(db.String(20))
    _image = db.Column(db.String(20))
    content = db.Column(db.Text)

    @property
    def image(self):
        return url_for('/', filename=self.image)

    @image.setter
    def image(self, filename):
        self._image = filename
