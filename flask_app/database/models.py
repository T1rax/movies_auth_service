import uuid
import enum

from sqlalchemy import Enum
from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime

from database.db import db


class User(db.Model):
    """ Model for User """
    __tablename__ = 'users'

    id = db.Column(UUID(as_uuid=True),
                   primary_key=True,
                   default=uuid.uuid4,
                   unique=True,
                   nullable=False)
    login = db.Column(db.String(100), unique=True, nullable=False)
    # email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    roles = db.Column(db.PickleType(), nullable=False)

    def __repr__(self):
        return f'<User {self.login}>'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class ActionType(enum.Enum):
    """ Action types for UserHistory """
    login = 'login'
    logout = 'logout'


class UserHistory(db.Model):
    """ Model for recording user login history """
    __tablename__ = 'histories'

    id = db.Column(UUID(as_uuid=True),
                   primary_key=True,
                   default=uuid.uuid4,
                   unique=True,
                   nullable=False)
    useragent = db.Column(db.String(100), nullable=False)
    action = db.Column(Enum(ActionType))
    timestamp = db.Column(db.DateTime, default=datetime.now())
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'))

    def __repr__(self):
        return f'<UserHistory {self.user_id}>'