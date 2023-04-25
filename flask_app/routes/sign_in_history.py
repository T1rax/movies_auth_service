from flask_jwt_extended import get_jwt
from flask import current_app

from core.errors import HistoryException
from database.db import db
from database.models import User, UserHistory
from performance.tracing.tracer import trace_it


@trace_it
def get_history(request):
    current_app.logger.info('Reading JWT')
    user_jwt = get_jwt()['userid']

    current_app.logger.info('Verifying user in DB')
    user = User.get_user_by_id(id=user_jwt)
    if 'admin' in user.roles or 'superUser' in user.roles:
        body_json = request.get_json()
        user_id = body_json.get('id')
    else:
        user_id = get_jwt()['userid']

    current_app.logger.info('Analyzing pagination parameters')
    if body_json.get('page') is not None:
        page = body_json.get('page')
    else:
        page = 1

    if body_json.get('per_page') is not None:
        per_page = body_json.get('per_page')
    else:
        per_page = 3

    current_app.logger.info('Looking for user in DB')
    history = UserHistory.get_history_by_user_id(user_id, page, per_page)

    if not history:
        current_app.logger.error('No history')
        raise HistoryException('No history')
    else:
        res = []
        for user in history:
             res.append({
                'user_id': user.user_id,
                'user_device_type': user.user_device_type,
                'useragent': user.useragent,
                'remote_addr': user.remote_addr,
                'referrer': user.referrer,
                'action': user.action.value,
                'action_time': user.timestamp,
            })
        return res


@trace_it
def add_history(request, user_id, action):
    user_history = UserHistory(user_id=str(user_id),
                               useragent=str(request.user_agent),
                               remote_addr=str(request.remote_addr),
                               referrer=str(request.referrer),
                               action=str(action))
    user_history.set_device_type()

    try:
        db.session.add(user_history)
        db.session.commit()
        return True
    except Exception as e:
        raise HistoryException('History error', e)