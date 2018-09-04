# -*- encoding:utf-8 -*-
"""
@ Created by Seven on  2018/08/06 
"""
from flask import jsonify

from app.api.seven.models.user import Delivery
from app.libs.error_code import DeleteSuccess, Success
from app.libs.token_auth import auth
from app.libs.redprint import Redprint

__author__ = 'Little Seven'

# 前台路由
api = Redprint('company')


@api.route('/')
@auth.login_required
def index():
    return jsonify({'a': 'a'})


@api.route('/add_resume', methods=['POST'])
@auth.login_required
def add_my_resume():
    pass


@api.route('/detail')
def detail():
    """
    企业详情
    """
    pass


@api.route('/profile', methods=['GET', 'POST'])
def profile():
    """更新企业信息
    """
    return Success(message="企业信息更新成功")


@api.route('/publish_job', methods=['GET', 'POST'])
def company_publish_job():
    """添加职位需求
    """
    return Success(message="职位添加成功")


@api.route('/edit_job', methods=['GET', 'POST'])
def company_edit_job():
    """更新职位需求
    """
    return Success(message="职位更新成功")


@api.route('/jobs/delete')
def company_delete_job():
    """删除职位需求
    """
    return DeleteSuccess(message="职位删除成功")


@api.route('/apply/reject')
def company_apply_reject():
    """拒绝简历
    """
    return Success(message="已拒绝该简历")


@api.route('/apply/accept')
def company_apply_accept():
    """通过简历
    """
    return Success(message="已经通过，可以安排面试了")


@api.route('/company/apply')
def company_apply(company_id):
    """用户投递反馈状态
    : STATUS_WAITING 等待企业确认
    : STATUS_ACCEPT 被接收，等待通知面试
    : STATUS_REJECT 被拒绝
    """
    status = '状态'
    q = Delivery.query.filter_by(company_id=company_id)
    if status == 'waiting':
        q = q.filter(Delivery.status == Delivery.STATUS_WAITING)
    elif status == 'accept':
        q = q.filter(Delivery.status == Delivery.STATUS_ACCEPT)
    elif status == 'reject':
        q = q.filter(Delivery.status == Delivery.STATUS_REJECT)
    pagination = q.order_by(Delivery.created_at.desc()).paginate()
    return jsonify({"1": pagination})
