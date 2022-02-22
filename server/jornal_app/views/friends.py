from rest_framework.generics import GenericAPIView, ListAPIView
from server.jornal_app.api.permissions import IsUser
from server.jornal_app.api.response import CustomResponse
from server.jornal_app.models import *
from server.jornal_app.serializers.friends import FriendRequestSerializer
from server.jornal_app.services.friends import (
    custom_friend_request_response, get_follow_list, get_friends_list, get_mutual_friends, list_response, 
    get_any_friend_request_between_us, get_friend_request_by_id
)
from server.jornal_app.services.users import get_user_by_id

class SendFriendRequestAPIView(GenericAPIView):
    """Send FriendRequest to users"""
    permission_classes = [IsUser,]
    def post(self, request, id, format=None):
        sender = request.user
        receiver = get_user_by_id(int(id))
        if receiver is not None:
            sender_follow_list = get_follow_list(sender)
            receiver_follow_list = get_follow_list(receiver)
            if not receiver in sender_follow_list.followers.all():
                sender_follow_list.following.add(receiver)
                receiver_follow_list.followers.add(sender)
                # this will return any friend request btween those users, else: create one
                friend_request = get_any_friend_request_between_us(request.user, receiver)
                return CustomResponse.success(data = custom_friend_request_response(friend_request))
            return CustomResponse.bad_request(
                message="User already in your following", 
                data = list_response(sender_follow_list.following.all()))
        return CustomResponse.not_found(message = f"Can not find user with id {id}")

class AcceptingFriendRequestApiVeiw(GenericAPIView):
    """Accept FriendRequest and add it to friends list"""
    permission_classes = [IsUser,]
    def put(self, request, id, format=None):
        friend_request = get_friend_request_by_id(int(id))
        if friend_request:
            sender_friends_list     = get_friends_list(friend_request.sender)
            receiver_friends_list   = get_friends_list(friend_request.receiver)
            sender_follow_list      = get_follow_list(friend_request.sender)
            receiver_follow_list    = get_follow_list(friend_request.receiver)
            if request.user.id == friend_request.receiver.id:
                # Add to friends sys
                sender_friends_list.friends.add(friend_request.receiver)
                receiver_friends_list.friends.add(friend_request.sender)
                # Add to following sys
                sender_follow_list.following.add(friend_request.receiver)
                receiver_follow_list.followers.add(friend_request.sender)
                # Update friend request stats
                friend_request.status = REQUESTFRIENDSTATUS.ACCEPRING
                friend_request.save()
                return CustomResponse.success(message="ACCEPRING FriendRequest", data=custom_friend_request_response(friend_request))
            return CustomResponse.bad_request('You dont have permission to access this endpoint')
        return CustomResponse.not_found(f'Friend Request with id {id} not found')

class DecliningFriendRequestApiVeiw(GenericAPIView):
    """Update FriendRequest and remove it from friends list"""
    permission_classes = [IsUser,]
    def delete(self, request, id, format=None):
        friend_request = get_friend_request_by_id(id)
        if friend_request:
            friend_request.status = REQUESTFRIENDSTATUS.DECLINING
            friend_request.save()
            return CustomResponse.success(message="Valid")
        return CustomResponse.bad_request(message = "Remove request error, Make sure that you entered a valid request id")

class AddUserToBlackListApiVeiw(GenericAPIView):
    """Update FriendRequest and remove it from friends list"""
    permission_classes = [IsUser,]
    def put(self, request, id, format=None):
        blooking_user = get_user_by_id(id)
        if blooking_user:
            # remove follow
            sender_follow_list      = get_follow_list(request.user)
            receiver_follow_list    = get_follow_list(blooking_user)
            if blooking_user in sender_follow_list.following.all():
                sender_follow_list.following.remove(blooking_user)
                receiver_follow_list.followers.remove(request.user)
            # remove friend
            request_user_friends_list = get_friends_list(request.user)
            blooking_user_friends_list = get_friends_list(blooking_user)
            if blooking_user in request_user_friends_list.friends.all():
                blooking_user_friends_list.friends.remove(request.user)
                request_user_friends_list.friends.remove(blooking_user)
            request_user_friends_list.blooking_users.add(blooking_user)
            freqnd_request = get_any_friend_request_between_us(request.user, blooking_user)
            freqnd_request.status = REQUESTFRIENDSTATUS.REMOVED
            freqnd_request.save()
            return CustomResponse.success(
                message="Success Removing: Black List Detail",
                data = list_response(
                    request_user_friends_list.blooking_users.all()
                ),status_code=204)
        return CustomResponse.not_found(message = f"User with id {id} not found.")

class RemoveUserFromBlackListApiVeiw(GenericAPIView):
    """Update FriendRequest and remove it from friends list"""
    permission_classes = [IsUser,]
    def put(self, request, id, format=None):
        blooking_user = get_user_by_id(id)
        if blooking_user:
            friends_list = FriendList.objects.get_or_create(user = request.user)
            if blooking_user in friends_list[0].blooking_users.all():
                friends_list[0].blooking_users.remove(blooking_user)
                return CustomResponse.success(
                    message="Success Removing",
                    data = list_response(
                        friends_list[0].blooking_users.all()
                    ),status_code=204)
            return CustomResponse.not_found(message=f"User With ID {id} Not Found In You'r Black List")
        return CustomResponse.bad_request(message = "Remove request error, Make sure that you entered a valid request id")

