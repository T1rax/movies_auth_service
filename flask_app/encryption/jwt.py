from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token, get_jwt
from flask_jwt_extended import JWTManager
from flask_jwt_extended import unset_jwt_cookies, set_access_cookies, set_refresh_cookies

from database.db import jwt_redis_blocklist
from datetime import datetime as dt


class JWTHelper():
    def __init__(self):
        self.user_id = "example_user"
        self.access_token = None
        self.refresh_token = None
        pass

    def set_tokens(self, response):
        set_access_cookies(response, self.access_token)
        set_refresh_cookies(response, self.refresh_token)

    def create_tokens(self):
        self.create_access()
        self.refresh_token = create_refresh_token(identity=self.user_id)
    
    def create_access(self):
        payload = {'roles': ['basicRole', 'premiumUser']}
        self.access_token = create_access_token(identity=self.user_id, additional_claims=payload)
        return self.access_token
    
    def drop_tokens(self, response):
        unset_jwt_cookies(response)

        jti = get_jwt()["jti"]
        token_exp = dt.fromtimestamp(get_jwt()["exp"])
        ex = token_exp-dt.now()

        jwt_redis_blocklist.set(jti, "", ex=ex)


jwt_helper = JWTHelper()