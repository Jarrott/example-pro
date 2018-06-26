FROM alpine:latest

RUN echo http://mirrors.ustc.edu.cn/alpine/v3.6/main > /etc/apk/repositories; \
    echo http://mirrors.ustc.edu.cn/alpine/v3.6/community >> /etc/apk/repositories \
    && mkdir /run/nginx

RUN apk update \
    && apk upgrade \
    && apk add --no-cache \
       gcc \
       g++ \
       nginx \
       libc-dev \
       libffi-dev \
       openssl-dev \
       libxml2-dev \
       libxslt \
       libxslt-dev \
       linux-headers \
       pcre-dev \
       python3 \
       git

RUN python3 -m pip install -i https://pypi.douban.com/simple pipenv
