from flask import Flask
from sku import *
from application.controllers import *

#建立Flask APP
def create_app(config_filename):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile(config_filename)

    register_blueprints(app)
    register_extension(app)
    return app

#註冊API
def register_blueprints(app):
    app.register_blueprint(product_bp, url_prefix="/3c_store/api/v1"+"/product")
    app.register_blueprint(member_bp, url_prefix="/3c_store/api/v1"+"/member")
    app.register_blueprint(sku_bp, url_prefix="/3c_store/api/v1"+"/sku")
    app.register_blueprint(transaction_bp, url_prefix="/3c_store/api/v1"+"/transaction")

#註冊擴充
def register_extension(app):
    db.init_app(app)