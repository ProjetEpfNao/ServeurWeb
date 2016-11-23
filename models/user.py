from flask_sqlalchemy import orm


def create_user_class(db):
    class User(db.Model):
        # DB Setup
        __tablename__ = "users"
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(32), unique=True)
        password = db.Column(db.String(32))
        is_robot = db.Column(db.Boolean)
        robot_id = db.Column(db.Integer,
                             db.ForeignKey('users.id'), nullable=True,
                             unique=True)
        robot = db.relationship('User', uselist=False, remote_side=[id],
                                backref=db.backref('human', uselist=False),
                                lazy='subquery')

        # Model
        ALLOWED = ["raise_arm",
                   "lower_arm",
                   "stand_up",
                   "sit_down",
                   "look_up",
                   "look_down",
                   "look_left",
                   "look_right",
                   "battery"]

        @orm.reconstructor
        def init_on_load(self):
            self.command_queue = []
            self.battery = 0.

        def append_command(self, command):
            if command not in self.ALLOWED:
                return False
            self.command_queue.append(command)
            return True

        def pop_command(self):
            if len(self.command_queue) > 0:
                return self.command_queue.pop(0)
            return None

        def purge(self):
            self.command_queue = []

    return User
