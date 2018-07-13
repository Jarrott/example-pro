# -*- encoding:utf-8 -*-
"""
@ Created by Seven on  2018/06/20 
"""
import os

from flask_uploads import (configure_uploads, patch_request_class,
                           UploadSet)

from app.config.setting import DOCUMENTS
from .app import Flask

files = UploadSet('files', DOCUMENTS)


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
    from app.web import create_blueprint_web
    app.register_blueprint(create_blueprint(), url_prefix='/seven/v1')  # subdomain='api'  api.77.art:port
    app.register_blueprint(create_blueprint_web())


# 解决跨域
def apply_cors(app):
    from flask_cors import CORS
    CORS(app)


# 注册swagger
def register_swagger(app):
    from flasgger import Swagger
    template = {
        # "host": "77.art:5000",
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
    app.config['UPLOADED_FILES_DEST'] = os.getcwd() + '/vendor/uploads'
    configure_uploads(app, files)
    patch_request_class(app)
    apply_cors(app)
    register_blueprints(app)
    register_database(app)
    register_swagger(app)
    return app
