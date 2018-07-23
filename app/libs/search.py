# -*- encoding:utf-8 -*-
"""
@ Created by Seven on  2018/06/23 
"""
from flask import jsonify
from sqlalchemy import and_, or_

from app.libs.helper import get_timestamp
from app.validators.forms import SearchForm


def search(model, view_model):
    form = SearchForm().validate_for_api()
    q = form.q.data
    s_data = '%' + q + '%' if q is not "" else None
    start = get_timestamp(form.start_time.data) if form.start_time.data is not "" else None
    end = get_timestamp(form.end_time.data if form.end_time.data is not "" else None)
    '如果为空 返回 "False" '
    _time = all([start, end])
    _data = all([s_data])
    _choose = ''
    if not _time and _data:
        _choose = 0
    elif not _data and _time:
        _choose = 1
    elif not _time and not _data:
        _choose = 2
    else:
        _choose = 3
    print(_choose)


def only_title(model, view_model, s_data):
    data = model.query.filter(model.title.like(s_data)).all()
    data = view_model(data)
    new_list = {
        'error_code': 0,
        'list': data.data
    }

    return jsonify(new_list)


def only_time(model, view_model, __start, __end):
    data = model.query.filter(model.create_time.between(__start, __end)).all()
    data = view_model(data)
    new_list = {
        'error_code': 0,
        'list': data.data

    }

    return jsonify(new_list)


def all_tag(model, view_model):
    form = SearchForm().validate_for_api()
    q = form.q.data
    s_data = '%' + q + '%' if q is not None else ''
    title = model.title.like(s_data) if q is not "" else None
    __start = get_timestamp(form.start_time.data) if form.start_time.data is not "" else None
    __end = get_timestamp(form.end_time.data if form.end_time.data is not "" else None)
    data = model.query.filter(and_
                              (model.create_time.between(__start, __end), model.title.like(title)).all())
    data = view_model(data)
    new_list = {
        'error_code': 0,
        'list': data.data

    }
    return jsonify(new_list)


def __search(model, view_model):
    form = SearchForm().validate_for_api()
    q = form.q.data
    s_data = '%' + q + '%'
    start = get_timestamp(form.start_time.data)
    end = get_timestamp(form.end_time.data)
    data = model.query.filter(or_(
        model.create_time.between(start, end), model.title.like(s_data)
    )).all()
    data = view_model(data)
    new_list = {
        'error_code': 0,
        'list': data.data

    }
    return jsonify(new_list)


def all_none(model, pagenum=1, pagesize=10, sort='-id'):
    data = model.query.filter(model.deleted == 0).order_by(sort).paginate(page=int(pagenum),
                                                                          per_page=int(pagesize)).items
    new_list = {
        'error_code': 0,
        'list': data,
        'counts': model.query.filter_by().count()
    }

    return jsonify(new_list)
