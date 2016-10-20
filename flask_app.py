# A very simple Flask Hello World app for you to get started with...

from flask import Flask
from flask import request
from flask import session
from flask import make_response
from flask_sqlalchemy import SQLAlchemy
from command_manager import CommandManager
from json_formatter import JsonFormatter
from user_manager import UserManager
import rest_api
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

def clean_app():
    server.purge()
app.clean = clean_app



@app.route('/')
def hello_world():
    return str(server.command_queue)


@app.route(rest_api.ADD_COMMAND_EXT, methods=['POST'])
def append_command():
    command = request.form[rest_api.COMMAND_KEY]
    result = server.append_command(command)
    return json.dumps(result)


@app.route(rest_api.GET_LAST_COMMAND_EXT, methods=['GET'])
def get_command():
    result = server.pop_command()
    return json.dumps(result)


@app.route(rest_api.REGISTER_EXT, methods=['POST'])
def register():
    result = users.add_user(request.form[rest_api.USERNAME_KEY], request.form[rest_api.PASSWORD_KEY])
    return json.dumps(result)


@app.route(rest_api.LOGIN_EXT, methods=['POST'])
def login():
    username, password = request.form[rest_api.USERNAME_KEY], request.form[rest_api.PASSWORD_KEY]
    result = users.get_user(username, password)
    if result:
        resp = make_response(json.dumps({rest_api.STATUS_KEY: rest_api.STATUS_SUCCESS}))
        session_id = str(uuid.uuid4())
        users.set_user_session(username, session_id)
        session[rest_api.COOKIE_KEY] = session_id
        return resp
    return json.dumps({rest_api.STATUS_KEY: rest_api.STATUS_FAILURE})
