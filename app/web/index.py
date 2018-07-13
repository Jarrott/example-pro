# -*- encoding:utf-8 -*-
"""
@ Created by Seven on  2018/07/12
"""
from flask import request, app

from app.libs.redprint import Redprint
from flask_uploads import UploadSet, configure_uploads, IMAGES, \
    patch_request_class

__author__ = 'Little、seven'

web = Redprint('index', with_prefix=False)
