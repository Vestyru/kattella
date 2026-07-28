from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_wtf.csrf import CSRFProtect
from .extensions import db, migrate, login_manager
from .config import Config

from  .routes.user import user
from  .routes.main import main
from  .routes.quiz import quiz_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    csrf = CSRFProtect(app)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    app.register_blueprint(quiz_bp)
    app.register_blueprint(user)
    app.register_blueprint(main)

    db.init_app(app)
    migrate.init_app(app,db)
    login_manager.init_app(app)

    # LOGIN MANAGER
    login_manager.login_view = '/login'
    login_manager.login_message = 'Доступ закрыт'

    with app.app_context():
        #db.create_all()

    return app
