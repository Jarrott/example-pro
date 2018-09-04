# -*- encoding:utf-8 -*-
"""
@ Created by Seven on  2018/08/22 
"""
from wtforms import (StringField, SelectField,
                     TextAreaField, FileField)
from wtforms.validators import (DataRequired, Length, Email)

from app.libs.form_base import BaseForm


class ExperienceForm(BaseForm):
    """工作经历"""
    company = StringField(validators=[DataRequired(message="公司名称不能为空！")])
    begin_at = StringField(validators=[DataRequired(message="在职期间时间不能为空！")])
    end_at = StringField(validators=[DataRequired(message="在职期结束时间不能为空！")])
    role = StringField(validators=[DataRequired(message="在项目中充当的角色不能为空！")])
    technology = StringField(validators=[DataRequired(message="掌握的技能不能为空！")])
    description = TextAreaField(validators=[DataRequired(message="项目经历不能为空！"), Length(0, 1500)])


class EduExperienceForm(BaseForm):
    """教育经历"""
    degree_requirement = [
        ('大专以下', '大专以下'),
        ('专科', '专科'),
        ('本科', '本科'),
        ('硕士', '硕士'),
        ('硕士以上', '硕士以上')
    ]

    school = StringField(validators=[DataRequired(message="学校不能为空！")])
    specialty = StringField(validators=[DataRequired(message="所学专业！")])
    degree = SelectField(validators=[DataRequired(message="学位不能为空！")], choices=degree_requirement)
    end_time = StringField(validators=[DataRequired(message="毕业年份不能为空！")])


class ProjectExperienceForm(BaseForm):
    """期望工作"""
    choices = [
        ('面谈', '面谈'),
        ('1~2k', '1~2k'),
        ('2~3k', '2~3k'),
        ('3~4k', '3~4k'),
        ('4~5k', '4~5k')
    ]
    name = StringField(validators=[DataRequired(message="期望职位不能为空！")])
    city = StringField(validators=[DataRequired(message="期望城市不能为空！")])
    monthly_pay = StringField(validators=[DataRequired(message="期望月薪不能为空！")], choices=choices)
    description = TextAreaField(validators=[DataRequired(message="补充说明不能为空！"), Length(0, 1500)])


class UserProfileForm(BaseForm):
    """
    用户配置页
    author: little、seven
    """
    email = StringField(
        label='邮箱',
        validators=[
            DataRequired('邮箱不能为空!'),
            Length(1, 64),
            Email()
        ]
    )

    # job_experiences = SelectField(
    #     label="年限",
    #     validators=[
    #         DataRequired("工作年限!"),
    #     ],
    #     coerce=int,
    #     choices=[
    #         (1, "1年"),
    #         (2, "2年"),
    #         (3, "3年"),
    #         (4, "4年"),
    #         (5, "5年"),
    #
    #     ]
    # )

    # pay = [
    #     ('面谈', '面谈'),
    #     ('1~2k', '1~2k'),
    #     ('2~3k', '2~3k'),
    #     ('3~4k', '3~4k'),
    #     ('4~5k', '4~5k')
    # ]
    city = StringField(validators=[DataRequired(message="期望城市不能为空！")])
    # monthly_pay = StringField(validators=[DataRequired(message="期望月薪不能为空！")], choices=pay)
    description = TextAreaField(validators=[DataRequired(message="补充说明不能为空！"), Length(0, 1500)])

    # degree_requirement = [
    #     ('大专以下', '大专以下'),
    #     ('专科', '专科'),
    #     ('本科', '本科'),
    #     ('硕士', '硕士'),
    #     ('硕士以上', '硕士以上')
    # ]
    #
    school = StringField(validators=[DataRequired(message="学校不能为空！")])
    specialty = StringField(validators=[DataRequired(message="所学专业！")])
    # degree = SelectField(validators=[DataRequired(message="学位不能为空！")], choices=degree_requirement)
    end_time = StringField(validators=[DataRequired(message="毕业年份不能为空！")])


class JobExperienceForm(BaseForm):
    company = StringField(validators=[DataRequired(message="1")])
    city = StringField(validators=[DataRequired()])
    begin_at = StringField(validators=[DataRequired()])
    end_at = StringField(validators=[DataRequired()])
    description = StringField(validators=[DataRequired()])

