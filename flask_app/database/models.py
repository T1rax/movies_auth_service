import uuid
import enum

from sqlalchemy import Enum, UniqueConstraint, or_
from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import generate_password_hash, check_password_hash
from device_detector import DeviceDetector
import string
from secrets import choice as secrets_choice
from datetime import datetime

from database.db import db
from performance.tracing.tracer import trace_it


class User(db.Model):
    """Model for User"""

    __tablename__ = "users"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    login = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=True)
    password = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String(100), nullable=True)
    last_name = db.Column(db.String(100), nullable=True)
    age_group = db.Column(
        db.Enum(
            "undefined",
            "0-17",
            "18-24",
            "25-34",
            "35-44",
            "45-64",
            "65+",
            name="age_groups",
        ),
        nullable=False,
        default="undefined",
    )
    roles = db.Column(db.PickleType(), nullable=False)

    def __repr__(self):
        return f"<User {self.login}>"

    @classmethod
    @trace_it
    def get_user_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    @trace_it
    def get_user_by_universal_login(cls, login=None, email=None):
        if login is None:
            return cls.query.filter(cls.email == email).first()
        elif email is None:
            return cls.query.filter(cls.login == login).first()
        else:
            return cls.query.filter(or_(cls.login == login, cls.email == email)).first()

    @staticmethod
    def generate_random_string():
        alphabet = string.ascii_letters + string.digits
        return "".join(secrets_choice(alphabet) for _ in range(16))

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class ActionType(enum.Enum):
    """Action types for UserHistory"""

    login = "login"
    logout = "logout"


class UserHistory(db.Model):
    """Model for recording user login history"""

    __tablename__ = "histories"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    user_device_type = db.Column(db.Text, primary_key=True, nullable=False)
    useragent = db.Column(db.String(500), nullable=False)
    remote_addr = db.Column(db.String(500), nullable=False)
    referrer = db.Column(db.String(500), nullable=True)
    action = db.Column(Enum(ActionType))
    timestamp = db.Column(db.DateTime, default=datetime.now())
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"))

    def __repr__(self):
        return f"<UserHistory {self.user_id}>"

    @classmethod
    @trace_it
    def get_history_by_user_id(cls, user_id, page, per_page):
        return cls.query.filter_by(user_id=user_id).paginate(
            page=page, per_page=per_page
        )

    @trace_it
    def set_device_type(self):
        try:
            device = DeviceDetector(self.useragent, skip_bot_detection=True).parse()
            device_type = device.device_type()
        except:
            device_type = "other"

        if device_type in {"smartphone", "desktop", "tv"}:
            self.user_device_type = device_type
        else:
            self.user_device_type = "other"


class SocialAccount(db.Model):
    """Model for recording user's social accounts"""

    __tablename__ = "social_accounts"
    __table_args__ = (UniqueConstraint("social_id", "provider"),)

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    social_id = db.Column(db.Text, nullable=False)
    provider = db.Column(db.Text, nullable=False)
    user = db.relationship(User, backref=db.backref("social_accounts"))
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"), nullable=False)

    def __repr__(self):
        return f"<SocialAccount {self.provider}:{self.user_id}>"

    @classmethod
    @trace_it
    def get_user_social(cls, provider, social_id):
        return cls.query.filter_by(provider=provider, social_id=social_id).one_or_none()
