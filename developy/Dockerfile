FROM registry.cn-hangzhou.aliyuncs.com/littleseven/bigdata

MAINTAINER little.seven <https://soo9s.com>

COPY example-pro/Pipfile /usr/project/Pipfile
COPY example-pro/Pipfile.lock /usr/project/Pipfile.lock
COPY example-pro/developy/supervisor.conf /usr/supervisord.conf
COPY example-pro/developy/bigdata /etc/nginx/conf.d/default.conf

RUN adduser -s -S -D jiandan

USER jiandan

WORKDIR /usr/project

# 安装项目所需的第三方
RUN pipenv install --system \
    && pip install flask-wtf