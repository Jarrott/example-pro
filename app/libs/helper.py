# -*- encoding:utf-8 -*-
"""
@ Created by Seven on  2018/07/12 
"""
import datetime
import os
import uuid


def change_filename(filename):
    """
    修改文件名称
    :param filename:
    :return:
    """
    fileinfo = os.path.splitext(filename)
    filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + \
               str(uuid.uuid4().hex) + fileinfo[-1]
    return filename
