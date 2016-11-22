curl --data "username=test_user&password=test_password" localhost:5000/login -D - -c mycookie
curl localhost:5000/check_login -c mycookie -b mycookie
curl --data "command=stand_up" localhost:5000/add_command -c mycookie -b mycookie
curl --data "username=test_robot&password=test_password2" localhost:5000/login -D - -c mycookierobot
curl localhost:5000/check_login -c mycookierobot -b mycookierobot
curl localhost:5000/get_last_command -c mycookierobot -b mycookierobot
