from django.conf.urls import include
from django.urls import path

from server.jornal_app.realtime.messanger import *
from server.jornal_app.views.messanger import CreateRoomAPIView, GetMessageAPIView, GetUserConversationsAPIView
websocket_urlpatterns = [
  path('chat/', JornalMessageConsumers.as_asgi()),
]

urlpatterns = [
    path('', include([
        path('create-room/', CreateRoomAPIView.as_view()),
        path('conversations/', GetMessageAPIView.as_view()),
        path('user-conversation/<int:user_id>/', GetUserConversationsAPIView.as_view()),
    ]))
]