# -*- encoding:utf-8 -*-
"""
@ Created by Seven on  2018/06/26 
@ 园区综合管理
"""
from app.libs.model_base import (db, Base,
                                 MixinModelJSONSerializer)


class ParkPush(Base, MixinModelJSONSerializer):
    """
    需求推送
    """
    __tablename__ = 'park_push'
    id = db.Column(db.Integer, primary_key=True, doc="需求推送自增ID")
    demand = db.Column(db.String(20))
    company = db.Column(db.String(20))
    content = db.Column(db.Text)


class ParkNews(Base, MixinModelJSONSerializer):
    """
    新闻动态
    """
    __tablename__ = 'park_news'
    id = db.Column(db.Integer, primary_key=True, doc="新闻动态自增ID")
    title = db.Column(db.String(20))
    image = db.Column(db.String(20))
    content = db.Column(db.Text)


class ParkEduNotices(Base, MixinModelJSONSerializer):
    """
    园区&政府动态
    """
    __tablename__ = 'park_notices'
    id = db.Column(db.Integer, primary_key=True, doc="园区动态自增ID")
    title = db.Column(db.String(20))
    image = db.Column(db.String(20))
    type = db.Column(db.String(20))
    content = db.Column(db.Text)


class ParkPolicy(Base, MixinModelJSONSerializer):
    """
    园区政策
    """
    __tablename__ = 'park_policy'
    id = db.Column(db.Integer, primary_key=True, doc="政策动态自增ID")
    title = db.Column(db.String(20))
    image = db.Column(db.String(20))
    file = db.Column(db.String(20))
    type = db.Column(db.String(20))
    content = db.Column(db.Text)


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
    image = db.Column(db.String(20))
    city = db.Column(db.String(20))
    url = db.Column(db.String(20))
    mobile = db.Column(db.String(20))
    content = db.Column(db.Text)


class ParkIndustry(Base, MixinModelJSONSerializer):
    """
    行业资讯
    """
    __tablename__ = 'park_industry'
    id = db.Column(db.Integer, primary_key=True, doc="行业资讯自增ID")
    title = db.Column(db.String(20))
    type = db.Column(db.String(20))
    content = db.Column(db.String(20))
    remark = db.Column(db.String(20))


class ParkMerchant(Base, MixinModelJSONSerializer):
    """
    招商资讯
    """
    __tablename__ = 'park_merchant'
    id = db.Column(db.Integer, primary_key=True, doc="招商资讯自增ID")
    company = db.Column(db.String(20))
    city = db.Column(db.String(20))
    content = db.Column(db.String(20))


class ParkIndustryShow(Base, MixinModelJSONSerializer):
    """
    资讯分类
    """
    __tablename__ = 'park_ind_show'
    id = db.Column(db.Integer, primary_key=True, doc="资讯分类自增ID")
    name = db.Column(db.String(20))
    active = db.Column(db.SmallInteger, default=0)
    image = db.Column(db.String(20))
