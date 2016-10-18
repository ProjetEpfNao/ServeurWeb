# A very simple Flask Hello World app for you to get started with...

from flask import Flask
from flask import request
from command_manager import CommandManager

app = Flask(__name__)
server = CommandManager()


@app.route('/')
def hello_world():
    return 'Hello from Flask!'


@app.route('/add_command', methods=['POST'])
def append_command():
    command = request.form["command"]
    return server.append_command(command)


@app.route('/get_last_command', methods=['GET'])
def get_command():
    return server.pop_command()
