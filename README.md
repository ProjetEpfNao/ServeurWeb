# REST API [![Build Status](https://travis-ci.org/ProjetEpfNao/ServeurWeb.svg?branch=master)](https://travis-ci.org/ProjetEpfNao/ServeurWeb)

## Deployed 

Add command  
POST /add_command command=COMMAND (raise_arm || lower_arm || stand_up || sit_down || look_up)  

Get last command  
GET /get_last_command  

Login  
POST /login username=USERNAME&password=PASSWORD  (test_user, test_pass)

## Not deployed

Register new user  
POST /register username=USERNAME&password=PASSWORD  

## Standard response format  

On success:  
{  
&nbsp;&nbsp;&nbsp;&nbsp;"result": "SUCCESS",  
&nbsp;&nbsp;&nbsp;&nbsp;["optionnal content": "value"]  
}  

On failure:  
{  
&nbsp;&nbsp;&nbsp;&nbsp;"result": "FAILURE",  
&nbsp;&nbsp;&nbsp;&nbsp;"error_message": "Relevant error message."  
}  

# TODO

## Sprint 1

1. ~~Add set command url~~
2. ~~Add get command url~~
3. ~~Set up CI scripts for db and env vars~~
4. ~~Write unit tests~~
5. ~~Clean up hardcoded values~~

## Sprint 2


1. ~~Add db~~  
2. ~~Add authentication request~~  
3. ~~Add sign-up request~~  
4. ~~Add session check to command urls~~  
5. ~~Add admin robot-user association~~  
5.5 Add admin dashboard  PRIORITY
6. Add robot credentials generator url  PRIORITY
7. ~~Fuse the two managers into user_manager: 1 command queue per session~~  
8. ~~Check if we need to rethink framework selection~~  
9. Add salted hashes  
10. Find HLS streaming module  
11. Register certificate  
12. Activate https  
13. Add logout route   PRIORITY  
14. Migrate to heroku  
15. Remove test interdependence
16. Add documentation
17. Test Register PRIORITY  
