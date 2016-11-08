#!/bin/bash
curl --data "username=test_user&password=test_password" etiennedesticourt.pythonanywhere.com/login -D - -c mycookie
curl etiennedesticourt.pythonanywhere.com/check_login -c mycookie -b mycookie
curl --data "command=stand_up" etiennedesticourt.pythonanywhere.com/add_command -c mycookie -b mycookie
curl --data "username=test_robot&password=test_password2" etiennedesticourt.pythonanywhere.com/login -D - -c mycookierobot
curl etiennedesticourt.pythonanywhere.com/check_login -c mycookierobot -b mycookierobot
curl etiennedesticourt.pythonanywhere.com/get_last_command -c mycookierobot -b mycookierobot
