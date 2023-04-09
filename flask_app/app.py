import sys
sys.path.insert(0, '/home/tirax/movies_auth_service')

from flask import Flask
from flask import jsonify
from database.db import init_db, jwt_redis_blocklist
from core.flask_configuration import set_flask_configuration

from datetime import datetime
from datetime import timedelta
from datetime import timezone

from flask_jwt_extended import jwt_required, get_jwt
from flask_jwt_extended import JWTManager
from flask_jwt_extended import set_access_cookies, set_refresh_cookies
from flask_jwt_extended import get_jwt_identity

from encryption.jwt import jwt_helper

app = Flask(__name__)

set_flask_configuration(app)

jwt = JWTManager(app)


#JWT tokens
# Using an `after_request` callback, we refresh any token that is within 30
# minutes of expiring. Change the timedeltas to match the needs of your application.
@app.after_request
@jwt_required(refresh=True, locations=["cookies"])
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token, refresh_token = jwt_helper.create_tokens()
            set_access_cookies(response, access_token)
            set_refresh_cookies(response, refresh_token)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original response
        return response


# Callback function to check if a JWT exists in the redis blocklist
@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    token_in_redis = jwt_redis_blocklist.get(jti)
    return token_in_redis is not None


# Test pages
@app.route('/', methods=["GET", "POST"])
async def main_page():
    return 'Hello, World!'    


# Account authorization routes
from routes.authorize import authorize_user

@app.route('/authorize', methods=["GET", "POST"])
@jwt_required(locations=["cookies"])
async def authorize():
    current_user = get_jwt_identity()
    exp_timestamp = get_jwt()["exp"]
    return jsonify(logged_in_as=current_user,exp_timestamp=exp_timestamp), 200


@app.route('/logout', methods=["GET", "POST"])
@jwt_required(locations=["cookies"])
async def logout():
    response = jsonify({"msg": "logout successful"})
    jwt_helper.drop_tokens(response)
    return response


@app.route('/sign-in', methods=["GET", "POST"])
async def sign_in():
    response = jsonify({"msg": "login successful"})
    # access_token = create_access_token(identity="example_user")
    jwt_helper.create_tokens()
    jwt_helper.set_tokens(response)
    return response


@app.route('/sign-up', methods=["GET", "POST"])
async def sign_up():
    response = jsonify({"msg": "registration successful"})
    jwt_helper.create_tokens()
    jwt_helper.set_tokens(response)
    return response



# Token-related routes
# from routes. import
@app.route('/refresh', methods=["GET", "POST"])
@jwt_required(refresh=True, locations=["cookies"])
async def refresh():
    response = jsonify({"msg": "tokens refreshed"})
    jwt_helper.create_tokens()
    jwt_helper.set_tokens(response)
    return response


# Roles routes
# from routes. import
@app.route('/change-role', methods=["GET", "POST"])
async def change_role():
    return 'Hello, World! change-role'


# Support routes
# from routes. import
@app.route('/get-user-description', methods=["GET"])
async def get_user_description():
    return 'Hello, World! get-user-description'


@app.route('/sign-in-history', methods=["GET"])
async def sign_in_history():
    return 'Hello, World! sign-in-history'


def main():
    init_db(app)
    app.run()


if __name__ == '__main__':
    main() 