# -*- encoding:utf-8 -*-
"""
@ Created by Seven on  2018/06/20
"""
import smtplib
from threading import Thread

from flask import current_app, render_template, url_for

from email.mime.text import MIMEText


class Email:
    __user = current_app.config["EMAIL_USERNAME"]
    __password = current_app.config["EMAIL_PASSWORD"]
    __host = current_app.config["EMAIL_HOST"]

    @classmethod
    def send_html(cls, to_user, sub, template=None, **kwargs):
        """
        发送邮件
        :param to_user:
        :param sub:
        :param template:
        :param kwargs:
        :return:
        """
        content = render_template(template, **kwargs)
        msg = MIMEText(content, _subtype='html', _charset='utf-8')
        thr = Thread(target=cls.send_email_async, args=[cls, msg, to_user, sub])
        thr.start()
        return thr

    def send_email_async(self, msg, to_user, sub):
        __me = "<" + self.__user + ">"
        server = smtplib.SMTP()
        server.connect(self.__host, 80)
        server.login(self.__user, self.__password)
        client = server

        msg['Subject'] = sub
        msg['Form'] = __me
        msg['To'] = to_user
        try:
            client.sendmail(__me, to_user, msg.as_string())
        except Exception as e:
            raise e

    def send_reset_password_email(self):
        """
        重置密码
        :return:
        """
        pass
