# -*- encoding:utf-8 -*-
"""
@ Created by Seven on  2018/06/26 
"""
from flask import jsonify
from sqlalchemy import desc

from app.libs.helper import encode_base64, decode_base64
from app.validators.park import *
from app.api.seven.models import *
from app.libs.token_auth import auth
from app.libs.redprint import Redprint
from app.libs.error_code import Success
from app.libs.search import api_paging
from app.api.seven.view_model.park import ParkCollection

__author__ = 'Little Seven'

api = Redprint('park')


@api.route('/search/sort', methods=['POST'])
@auth.login_required
def search_sort():
    """排序"""
    data = ParkNews.query.filter(ParkNews.deleted.notin_('1')).order_by('-id').all()
    return jsonify(data)


@api.route('/search/news', methods=['POST'])
@auth.login_required
def search_news():
    """新闻动态搜索"""
    data = api_paging(ParkNews)
    return data


@api.route('/search/news', methods=['POST'])
@auth.login_required
def search_date():
    """
        时间范围内搜搜
        这个方法存在的位置和路由定义都是不符合规范的
        比如创建一个search的宏图
        ！"有为"看到请修改！
            ---
            tags:
              - 用户模块
            parameters:
              - name: start_time
                in: body
                type: string
                required: true
                example: 2017-07-01
              - name: end_time
                in: body
                type: string
                required: true
                example: 2018-08-01
            responses:
              200:
                description: 返回信息
                examples:
                  success : {"error_code": 0,"msg": "ok","request": "POST /seven/v1/user/search/news"}
        """
    park = api_paging(ParkNews)
    return park


@api.route('', methods=['GET'])
@auth.login_required
def get_news():
    """新闻动态列表"""
    news_list = ParkNews.query.order_by(desc(ParkNews.id)).all()
    new_list = ParkCollection(news_list)
    return jsonify(new_list.data)


@api.route('<int:nid>', methods=['DELETE'])
@auth.login_required
def deleted_news(nid):
    """删除新闻动态"""
    ParkNews.query.filter_by(id=nid).delete()
    return Success(message="新闻的动态删除成功！")


@api.route('', methods=['POST'])
@auth.login_required
def push_demand():
    """ 发布需求
            ---
            tags:
              - 园区综合合管理-资讯管理
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
        form.populate_obj(data)  # 使用此语法可以简化以下写法
        # data.content = form.content.data
        # data.company = form.company.data
        # data.type = form.type.data
        db.session.add(data)
    return Success(message="需求发布成功！")


@api.route('/edit/<int:id>', methods=['POST'])
@auth.login_required
def push_edit(id=None):
    """ 编辑需求
            ---
            tags:
              - 园区综合合管理-资讯管理
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
    data = ParkPush.query.filter_by(id=id).first_or_404()
    form = ParkPushForm()
    form.validate_for_edit(form.company.data, data)
    with db.auto_commit():
        form.populate_obj(data)  # 使用此语法可以简化以下写法
        # data.content = form.content.data
        # data.company = form.company.data
        # data.type = form.type.data
        db.session.add(data)
    return Success(message="需求修改成功！")


@api.route('/news', methods=['POST'])
@auth.login_required
def news():
    """ 新闻动态
            ---
            tags:
              - 园区综合合管理-资讯管理
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
        form.populate_obj(data)  # 使用此语法可以简化以下写法
        # data.title = form.title.data
        # data.image = form.image.data
        # data.content = form.content.data
        db.session.add(data)
    return Success(message="新闻发布成功!")


@api.route('/notices', methods=['POST'])
@auth.login_required
def notices():
    """ 园区&政府模块
            ---
            tags:
              - 园区综合合管理-资讯管理
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
    form = ParkNoticesForm().validate_for_api()
    with db.auto_commit():
        data = ParkEduNotices()
        form.populate_obj(data)  # 使用此语法可以简化以下写法
        # data.title = form.title.data
        # data.image = form.image.data
        # data.type = form.type.data
        # data.content = form.content.data
        db.session.add(data)
    return Success(message="添加公告成功！")


@api.route('/policy', methods=['POST'])
@auth.login_required
def policy():
    """ 园区政策
            ---
            tags:
              - 园区综合合管理-资讯管理
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
    form = ParkPolicyForm().validate_for_api()
    with db.auto_commit():
        data = ParkPolicy()
        form.populate_obj(data)  # 使用此语法可以简化以下写法
        # data.title = form.title.data
        # data.type = form.type.data
        # data.image = form.image.data
        # data.file = form.file.data
        # data.content = form.content.data
        db.session.add(data)
    return Success(message="政策发布成功！")


@api.route('/breaking', methods=['POST'])
@auth.login_required
def breaking():
    """ 大事件
            ---
            tags:
              - 园区综合合管理-资讯管理
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
        form.populate_obj(data)  # 使用此语法可以简化以下写法
        # data.title = form.title.data
        # data.note = form.remark.data
        db.session.add(data)
    return Success(message="事件保存成功！")


@api.route('/circum', methods=['POST'])
@auth.login_required
def circum():
    """周边园区
            ---
            tags:
              - 园区综合合管理-资讯管理
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
                  success : {"error_code": 0,"msg": "ok","request": "POST /seven/v1/circum"}
    """
    form = ParkCircumForm().validate_for_api()
    with db.auto_commit():
        data = ParkCircum()
        form.populate_obj(data)  # 使用此语法可以简化以下写法
        # data.title = form.title.data
        # data.image = form.image.data
        # data.city = form.city.data
        # data.url = form.url.data
        # data.mobile = form.mobile.data
        # data.content = form.content.data
        db.session.add(data)
    return Success(message="周边园区文章发布成功！")


