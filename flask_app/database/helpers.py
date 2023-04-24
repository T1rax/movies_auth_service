from database.models import User, UserHistory
from performance.tracing.tracer import trace_it


class User_helper():
    def __init__(self):
        self.model = User     

    @trace_it
    def get_user_by_id(self, id):
        return self.model.query.filter_by(id=id).first()
    
    @trace_it
    def get_user_by_login(self, login):
        return self.model.query.filter_by(login=login).first()
    

user_helper = User_helper()


class History_helper():
    def __init__(self):
        self.model = UserHistory     

    @trace_it
    def get_history_by_user_id(self, user_id, page, per_page):
        return self.model.query.filter_by(user_id=user_id).paginate(page=page, per_page=per_page)
    

history_helper = History_helper()