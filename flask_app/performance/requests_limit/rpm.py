from datetime import datetime as dt
from flask import request, current_app, jsonify
from flask_jwt_extended import get_jwt
from uuid import uuid4
from http import HTTPStatus

from core.config import configs
from database.db import request_limit_storage


def set_rpm_limit(app) -> None:

    @app.before_request
    def rpm_limit():

        #trying to read user_id
        try:
            user_id = get_jwt()['userid']
        except:
            user_id = request.cookies.get('anonymous_id')
            if user_id is None:
                user_id = str(uuid4())
                configs.main.pending_anonymous_id = user_id

        # For testing RPM limits could be turned off
        # Because during tests there are too many requests
        if configs.main.testing is True and request.headers.get('ignore_rpm') == 'True':
            pass
        else:
            pipe = request_limit_storage.pipeline()
            now = dt.now()

            # Key consists of user_id and current minute
            # Which allows to control rpm
            key = f'{user_id}:{now.minute}'
            # Each request increments counter
            pipe.incr(key, 1)
            # after minute key deletes
            pipe.expire(key, 59)
            result = pipe.execute()

            request_number = result[0]
            if request_number > configs.rpm.limit:
                current_app.logger.info('Requests per minute limit exceeded')
                return jsonify({"msg": 'Requests per minute limit exceeded'}), HTTPStatus.TOO_MANY_REQUESTS

        
    @app.after_request
    def set_anonymous_id(response):
        if configs.main.pending_anonymous_id is not None:
            response.set_cookie('anonymous_id', configs.main.pending_anonymous_id)
        return response