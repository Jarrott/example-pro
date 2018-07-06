## 城南大数据平台项目

### 架构与代码重构


> 运行服务的话需要在config目录下新建一个“securecrt”文件，并填入对应的mysql信息 *(代码在私有仓库这条信息请忽略)*

## 运行服务
1.首先将“77.art”加入到自己电脑的hosts中

2.将项目下载好后，运行bigdata.py即可。

3.在 Dockerfile 中安装依赖，加--system参数表示使用 pip 直接安装相应依赖，不创建虚拟环境。

 `RUN pipenv install --deploy --system`
 
4.也可以将pipenv的包转到`requirements`里面
`pipenv lock -r > requirements.txt`
 
## securect.py
```
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
```

## 项目API接口展示

http://77.art:5000/apidocs

![项目接口](https://github.com/litt1eseven/python-project/blob/master/Company-project/images/api-list-sw0.9.png)

## Deploy
### Docker部署

 部署脚本已经完成。 


## TODO LIST
- [x] 重构架构，优化代码
- [x] 用户登录、注册
- [x] 超权问题
- [x] 权限
- [x] 密码修改，重置
- [x] 邮件发送
- [x] 园区综合管理1-2模块
- [ ] ip 监控，限流
- [ ] and so on....