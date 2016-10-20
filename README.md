# REST API

## Deployed 

Add command  
POST /add_command command=COMMAND_NAME  

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
3. ~~Add db~~
4. ~~Add authentication request~~
5. ~~Add sign-up request~~
6. Add session check to command urls
7. Add admin robot-user association dashboard
8. Add robot credentials generator url
9. Set up CI scripts for db and env vars
10. Write unit tests
11. ~~Clean up hardcoded values~~
12. Fuse the two managers into user_manager: 1 command queue per session

## Sprint 2

1. Check if we need to rethink framework selection
2. Add salted hashes, drop users
3. Find HLS streaming module
4. Register certificate
5. Activate https
