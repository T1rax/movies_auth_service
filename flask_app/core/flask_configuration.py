from datetime import timedelta
from core.config import configs


def set_flask_configuration(app):

    app.config['SQLALCHEMY_DATABASE_URI'] = configs.db.url
    app.config['SECRET_KEY'] = configs.oauth.secret_key

    set_oauth_configuration(app)
    set_jwt_configuration(app)
    set_swagger_configuration(app)


def set_jwt_configuration(app):
    app.config["JWT_SECRET_KEY"] = "super-secret"
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
    # If true this will only allow the cookies that contain your JWTs to be sent
    # over https. In production, this should always be set to True
    app.config["JWT_COOKIE_SECURE"] = False 
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False 
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
    app.config["JWT_IDENTITY_CLAIM"] = "userid"


def set_swagger_configuration(app):
    app.config['SWAGGER'] = {
        'title': 'Auth API',
        "description": "Online cinema API for user authentification",
        'version': "0.0.1",
    }


def set_oauth_configuration(app):
    app.config['GOOGLE_CLIENT_ID'] = configs.oauth.google.client_id
    app.config['GOOGLE_CLIENT_SECRET'] = configs.oauth.google.secret

    app.config['YANDEX_CLIENT_ID'] = configs.oauth.yandex.client_id
    app.config['YANDEX_CLIENT_SECRET'] = configs.oauth.yandex.secret

    app.config['VK_CLIENT_ID'] = configs.oauth.vk.client_id
    app.config['VK_CLIENT_SECRET'] = configs.oauth.vk.secret