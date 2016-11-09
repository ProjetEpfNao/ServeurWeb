# A very simple Flask Hello World app for you to get started with...

from flask import Flask
from flask import flash
from flask import request
from flask import session
from flask import make_response
from flask import render_template
from flask import redirect
from flask import url_for
from flask_sqlalchemy import SQLAlchemy
from command_manager import CommandManager
from json_formatter import JsonFormatter
from user_manager import UserManager
from streamer import Streamer
import rest_api
import models.user
import config
import os
import sys
import uuid

# CHECK ENV
if 'FLASK_ENV' not in os.environ:
    raise ValueError('FLASK_ENV variable not set. Set to DEV or TEST.')

env = os.environ['FLASK_ENV']
if env == 'DEV':
    import config.dev as config
elif env == 'TEST':
    import config.test as config
else:
    raise ValueError('Wrong FLASK_ENV value. Set to DEV or TEST.')

AUTH_ON = False

# START APP
app = Flask(__name__)

# DATABASE CONFIG
SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}'.format(
    username=config.db_user,
    password=config.db_password,
    hostname=config.db_host,
    databasename=config.db_name)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_POOL_RECYCLE'] = 299
app.config['SECRET_KEY'] = config.secret_key
db = SQLAlchemy(app)


def fill_db():
    with app.open_resource('static/seeds.sql', mode='r') as f:
        sql = f.read()
    for statement in sql.split(";")[:-1]:
        db.session.execute(statement)
    db.session.commit()

# INIT MODELS
User = models.user.create_user_class(db)

# SERVER START
users = UserManager(db, User)
json = JsonFormatter(indent=4)
streamer = Streamer()


@app.route('/')
def hello_world():
    flash("test flash message")
    return render_template("layout.html", users=users)


@app.route('/login_page', methods=['GET', 'POST'])
def login_page():
    if request.method == 'GET':
        return render_template("login.html", users=users)
    if request.method == 'POST':
        login()
        return redirect(url_for("user_page"))

@app.route('/user_page')
def user_page():
    user = users.get_user_by_session(session)
    robot = users.get_robot(user)
    return render_template("user.html", users=users, robot=robot)

@app.route('/logout_page', methods=['GET', 'POST'])
def logout_page():
    return render_template("logout.html", users=users)


@app.route('/register_page', methods=['GET', 'POST'])
def register_page():
    return render_template("register.html", users=users)


@app.route(rest_api.ADD_COMMAND_EXT, methods=['POST'])
def append_command():
    # Get user
    user = users.get_user_by_session(session)
    if not user:
        return rest_api.UNAUTH_RESPONSE, 401
    if user.is_robot:
        return rest_api.FORBID_RESPONSE, 403

    # Try to append command
    command = request.form[rest_api.COMMAND_KEY]
    command_added = user.append_command(command)

    # Format response
    if command_added:
        result = {rest_api.STATUS_KEY: rest_api.STATUS_SUCCESS}
    else:
        result = {rest_api.STATUS_KEY: rest_api.STATUS_FAILURE,
                  rest_api.ERROR_KEY: rest_api.NO_SUCH_COMMAND_ERROR}
    return json.dumps(result)


@app.route(rest_api.GET_LAST_COMMAND_EXT, methods=['GET'])
def get_command():
    # Get user and make sure it's a robot
    robot = users.get_user_by_session(session)
    if not robot:
        return rest_api.UNAUTH_RESPONSE, 401
    if not robot.is_robot:
        return rest_api.FORBID_RESPONSE, 403

    # Get his human's command
    human = users.get_human(robot)
    command = human.pop_command()

    # Format response
    if command:
        result = {rest_api.STATUS_KEY: rest_api.STATUS_SUCCESS,
                  rest_api.COMMAND_KEY: command}
    else:
        result = {rest_api.STATUS_KEY: rest_api.STATUS_SUCCESS,
                  rest_api.COMMAND_KEY: ""}
    return json.dumps(result)


@app.route(rest_api.REGISTER_EXT, methods=['POST'])
def register():
    result = users.add_user(request.form[rest_api.USERNAME_KEY],
                            request.form[rest_api.PASSWORD_KEY],
                            request.form[rest_api.ROBOT_KEY])
    return json.dumps({rest_api.STATUS_KEY: rest_api.STATUS_SUCCESS})


@app.route("/check_login")
def check_login():
    user = users.get_user_by_session(session)
    if user:
        return "You're logged in as " + str(user) + "."
    else:
        return "You're not logged in."


@app.route(rest_api.LOGIN_EXT, methods=['POST'])
def login():
    username = request.form[rest_api.USERNAME_KEY]
    password = request.form[rest_api.PASSWORD_KEY]
    user = users.get_user(username, password)
    if user:
        resp = make_response(json.dumps(
            {rest_api.STATUS_KEY: rest_api.STATUS_SUCCESS}))
        session_id = str(uuid.uuid4())
        users.set_user_session(user, session_id)
        session[rest_api.COOKIE_KEY] = session_id
        return resp
    return json.dumps({rest_api.STATUS_KEY: rest_api.STATUS_FAILURE,
                       rest_api.ERROR_KEY: rest_api.INCORRECT_CREDENTIALS_ERROR})


def feed(streamer):
    while True:
        data = streamer.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        time.sleep(0.1)


@app.route(rest_api.STREAM_EXT, methods=['GET', 'POST'])
def stream():
    if request.method == 'POST':
        streamer.add_frame(request.data)
        return json.dumps({rest_api.STATUS_KEY: rest_api.STATUS_SUCCESS})
    if request.method == 'GET':
        return Response(feed(streamer),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
