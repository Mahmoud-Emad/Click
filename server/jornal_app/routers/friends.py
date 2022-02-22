from django.urls import path,include

from server.jornal_app.views.friends import *

urlpatterns = [
    path('', include([
        path('friend-request/send/<int:id>/', SendFriendRequestAPIView.as_view()),
        path('friend-request/accept/<int:id>/', AcceptingFriendRequestApiVeiw.as_view()),
        path('friend-request/remove/<int:id>/', DecliningFriendRequestApiVeiw.as_view()),
        path('friend-request/get_send/', MySendFriendRequestApiVeiw.as_view()),
        path('friend-request/get_received/', MyFriendRequestApiVeiw.as_view()),
        
        path('add-user-to-black-list/<int:id>/', AddUserToBlackListApiVeiw.as_view()),
        path('remove-user-from-black-list/<int:id>/', RemoveUserFromBlackListApiVeiw.as_view()),
        
        path('action-user-following-list/<int:id>/', FollowUserApiVeiw.as_view()),
        path('remove-user-from-friends-list/<int:id>/', RemoveUserFromFriendsListApiVeiw.as_view()),
        
        path('my-followers-list/', UserFollowersListApiVeiw.as_view()),
        path('my-following-list/', UserFollowingListApiVeiw.as_view()),
        
        path('my-friends-list/', UserFriendsListApiVeiw.as_view()),
        path('my-black-list/', UserBlackListApiVeiw.as_view()),
        
        path('mutual-friends/', GetMutualFriendsAPIView.as_view()),
    ]))
]