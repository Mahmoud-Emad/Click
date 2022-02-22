from django.shortcuts import redirect, render
from rest_framework.generics import GenericAPIView, ListAPIView

from server.jornal_app.api.permissions import IsUser
from server.jornal_app.api.response import CustomResponse
from server.jornal_app.models.friends import FriendList
from server.jornal_app.models.pages import UserPage
from server.jornal_app.models.posts import Post
from server.jornal_app.serializers.pages import UserPageSerializer
from server.jornal_app.serializers.posts import CustomPostSerializer
from server.jornal_app.serializers.users import TimeLineUserSerializer
from server.jornal_app.services.friends import get_follow_list, get_friends_list
from server.jornal_app.services.lobby import get_time_line_following_list, get_time_line_friends_list

def home_page(request):
    # if request.user.is_authenticated:
    # return redirect("login")
    return render(request,'messanger/chat.html')


class GetTimeLineApiView(ListAPIView):
    """Time line for each user"""
    permission_classes = [IsUser,]
    serializer_class = CustomPostSerializer
    def get_queryset(self):
        friends_list = get_friends_list(self.request.user).friends.all() # -> Return all friends list
        friends_time_line = get_time_line_friends_list(friends_list) # -> Return all posts with any author in friends list

        following_list = get_follow_list(self.request.user).following.all() # -> Return all following list
        follow_time_line = get_time_line_following_list(following_list) # -> Return all posts with any author in following list
        
        pages_list = UserPage.objects.filter(followers__id = self.request.user.id) # -> Filter pages to what pages user following
        pages_time_line = Post.objects.filter(page_posts__in=pages_list) # -> Return all posts in any page user like

        return pages_time_line.union(friends_time_line,follow_time_line)

class SuggestedPagesAPIView(GenericAPIView):
    """Suggested pages endpoint"""
    permission_classes = [IsUser,]
    serializer_class = UserPageSerializer
    def get(self, request, format=None):
        friends_list = get_friends_list(request.user).friends.all()
        if len(friends_list) >= 50:
            friends_pages_suggest = UserPage.objects.filter(followers__id__in = friends_list,is_active = True)
            if len(friends_pages_suggest) >= 10:
                return CustomResponse.success(message="Successfully", data=UserPageSerializer(friends_pages_suggest, many=True).data)
        friends_pages_suggest = UserPage.objects.filter(is_active = True)
        return CustomResponse.success(message="Successfully", data=UserPageSerializer(friends_pages_suggest, many=True).data)

class SuggestedFriendsAPIView(GenericAPIView):
    """Suggested friends endpoint"""
    permission_classes = [IsUser,]
    serializer_class = TimeLineUserSerializer
    def get(self, request, format=None):
        # friends_list = get_friends_list(request.user).friends.all() TODO :
        users = FriendList.objects.all()
        return CustomResponse.success(message="Successfully")

