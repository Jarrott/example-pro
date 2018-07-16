# -*- encoding:utf-8 -*-
"""
@ Created by Seven on  2018/06/23 
"""
import time

from flask import jsonify

from app.validators.forms import SearchForm, PostSearchForm


def search(model, view_model):
    form = SearchForm().validate_for_api()
    q = form.q.data
    s_data = '%' + q + '%'
    data = model.query.filter(
        (model.title.like(s_data))).all()
    data = view_model(data)
    new_list = {
        'error_code': 0,
        'list': data.data
    }
    return jsonify(new_list)


def int_time(str_time):
    str_time = time.strptime(str_time, "%Y-%m-%d")
    time_stamp = int(time.mktime(str_time))
    return time_stamp


def date_search(model, view_model):
    """通过时间检索内容"""
    form = PostSearchForm().validate_for_api()
    __start = int_time(form.start_time.data)
    __end = int_time(form.end_time.data)
    park = model.query.filter(model.create_time.between(__start, __end)).all()
    park = view_model(park)
    new_list = {
        'error_code': 0,
        'list': park.data
    }
    return jsonify(new_list)

# __exact        精确等于 like 'aaa'
# __iexact       精确等于 忽略大小写 ilike 'aaa'
# __contains     包含  like '%aaa%'
# __icontains    包含  忽略大小写 ilike '%aaa%'，但是对于sqlite来说，contains的作用效果等同于icontains。
# __gt           大于
# __gte          大于等于
# __lt           小于
# __lte          小于等于
# __in           存在于一个list范围内
# __startswith   以...开头
# __istartswith  以...开头 忽略大小写
# __endswith     以...结尾
# __iendswith    以...结尾，忽略大小写
# __range        在...范围内
# __year         日期字段的年份
# __month        日期字段的月份
# __day          日期字段的日# __isnull       = True / False
