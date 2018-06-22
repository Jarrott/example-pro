# -*- encoding:utf-8 -*-
"""
@ Created by Seven on  2018/06/20 
"""
from werkzeug.exceptions import HTTPException

from app import create_app
from app.libs.error import JsonTypeException
from app.libs.error_code import ServerError

app = create_app()


@app.errorhandler(Exception)
def framework_error(err):
    """
    全局异常处理
    :param err:
    :return:
    """
    if isinstance(err, JsonTypeException):
        return err
    if isinstance(err, HTTPException):
        code = err.code
        message = err.message
        error_code = 10015
        return JsonTypeException(code, message, error_code)
    else:
        if not app.config["DEBUG"]:
            return ServerError()
        else:
            raise err


if __name__ == '__main__':
    app.run()
