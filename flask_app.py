import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_mongoengine import MongoEngine
from flask_cors import CORS
from flask_caching import Cache

from elasticsearch import Elasticsearch

import config

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logging.getLogger().setLevel(logging.INFO)


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    cache = Cache(app, config={'CACHE_TYPE': 'simple'})
    cache.init_app(app)
    db = MongoEngine(app)
    mysql_db = SQLAlchemy(app)
    mysql_conn = create_engine("mysql+postgresql://user:passwd@localhost/ptg")
    es = Elasticsearch(config.ELASTICSEARCH_URI, timeout=30)

    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    return app, db, cache, mysql_db, mysql_conn, es


app, db, cache, mysql_db, mysql_conn, es = create_app()

from apis.apiv1 import blueprint as api_v1
app.register_blueprint(api_v1)
