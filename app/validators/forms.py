# -*- encoding:utf-8 -*-
"""
@ Created by Seven on  2018/06/20 
"""
from flask_wtf.file import FileAllowed
from wtforms import (StringField,
                     PasswordField, IntegerField,
                     FileField, SelectField)
from wtforms.validators import (DataRequired, Length,
                                ValidationError,
                                Regexp, EqualTo)

from app import files
from app.api.seven.models import User
from app.libs.auto_pro import get_data_cache
from app.libs.error_code import NotFound, ClientTypeError
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
        Regexp(r'^[A-Za-z0-9_*&$#@]{6,22}$', message='用户密码必须在6~22位之间')
    ])
    type = IntegerField(validators=[DataRequired(message="类型不能为空!")], default=100)

    code = StringField(validators=[DataRequired(message="请重新输入验证码!"), Length(4, 4)])

    def validate_type(self, value):
        try:
            client = ClientTypeEnum(value.data)
        except ValueError as e:
            raise e
        self.type.data = client

    def validate_code(self,value):
        uid = User.query.filter_by(username=self.username.data).first()
        s_code = value.data.lower()
        b_data = value.data.upper()
        if s_code in b_data:
            code = get_data_cache(s_code)
            if code is None:
                raise ClientTypeError(message="请重新输入验证码！")
            elif uid is None:
                raise NotFound(message="用户不存在！")
            self.code.data = code


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
        Regexp(r'^[A-Za-z0-9_*&$#@]{6,22}$', message='用户密码必须在6~22位之间')
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


# 重置密码校验
class ResetPasswordForm(BaseForm):
    new_password = PasswordField('新密码', validators=[
        DataRequired(message='新密码不可为空'),
        Regexp(r'^[A-Za-z0-9_*&$#@]{6,22}$', message='密码长度必须在6~22位之间，包含字符、数字和 _ '),
        EqualTo('confirm_password', message='两次输入的密码不一致，请输入相同的密码')])
    confirm_password = PasswordField('确认新密码', validators=[DataRequired(message='请确认密码')])


# 更改密码校验
class ChangePasswordForm(ResetPasswordForm):
    old_password = PasswordField('原密码', validators=[DataRequired(message='不可为空')])


class SearchForm(BaseForm):
    """搜索用到的关键字"""
    q = StringField()
    start_time = StringField()
    end_time = StringField()
    page_num = IntegerField(default=1)
    page_size = IntegerField()
    sort = StringField()


class UploadForm(BaseForm):
    """上传文件"""

    files = FileField(validators=[FileAllowed(files, message="文件格式不正确！"), DataRequired(message="文件不能为空！")])


class RoleForm(BaseForm):
    """添加角色"""
    name = StringField(validators=[DataRequired()])
    auths = StringField(validators=[DataRequired()])


class RoleGroupForm(BaseForm):
    """指定用户属于哪个用户组"""
    role = StringField(validators=[DataRequired(message="用户组不能为空")])


class UserTypeForm(BaseForm):
    """用户类型"""
    choices = [(775, '管理员'), (755, '企业用户'), (707, '招商管理用户'), (706, '物业用户')]
    type = SelectField(validators=[DataRequired(message="请选择用户类型")], choices=choices, coerce=int)
