FROM registry.cn-hangzhou.aliyuncs.com/littleseven/bigdata

MAINTAINER little.seven <https://soo9s.com>

ADD example-pro /usr/project/bigdata

COPY example-pro/developy/supervisor-app.conf /usr/supervisord.conf
COPY example-pro/developy/bigdata /etc/nginx/conf.d/default.conf

WORKDIR /usr/project/bigdata

# 安装项目所需的第三方
RUN pipenv install --system