# -*- encoding:utf-8 -*-
"""
@ Created by Seven on  2018/08/22 
"""
from wtforms import (StringField,
                     PasswordField, IntegerField,
                     SelectField, TextAreaField)
from wtforms.validators import (DataRequired, Length,
                                Email)

from app.api.seven.models import db
from app.api.seven.models.user import CompanyDetail, Job
from app.libs.form_base import BaseForm


class CompanyProfileForm(BaseForm):
    name = StringField(validators=[DataRequired(message="企业名称不能为空！")])
    email = StringField(validators=[DataRequired(message="邮箱不能为空！"), Email()])
    phone = StringField(validators=[DataRequired(message="手机不能为空！")])
    slug = StringField(validators=[DataRequired(), Length(3, 24)])
    location = StringField(validators=[DataRequired(message="公司地址不能为空！"), Length(0, 64)])
    site = StringField(validators=[DataRequired(message="公司网站不能为空！"), Length(0, 64)])
    logo = StringField(validators=[DataRequired(message="网站LOGO不能为空！")])
    # 公司名称
    description = StringField(validators=[Length(0, 100)])
    # 公司详情
    about = TextAreaField(validators=[Length(0, 1024)])


class CompanyEditForm(BaseForm):
    name = StringField('企业名称')
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码')
    phone = StringField('手机号')
    site = StringField('公司网站', validators=[Length(0, 64)])
    description = StringField('一句话简介', validators=[Length(0, 100)])

    def update(self, company):
        company.name = self.name.data
        company.email = self.email.data
        if self.password.data:
            company.password = self.password.data
        if company.detail:
            detail = company.detail
        else:
            detail = CompanyDetail()
            detail.user_id = company.id
        detail.site = self.site.data
        detail.description = self.description.data
        db.session.add(company)
        db.session.add(detail)
        db.session.commit()


class JobForm(BaseForm):
    name = StringField('职位名称')
    salary_low = IntegerField('最低薪酬')
    salary_high = IntegerField('最高薪酬')
    location = StringField('工作地点')
    tags = StringField('职位标签（多个用,隔开）')
    experience_requirement = SelectField(
        '经验要求(年)',
        choices=[
            ('不限', '不限'),
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('1-3', '1-3'),
            ('3-5', '3-5'),
            ('5+', '5+')
        ]
    )
    degree_requirement = SelectField(
        '学历要求',
        choices=[
            ('不限', '不限'),
            ('专科', '专科'),
            ('本科', '本科'),
            ('硕士', '硕士'),
            ('博士', '博士')
        ]
    )
    description = TextAreaField('职位描述', validators=[Length(0, 1500)])

    def create_job(self, company):
        job = Job()
        self.populate_obj(job)
        job.company_id = company.id
        db.session.add(job)
        db.session.commit()
        return job

    def update_job(self, job):
        self.populate_obj(job)
        db.session.add(job)
        db.session.commit()
        return job
