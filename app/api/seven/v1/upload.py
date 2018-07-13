# -*- encoding:utf-8 -*-
"""
@ Created by Seven on  2018/07/13 
"""
from flask import jsonify

from app import files
from app.libs.error_code import ImagesError
from app.libs.helper import change_filename
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.validators.forms import UploadForm

__author__ = 'Little Seven'

# 前台路由
api = Redprint('upload')


@api.route('', methods=['POST'])
@auth.login_required
def uploads():
    """ 图片上传
            ---
            tags:
              - 用户模块
            parameters:
              - name: files
                in: body
                type: file
                required: true
                example: 图片.jpg
            responses:
              200:
                description: 返回信息
                examples:
                  success : {"code": 0,"file_url": "http://77.art:5000/uploads/files/123123.jpg", \
                  "filename": "123123.jpg"}
        """
    form = UploadForm()
    form.validate_for_api()
    re_name = change_filename(form.files.data.filename)
    filename = files.save(form.files.data, name=re_name)
    if re_name is None:
        return ImagesError(message="文件上传失败！")
    return jsonify({'code': 0, 'filename': filename, 'file_url': files.url(filename)})
