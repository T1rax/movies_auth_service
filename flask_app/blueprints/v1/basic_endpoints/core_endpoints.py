from flask import Blueprint, jsonify, request, render_template, current_app, url_for
import json
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt

from core.errors import (
    RegistrationException,
    UserIdException,
    LoginException,
    HistoryException,
    OAuthException,
)
from encryption.jwt import jwt_helper
from apispec_fromfile import from_file

from core.oauth import oauth, oauth_google, oauth_yandex, oauth_vk
from core.config import configs

# Account authorization routes
from routes.authorize import authorize_user
from routes.sign_up import register_user
from routes.sign_in import login_user

# Roles routes
from routes.change_role import user_change_role

# Support routes
from routes.get_user_description import user_description
from routes.sign_in_history import get_history, add_history


blueprint = Blueprint("auth", __name__, url_prefix="/auth")


# Home page
@blueprint.route("/", methods=["GET"])
def main_page():
    return render_template("home.html")


# Account authorization routes
@from_file("core/swagger/authorize.yml")
@blueprint.route("/authorize", methods=["POST"])
@jwt_required(locations=["cookies"])
def authorize():
    try:
        response = authorize_user(get_jwt())
        return jsonify(response), HTTPStatus.OK
    except Exception as e:
        current_app.logger.error(e)
        return (
            jsonify({"msg": "Internal server error"}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )


# http://127.0.0.1/auth/v1/google/login
# http://127.0.0.1/auth/v1/yandex/login
# http://127.0.0.1/auth/v1/vk/login
@from_file("core/swagger/oauth.yml")
@blueprint.route("/<string:provider>/login", methods=["GET"])
def oauth_login(provider):
    try:
        if provider not in configs.oauth.apps:
            raise OAuthException("Provider nor supported")

        client = oauth.create_client(provider)
        redirect_uri = url_for("auth.oauth_callback", provider=provider, _external=True)
        return client.authorize_redirect(redirect_uri)
    except OAuthException as e:
        current_app.logger.error(e)
        return jsonify({"msg": str(e)}), HTTPStatus.NOT_FOUND
    except Exception as e:
        current_app.logger.error(e)
        return (
            jsonify({"msg": "Internal server error", "error": e}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )


@blueprint.route("/<string:provider>/callback", methods=["GET"])
def oauth_callback(provider):
    try:
        if provider not in configs.oauth.apps:
            raise OAuthException("Provider nor supported")

        client = oauth.create_client(provider)
        token = client.authorize_access_token()

        if provider == "google":
            user = oauth_google(provider)
        elif provider == "yandex":
            user = oauth_yandex(provider)
        elif provider == "vk":
            user = oauth_vk(provider, token)

        response = jsonify({"msg": user.login})
        current_app.logger.info("Adding JWT to cookies")
        jwt_helper.user_id = user.id
        jwt_helper.create_tokens()
        jwt_helper.set_tokens(response)
        return response, HTTPStatus.OK
    except OAuthException as e:
        current_app.logger.error(e)
        return jsonify({"msg": str(e)}), HTTPStatus.NOT_FOUND
    except Exception as e:
        current_app.logger.error(e)
        return (
            jsonify({"msg": "Internal server error"}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )


@from_file("core/swagger/logout.yml")
@blueprint.route("/logout", methods=["GET", "POST"])
@jwt_required(locations=["cookies"])
def logout():
    try:
        response = jsonify({"msg": "logout successful"})

        current_app.logger.info("Adding logout to user history")
        add_history(request, get_jwt().get("userid"), "logout")

        current_app.logger.info("Dropping JWT from cookies")
        jwt_helper.drop_tokens(response)

        return response, HTTPStatus.OK
    except Exception as e:
        current_app.logger.error(e)
        return (
            jsonify({"msg": "Internal server error"}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )


@from_file("core/swagger/sign_in.yml")
@blueprint.route("/sign-in", methods=["POST"])
def sign_in():
    try:
        user = login_user(request)
        response = jsonify({"msg": "login successful"})

        current_app.logger.info("Adding JWT to cookies")
        jwt_helper.user_id = user.id
        jwt_helper.create_tokens()
        jwt_helper.set_tokens(response)
        return response, HTTPStatus.OK
    except LoginException as e:
        current_app.logger.error(e)
        return jsonify({"msg": str(e)}), HTTPStatus.UNAUTHORIZED
    except Exception as e:
        current_app.logger.error(e)
        return (
            jsonify({"msg": "Internal server error"}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )


@from_file("core/swagger/sign_up.yml")
@blueprint.route("/sign-up", methods=["POST"])
def sign_up():
    try:
        user = register_user(request)
        response = jsonify({"msg": "registration successful"})

        current_app.logger.info("Adding JWT to cookies")
        jwt_helper.user_id = user.id
        jwt_helper.create_tokens()
        jwt_helper.set_tokens(response)
        return response, HTTPStatus.OK
    except RegistrationException as e:
        current_app.logger.error(e)
        return jsonify({"msg": str(e)}), HTTPStatus.UNAUTHORIZED
    except Exception as e:
        current_app.logger.error(e)
        return (
            jsonify({"msg": "Internal server error"}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )


# Token-related routes
@from_file("core/swagger/refresh.yml")
@blueprint.route("/refresh", methods=["POST"])
@jwt_required(refresh=True, locations=["cookies"])
def refresh():
    try:
        response = jsonify({"msg": "tokens refreshed"})

        current_app.logger.info("Adding JWT to cookies")
        jwt_helper.create_tokens()
        jwt_helper.set_tokens(response)
        return response, HTTPStatus.OK
    except Exception as e:
        current_app.logger.error(e)
        return (
            jsonify({"msg": "Internal server error"}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )


# Roles routes
@from_file("core/swagger/change_role.yml")
@blueprint.route("/change-role", methods=["POST"])
@jwt_required(locations=["cookies"])
def change_role():
    try:
        data = request.get_json()
        raw_response = user_change_role(data)
        response = jsonify(raw_response)

        return response, HTTPStatus.OK
    except UserIdException as e:
        current_app.logger.error(e)
        return jsonify({"msg": str(e)}), HTTPStatus.UNAUTHORIZED
    except Exception as e:
        current_app.logger.error(e)
        return (
            jsonify({"msg": "Internal server error"}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )


# Support routes
@from_file("core/swagger/get_user_description.yml")
@blueprint.route("/get-user-description", methods=["GET"])
@jwt_required(locations=["cookies"])
def get_user_description():
    try:
        data = request.get_json()
        user = user_description(data)
        response = jsonify({"msg": "User exists", "user": user})

        return response, HTTPStatus.OK
    except UserIdException as e:
        current_app.logger.error(e)
        return jsonify({"msg": str(e)}), HTTPStatus.UNAUTHORIZED
    except Exception as e:
        current_app.logger.error(e)
        return (
            jsonify({"msg": "Internal server error"}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )


@from_file("core/swagger/sign_in_history.yml")
@blueprint.route("/sign-in-history", methods=["GET"])
@jwt_required(locations=["cookies"])
def sign_in_history():
    try:
        data = get_history(request)
        return jsonify(data)
    except HistoryException as e:
        current_app.logger.error(e)
        return jsonify({"msg": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
    except Exception as e:
        current_app.logger.error(e)
        return (
            jsonify({"msg": "Internal server error"}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )


# Documentation
@blueprint.route("/swagger.json")
def swagger():
    try:
        with open("core/swagger/swagger.json", "r") as f:
            return jsonify(json.load(f))
    except Exception as e:
        current_app.logger.error(e)
        return (
            jsonify({"msg": "Internal server error"}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )
