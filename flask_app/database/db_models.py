import uuid
from sqlalchemy.dialects.postgresql import UUID
import enum
import datetime

from database.db import db


class UUIDMixin(db.Model):
    """ Mixin with ID """

    id = db.Column(UUID(as_uuid=True),
                   primary_key=True,
                   default=uuid.uuid4,
                   unique=True,
                   nullable=False)


class User(UUIDMixin, db.Model):
    """ Model for User """
    __tablename__ = 'users'

    login = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    role_id = db.Column(UUID(as_uuid=True), db.ForeignKey('role.id'), nullable=False) # вторичный ключ
    histories = db.relationship('UserHistory', backref='user')

    def __repr__(self):
        return f'<User {self.login}>'


class RoleType(enum.Enum):
    """ Role types for User """
    default = 'default'
    subscribers = 'subscribers'
    staff = 'staff'
    admin = 'admin'


class Role(UUIDMixin, db.Model):
    """ Model for user's roles"""
    __tablename__ = 'roles'

    name = db.Column(db.Enum(RoleType))
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return f'<Role {self.name}>'


class ActionType(enum.Enum):
    """ Action types for UserHistory """
    login = 'login'
    logout = 'logout'


class UserHistory(UUIDMixin, db.Model):
    """ Model for recording user login history """
    __tablename__ = 'histories'

    useragent = db.Column(db.String(100), nullable=False)
    action = db.Column(db.Enum(ActionType))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now())
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<UserHistory {self.user_id}>'
