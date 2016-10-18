# A very simple Flask Hello World app for you to get started with...

from flask import Flask
from flask import request
from command_manager import CommandManager
from json_formatter import JsonFormatter

app = Flask(__name__)
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
