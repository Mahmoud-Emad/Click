from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from server.jornal_app.serializers.auth import (
    MyTokenObtainPairSerializer,
    MyTokenRefreshSerializer
)

class MyTokenObtainPairView(TokenObtainPairView):
    """
    An end point for the user token
    """
    serializer_class = MyTokenObtainPairSerializer

class MyTokenRefreshView(TokenRefreshView):
    """
    An end point to refresh the user token
    """
    serializer_class = MyTokenRefreshSerializer

def get_tokens_for_user(user):
    """Return token for user to authenticate"""
    refresh = RefreshToken.for_user(user)
    response = {
        'id': user.id,
        "access_token": f"{refresh.access_token}",
        "refresh_token": f"{refresh}"
    }
    return response

def validate_email(email: str):
    """Validate email method that confirms if this valid email or not"""
    import re
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return email if(re.fullmatch(regex, email)) else None