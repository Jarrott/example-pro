# -*- encoding:utf-8 -*-
"""
@ Created by Seven on  2018/06/20 
"""
from flask import jsonify, g

from app import files
from app.api.seven.models import User, db
from app.libs.error_code import (DeleteSuccess, Success, Failed, ImagesError)
from app.libs.helper import change_filename
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.validators.forms import ChangePasswordForm, UploadForm

__author__ = 'Little Seven'

api = Redprint('user')


@api.route('/<int:uid>', methods=['GET'])
@auth.login_required
def super_get_user(uid):
    """ 查询用户
            重写了sqlalchemy中的get_or_404
            出错可以返回想要的报错信息
            filter_by 过滤了软删除的用户
            所以filter_by 也是必不可少的
            ---
            tags:
              - 超级管理员模块
            parameters:
              - name: id
                in: body
                type: int
                required: true
                example: 1
            responses:
              200:
                description: 返回信息
                schema:
                    id: User
                    type: object
                examples:
                  success : {"error_code": 0,"msg": "ok","request": "GET /seven/v1/<id>"}
        """
    user = User.query.filter_by(id=int(uid)).first_or_404()
    return jsonify(user)


@api.route('/<int:uid>', methods=['DELETE'])
@auth.login_required
def super_delete_user(uid):
    """ 删除用户
            ---
            tags:
              - 超级管理员模块
            parameters:
              - name: id
                in: body
                type: int
                required: true
                example: 1
            responses:
              200:
                description: 返回信息
                examples:
                  success : {"error_code": 0,"msg": "ok","request": "DELETE /seven/v1/<id>"}
        """
    with db.auto_commit():
        user = User.query.filter_by(id=int(uid)).first_or_404()
        user.delete()
    return DeleteSuccess()


@api.route('/int:<uid>', methods=['POST'])
@auth.login_required
def super_edit_user(uid):
    with db.auto_commit():
        user = User()
        pass


@api.route('/clear_myself', methods=['DELETE'])
@auth.login_required
def delete_user():
    """
    清空账号
        ---
        tags:
          - 用户模块
        parameters:
          - name: id
            in: body
            type: int
            required: true
            example: 1
        responses:
          200:
            description: 返回信息
            examples:
              success : {"error_code": 0,"msg": "ok","request": "DELETE /seven/v1/clear_myself"}
    """
    uid = g.user.uid
    with db.auto_commit():
        user = User.query.filter_by(id=int(uid)).first_or_404()
        user.delete()
        return DeleteSuccess()


@api.route('/get_myself', methods=['GET'])
@auth.login_required
def get_user():
    """
    查看自己的资料
    :return:
    """
    uid = g.user.uid
    user = User.query.filter_by(id=int(uid)).first_or_404()
    return jsonify(user)


@api.route('/change/password', methods=['POST'])
@auth.login_required
def change_password():
    """
    修改密码
        ---
        tags:
          - 用户模块
        parameters:
          - name: id
            in: body
            type: int
            required: true
            example: 1
        responses:
          200:
            description: 返回信息
            examples:
              success : {"error_code": 0,"msg": "ok","request": "POST /seven/v1/change/password"}
    """
    form = ChangePasswordForm().validate_for_api()
    ok = User.change_password(form.old_password.data, form.new_password.data)
    if ok:
        return Success(message="密码修改成功!")
    else:
        return Failed(message="密码修改失败!")


@api.route('/flash/message', methods=['POST'])
@auth.login_required
def show_message():
    """
    消息提醒
    :return:
    """
    pass


# @api.route('/upload', methods=['POST'])
# @auth.login_required
# def uploads():
#     if request.method == 'POST':
#         if 'photo' not in request.files:
#             return ImagesError()
#         file = request.files['photo']
#         re_name = change_filename(file.filename)
#         if file.filename == '':
#             return ImagesError(message="没有找到这个文件！")
#         else:
#             try:
#                 filename = photos.save(file, name=re_name)
#                 return jsonify({'code': 0, 'filename': filename, 'image_url': photos.url(filename)})
#             except Exception as e:
#                 return ImagesError(message="上传的文件格式不支持！")
#     else:
#         return ImagesError(message="错误的请求方式！")

@api.route('/upload', methods=['POST'])
@auth.login_required
def uploads():
    form = UploadForm()
    form.validate_for_api()
    re_name = change_filename(form.files.data.filename)
    filename = files.save(form.files.data, name=re_name)
    if re_name is None:
        return ImagesError(message="文件上传失败！")
    return jsonify({'code': 0, 'filename': filename, 'file_url': files.url(filename)})
