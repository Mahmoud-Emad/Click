from django.contrib.auth.hashers import make_password
from rest_framework import fields
from rest_framework import serializers
from rest_framework.serializers import EmailField

from rest_framework.serializers import ModelSerializer
from server.jornal_app.models.pages import Permissions

from server.jornal_app.models.users import UserProfile, User
from server.jornal_app.services.friends import get_follow_list


class UserRegisterInfoSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['phone_nummber', 'first_name', 'last_name', 'email', 'password']
    
    def validate_password(self, password) -> str:
        return make_password(password)

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'is_admin', 'last_login']

class UpdateUserProfileSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'email', 'first_name', 'last_name',
            'profile_image', 'profile_cover', 
            'phone_nummber', 'gender', 'Bio',
            'country', 'city'
            ]

class UserLoginSerializer(ModelSerializer):
    login_field = fields.CharField()
    class Meta:
        model = User
        fields = ['login_field', 'password']

class PermissionSerializers(ModelSerializer):
    class Meta:
        model = Permissions
        fields = ['permission', 'user_type']
        read_only_fields = ['permission', 'user_type']

class TimeLineUserSerializer(ModelSerializer):
    """Custom Serializer to get page details"""
    followers = serializers.SerializerMethodField(read_only=True)
    profile_image = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = UserProfile
        fields = [
            'id','full_name', 'profile_image', 'followers','is_online'
        ]
    
    def get_followers(self, obj):
        """Get followers count"""
        followers = get_follow_list(obj)
        return followers.followers.all().count()
    
    def get_profile_image(self, obj):
        """Get profile image url"""
        if obj.userprofile.profile_image:
            return obj.userprofile.profile_image.url
        return None

class ForgetPasswordUser(ModelSerializer):
    email = EmailField()

    class Meta:
        model = User
        fields = ('email',)