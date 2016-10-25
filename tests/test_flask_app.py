import os
import flask_app
import unittest
import tempfile
import json
import rest_api

TEST_COMMAND_ALLOWED = "test_command_allowed"
TEST_COMMAND_NOT_ALLOWED = "test_command_not_allowed"
ENCODING = "utf8"


class TestFlaskApp(unittest.TestCase):

    def decode_json(self, result):
        return json.loads(result.data.decode(ENCODING))

    def setUp(self):
        flask_app.app.config['TESTING'] = True
        flask_app.server.ALLOWED.append(TEST_COMMAND_ALLOWED)
        self.app = flask_app.app.test_client()

    def tearDown(self):
        flask_app.app.clean()

    def test_add_command_success(self):
        result = self.app.post(rest_api.ADD_COMMAND_EXT,
                               data=dict(command=TEST_COMMAND_ALLOWED))
        assert result.status_code == 200
        content = json.loads(result.data.decode('utf8'))
        assert content[rest_api.STATUS_KEY] == rest_api.STATUS_SUCCESS

    def test_add_command_not_allowed(self):
        result = self.app.post(rest_api.ADD_COMMAND_EXT,
                               data=dict(command=TEST_COMMAND_NOT_ALLOWED))
        assert result.status_code == 200
        content = json.loads(result.data.decode('utf8'))
        assert content[rest_api.STATUS_KEY] == rest_api.STATUS_FAILURE
        assert content[rest_api.ERROR_KEY] == rest_api.NO_SUCH_COMMAND_ERROR

    def test_get_last_command_success(self):
        self.app.post(rest_api.ADD_COMMAND_EXT,
                      data=dict(command=TEST_COMMAND_ALLOWED))
        result = self.app.get(rest_api.GET_LAST_COMMAND_EXT)
        assert result.status_code == 200
        content = json.loads(result.data.decode('utf8'))
        assert content[rest_api.STATUS_KEY] == rest_api.STATUS_SUCCESS
        assert content[rest_api.COMMAND_KEY] == TEST_COMMAND_ALLOWED

    def test_get_last_command_no_command(self):
        result = self.app.get(rest_api.GET_LAST_COMMAND_EXT)
        assert result.status_code == 200
        content = json.loads(result.data.decode('utf8'))
        assert content[rest_api.STATUS_KEY] == rest_api.STATUS_SUCCESS
        assert content[rest_api.COMMAND_KEY] == ""

if __name__ == "__main__":
    unittest.main()
