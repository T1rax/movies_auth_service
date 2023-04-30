from flask_sqlalchemy import SQLAlchemy

import redis
from core.config import configs


db = SQLAlchemy()

jwt_redis_blocklist = redis.Redis(
    host=configs.mds.host, port=configs.mds.port, db=0, decode_responses=True
)
request_limit_storage = redis.Redis(
    host=configs.mds.host, port=configs.mds.port, db=1, decode_responses=True
)
