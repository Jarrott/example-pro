# -*- encoding:utf-8 -*-
"""
@ Created by Seven on  2018/08/15 
"""
from flask import Blueprint
from app.web import index


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
