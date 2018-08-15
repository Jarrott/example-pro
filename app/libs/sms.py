# -*- encoding:utf-8 -*-
"""
@ Created by Seven on  2018/08/15 
"""
import uuid

from aliyunsdkcore.client import AcsClient as connection
from aliyunsdkcore.profile import region_provider
from flask import current_app

from app.libs.alidayu import SendSmsRequest

sign_name = current_app.config['ALI_NAME']
template_code = current_app.config['ALI_CODE']

acs_client = connection(current_app.config['ALI_ID'], current_app.config['ALI_KEY'],
                        current_app.config['ALI_REGION'])

region_provider.modify_point(current_app.config['ALI_PRODUCT_NAME'],
                             current_app.config['ALI_REGION'],
                             current_app.config['ALI_DOMAIN'])


def send_sms(phone_numbers, param=None):
    __business_id = uuid.uuid1()
    sms_request = SendSmsRequest()
    sms_request.set_template_code(template_code)

    # 短信模板变量参数
    if param is not None:
        sms_request.set_template_param(param)

    # 设置业务请求流水号，必填。
    sms_request.set_out_id(__business_id)
    # 短信签名
    sms_request.set_sign_name(sign_name)

    sms_request.set_phone_numbers(phone_numbers)

    sms_response = acs_client.do_action_with_exception(sms_request)

    return sms_response
