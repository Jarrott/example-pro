# -*- encoding:utf-8 -*-
"""
@ Created by Seven on  2018/07/02 
"""
from wtforms import (StringField, IntegerField,
                     SelectField)
from wtforms.validators import (DataRequired, Length,
                                ValidationError)

from app.api.seven.models import ParkEduNotices
from app.libs.form_base import BaseForm

__all__ = ['ParkPushForm', 'ParkBreakingForm', 'ParkEnterpriseForm',
           'ParkNoticesForm', 'ParkNewsForm', 'ParkPersonalForm',
           'ParkPolicyForm', 'ParkCircumForm',
           'ParkIndustryForm', 'ParkMerchantForm',
           'ParkIndustryShowForm', 'ParkIndustrialParkForm']

"↓ 资讯管理 ↓"


class ParkPushForm(BaseForm):
    """需求推送"""
    choices = [(1, '资金'), (2, '人才'), (3, '物业'), (4, '政策'), (5, '其他')]
    type = SelectField('需求分类', validators=[DataRequired()], choices=choices, coerce=int)
    company = StringField('推送企业', validators=[DataRequired(message="企业名称不能为空！")])
    content = StringField('推送内容', validators=[DataRequired(message="推送内容不能为空！")])

    def validate_type(self, value):
        try:
            client = value.data
        except ValueError as e:
            raise e
        self.type.data = client


class ParkBreakingForm(BaseForm):
    """园区大事件"""
    title = StringField(validators=[DataRequired(message="标题不能为空！")])
    remark = StringField(validators=[DataRequired(message="备注不能为空！")])


class ParkNewsForm(BaseForm):
    """新闻动态"""
    choices = [(1, '园区公告'), (2, '政府公告')]
    title = StringField(validators=[DataRequired(message="标题不能为空！")])
    image = StringField(validators=[DataRequired(message="图片不能为空！")])
    content = StringField(validators=[DataRequired(message="公告内容不能为空！")])


class ParkNoticesForm(BaseForm):
    """园区&政府公告"""
    choices = [(1, '园区公告'), (2, '政府公告')]
    title = StringField(validators=[DataRequired(message="标题不能为空！")])
    image = StringField(validators=[DataRequired(message="图片不能为空！")])
    type = SelectField(validators=[DataRequired(message="公告类型不能为空！")], choices=choices, coerce=int)
    content = StringField(validators=[DataRequired(message="公告内容不能为空！")])

    def validate_title(self, value):
        if ParkEduNotices.query.filter_by(title=value.data).first():
            raise ValidationError("标题已存在！")


class ParkPolicyForm(BaseForm):
    """园区政策"""
    choices = [(1, '财政引导政策'), (2, '收优惠政策'), (3, '产业扶持政策税'),
               (4, '金融扶持政策'), (5, '人才激励政策'), (6, '知识产权政策')]
    title = StringField(validators=[DataRequired(message="政策名称不能为空！")])
    type = SelectField(validators=[DataRequired(message="公告类型不能为空！")], choices=choices)
    image = StringField(validators=[DataRequired(message="图片不能为空！")])
    file = StringField(validators=[DataRequired(message="文件不能为空！")])
    content = StringField(validators=[DataRequired(message="公告内容不能为空！")])


class ParkCircumForm(BaseForm):
    """园区周边"""
    title = StringField(validators=[DataRequired(message="标题不能为空！")])
    image = StringField(validators=[DataRequired(message="图片不能为空！")])
    city = StringField(validators=[DataRequired(message="周边地址不能为空！")])
    url = StringField(validators=[DataRequired(message="网址不能为空！"), Length(6, 12, message="电话号码为6-12位")])
    mobile = IntegerField(validators=[DataRequired(message="园区电话不能为空！")])
    content = StringField(validators=[DataRequired(message="公告内容不能为空！")])


class ParkIndustryForm(BaseForm):
    """
    行业资讯
    """
    choices = [(1, 'IT'), (2, 'IT2')]
    title = StringField(validators=[DataRequired(message="标题不能为空！")])
    type = SelectField(validators=[DataRequired(message="行业分类不能为空！")], choices=choices, coerce=int)
    image = StringField(validators=[DataRequired(message="图片不能为空！")])
    content = StringField(validators=[DataRequired(message="行业资讯内容不能为空！")])


class ParkMerchantForm(BaseForm):
    """
    招商资讯
    """
    title = StringField(validators=[DataRequired(message="标题不能为空！")])
    content = StringField(validators=[DataRequired(message="行业资讯内容不能为空！")])


class ParkIndustryShowForm(BaseForm):
    """
    资讯分类
    """
    choices = [(1, 'IT'), (2, 'IT2')]
    type = SelectField(validators=[DataRequired(message="行业分类不能为空！")], choices=choices, coerce=int)
    active = IntegerField(default=0)


"↓ 园区形象 ↓"


class ParkInfoForm(BaseForm):
    """城南新区信息"""
    pass


class ParkSmallTownForm(BaseForm):
    """数梦小镇"""
    pass


class ParkIndustrialParkForm(BaseForm):
    """园区实景"""
    choices = [(1, '科创大厦'), ('A', '展厅')]
    type = SelectField(validators=[DataRequired(message="行业分类不能为空！")], choices=choices, coerce=int)
    name = StringField(validators=[DataRequired(message="标题不能为空！")])
    image = StringField(validators=[DataRequired(message="请上传图片！")])


class ParkEnterpriseForm(BaseForm):
    """企业风采"""
    name = StringField(validators=[DataRequired(message="标题不能为空！")])
    image = StringField(validators=[DataRequired(message="请上传图片！")])
    content = StringField(validators=[DataRequired(message="企业简介不能为空！")])


class ParkPersonalForm(BaseForm):
    """个人风采"""
    name = StringField(validators=[DataRequired(message="标题不能为空！")])
    company = StringField(validators=[DataRequired(message="请输入所属企业！")])
    job = StringField(validators=[DataRequired(message="请输入工作职位！")])
    image = StringField(validators=[DataRequired(message="请上传图片！")])
    content = StringField(validators=[DataRequired(message="个人简介不能为空！")])


"↓ 园区生活 ↓"

"↓ 园区服务 ↓"
