
# GENERIC CONTENT
STATUS_KEY = "result"
STATUS_SUCCESS = "SUCCESS"
STATUS_FAILURE = "FAILURE"
ERROR_KEY = "error_message"

# COMMAND CONTENT
COMMAND_KEY = "command"
CONTENT_KEY = "content"
ADD_COMMAND_EXT = "/add_command"
GET_LAST_COMMAND_EXT = "/get_last_command"
UPDATE_BATTERY_INFO = "/update_battery_info"
BATTERY_KEY = "battery"

# ACCOUNT CONTENT
REGISTER_EXT = "/register"
LOGIN_EXT = "/login"
COOKIE_KEY = "session-id"
USERNAME_KEY = "username"
PASSWORD_KEY = "password"
ROBOT_KEY = "is_robot"

# STREAM (deprecated)
STREAM_EXT = "/stream"

# ERRORS
NO_SUCH_COMMAND_ERROR = "No such command."
INCORRECT_CREDENTIALS_ERROR = "Incorrect credentials."
NO_OWNER = "This robot has no owner."

# HTTP CODES
UNAUTH_RESPONSE = "401 Unauthorized"
FORBID_RESPONSE = "403 Forbidden"
