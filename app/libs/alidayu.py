# -*- encoding:utf-8 -*-
"""
@ Created by Seven on  2018/08/14 
"""

from aliyunsdkcore.request import RpcRequest


class SendSmsRequest(RpcRequest):

    def __init__(self):
        RpcRequest.__init__(self, 'Dysmsapi', '2017-05-25', 'SendSms')

    def get_template_code(self):
        return self.get_query_params().get('TemplateCode')

    def set_template_code(self, template_code):
        self.add_query_param('TemplateCode', template_code)

    def get_PhoneNumbers(self):
        return self.get_query_params().get('PhoneNumbers')

    def set_phone_numbers(self, set_phone_numbers):
        self.add_query_param('PhoneNumbers', set_phone_numbers)

    def get_SignName(self):
        return self.get_query_params().get('SignName')

    def set_sign_name(self, set_sign_name):
        self.add_query_param('SignName', set_sign_name)

    def get_ResourceOwnerAccount(self):
        return self.get_query_params().get('ResourceOwnerAccount')

    def set_ResourceOwnerAccount(self, ResourceOwnerAccount):
        self.add_query_param('ResourceOwnerAccount', ResourceOwnerAccount)

    def get_TemplateParam(self):
        return self.get_query_params().get('TemplateParam')

    def set_template_param(self, template_param):
        self.add_query_param('TemplateParam', template_param)

    def get_ResourceOwnerId(self):
        return self.get_query_params().get('ResourceOwnerId')

    def set_ResourceOwnerId(self, ResourceOwnerId):
        self.add_query_param('ResourceOwnerId', ResourceOwnerId)

    def get_OwnerId(self):
        return self.get_query_params().get('OwnerId')

    def set_OwnerId(self, OwnerId):
        self.add_query_param('OwnerId', OwnerId)

    def get_SmsUpExtendCode(self):
        return self.get_query_params().get('SmsUpExtendCode')

    def set_SmsUpExtendCode(self, SmsUpExtendCode):
        self.add_query_param('SmsUpExtendCode', SmsUpExtendCode)

    def get_OutId(self):
        return self.get_query_params().get('OutId')

    def set_out_id(self, out_id):
        self.add_query_param('OutId', out_id)
