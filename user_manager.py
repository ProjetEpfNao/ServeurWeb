import rest_api


class UserManager(object):

    def __init__(self, db, User):
        self.db = db
        self.User = User
        self.sessions = {}

    def add_user(self, username, password):
        user = self.User(username=username, password=password)
        self.db.session.add(user)
        self.db.session.commit()
        return {'result': 'SUCCESS'}

    def get_user(self, username, password):
        return self.User.query.filter_by(username=username, password=password).first()

    def get_robot(self, human_user):
        return self.get_associate(human_user)

    def get_human(self, robot_user):
        return self.get_associate(robot_user)

    def get_associate(self, user):
        if user.is_robot:
            # Return loaded user instance if it's our sessions
            for sess in self.sessions:
                logged_user = self.sessions[sess]
                if logged_user.robot_id == user.id:
                    return logged_user
            # Otherwise load it from db
            return self.User.query.filter_by(robot_id=user.id).first()
        else:
            return user.robot

    def set_user_session(self, username, session_id):
        self.sessions[session_id] = username

    def get_user_by_session(self, session):
        if rest_api.COOKIE_KEY in session:
            session_id = session[rest_api.COOKIE_KEY]
            if session_id in self.sessions:
                return self.sessions[session_id]
        return None

    def clean_sessions(self):
        self.sessions = {}
