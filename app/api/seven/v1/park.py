# -*- encoding:utf-8 -*-
"""
@ Created by Seven on  2018/06/26 
"""
from app.api.seven.models import ParkPush, ParkBreaking
from app.libs.error_code import Success
from app.libs.model_base import db
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.validators.forms import (ParkPushForm, ParkBreakingForm)

api = Redprint('park')


@api.route('', methods=['POST'])
@auth.login_required
def push_demand():
    """
    需求推送
    发布需求
    :return:
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
    """
    新闻发布
    :return:
    """
    pass


@api.route('/notices', methods=['POST'])
@auth.login_required
def notices():
    """
    园区&政府公告
    :return:
    """
    pass


@api.route('/policy', methods=['POST'])
@auth.login_required
def policy():
    """
    园区政策
    :return:
    """
    pass


@api.route('/breaking', methods=['POST'])
@auth.login_required
def breaking():
    """
    大事件
    :return:
    """
    form = ParkBreakingForm().validate_for_api()
    with db.auto_commit():
        data = ParkBreaking()
        data.title = form.title.data
        data.note = form.remark.data
        db.session.add(data)
    return Success(message="事件保存成功！")
