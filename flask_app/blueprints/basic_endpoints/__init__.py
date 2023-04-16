from flask import Blueprint, jsonify, request
import json
import click
from flask_jwt_extended import jwt_required, get_jwt
from flask import current_app

from core.errors import RegistrationException, UserIdException, LoginException, HistoryException
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
    create_superuser(name, password)
    current_app.logger.info('Superuser created')
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
    try:
        response = authorize_user(get_jwt())
        return jsonify(response), 200
    except Exception:
        return jsonify({"msg": 'Internal server error'}), 500


@from_file("core/swagger/logout.yml")
@blueprint.route('/logout', methods=["GET", "POST"])
@jwt_required(locations=["cookies"])
async def logout():
    try:
        response = jsonify({"msg": "logout successful"})
        current_app.logger.info('Dropping JWT from cookies')
        jwt_helper.drop_tokens(response)
        return response, 200
    except Exception:
        return jsonify({"msg": 'Internal server error'}), 500


@from_file("core/swagger/sign_in.yml")
@blueprint.route('/sign-in', methods=["POST"])
async def sign_in():
    try:
        user = login_user(request)
        response = jsonify({"msg": "login successful"})

        current_app.logger.info('Adding JWT to cookies')
        jwt_helper.user_id = user.id
        jwt_helper.create_tokens()
        jwt_helper.set_tokens(response)
        return response, 200
    except LoginException as e:
        return jsonify({"msg": str(e)}), 401
    except Exception as e:
        return jsonify({"msg": 'Internal server error'}), 500


@from_file("core/swagger/sign_up.yml")
@blueprint.route('/sign-up', methods=["POST"])
async def sign_up():
    try:
        data = request.get_json()
        user = register_user(data)
        response = jsonify({"msg": "registration successful"})

        current_app.logger.info('Adding JWT to cookies')
        jwt_helper.user_id = user.id
        jwt_helper.create_tokens()
        jwt_helper.set_tokens(response)
        return response, 200
    except RegistrationException as e:
        return jsonify({"msg": str(e)}), 401
    except Exception:
        return jsonify({"msg": 'Internal server error'}), 500


# Token-related routes
@from_file("core/swagger/refresh.yml")
@blueprint.route('/refresh', methods=["POST"])
@jwt_required(refresh=True, locations=["cookies"])
async def refresh():
    try:
        response = jsonify({"msg": "tokens refreshed"})
        
        current_app.logger.info('Adding JWT to cookies')
        jwt_helper.create_tokens()
        jwt_helper.set_tokens(response)
        return response, 200
    except Exception:
        return jsonify({"msg": 'Internal server error'}), 500


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
    except Exception:
        return jsonify({"msg": 'Internal server error'}), 500


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
    except Exception:
        return jsonify({"msg": 'Internal server error'}), 500


@from_file("core/swagger/sign_in_history.yml")
@blueprint.route('/sign-in-history', methods=["GET"])
@jwt_required(locations=["cookies"])
async def sign_in_history():
    try:
        data = get_history(request)
        return jsonify(data)
    except HistoryException as e:
        return jsonify({"msg": str(e)}), 500
    except Exception:
        return jsonify({"msg": 'Internal server error'}), 500


# Documentation
@blueprint.route('/swagger.json')
async def swagger():
    try:
        with open('core/swagger/swagger.json', 'r') as f:
            return jsonify(json.load(f))
    except Exception:
        return jsonify({"msg": 'Internal server error'}), 500