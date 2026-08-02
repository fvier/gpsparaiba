import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from importlib import import_module
from sqlalchemy import inspect, text

db = SQLAlchemy()
migrate = Migrate(compare_type=True)

def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)

apps = ('pages',)

def register_blueprints(app):
    for module_name in apps:
        module = import_module('apps.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)

def ensure_user_columns(app):
    with app.app_context():
        try:
            inspector = inspect(db.engine)
            if 'users' in inspector.get_table_names():
                columns = [column['name'] for column in inspector.get_columns('users')]
                missing_columns = {
                    'role': "VARCHAR(32) NOT NULL DEFAULT 'usuario'",
                    'category': "VARCHAR(32) NOT NULL DEFAULT 'Orange'",
                    'full_name': 'VARCHAR(120)',
                    'ddd': 'VARCHAR(2)',
                    'contact': 'VARCHAR(9)',
                    'active': 'BOOLEAN NOT NULL DEFAULT TRUE',
                    'must_change_password': 'BOOLEAN NOT NULL DEFAULT FALSE',
                    'avatar_filename': 'VARCHAR(160)',
                }
                for column_name, column_type in missing_columns.items():
                    if column_name not in columns:
                        db.session.execute(text(f'ALTER TABLE users ADD COLUMN {column_name} {column_type}'))
                if any(column_name not in columns for column_name in missing_columns):
                    db.session.commit()
        except Exception as e:
            print('> Warning: user columns migration exception: ' + str(e))
            db.session.rollback()

def ensure_carousel_columns(app):
    with app.app_context():
        try:
            inspector = inspect(db.engine)
            if 'carousel_images' in inspector.get_table_names():
                columns = [column['name'] for column in inspector.get_columns('carousel_images')]
                if 'set_type' not in columns:
                    db.session.execute(text("ALTER TABLE carousel_images ADD COLUMN set_type VARCHAR(32) NOT NULL DEFAULT 'outros'"))
                    db.session.commit()
        except Exception as e:
            print('> Warning: carousel column migration exception: ' + str(e))
            db.session.rollback()

def configure_database(app):
    with app.app_context():
        if app.config.get('REQUIRE_SECRET_KEY') and not os.getenv('SECRET_KEY'):
            raise RuntimeError('SECRET_KEY is required in production.')

        if app.config.get('REQUIRE_DATABASE_URL') and not (
            os.getenv('DATABASE_URL') or os.getenv('POSTGRES_URL')
        ):
            raise RuntimeError('DATABASE_URL is required in production.')

        if app.config.get('REQUIRE_POSTGRES') and not app.config[
            'SQLALCHEMY_DATABASE_URI'
        ].startswith(('postgresql://', 'postgresql+psycopg2://')):
            raise RuntimeError('Production DATABASE_URL must use PostgreSQL.')

        if app.config.get('AUTO_CREATE_SCHEMA'):
            db.create_all()
            ensure_user_columns(app)
            ensure_carousel_columns(app)

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    
    @app.route('/health')
    def health_check():
        try:
            db.session.execute(text('SELECT 1'))
        except Exception:
            app.logger.exception('Database health check failed')
            return {'status': 'unhealthy', 'database': 'unavailable'}, 503
        return {'status': 'ok', 'database': 'available'}, 200

    register_extensions(app)
    register_blueprints(app)
    configure_database(app)
    return app
