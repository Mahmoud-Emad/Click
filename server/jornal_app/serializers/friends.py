
from rest_framework.serializers import ModelSerializer
from server.jornal_app.models import *

class FriendRequestSerializer(ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = '__all__'
