from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token, get_jwt
from flask_jwt_extended import unset_jwt_cookies, set_access_cookies, set_refresh_cookies

from flask_jwt_extended import get_jwt, get_jwt_header
from flask_jwt_extended import JWTManager

from datetime import datetime
from datetime import timedelta
from datetime import timezone

from database.db import db, jwt_redis_blocklist
from datetime import datetime as dt
from database.models import User
from performance.tracing.tracer import trace_it


class JWTHelper():
    def __init__(self):
        self.user_id = "example_user"
        self.user = None
        self.access_token = None
        self.refresh_token = None
        pass

    @trace_it
    def get_additional_claims(self):
        user = User.query.filter_by(id=self.user_id).first()
        return {
            "roles": user.roles,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }

    @trace_it
    def set_tokens(self, response):
        set_access_cookies(response, self.access_token)
        set_refresh_cookies(response, self.refresh_token)

    @trace_it
    def create_tokens(self):
        claims = self.get_additional_claims()
        self.access_token = create_access_token(identity=self.user_id, additional_claims=claims)
        self.refresh_token = create_refresh_token(identity=self.user_id)

    @trace_it
    def drop_tokens(self, response):
        unset_jwt_cookies(response)

        jti = get_jwt()["jti"]
        token_exp = dt.fromtimestamp(get_jwt()["exp"])
        ex = token_exp-dt.now()

        jwt_redis_blocklist.set(jti, "", ex=ex)


jwt_helper = JWTHelper()


def create_jwt(app):

    jwt = JWTManager(app)

    #JWT tokens
    # Using an `after_request` callback, we refresh any token that is within 10
    # minutes of expiring.
    @app.after_request
    def refresh_expiring_jwts(response):
        try:
            exp_timestamp = get_jwt()["exp"]
            now = datetime.now(timezone.utc)
            target_timestamp = datetime.timestamp(now + timedelta(minutes=10))
            if target_timestamp > exp_timestamp:
                if not check_if_token_is_revoked(get_jwt_header(), get_jwt()):
                    jwt_helper.create_tokens()
                    jwt_helper.set_tokens(response)
            return response
        except (RuntimeError, KeyError):
            # Case where there is not a valid JWT. Just return the original response
            return response


    # Callback function to check if a JWT exists in the redis blocklist
    # Applies for every call of @jwt_required
    @jwt.token_in_blocklist_loader
    def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
        jti = jwt_payload["jti"]
        token_in_redis = jwt_redis_blocklist.get(jti)
        return token_in_redis is not None
    
    return jwt