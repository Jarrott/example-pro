# -*- encoding:utf-8 -*-
"""
@ Created by Seven on  2018/08/15 
"""
from flask import render_template

from app.libs.redprint import Redprint

web = Redprint('index', with_prefix=False)


@web.route('/', methods=['GET'])
def index():
    return render_template('index.html')
