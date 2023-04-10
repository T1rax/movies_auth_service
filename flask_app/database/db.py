import redis
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from core.config import configs


db = SQLAlchemy()
jwt_redis_blocklist = redis.Redis(host=configs.mds.host, port=configs.mds.port, db=0, decode_responses=True)


def init_db(app: Flask):
    app.config['SQLALCHEMY_DATABASE_URI'] = configs.db.url
    db.init_app(app)