from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from jwt import decode as jwt_decode
from django.conf import settings
from urllib.parse import parse_qs
from server.jornal_app.services.users import get_user_by_id
from channels.db import database_sync_to_async


@database_sync_to_async
def get_user(decoded_data):
    """
    get_user from token
    """
    try:
        return get_user_model().objects.get(id=decoded_data["user_id"])
    except (InvalidToken, TokenError, get_user_model().DoesNotExist):
        return AnonymousUser()


class TokenAuthMiddleware:
    """
    Custom token auth middleware
    """
 
    def __init__(self, inner):
        # Store the ASGI application we were passed
        self.inner = inner
 
    async def __call__(self, scope, receive, send):
 
        # Close old database connections to prevent usage of timed out connections
        close_old_connections()
 
        # Get the token
        token = parse_qs(scope["query_string"].decode("utf8"))["token"][0].replace('Bearer ', '') 
        # Try to authenticate the user
        try:
            # This will automatically validate the token and raise an error if token is invalid
            UntypedToken(token)
        except (InvalidToken, TokenError) as e:
            # Token is invalid
            print(e)
        else:
            #  Then token is valid, decode it
            decoded_data = jwt_decode(token, settings.SECRET_KEY, algorithms=["HS256"])

            user = await get_user(decoded_data)
            scope["user"] = user

        return await self.inner(scope, receive, send)
    
