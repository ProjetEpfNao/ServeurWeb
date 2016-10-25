import rest_api


class CommandManager(object):
    ALLOWED = ["raise_arm",
               "lower_arm",
               "stand_up",
               "sit_down"]

    def __init__(self):
        self.command_queue = []

    def append_command(self, command):
        if command not in self.ALLOWED:
            return {rest_api.STATUS_KEY: rest_api.STATUS_FAILURE,
                    rest_api.ERROR_KEY: rest_api.NO_SUCH_COMMAND_ERROR}
        self.command_queue.append(command)
        return {rest_api.STATUS_KEY: rest_api.STATUS_SUCCESS}

    def pop_command(self):
        if len(self.command_queue) > 0:
            return {rest_api.STATUS_KEY: rest_api.STATUS_SUCCESS, rest_api.COMMAND_KEY: self.command_queue.pop(0)}
        return {rest_api.STATUS_KEY: rest_api.STATUS_SUCCESS, rest_api.COMMAND_KEY: ""}

    def purge(self):
        self.command_queue = []
