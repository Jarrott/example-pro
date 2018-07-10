# -*- encoding:utf-8 -*-
"""
@ Created by Seven on  2018/06/20 
"""

from .app import Flask


def register_database(app):
    """
    注册数据库，初始化数据库
    :param app:
    :return:
    """
    from app.libs.model_base import db
    db.init_app(app)
    # Migrate(app, db)
    with app.app_context():
        db.create_all()


def register_blueprints(app):
    """
    注册蓝图
    :param app:
    :return:
    """
    from app.api.seven.v1 import create_blueprint
    app.register_blueprint(create_blueprint(), url_prefix='/seven/v1')


# 解决跨域
def apply_cors(app):
    from flask_cors import CORS
    CORS(app)


def register_swagger(app):
    from flasgger import Swagger
    template = {
        "host": "77.art:7000",
        "securityDefinitions": {'basicAuth': {'type': 'basic'}}
    }
    Swagger(app, template=template)


def create_app():
    """
    初始化项目
    :return:
    """
    app = Flask(__name__)
    app.config.from_object('app.config.setting')
    app.config.from_object('app.config.securecrt')
    apply_cors(app)
    register_blueprints(app)
    register_database(app)
    register_swagger(app)
    return app
