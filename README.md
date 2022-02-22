# Description:
    -A social media web-application with Django.

# Features:
- Sign Up, Login, OAuth 2.0(Google, Github), Logout, Forgot Password
- CRUDS For Posts `[CREATE, DELETE, UPDATE, RETRIEVE]`
    POST, COMMENT, REPLY, LIKE, SHARE

- CRUDS For Pages`[CREATE, DELETE, UPDATE, RETRIEVE]`
    POST, COMMENT, REPLY, LIKE, SHARE

- Add, Remove, Get Posts to Bookmarks
- Like a Comment
- Add Friend
- UnFriend
- Cancel a Friend Request
- Accept a Friend Request
- Hide Email Address
- Private/Public Account
- Enable/Disable Active Status (Online/Offline)
- User Profile
- User Edit Profile
- Chat with Friends (using django channels)
- Block, UnBlock User
- Follow, UnFollow User
- Follow, UnFollow Page
- Page Users Permissions `[ADMIN, AUTHOR, CREATORS]`
- Search For New Friends
- Mutual Friends
- User Settings Table `[language, Other Messages, Hide Friends]`
- User Work Experience Table
- User School Table
User University Table


# Authentication used:
- Djangorestframework-simpleJWT



# Installation
There is a few packages were used in this application such as:
djangorestframework, django-channels, djangorestframework-simpleJWT, channels-redis

if you faced a problem loading these packages try to install them using requirements.txt file using this command.
- pip install -r requirements.txt

# After Installation
- You have to create environment and this is the first step, check command below
    * for windows try tio use this "python -m venv (name_of_env)"
    - To activate it use ".\Scripts\activate"
    * for mac try tio use this "python3 -m venv (name_of_env)"
    - To activate it use "source (name_of_env)/bin/activate"

- After using commands above you just have to use `[python manage.py migrate]` then `[python manage.py runserver]`
- Go to `[http://127.0.0.1:8000/swagger/]` and use `[http://127.0.0.1:8000/api/auth/sign-up/]` endpoint to register a new account on our system
- Go to `[http://127.0.0.1:8000/swagger/]` and use `[http://127.0.0.1:8000/api/auth/sign-in/]` endpoint to take a token
- Put your `Bearer {token}` in authorization button to take access on all of endpoints except ADMIN endpoint

# Note
- Feel free to contact me if there are any problem 
- To try Real Time Part you have to install redis 5 or above then use `[redis-server]` in another CMD, # working on
- Still work on OAuth 2.0(Google, Github) part right now
