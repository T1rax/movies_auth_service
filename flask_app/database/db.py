from core.config import configs

import redis
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
redis_db = redis.Redis(host=configs.mds.host, port=configs.mds.port, db=0)


def init_db(app: Flask):
    app.config['SQLALCHEMY_DATABASE_URI'] = configs.db.url
    db.init_app(app)