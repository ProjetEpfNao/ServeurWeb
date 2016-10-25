# REST API

## Deployed 

Add command  
POST /add_command command=COMMAND_NAME  
&nbsp;&nbsp;&nbsp;&nbsp;Allowed:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;raise_arm  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;lower_arm  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;stand_up  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;sit_down  

Get last command  
GET /get_last_command  

## Not deployed

Register new user  
POST /register username=USERNAME&password=PASSWORD  

Login  
POST /login username=USERNAME&password=PASSWORD  

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
4. Add session check to command urls
5. Add admin robot-user association dashboard
6. Add robot credentials generator url
7. Fuse the two managers into user_manager: 1 command queue per session
8. Check if we need to rethink framework selection
9. Add salted hashes, drop users
10. Find HLS streaming module
11. Register certificate
12. Activate https
