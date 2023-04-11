from datetime import timedelta
from core.config import configs


def set_flask_configuration(app):

    app.config['SQLALCHEMY_DATABASE_URI'] = configs.db.url

    set_jwt_configuration(app)
    set_swagger_configuration(app)


def set_jwt_configuration(app):
    app.config["JWT_SECRET_KEY"] = "super-secret"
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
    # If true this will only allow the cookies that contain your JWTs to be sent
    # over https. In production, this should always be set to True
    app.config["JWT_COOKIE_SECURE"] = False 
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
    app.config["JWT_IDENTITY_CLAIM"] = "userid"


def set_swagger_configuration(app):
    app.config['SWAGGER'] = {
        'title': 'Auth API',
        "description": "Online cinema API for user authentification",
        'version': "0.0.1",
    }