import json


class JsonFormatter(object):

    def __init__(self, indent):
        self.indent = indent

    def dumps(self, data):
        return json.dumps(data, indent=self.indent)
