# -*- encoding:utf-8 -*-
"""
@ Created by Seven on  2018/07/13 
"""
from flask import jsonify, request, current_app

from app import files
from app.libs.token_auth import auth
from app.libs.redprint import Redprint
from app.libs.error_code import ImagesError
from app.validators.forms import UploadForm
from app.libs.helper import change_filename
from openpyxl import load_workbook

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
    re_name = change_filename(form.files.data['files'].filename)
    filename = files.save(form.files.data['files'], name=re_name)
    if re_name is None:
        return ImagesError(message="文件上传失败！")
    return jsonify({'code': 0, 'filename': filename, 'file_url': files.url(filename)})


@api.route('/many', methods=['POST'])
@auth.login_required
def many_files():
    """ 多文件上传
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
    _file = []
    _file_url = []
    form = UploadForm().validate_for_api()
    for filename in request.files.getlist(form.files.id):
        re_name = change_filename(filename.filename)
        filename = files.save(filename, name=re_name)
        _file.append(filename)
        _file_url.append(files.url(filename))
    return jsonify({'code': 0, 'filename': _file, 'file_url': _file_url})


@api.route('/get_excel', methods=['POST'])
# @auth.login_required
def get_excel():
    form = UploadForm().validate_for_api()
    re_name = change_filename(form.files.data['files'].filename)
    files.save(form.files.data['files'], name=re_name)
    file = load_workbook(current_app.config['UPLOADED_FILES_DEST'] + "/" + re_name)
    sheet_name = file.get_sheet_names()  # 获取所有工作表名称
    name = str("".join(sheet_name))
    a_sheet = file[name]
    data_sheet = []
    for row in a_sheet.values:
        data_sheet.append(row)
    for i in data_sheet[1:]:
        data = list(tuple(i))
        print(data[0])
    return jsonify({'1': '1'})
