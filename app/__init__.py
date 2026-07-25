from flask import Flask
from .extensions import db, migrate, login_manager
from .config import Config

from  .routes.user import user
from  .routes.main import main
from  .routes.quiz import participants

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.register_blueprint(user)
    app.register_blueprint(main)
    app.register_blueprint(participants)

    db.init_app(app)
    migrate.init_app(app,db)
    login_manager.init_app(app)

    # LOGIN MANAGER
    login_manager.login_view = '/login'
    login_manager.login_message = 'Доступ закрыт'

    with app.app_context():
        db.create_all()

    return app
