import os
import flask_app
import unittest
import tempfile
import json
import rest_api
import sys

TEST_COMMAND_ALLOWED = flask_app.User.ALLOWED[0]
TEST_COMMAND_NOT_ALLOWED = "test_command_not_allowed"
TEST_USER = "test_user"
TEST_USER_PASSWORD = "test_password"
TEST_WRONG_PASSWORD = "test_wrong_password"
TEST_ROBOT = "test_robot"
TEST_ROBOT_PASSWORD = "test_password2"
SESSION_COOKIE = "session"
ENCODING = "utf8"


class TestFlaskApp(unittest.TestCase):

    # HELPERS

    def decode_json(self, result):
        return json.loads(result.data.decode(ENCODING))

    def login_as_user(self):
        return self.app.post(rest_api.LOGIN_EXT,
                             data=dict(username=TEST_USER, password=TEST_USER_PASSWORD))

    def login_as_robot(self):
        return self.app.post(rest_api.LOGIN_EXT,
                             data=dict(username=TEST_ROBOT, password=TEST_ROBOT_PASSWORD))

    def setUpClass():
        flask_app.db.drop_all()

    def setUp(self):
        self.db_fd, flask_app.app.config['DATABASE'] = tempfile.mkstemp()
        flask_app.app.config['TESTING'] = True
        self.app = flask_app.app.test_client()
        with flask_app.app.app_context():
            flask_app.db.create_all()
            flask_app.fill_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(flask_app.app.config['DATABASE'])
        with flask_app.app.app_context():
            flask_app.db.drop_all()
            flask_app.users.clean_sessions()

    def test_login_success(self):
        result = self.login_as_user()
        assert result.status_code == 200
        content = self.decode_json(result)

        assert content[rest_api.STATUS_KEY] == rest_api.STATUS_SUCCESS
        cookie = result.headers.get('Set-Cookie')
        assert cookie != None
        assert SESSION_COOKIE in cookie

    def test_login_wrong_creds(self):
        result = self.app.post(rest_api.LOGIN_EXT,
                               data=dict(username=TEST_USER, password=TEST_WRONG_PASSWORD))
        assert result.status_code == 200
        content = self.decode_json(result)
        assert content[rest_api.STATUS_KEY] == rest_api.STATUS_FAILURE

    def test_append_command_success(self):
        self.login_as_user()
        result = self.app.post(rest_api.ADD_COMMAND_EXT,
                               data=dict(command=TEST_COMMAND_ALLOWED))
        assert result.status_code == 200
        content = self.decode_json(result)
        assert content[rest_api.STATUS_KEY] == rest_api.STATUS_SUCCESS

    def test_append_command_no_auth(self):
        result = self.app.post(rest_api.ADD_COMMAND_EXT,
                               data=dict(command=TEST_COMMAND_ALLOWED))
        assert result.status_code == 401
        assert result.data.decode(ENCODING) == rest_api.UNAUTH_RESPONSE

    def test_append_command_forbidden_user(self):
        self.login_as_robot()
        result = self.app.post(rest_api.ADD_COMMAND_EXT,
                               data=dict(command=TEST_COMMAND_ALLOWED))
        assert result.status_code == 403
        assert result.data.decode(ENCODING) == rest_api.FORBID_RESPONSE

    def test_append_command_not_allowed(self):
        self.login_as_user()
        result = self.app.post(rest_api.ADD_COMMAND_EXT,
                               data=dict(command=TEST_COMMAND_NOT_ALLOWED))
        assert result.status_code == 200
        content = self.decode_json(result)
        assert content[rest_api.STATUS_KEY] == rest_api.STATUS_FAILURE
        assert content[rest_api.ERROR_KEY] == rest_api.NO_SUCH_COMMAND_ERROR

    def test_get_last_command_success(self):
        self.login_as_user()
        result = self.app.post(rest_api.ADD_COMMAND_EXT,
                               data=dict(command=TEST_COMMAND_ALLOWED))
        self.login_as_robot()
        result = self.app.get(rest_api.GET_LAST_COMMAND_EXT)
        assert result.status_code == 200
        content = self.decode_json(result)
        assert content[rest_api.STATUS_KEY] == rest_api.STATUS_SUCCESS
        assert content[rest_api.COMMAND_KEY] == TEST_COMMAND_ALLOWED

    def test_get_last_command_no_command(self):
        self.login_as_robot()
        result = self.app.get(rest_api.GET_LAST_COMMAND_EXT)
        assert result.status_code == 200
        content = self.decode_json(result)
        assert content[rest_api.STATUS_KEY] == rest_api.STATUS_SUCCESS
        assert content[rest_api.COMMAND_KEY] == ""

    def test_get_last_command_no_auth(self):
        result = self.app.get(rest_api.GET_LAST_COMMAND_EXT)
        assert result.status_code == 401
        assert result.data.decode(ENCODING) == rest_api.UNAUTH_RESPONSE

    def test_get_last_command_forbidden(self):
        self.login_as_user()
        result = self.app.get(rest_api.GET_LAST_COMMAND_EXT)
        assert result.status_code == 403
        assert result.data.decode(ENCODING) == rest_api.FORBID_RESPONSE

if __name__ == "__main__":
    unittest.main()
