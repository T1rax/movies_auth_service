from flask import Blueprint, jsonify, request
import json
import click
from flask_jwt_extended import jwt_required, get_jwt

from core.errors import RegistrationException, UserIdException
from encryption.jwt import jwt_helper
from apispec_fromfile import from_file

#Routes import
from routes.superuser import create_superuser
# Account authorization routes
from routes.authorize import authorize_user
from routes.sign_up import register_user
from routes.sign_in import login_user
# Roles routes
from routes.change_role import user_change_role
# Support routes
from routes.get_user_description import user_description
from routes.sign_in_history import get_history


blueprint = Blueprint('auth', __name__, url_prefix='/auth')


#Bash routes
@blueprint.cli.command('createsuperuser')
@click.argument('name')
@click.argument('password')
def create_su(name, password):
    data = create_superuser(name, password)
    return True


 # Test pages
# @blueprint.route('/', methods=["GET"])
# async def main_page():
#     return 'Hello, World!'   


# Account authorization routes
@from_file("core/swagger/authorize.yml")
@blueprint.route('/authorize', methods=["POST"])
@jwt_required(locations=["cookies"])
async def authorize():
    response = authorize_user(get_jwt())
    return jsonify(response), 200


@from_file("core/swagger/logout.yml")
@blueprint.route('/logout', methods=["GET", "POST"])
@jwt_required(locations=["cookies"])
async def logout():
    response = jsonify({"msg": "logout successful"})
    jwt_helper.drop_tokens(response)
    return response


@from_file("core/swagger/sign_in.yml")
@blueprint.route('/sign-in', methods=["POST"])
async def sign_in():
    try:
        user = login_user(request)
        response = jsonify({"msg": "login successful"})

        jwt_helper.user_id = user.id
        jwt_helper.create_tokens()
        jwt_helper.set_tokens(response)
        return response, 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 401


@from_file("core/swagger/sign_up.yml")
@blueprint.route('/sign-up', methods=["POST"])
async def sign_up():
    try:
        data = request.get_json()
        user = register_user(data)
        response = jsonify({"msg": "registration successful"})

        jwt_helper.user_id = user.id
        jwt_helper.create_tokens()
        jwt_helper.set_tokens(response)
        return response, 200
    except RegistrationException as e:
        return jsonify({"msg": str(e)}), 401


# Token-related routes
@from_file("core/swagger/refresh.yml")
@blueprint.route('/refresh', methods=["POST"])
@jwt_required(refresh=True, locations=["cookies"])
async def refresh():
    response = jsonify({"msg": "tokens refreshed"})
    jwt_helper.create_tokens()
    jwt_helper.set_tokens(response)
    return response


# Roles routes
@from_file("core/swagger/change_role.yml")
@blueprint.route('/change-role', methods=["POST"])
@jwt_required(locations=["cookies"])
async def change_role():
    try:
        data = request.get_json()
        raw_response = user_change_role(data)
        response = jsonify(raw_response)

        return response, 200
    except UserIdException as e:
        return jsonify({"msg": str(e)}), 401
    except Exception as e:
        return jsonify({"msg": 'some error'}), 401


# Support routes
@from_file("core/swagger/get_user_description.yml")
@blueprint.route('/get-user-description', methods=["GET"])
@jwt_required(locations=["cookies"])
async def get_user_description():
    try:
        data = request.get_json()
        user = user_description(data)
        response = jsonify({"msg": 'User exists', 'user': user})

        return response, 200
    except UserIdException as e:
        return jsonify({"msg": str(e)}), 401
    except Exception as e:
        return jsonify({"msg": 'some error'}), 401


@from_file("core/swagger/sign_in_history.yml")
@blueprint.route('/sign-in-history', methods=["GET"])
@jwt_required(locations=["cookies"])
async def sign_in_history():
    try:
        data = get_history(request)
        return jsonify(data)
    except Exception as e:
        return jsonify({"msg": e}), 401


# Documentation
@blueprint.route('/swagger.json')
async def swagger():
    with open('core/swagger/swagger.json', 'r') as f:
        return jsonify(json.load(f))