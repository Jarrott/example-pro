# -*- encoding:utf-8 -*-
"""
@ Created by Seven on  2018/06/26 
"""

from app.libs.error_code import Success
from app.libs.model_base import db
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.validators.forms import (ParkPushForm, ParkBreakingForm,
                                  ParkNoticesForm, ParkNewsForm)
from app.api.seven.models import (ParkPush, ParkBreaking,
                                  ParkNews)

api = Redprint('park')


@api.route('', methods=['POST'])
@auth.login_required
def push_demand():
    """ 发布需求
            发送json数据进行注册(注册为开发者的type为300)
            ---
            tags:
              - 公园综合管理
            parameters:
              - name: username
                in: body
                type: string
                required: true
                example: simple
              - name: password
                in: body
                type: string
                required: true
                example: 123456
              - name: type
                in: body
                type: int
                required: true
                example: 100
            responses:
              200:
                description: 返回信息
                examples:
                  success : {"error_code": 0,"msg": "ok","request": "POST /seven/v1/park"}
        """
    form = ParkPushForm().validate_for_api()
    with db.auto_commit():
        data = ParkPush()
        data.content = form.content.data
        data.company = form.company.data
        data.type = form.type.data
        db.session.add(data)
    return Success(message="需求发布成功！")


@api.route('/news', methods=['POST'])
@auth.login_required
def news():
    """ 新闻发布
            发送json数据进行注册(注册为开发者的type为300)
            ---
            tags:
              - 公园综合管理
            parameters:
              - name: title
                in: body
                type: string
                required: true
                example: simple
              - name: image
                in: body
                type: file
                required: true
              - name: content
                in: body
                type: string
                required: true
                example: 100
            responses:
              200:
                description: 返回信息
                examples:
                  success : {"error_code": 0,"msg": "ok","request": "POST /seven/v1/news"}
        """
    form = ParkNewsForm().validate_for_api()
    with db.auto_commit():
        data = ParkNews()
        data.title = form.title.data
        data.image = form.image.data
        data.content = form.content.data
        db.session.add(data)
    return Success(message="新闻发布成功!")


@api.route('/notices', methods=['POST'])
@auth.login_required
def notices():
    """ 园区&政府模块
            发送json数据进行注册(注册为开发者的type为300)
            ---
            tags:
              - 公园综合管理
            parameters:
              - name: username
                in: body
                type: string
                required: true
                example: simple
              - name: password
                in: body
                type: string
                required: true
                example: 123456
              - name: type
                in: body
                type: int
                required: true
                example: 100
            responses:
              200:
                description: 返回信息
                examples:
                  success : {"error_code": 0,"msg": "ok","request": "POST /seven/v1/notices"}
        """
    pass


@api.route('/policy', methods=['POST'])
@auth.login_required
def policy():
    """ 园区政策
            发送json数据进行注册(注册为开发者的type为300)
            ---
            tags:
              - 公园综合管理
            parameters:
              - name: username
                in: body
                type: string
                required: true
                example: simple
              - name: password
                in: body
                type: string
                required: true
                example: 123456
              - name: type
                in: body
                type: int
                required: true
                example: 100
            responses:
              200:
                description: 返回信息
                examples:
                  success : {"error_code": 0,"msg": "ok","request": "POST /seven/v1/policy"}
        """
    pass


@api.route('/breaking', methods=['POST'])
@auth.login_required
def breaking():
    """ 大事件
            发送json数据进行注册(注册为开发者的type为300)
            ---
            tags:
              - 公园综合管理
            parameters:
              - name: title
                in: body
                type: string
                required: true
                example: simple
              - name: note
                in: body
                type: int
                required: true
                example: 100
            responses:
              200:
                description: 返回信息
                examples:
                  success : {"error_code": 0,"msg": "ok","request": "POST /seven/v1/breaking"}
        """
    form = ParkBreakingForm().validate_for_api()
    with db.auto_commit():
        data = ParkBreaking()
        data.title = form.title.data
        data.note = form.remark.data
        db.session.add(data)
    return Success(message="事件保存成功！")
