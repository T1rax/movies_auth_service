from core.config import configs

import redis
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import uuid
from sqlalchemy.dialects.postgresql import UUID

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    login = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    roles = db.Column(db.PickleType, nullable=False)

    def __repr__(self):
        return f'<User {self.login}>' 


jwt_redis_blocklist = redis.Redis(host=configs.mds.host, port=configs.mds.port, db=0, decode_responses=True)


def init_db(app: Flask):
    db.init_app(app)
    with app.app_context():
        db.create_all()