class RemoveUserFromFriendsListApiVeiw(GenericAPIView):
    """Update FriendRequest and remove it from friends list"""
    permission_classes = [IsUser,]
    def put(self, request, id, format=None):
        user = get_user_by_id(id)
        if user:
            friends_list = FriendList.objects.get_or_create(user = request.user)
            if user in friends_list[0].friends.all():
                friends_list[0].friends.remove(user)
                return CustomResponse.success(
                    message="Success Removing",
                    data = list_response(
                        friends_list[0].friends.all()
                    ),status_code=204)
            return CustomResponse.not_found(message=f"User With ID {id} Not Found In You'r Friends List")
        return CustomResponse.bad_request(message = "Remove request error, Make sure that you entered a valid request id")

class FollowUserApiVeiw(GenericAPIView):
    """Following system. add, remove methods connect with user following, followers list"""
    permission_classes = [IsUser,]
    def post(self, request, id, format=None):
        user = get_user_by_id(request.user.id)
        following_user = get_user_by_id(id)
        if following_user:
            user_follow_list = Following.objects.get_or_create(user = user)
            user_following_list = Following.objects.get_or_create(user = following_user)
            if user not in user_following_list[0].followers.all():
                user_following_list[0].followers.add(user)
                user_follow_list[0].following.add(following_user)
                return CustomResponse.success(
                        message="Success Following: Following List Detail",
                        data = list_response(
                            user_follow_list[0].following.all()
                        ))
            return CustomResponse.bad_request(message = f"User with id {id} already in you'r following list")
        return CustomResponse.bad_request(message = "Remove request error, Make sure that you entered a valid request id")
    
    def delete(self, request, id, format=None):
        user = get_user_by_id(request.user.id)
        following_user = get_user_by_id(id)
        if following_user:
            user_follow_list = Following.objects.get_or_create(user = user)
            user_following_list = Following.objects.get_or_create(user = following_user)
            if user in user_following_list[0].followers.all():
                user_following_list[0].followers.remove(user)
                user_follow_list[0].following.remove(following_user)
                return CustomResponse.success(
                        message="Success Remove: Following List Detail",
                        data = list_response(
                            user_follow_list[0].following.all()
                        ),status_code=204)
            return CustomResponse.bad_request(message = f"You are not followed user with id {id}")
        return CustomResponse.bad_request(message = "Remove error, Make sure that you entered a valid request id")

class MyFriendRequestApiVeiw(ListAPIView):
    """Get all of my friend requests"""
    permission_classes = [IsUser,]
    serializer_class = FriendRequestSerializer
    def get_queryset(self):
        try:
            requests = FriendRequest.objects.filter(
                    receiver = self.request.user, 
                    status = REQUESTFRIENDSTATUS.SENDING
                ).select_related('receiver')
            return requests
        except:
            return CustomResponse.bad_request(message = "Get requests error, Make sure that you entered a valid data")

class MySendFriendRequestApiVeiw(ListAPIView):
    """Get all of my seinding friend requests"""
    permission_classes = [IsUser,]
    serializer_class = FriendRequestSerializer
    def get_queryset(self):
        try:
            requests = FriendRequest.objects.filter(
                    sender = self.request.user, 
                    status = REQUESTFRIENDSTATUS.SENDING
                ).select_related('sender')
            return requests
        except:
            return CustomResponse.bad_request(message = "Get requests error, Make sure that you entered a valid data")

class UserBlackListApiVeiw(ListAPIView):
    permission_classes = [IsUser,]
    def get(self, request, format=None):
        friends_list = FriendList.objects.get_or_create(user = request.user)
        black_list = friends_list[0].blooking_users.all()
        try:
            return CustomResponse.success(message="Success Response",data = list_response(black_list))
        except:
            return CustomResponse.bad_request(message = "Get requests error, Make sure that you entered a valid data")

class UserFriendsListApiVeiw(ListAPIView):
    permission_classes = [IsUser,]
    def get(self, request, format=None):
        friends_list = FriendList.objects.get_or_create(user = request.user)
        friends = friends_list[0].friends.all()
        try:
            return CustomResponse.success(message="Success Response",data = list_response(friends))
        except:
            return CustomResponse.bad_request(message = "Get requests error, Make sure that you entered a valid data")

class UserFollowersListApiVeiw(ListAPIView):
    permission_classes = [IsUser,]
    def get(self, request, format=None):
        friends_list = Following.objects.get_or_create(user = request.user)
        followers = friends_list[0].followers.all()
        try:
            return CustomResponse.success(message="Success Response",data = list_response(followers))
        except:
            return CustomResponse.bad_request(message = "Get requests error, Make sure that you entered a valid data")

class UserFollowingListApiVeiw(ListAPIView):
    permission_classes = [IsUser,]
    def get(self, request, format=None):
        friends_list = Following.objects.get_or_create(user = request.user)
        following = friends_list[0].following.all()
        try:
            return CustomResponse.success(message="Success Response",data = list_response(following))
        except:
            return CustomResponse.bad_request(message = "Get requests error, Make sure that you entered a valid data")


class GetMutualFriendsAPIView(GenericAPIView):
    # TODO
    permission_classes = [IsUser,]
    def get(self, request, format=None):
        mutual_friends = get_mutual_friends(request.user)
        return CustomResponse.success(message="")