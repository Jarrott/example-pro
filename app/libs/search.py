# -*- encoding:utf-8 -*-
"""
@ Created by Seven on  2018/06/23 
"""
from flask import jsonify
from sqlalchemy import or_

from app.libs.helper import get_timestamp
from app.validators.forms import SearchForm


def search(model, view_model):
    form = SearchForm().validate_for_api()
    q = form.q.data
    __start = get_timestamp(form.start_time.data) if form.start_time.data is not "" else None
    __end = get_timestamp(form.end_time.data if form.end_time.data is not "" else None)
    s_data = '%' + q + '%' if q is not None else ''
    data = model.query.filter(
        or_(model.create_time.between(__start, __end), model.title.like(s_data))).all()

    data = view_model(data)
    new_list = {
        'error_code': 0,
        'list': data.data
    }
    return jsonify(new_list)
