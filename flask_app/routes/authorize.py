from flask import current_app
from performance.tracing.tracer import trace_it


@trace_it
def authorize_user(jwt_token):
    current_app.logger.info('Reading JWT')

    response = {'msg': 'User authorized',
                'first_name': jwt_token.get('first_name'),
                'last_name': jwt_token.get('last_name'),
                'roles': jwt_token.get('roles'),}
    
    return response