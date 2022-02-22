from django.urls import path,include

from server.jornal_app.views.users import (
    GetUserInfoApiView, 
    GetUserLogedInApiView,
    GetAllUsersApiView,
    SetPagesAndGroupPermission,
)

urlpatterns = [
    path('', include([
        path('get-user/<int:id>/', GetUserInfoApiView.as_view()),
        path('user-me/', GetUserLogedInApiView.as_view()),
        path('user-all/', GetAllUsersApiView.as_view()),
        path('set-permissions/', SetPagesAndGroupPermission.as_view()),
    ]))
]