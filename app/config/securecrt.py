# -*- encoding:utf-8 -*-
"""
@ Created by Seven on  2018/06/20 
"""
# 重要的基本配置
SECRET_KEY = '7d58afd5-5fdb-48b0-9c99-3466c2838745'
# JSON_AS_ASCII = False
SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://root:{}@sh-cdb-4r50kts5.sql.tencentcdb.com:63198/example'.format(
    'jiandan123*#')
SQLALCHEMY_TRACK_MODIFICATIONS = True

# mysql 配置


# 阿里云邮件服务
EMAIL_USERNAME = 'jiandan@soo9s.com'
EMAIL_PASSWORD = 'JIANdan147'
EMAIL_HOST = 'smtpdm.aliyun.com'
