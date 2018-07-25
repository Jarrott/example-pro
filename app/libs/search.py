# -*- encoding:utf-8 -*-
"""
@ Created by Seven on  2018/06/23 
"""
from flask import jsonify, json, current_app
from sqlalchemy import and_

from app.libs.error_code import NotFound
from app.libs.helper import get_timestamp
from app.validators.forms import SearchForm


def api_paging(request, model):
    """请求格式：
    http://77.art:5000/seven/v1/park/search?page_num=xxx&page_size=xxx&sort=[{"field":"id","asc":"false"}]
    """
    form = SearchForm().validate_for_api()
    try:
        page_num = form.page_num.data
        page_size = form.page_size.data or current_app.config['PER_PAGE']
        q = form.q.data
        start = get_timestamp(form.start_time.data) if form.start_time.data is not "" else None
        end = get_timestamp(form.end_time.data) if form.end_time.data is not "" else None
        s_data = q if q is not None else ''
        _time = all([start, end])
        _data = all([s_data])
        data = model.query.filter_by()
        if not _time and _data:
            data = data.filter(model.title.contains(s_data))
        elif not _data and _time:
            data = data.filter(model.create_time.between(start, end))
        elif not _data and not _time:
            pass
        else:
            data = data.filter(and_(model.title.contains(s_data), model.create_time.between(start, end)))
        pagination = data.order_by(build_sort(model, form)).paginate(
            page=int(page_num), per_page=int(page_size)).items

        new_list = {
            'error_code': 0,
            'data': pagination
        }
        return jsonify(new_list)

    except ValueError:
        return NotFound(message="检索错误")


def build_sort(model, form):
    """
    排序方法
    &sort=[{"field":"id","asc":"false"}]
    或者放在请求体中
    "sort":[{"field":"id","asc":"false"}]
    """

    sort_list = ""
    sort = form.sort.data
    sorts = json.loads(form.sort.data) if "[" in form.sort.data else sort
    if sorts:
        for sort in sorts:
            field = sort["field"]
            asc = sort["asc"]
            if asc == "false" and field == "time":
                sort_list = model.create_time.desc()
            elif asc == "false" and field == "id":
                sort_list = model.id.desc()
            else:
                sort_list = model.id.asc()
    return sort_list

    #
    # if request.args.get('sort', ''):
    #     sorts = json.loads(request.args.get('sort'))
    #     for sort in sorts:
    #         field = sort["field"]
    #         asc = sort["asc"]
    #         if asc == "false" and field == "time":
    #             sort_list = model.create_time.desc()
    #         elif asc == "false" and field == "id":
    #             sort_list = model.id.desc()
    #         else:
    #             sort_list = model.id.asc()
    # return sort_list
