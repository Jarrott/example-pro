# -*- encoding:utf-8 -*-
"""
@ Created by Seven on  2018/06/20 
"""
from wtforms import (StringField,
                     PasswordField, IntegerField,
                     SelectField)
from wtforms.validators import (DataRequired, Length, regexp, ValidationError)

from app.api.seven.models import User
from app.libs.enums import ClientTypeEnum
from app.libs.form_base import BaseForm


class ClientForm(BaseForm):
    """
    验证用户的登录信息
    """
    username = StringField(validators=[
        DataRequired(message="用户名不能为空"),
        Length(6, 32, message="用户名必须在6~32位之间")
    ])

    password = PasswordField(validators=[
        DataRequired(message="密码不能为空"),
        regexp(r'^[A-Za-z0-9_*&$#@]{6,22}$', message='用户密码必须在6~22位之间')
    ])
    type = IntegerField(validators=[DataRequired(message="类型不能为空!")])

    def validate_type(self, value):
        try:
            client = ClientTypeEnum(value.data)
        except ValueError as e:
            raise e
        self.type.data = client


class UserForm(ClientForm):
    """
    验证注册
    """
    username = StringField(validators=[
        DataRequired(message="用户名不能为空"),
        Length(6, 32, message="用户名必须在6~32位之间")
    ])

    password = PasswordField(validators=[
        DataRequired(message="密码不能为空"),
        regexp(r'^[A-Za-z0-9_*&$#@]{6,22}$', message='用户密码必须在6~22位之间')
    ])

    nickname = StringField(
        validators=[
            DataRequired(message="用户昵称不能为空"),
            Length(6, 32, message="用户昵称必须在6~32位之间")
        ])

    def validate_username(self, value):
        """
        查询用户是否已经存在
        :param value:
        :return:
        """
        if User.query.filter_by(username=value.data).first():
            raise ValidationError('该用户已注册')

    def validate_nickname(self, value):
        """
        查询用户昵称是否已经存在
        :param value:
        :return:
        """
        if User.query.filter_by(nickname=value.data).first():
            raise ValidationError('该昵称已被占用')


class ChangePasswordForm(BaseForm):
    old_password = PasswordField('原密码', validators=[DataRequired(message="不能为空")])
    new_password = PasswordField('新密码', validators=[DataRequired(message="不能为空")])


class SearchForm(BaseForm):
    """搜索用到的关键字"""
    q = StringField(validators=DataRequired())


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
