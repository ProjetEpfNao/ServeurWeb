import rest_api
from sqlalchemy.orm import subqueryload


class UserManager(object):

    def __init__(self, db, User):
        self.db = db
        self.User = User
        self.sessions = {}

    def add_user(self, username, password, is_robot=False):
        print(is_robot)
        user = self.User(username=username,
                         password=password, is_robot=is_robot)
        self.db.session.add(user)
        self.db.session.commit()

    def add_robot_to_user(self, user, robot):
        user.robot_id = robot.id
        robot.human = user
        self.db.session.merge(user)
        self.db.session.commit()

        # Hack to reinit session binding with user
        # TODO: remove this hack when it's not 6am
        for sess in self.sessions:
            if self.sessions[sess] == user:
                break
        self.sessions[sess] = self.get_user(user.username, user.password)

    def get_user(self, username, password):
        return self.User.query.options(subqueryload(self.User.robot)).filter_by(username=username, password=password).first()

    def get_robot_by_username(self, username):
        return self.User.query.filter_by(username=username).first()

    def get_free_robots(self):
        humans = self.User.query.all()
        owned_robot_ids = [human.robot_id for human in humans]
        robots = self.User.query.filter_by(is_robot=True)
        return [robot for robot in robots if robot.id not in owned_robot_ids]

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

    def set_user_session(self, user, session_id):
        self.sessions[session_id] = user

    def get_user_by_session(self, session):
        if rest_api.COOKIE_KEY in session:
            session_id = session[rest_api.COOKIE_KEY]
            if session_id in self.sessions:
                return self.sessions[session_id]
        return None

    def clean_sessions(self):
        self.sessions = {}
