from django.urls import path,include

from server.jornal_app.views.posts import *

urlpatterns = [
    path('', include([
        path('make-post/', MakePostApiVeiw.as_view()),
        path('make-comment/', MakeCommentOnPostApiVeiw.as_view()),
        path('make-reply/', MakeReplyOnCommentApiVeiw.as_view()),
        
        path('get-post/<int:id>/', GetPostByIdApiVeiw.as_view()),
        path('get-comment/<int:id>/', GetCommentByIdApiVeiw.as_view()),
        path('get-reply/<int:id>/', GetReplyByIdApiVeiw.as_view()),
        path('my-posts/', AllMyPostsListApiVeiw.as_view()),
        
        path('update-post/<int:id>/', UpdatePostApiVeiw.as_view()),
        path('update-comment/<int:id>/', UpdateCommentApiVeiw.as_view()),
        path('update-reply/<int:id>/', UpdateReplyApiVeiw.as_view()),
        
        path('delete-post/<int:id>/', DeletePostApiVeiw.as_view()),
        path('delete-comment/<int:id>/', DeleteCommentApiVeiw.as_view()),
        path('delete-reply/<int:id>/', DeleteReplyApiVeiw.as_view()),
        
        path('add-post-to-bookmark/<int:post_id>/', AddPostToBookmarksAPIView.as_view()),
        path('get-posts-from-bookmark/', GetMyBookMarksAPIView.as_view()),
        path('remove-posts-from-bookmark/<int:post_id>/', RemovePostFromBookMarksAPIView.as_view()),
        
        path('react-action-post/<int:id>/', LikePostApiVeiw.as_view()),
        path('react-action-comment/<int:id>/', LikeCommentPostApiVeiw.as_view()),
        path('react-action-reply/<int:id>/', LikeReplyPostApiVeiw.as_view()),
        path('shere-post/', SherePostApiVeiw.as_view()),
        path('translate-post/<int:id>/<str:code>/', PostTransleatorByIdApiVeiw.as_view()),
    ]))
]