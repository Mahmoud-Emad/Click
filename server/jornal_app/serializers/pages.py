from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from server.jornal_app.models.pages import PageUserPermission, UserPage
from server.jornal_app.serializers.posts import CustomPostSerializer


class AddUserToPageSerializer(ModelSerializer):
    class Meta:
        model = PageUserPermission
        fields = ['user', 'user_type']

class TimeLinePageSerializer(ModelSerializer):
    """Custom Serializer to get page details"""
    followers = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = UserPage
        fields = [
            'id','page_name', 'profile_image', 'followers'
        ]
    
    def get_followers(self, obj):
        return obj.followers.all().count()

class UserPageSerializer(ModelSerializer):
    """Custom Serializer to get page details"""
    followers = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = UserPage
        fields = [
            'id','page_name', 'category', 'address',
            'about','profile_image', 'profile_cover',
            'followers','is_active'
        ]
    
    def get_followers(self, obj):
        return obj.followers.all().count()

class PagePostsSerializer(ModelSerializer):
    """Custom Serializer to get posts in page"""
    posts = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = UserPage
        fields = ['posts']

    def get_posts(self, obj):
        posts = obj.posts.all()
        return CustomPostSerializer(posts, many=True).data