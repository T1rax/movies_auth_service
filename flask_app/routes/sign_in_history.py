from core.errors import HistoryException, UserIdException
from database.db import db
from database.models import User, UserHistory
from core.config import configs


def get_history(request):
    body_json = request.get_json()
    user_id = body_json.get('id')
    user = UserHistory.query.filter_by(user_id=user_id).first()

    if not user:
        raise UserIdException('invalid ID')
    else:
        return {
            'user_id': user.user_id,
            'useragent': user.useragent,
            'remote_addr': user.remote_addr,
            'referrer': user.referrer,
            'action': user.action.value,
        }


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