@api.route('/industry', methods=['POST'])
@auth.login_required
def industry():
    """ 行业资讯
            ---
            tags:
              - 园区综合合管理-资讯管理
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
                  success : {"error_code": 0,"msg": "ok","request": "POST /seven/v1/industry"}
    """
    form = ParkIndustryForm().validate_for_api()
    with db.auto_commit():
        data = ParkIndustry()
        form.populate_obj(data)  # 使用此语法可以简化以下写法
        # data.title = form.title.data
        # data.type = form.type.data
        # data.image = form.image.data
        # data.content = form.content.data
        db.session.add(data)
    return Success(message="行业资讯内容发布成功！")


@api.route('/merchant', methods=['POST'])
@auth.login_required
def merchant():
    """ 招商资讯
            ---
            tags:
              - 园区综合合管理-资讯管理
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
                  success : {"error_code": 0,"msg": "ok","request": "POST /seven/v1/emrchant"}
    """
    form = ParkMerchantForm().validate_for_api()
    with db.auto_commit():
        data = ParkMerchant()
        form.populate_obj(data)  # 使用此语法可以简化以下写法
        # data.title = form.title.data
        # data.content = form.content.data
        db.session.add(data)
    return Success(message="招商资讯发布成功！")


@api.route('/industry_show', methods=['POST'])
@auth.login_required
def industry_show():
    """行业资讯分类
            ---
            tags:
              - 园区综合合管理-资讯管理
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
                  success : {"error_code": 0,"msg": "ok","request": "POST /seven/v1/industry_show"}
    """
    form = ParkIndustryShowForm().validate_for_api()
    with db.auto_commit():
        data = ParkIndustryShow()
        form.populate_obj(data)  # 使用此语法可以简化以下写法
        # data.type = form.type.data
        # data.active = form.type.data
        db.session.add(data)
    return Success(message="行业资讯分类")


@api.route('/info', methods=['GET'])
@auth.login_required
def park_info():
    """城南新区信息
            ---
            tags:
              - 园区综合合管理-园区形象
            responses:
              200:
                description: 返回信息
                examples:
                  success : {"error_code": 0,"msg": "ok","request": "GET /seven/v1/park_info"}
    """
    pass


@api.route('/smalltown', methods=['GET'])
@auth.login_required
def smalltown():
    """数梦小镇
            ---
            tags:
              - 园区综合合管理-园区形象
            responses:
              200:
                description: 返回信息
                examples:
                  success : {"error_code": 0,"msg": "ok","request": "POST /seven/v1/smalltown"}
    """
    pass


@api.route('/industrial/show', methods=['POST'])
@auth.login_required
def industrialpark():
    """园区实景
            ---
            tags:
              - 园区综合合管理-园区形象
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
                  success : {"error_code": 0,"msg": "ok","request": "POST /seven/v1/industrial/show"}
    """
    form = ParkIndustrialParkForm().validate_for_api()
    with db.auto_commit():
        data = ParkIndustrialPark()
        form.populate_obj(data)  # 使用此语法可以简化以下写法
        # data.type = form.type.data
        # data.name = form.name.data
        # data.image = form.image.data
        db.session.add(data)
    return Success(message="信息修改成功！")


@api.route('/enterprise', methods=['POST'])
@auth.login_required
def enterprise():
    """企业风采
            ---
            tags:
              - 园区综合合管理-园区形象
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
                  success : {"error_code": 0,"msg": "ok","request": "POST /seven/v1/enterprise"}
    """
    form = ParkEnterpriseForm().validate_for_api()
    with db.auto_commit():
        data = ParkEnterprise()
        form.populate_obj(data)  # 使用此语法可以简化以下写法
        # data.name = form.name.data
        # data.image = form.image.data
        # data.content = form.content.data
        db.session.add(data)
    return Success(message="信息修改成功！")


@api.route('/personal', methods=['POST'])
@auth.login_required
def personal():
    """个人风采
            ---
            tags:
              - 园区综合合管理-园区形象
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
                  success : {"error_code": 0,"msg": "ok","request": "POST /seven/v1/personal"}
    """
    form = ParkPersonalForm().validate_for_api()
    with db.auto_commit():
        data = ParkPersonal()
        form.populate_obj(data)  # 使用此语法可以简化以下写法
        # data.nickname = form.name.data
        # data.company = form.company.data
        # data.job = form.job.data
        # data.image = form.image.data
        # data.content = form.content.data
        db.session.add(data)
    return Success(message="信息修改成功！")


@api.route('/point', methods=['POST'])
@auth.login_required
def point():
    """实现一些需要缓存实现的功能
    """
    from app.libs.auto_pro import add_data_cache, get_data_cache
    from app.validators.park import BigDataCacheForm
    form = BigDataCacheForm().validate_for_api()
    data = encode_base64({"title": form.title.data,
                          "content": form.content.data,
                          "type": form.type.data
                          })
    add_data_cache(form.start_time.data, form.end_time.data, data)
    get_data = decode_base64(get_data_cache(form.start_time.data))
    r_data = {
        'data': get_data
    }
    return jsonify(r_data)
