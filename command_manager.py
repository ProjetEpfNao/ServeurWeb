

class CommandManager(object):

    def __init__(self):
        self.command_queue = []

    def append_command(self, command):
        self.command_queue.append(command)
        return {"result": "OK"}

    def pop_command(self):
        if len(self.command_queue) > 0:
            return {"result": "SUCCESS", "command": self.command_queue.pop(0)}
        return {"result": "SUCCESS", "command": ""}
