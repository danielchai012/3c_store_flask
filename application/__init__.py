from flask import Flask
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
    app.register_blueprint(product_bp)
    app.register_blueprint(member_bp)
    app.register_blueprint(sku_bp)
    app.register_blueprint(transaction_bp)

#註冊擴充
def register_extension(app):
    db.init_app(app)