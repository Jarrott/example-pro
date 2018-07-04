FROM py3-flask1.0:latest

MAINTAINER little.seven <https://soo9s.com>

COPY example-pro /usr/project/bigdata

WORKDIR /usr/project/bigdata

# 安装项目所需的第三方
RUN pipenv install --system \
    && supervisord -c /usr/supervisord.conf -n