from flask_jwt_extended import get_jwt

from core.errors import HistoryException
from database.db import db
from database.models import User, UserHistory


def get_history(request):
    user_jwt = get_jwt()['userid']
    user = User.query.filter_by(id=user_jwt).first()
    if 'admin' in user.roles or 'superUser' in user.roles:
        body_json = request.get_json()
        user_id = body_json.get('id')
    else:
        user_id = get_jwt()['userid']

    history = UserHistory.query.filter_by(user_id=user_id)

    if not history:
        raise HistoryException('No history')
    else:
        res = []
        for user in history:
             res.append({
                'user_id': user.user_id,
                'useragent': user.useragent,
                'remote_addr': user.remote_addr,
                'referrer': user.referrer,
                'action': user.action.value,
                'action_time': user.timestamp,
            })
        return res


def add_history(request, user_id, action):
    user_history = UserHistory(user_id=str(user_id),
                               useragent=str(request.user_agent),
                               remote_addr=str(request.remote_addr),
                               referrer=str(request.referrer),
                               action=str(action))

    try:
        db.session.add(user_history)
        db.session.commit()
        return True
    except Exception as e:
        raise HistoryException('History error', e)