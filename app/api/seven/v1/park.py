# -*- encoding:utf-8 -*-
"""
@ Created by Seven on  2018/06/26 
"""
from app.libs.redprint import Redprint
from app.libs.token_auth import auth

api = Redprint('park')


@api.route('', methods=['POST'])
@auth.login_required
def push_demand():
    pass
