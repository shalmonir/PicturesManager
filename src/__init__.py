import os

from flask import Flask

from src.Configuration.Config import Config
from src.Configuration.Local import DB_SECRET
from src.DBConnectionMgr import DBConnectionMgr
from src.authentication import auth
from src.dashboard import dash
from src.download import download
from src.external import login_manager, db
from flask_bootstrap import Bootstrap


def create_app():
    if os.name != 'nt':
        link_store_directory()
    app = Flask(__name__, template_folder='template')
    app.config.from_object(Config())
    define_blueprints(app)
    define_externals(app)
    try:
        define_db(app)
    except Exception as e:
        print(e)
    return app


def link_store_directory():
    src = '/pictures'
    dst = '/python-docker/src/pictures'
    if not os.path.exists(dst):
        os.symlink(src, dst)


def define_blueprints(app):
    app.register_blueprint(auth)
    app.register_blueprint(dash)
    app.register_blueprint(download)


def define_externals(app):
    Bootstrap(app)
    login_manager.init_app(app)


def define_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_SECRET
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.init_app(app)
    with app.app_context():
        db.create_all()
    DBConnectionMgr().set_connection(db)
    DBConnectionMgr().set_session(db.session)
