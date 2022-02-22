from django.urls import path,include

from server.jornal_app.views.lobby import(
    GetTimeLineApiView, SuggestedPagesAPIView,
    SuggestedFriendsAPIView
    )


urlpatterns = [
    path('', include([
        path('time-line/', GetTimeLineApiView.as_view()),
        path('suggested-pages/', SuggestedPagesAPIView.as_view()),
        path('suggested-friends/', SuggestedFriendsAPIView.as_view()),
    ]))
]