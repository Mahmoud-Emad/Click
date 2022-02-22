from rest_framework.serializers import ModelSerializer, SerializerMethodField, Serializer, CharField

from server.jornal_app.models.messenger import Messages, Room
from server.jornal_app.models.users import User
from server.jornal_app.serializers.users import TimeLineUserSerializer
from server.jornal_app.services.friends import get_friends_list



class MessageSerializer(ModelSerializer):
    sender = SerializerMethodField(read_only=True)
    receiver = SerializerMethodField(read_only=True)
    
    class Meta:
        model = Messages
        fields = ['sender','receiver','text','is_read','created']
        read_only_fields = ('text','is_read','created')
    
    def get_sender(self, obj):
        return TimeLineUserSerializer(obj.sender).data

    def get_receiver(self, obj):
        return TimeLineUserSerializer(obj.receiver).data



class CreateRoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = ['room_id','sender','receiver']
        read_only_fields = ('room_id','sender',)

# class TestSerializer(ModelSerializer):
#     conversations = SerializerMethodField(read_only=True)
#     class Meta:
#         model = Messages
#         fields = ['conversations']

#     def get_conversations(self, obj):
#         user = None
#         request = self.context.get("request")
#         if request and hasattr(request, "user"):
#             user = request.user
#             conversations = get_conversations_response(user, obj)
#             return conversations
        