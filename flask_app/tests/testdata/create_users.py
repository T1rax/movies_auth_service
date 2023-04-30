from testdata.test_users import preloaded_users

from app import app
from database.db import db
from database.models import User


def create_user(user_json):
    user = User(
        login=user_json.get("login"),
        first_name=user_json.get("first_name"),
        last_name=user_json.get("last_name"),
        roles=["basicRole"],
    )

    user.set_password(user_json.get("password"))

    db.session.add(user)
    db.session.commit()


def create_super_user():
    user = User(
        login="superuser",
        first_name="Super",
        last_name="User",
        roles=["basicRole", "superUser"],
    )

    user.set_password("test_password")

    db.session.add(user)
    db.session.commit()


def load_test_data():
    with app.app_context():
        for user in preloaded_users:
            create_user(user)

        create_super_user()
