## 城南大数据平台项目
本项目以停止维护.2019-5-28,公开源代码
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
    name='root', password='*#', db='example')

# 阿里云邮件服务
EMAIL_USERNAME = ''
EMAIL_PASSWORD = ''
EMAIL_HOST = 'smtpdm.aliyun.com'
```

## 项目API接口展示

http://77.art:5000/apidocs

![项目接口](https://github.com/litt1eseven/python-project/blob/master/Company-project/images/api-list-sw0.9.png)

## Deploy
### Docker部署

 部署脚本已经完成。 

### 部署注意
如果要使用"0.0.0.0"，启动项目，并且任何ip可以访问
```
pydev debugger: process 5192 is connecting
Connected to pydev debugger (build 181.5087.37)
 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
 * Restarting with stat
pydev debugger: process 5193 is connecting
 * Debugger is active!
 * Debugger PIN: 210-279-564
127.0.0.1 - - [10/Jul/2018 14:32:41] "GET / HTTP/1.1" 0 -
```

需要这样启动项目

>run.py 其余任何配置不需要修改，然后把配置中的SERVER_NAME注释掉就好了
```
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```


在有域名，有固定的IP地址的时候可以这样配置
```
# -*- encoding:utf-8 -*-
"""
@ Created by Seven on  2018/06/20 
"""

# 基本配置

DEBUG = True
SERVER_NAME = '77.art:7000'
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
            "version": "0.1",
            "title": "主页API接口列表",
            "description": 'This is the version 0.1 of Big-data API',
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
        }
    ],
}

# Token 过期时间
JWT_TOKEN_EXPIRES = 1 * 24 * 3600
```

> 入口文件

```
if __name__ == '__main__':
    app.run()
```

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

:tada:
