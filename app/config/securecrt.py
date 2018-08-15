# -*- encoding:utf-8 -*-
"""
@ Created by Seven on  2018/06/20 
"""
# 重要的基本配置
SECRET_KEY = '7d58afd5-5fdb-48b0-9c99-3466c2838745'

SQLALCHEMY_TRACK_MODIFICATIONS = True

# mysql 配置

SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://{name}:{password}@sh-cdb-4r50kts5.sql.tencentcdb.com:63198/{db}' \
    .format(
    name='root', password='jiandan123*#', db='example')

# 阿里云邮件服务

EMAIL_USERNAME = 'jiandan@soo9s.com'
EMAIL_PASSWORD = 'JIANdan147'
EMAIL_HOST = 'smtpdm.aliyun.com'

# 阿里云短信服务

ALI_ID = '3gRhs2hqBDvuuB5f'
ALI_KEY = 'ObZzS6YmlPYHw2eC5qjvt7ATM9lo2P'
ALI_NAME = '实验室1024'
ALI_CODE = 'SMS_34480287'
ALI_REGION = "cn-hangzhou"
ALI_PRODUCT_NAME = "Dysmsapi"
ALI_DOMAIN = "dysmsapi.aliyuncs.com"

# redis 配置

REDIS_HOST = '192.168.10.183'
REDIS_PORT = '6379'
REDIS_DB = '0'
REDIS_PASSWORD = ''

# 云片短信服务

YUN_TOKEN = 'c04eb26377b4031e896ace19afd1b02b'
SMS_HOST = 'sms.yunpian.com'
SMS_PORT = 443
SMS_VERSION = 'v2'
SMS_URI = SMS_HOST + "/" + SMS_VERSION + "/sms/tpl_single_send.json"
