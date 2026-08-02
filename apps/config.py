import os, random, string

class Config(object):

    basedir = os.path.abspath(os.path.dirname(__file__))

    # Assets Management
    ASSETS_ROOT = os.getenv('ASSETS_ROOT', '/static')  
    
    # Set up the App SECRET_KEY
    SECRET_KEY = os.getenv('SECRET_KEY', None)
    if not SECRET_KEY:
        SECRET_KEY = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(64))

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }
    AUTO_CREATE_SCHEMA = True
    REQUIRE_DATABASE_URL = False
    REQUIRE_POSTGRES = False
    REQUIRE_SECRET_KEY = False

    DATABASE_URL = os.getenv('DATABASE_URL') or os.getenv('POSTGRES_URL')
    DB_ENGINE   = os.getenv('DB_ENGINE'   , None)
    DB_USERNAME = os.getenv('DB_USERNAME' , None)
    DB_PASS     = os.getenv('DB_PASS'     , None)
    DB_HOST     = os.getenv('DB_HOST'     , None)
    DB_PORT     = os.getenv('DB_PORT'     , None)
    DB_NAME     = os.getenv('DB_NAME'     , None)

    USE_SQLITE  = True 

    # Check for direct DATABASE_URL or POSTGRES_URL
    if DATABASE_URL:
        if DATABASE_URL.startswith("postgres://"):
            DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
        USE_SQLITE = False
    elif DB_ENGINE and DB_NAME and DB_USERNAME:
        try:
            engine = DB_ENGINE
            if engine == 'postgres' or engine == 'postgresql':
                engine = 'postgresql+psycopg2'
            SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(
                engine,
                DB_USERNAME,
                DB_PASS,
                DB_HOST or 'localhost',
                DB_PORT or '5432',
                DB_NAME
            ) 
            USE_SQLITE = False
        except Exception as e:
            print('> Error: DBMS Exception: ' + str(e) )
            print('> Fallback to SQLite ')    

    if USE_SQLITE:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')
    
class ProductionConfig(Config):
    DEBUG = False
    REQUIRE_DATABASE_URL = False
    REQUIRE_POSTGRES = False
    REQUIRE_SECRET_KEY = False

    # Security
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_SAMESITE = 'Lax'
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SECURE = False
    REMEMBER_COOKIE_SAMESITE = 'Lax'
    REMEMBER_COOKIE_DURATION = 3600

class DebugConfig(Config):
    DEBUG = True
    AUTO_CREATE_SCHEMA = True

# Load all possible configurations
config_dict = {
    'Production': ProductionConfig,
    'Debug'     : DebugConfig
}
