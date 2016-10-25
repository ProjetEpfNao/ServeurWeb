

class UserManager(object):

    def __init__(self, db, User):
        self.db = db
        self.User = User
        self.sessions = {}

    def add_user(self, username, password):
        comment = self.User(username=username, password=password)
        self.db.session.add(comment)
        self.db.session.commit()
        return {'result': 'SUCCESS'}

    def get_user(self, username, password):
        return self.User.query.filter_by(username=username, password=password).first()

    def set_user_session(self, username, session_id):
        self.sessions[session_id] = username

    def has_session(self, username):
        return username in self.sessions
