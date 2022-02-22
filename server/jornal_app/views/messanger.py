
from rest_framework.generics import GenericAPIView, ListAPIView
from django.db.models import Q

from server.jornal_app.api.response import CustomResponse
from server.jornal_app.api.permissions import IsUser
from server.jornal_app.models.messenger import Messages, Room
from server.jornal_app.models.users import User
from server.jornal_app.serializers.messanger import CreateRoomSerializer, MessageSerializer
from server.jornal_app.services.friends import get_follow_list, get_friends_list
from server.jornal_app.services.messanger import get_or_create_room
from server.jornal_app.services.users import get_user_by_id


class CreateRoomAPIView(GenericAPIView):
    """This will create a new room for each user"""
    permission_classes = [IsUser,]
    serializer_class = CreateRoomSerializer

    def post(self, request, format=None):
        """Create New Room To User"""
        serializer = CreateRoomSerializer(data=request.data)
        if serializer.is_valid():
            room = get_or_create_room(
                request.user, get_user_by_id(
                    int(request.data.get('receiver')
                    )
                )
            )
            return CustomResponse.success(message = "Valid", data = CreateRoomSerializer(room).data)
        return CustomResponse.bad_request(message="Make sure that you entered a valid data")

class GetUserConversationsAPIView(GenericAPIView):
    """This will return all of between user have logged in and user we have his id"""
    permission_classes = [IsUser,]
    serializer_class = MessageSerializer
    lookup_url_kwarg = "user_id"
    # filterset_fields = ['created',]
    def get(self, request, user_id, format=None):
        """Get all of conversation between user logged in and user that we send his id"""
        user = get_user_by_id(int(user_id))
        if user is not None:
            messages = Messages.objects.filter(
                Q(sender__id = int(user_id), receiver = self.request.user) | Q(receiver__id = int(user_id), sender = self.request.user)
            ).order_by('-created')[::-1]
            return CustomResponse.success(message = "Valid", data = MessageSerializer(messages, many=True).data)
        else:
            return CustomResponse.not_found(message="User not found")

class GetMessageAPIView(ListAPIView):
    """Get all conversations btween users"""
    permission_classes = [IsUser,]
    serializer_class = MessageSerializer

    def get_queryset(self):
        messages = Messages.objects.filter(
            Q(sender=self.request.user) | Q(receiver = self.request.user)
        ).order_by('-created') # Get any message related to user who logged in

        # Make loop on all of messages to push reciver id, sender id to conversations list
        conversations = []
        for message in messages:
            if message.sender.id == self.request.user.id and not [message.sender.id, message.receiver.id] in conversations:
                conversations.append([message.sender.id, message.receiver.id])
            elif message.receiver.id == self.request.user.id and not [message.receiver.id, message.sender.id] in conversations:
                conversations.append([message.receiver.id, message.sender.id])
    
        for i in range(0,len(conversations)):
            i = 0
            m = Messages.objects.filter(
                Q(
                    sender__id = conversations[i][0], receiver__id = conversations[i][1]
                    )| 
                Q(
                    receiver__id = conversations[i][0], sender__id= conversations[i][1]
                    )
            )[0]
            conversations.remove(conversations[i])
            conversations.append(m.id)

        queryset = Messages.objects.filter(id__in = conversations)
        return queryset.order_by('-created')