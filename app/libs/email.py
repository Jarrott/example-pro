# -*- encoding:utf-8 -*-
"""
@ Created by Seven on  2018/08/15 
"""
from flask import current_app, render_template, url_for
from flask_mail import Mail, Message
from app.libs.error_code import EmailException

mail = Mail()


def send_code_email(email_address, email_title, template=None, **kwargs):
    app = current_app._get_current_object()
    content = render_template(template, **kwargs)
    msg = Message(subject=email_title, sender=app.config['MAIL_SENDER'], recipients=[email_address])
    msg.html = content
    try:
        mail.send(msg)
    except Exception as e:
        raise EmailException()


def send_reset_password_email(email_address, email_title, token, user_name, template=None):
    app = current_app._get_current_object()
    redirect_url = generate_hash_and_token_url('web.index+index', hash='reset_password', token=token)
    content = render_template(template, user_name=user_name, redirect_url=redirect_url)
    msg = Message(subject=email_title, sender=app.config['MAIL_SENDER'], recipients=[email_address])
    msg.html = content
    try:
        mail.send(msg)
    except Exception as e:
        raise EmailException()


def send_email_async(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            app.logger.info("\n %s", e)


def generate_hash_and_token_url(endpoint, hash, token):
    base_url = url_for(endpoint)
    url = current_app.config['SERVER_NAME']
    return '{}{}#/{}?token={}'.format('http://' + url, base_url, hash, token)
