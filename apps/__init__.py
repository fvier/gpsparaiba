import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module

db = SQLAlchemy()

def register_extensions(app):
    db.init_app(app)

apps = ('pages',)

def register_blueprints(app):
    for module_name in apps:
        module = import_module('apps.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)

def configure_database(app):
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            print('> Warning: Database initialization exception: ' + str(e))
            # Fallback to local SQLite if remote DB is unreachable
            try:
                basedir = os.path.abspath(os.path.dirname(__file__))
                app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')
                db.create_all()
            except Exception as ex:
                print('> SQLite fallback error: ' + str(ex))

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    
    @app.route('/health')
    def health_check():
        return "OK", 200

    register_extensions(app)
    register_blueprints(app)
    configure_database(app)
    return app
