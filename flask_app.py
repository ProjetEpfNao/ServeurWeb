# A very simple Flask Hello World app for you to get started with...

from flask import Flask
from flask import request
from flask import session
from flask import make_response
from flask_sqlalchemy import SQLAlchemy
from command_manager import CommandManager
from json_formatter import JsonFormatter
from user_manager import UserManager
import models.user
import config
import os
import sys
import uuid

# DETERMINE ENV
if 'FLASK_ENV' not in os.environ:
    raise ValueError('FLASK_ENV variable not set. Set to DEV or TEST.')

env = os.environ['FLASK_ENV']
if env == 'DEV':
    import config.dev as config
elif env == 'TEST':
    import config.test as config
else:
    raise ValueError('Wrong FLASK_ENV value. Set to DEV or TEST.')

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
db = SQLAlchemy(app)

# INIT MODELS
User = models.user.create_user_class(db)

# SERVER START
users = UserManager(db, User)
server = CommandManager()
json = JsonFormatter(indent=4)


@app.route('/')
def hello_world():
    return 'Hello from Flask!'


@app.route('/add_command', methods=['POST'])
def append_command():
    command = request.form["command"]
    result = server.append_command(command)
    return json.dumps(result)


@app.route('/get_last_command', methods=['GET'])
def get_command():
    result = server.pop_command()
    return json.dumps(result)


@app.route('/register', methods=['POST'])
def register():
    result = users.add_user(request.form["username"], request.form["password"])
    return json.dumps(result)


@app.route('/login', methods=['POST'])
def login():
    username, password = request.form["username"], request.form["password"]
    result = users.get_user(username, password)
    if result:
        resp = make_response(json.dumps({"result": "SUCCESS"}))
        session_id = str(uuid.uuid4())
        users.set_user_session(username, session_id)
        session['session-id'] = session_id
        return resp
    return json.dumps({"result": "FAILURE"})
