from django.urls import path,include

from server.jornal_app.views.pages import (
    CreatePageApiVeiw, AddUserToPageApiVeiw,
    RemoveUserFromPageApiVeiw, UpdatePageInfoAPIView,
    DeletePageAPIView, FollowPageAPIView,
    PagePostAPIView, GetePageApiVeiw,
    PagePostsAPIView, DeletePagePostAPIView,
    PagePostsWithVideoAPIView
)



urlpatterns = [
    path('', include([
        path('create-page/', CreatePageApiVeiw.as_view()),
        path('add-users/<int:page_id>/', AddUserToPageApiVeiw.as_view()),
        path('get-page/<int:page_id>/', GetePageApiVeiw.as_view()),
        path('get-page-posts/<int:page_id>/', PagePostsAPIView.as_view()),
        path('update-page/<int:page_id>/', UpdatePageInfoAPIView.as_view()),
        path('delete-page/<int:page_id>/', DeletePageAPIView.as_view()),
        path('follow-page/<int:page_id>/', FollowPageAPIView.as_view()),
        path('videos-page/<int:page_id>/', PagePostsWithVideoAPIView.as_view()),
        path('make-post-on-page/<int:page_id>/', PagePostAPIView.as_view()),
        path('remove-user/<int:page_id>/<int:user_id>/', RemoveUserFromPageApiVeiw.as_view()),
        path('delete-post/<int:page_id>/<int:post_id>/', DeletePagePostAPIView.as_view()),
    ]))
]