"""
 Created by 七月 on 2018/7/12.
"""
from flask import Blueprint
from app.web import index

__author__ = 'Little、seven'


def create_blueprint_web():
    bp_web = Blueprint('web', __name__, template_folder='templates',
                       static_folder='static')

    index.web.register(bp_web)
    return bp_web


def create_blueprint_www():
    bp_www = Blueprint('www', __name__, template_folder='templates',
                       static_folder='static')

    index.web.register(bp_www)
    return bp_www
