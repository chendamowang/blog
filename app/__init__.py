#-*- coding: utf-8 -*-
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_pagedown import PageDown
from config import config

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
pagedown = PageDown()

login_manager = LoginManager()
login_manager.session_protection = 'strong'  #session_protection属性可以设置为None、'basic'、'strong' （不同的安全等级）
login_manager.login_view = 'auth.login'  #login_view属性设置登录页面的端点

def create_app(config_name):    #工厂函数
    app = Flask(__name__)
    app.config.from_object(config[config_name])     #导入程序
    config[config_name].init_app(app)       #初始化扩展

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)
        
    from .main import main as main_blueprint  #蓝本注册到程序上
    app.register_blueprint(main_blueprint)
    
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app

