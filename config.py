import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, 'a.env'))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SIMPLEMDE_JS_IIFE = True
    SIMPLEMDE_USE_CDN = True
    POST_PER_PAGE = 10
    MANAGE_POST_PER_PAGE = 15


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # in-memory database
