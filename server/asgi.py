import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from server.jornal_app.realtime.auth_middleware import TokenAuthMiddleware

from server.jornal_app.routers.real_time_url import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": TokenAuthMiddleware(
    URLRouter(
      websocket_urlpatterns
    ))
})