APPLICATION_PORT = 9090

DEFAULT_MONGO_HOST = 'mongodb://localhost/ptg_db'


MONGODB_SETTINGS = {
    'host': 'mongodb://localhost/ptg_db',
    'connect': True
}

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:passwd@localhost/ptg'
SQLALCHEMY_TRACK_MODIFICATIONS = False
CACHE_TYPE = 'simple'
