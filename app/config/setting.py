# -*- encoding:utf-8 -*-
"""
@ Created by Seven on  2018/06/20 
"""

# 基本配置
import os

DEBUG = True
# SERVER_NAME = '77.art:5000'
TYPE = 'Basic'
JSON_AS_ASCII = False

# Swagger 配置+跨域请求
SWAGGER = {
    "swagger_version": "2.0",
    "title": "大数据平台项目",
    # "headers": [
    #     ('Access-Control-Allow-Origin', '*'),
    #     ('Access-Control-Allow-Methods', "GET, POST, PUT, DELETE, OPTIONS"),
    #     ('Access-Control-Allow-Credentials', "true"),
    # ],
    "specs": [
        {
            "version": "0.5",
            "title": "主页API接口列表",
            "description": 'This is the version 0.5 of Big-data API',
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
        }
    ],
}

DOCUMENTS = tuple('jpg jpe jpeg png gif svg bmp doc docx xls xlsx'.split())  # 允许上传的文件类型

PER_PAGE = 10  # 页面显示条数

# Token 过期时间
JWT_TOKEN_EXPIRES = 1 * 24 * 3600
