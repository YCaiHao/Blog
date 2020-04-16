from elasticsearch import Elasticsearch
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from flask_bootstrap import Bootstrap
from flask_simplemde import SimpleMDE
from flask_moment import Moment

from config import Config


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
csrf = CSRFProtect()
bootstrap = Bootstrap()
simplemde = SimpleMDE()
moment = Moment()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    register_extensions(app)
    register_blueprint(app)

    return app


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bootstrap.init_app(app)
    simplemde.init_app(app)
    csrf.init_app(app)
    moment.init_app(app)


def register_blueprint(app):
    from app.blog import bp as blog_bp
    app.register_blueprint(blog_bp)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/amdin')


from app import models