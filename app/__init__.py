from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix
from .extensions import db, migrate, login_manager, csrf
from .config import Config
import os

from  .routes.user import user
from  .routes.quiz import quiz_bp
from  .routes.pdf import pdf_bp


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    app.register_blueprint(quiz_bp)
    app.register_blueprint(user)
    app.register_blueprint(pdf_bp)

    db.init_app(app)
    migrate.init_app(app,db)
    login_manager.init_app(app)
    csrf.init_app(app)

    # LOGIN MANAGER
    login_manager.login_view = '/login'
    login_manager.login_message = 'Доступ закрыт'

    with app.app_context():
        db.create_all()

    return app
