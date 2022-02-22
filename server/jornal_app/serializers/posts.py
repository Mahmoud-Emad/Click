from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from server.jornal_app.models.posts import Bookmarks, Comment, Post, Reply
from server.jornal_app.serializers.users import TimeLineUserSerializer


class CommentSerializer(ModelSerializer):
    """Comment serializer wil return just one comment"""
    likes = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Comment
        fields = ['author', 'id', 'body', 'likes']
        read_only_fields = ('author','id')

    def get_likes(self, obj):
        return obj.likes.count()

class CustomPostSerializer(ModelSerializer):
    """Return custome post view for real time and time line or list"""
    author = serializers.SerializerMethodField(read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)
    comments_on_post = serializers.SerializerMethodField(read_only=True)
    comments = serializers.SerializerMethodField(read_only=True)
    sheres = serializers.SerializerMethodField(read_only=True)
    shered_post = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Post
        fields = [
            'id','author', 'body', 'likes', 'comments', 
            'sheres', 'shered_post', 'media', 'iframe', 
            'comments_on_post',
        ]
        read_only_fields = ('author', 'id', 'comments_on_post')
    
    def get_likes(self, obj):
        """Return all of post likes"""
        return obj.likes.count()
    
    def get_comments(self, obj):
        """Return all of post comments"""
        comment = Comment.objects.filter(post = obj)
        return comment.count()
    
    def get_sheres(self, obj):
        """Return all of post sheres"""
        sheres = Post.objects.filter(shered_post = obj)
        return sheres.count()
    
    def get_shered_post(self, obj):
        """If this post is shered post"""
        try:
            sheres = Post.objects.get(id = obj.shered_post.id)
            return CustomPostSerializer(sheres).data
        except:
            return None
    
    def get_comments_on_post(self, obj):
        """Return all of comments on existing post as obj"""
        if self.get_comments(obj) >= 1:
            comments = Comment.objects.filter(post = obj).select_related('post')
            return CommentSerializer(comments, many=True).data
        return []

    def get_author(self, obj):
        """Return anme of page if posted by page else return author"""
        pages = obj.page_posts.all()
        for page in pages:
            if obj in page.posts.all():
                from server.jornal_app.serializers.pages import TimeLinePageSerializer
                return TimeLinePageSerializer(page).data
        return TimeLineUserSerializer(obj.author).data

class CustomCommentSerializer(ModelSerializer):
    """Return custom comments for list or post detail"""
    post  = serializers.SerializerMethodField(read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Comment
        fields = ['author', 'id', 'body', 'media','likes', 'post']
        read_only_fields = ('author','id')
    
    def get_post(self, obj):
        """Get the post to get comments"""
        try:
            post = Post.objects.get(id = obj.post.id)
            return CustomPostSerializer(post).data
        except:
            return None
    
    def get_likes(self, obj):
        """Return all likes"""
        return obj.likes.count()

class PostShereSerializer(ModelSerializer):
    """Post shere serializer"""
    class Meta:
        model = Post
        fields = ['shered_post', 'body', 'privecy']

class CommentReplySerializer(ModelSerializer):
    """comment reply serializer"""
    likes = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Reply
        fields = ['author', 'id', 'body', 'comment', 'media','likes']
        read_only_fields = ('author', 'id',)

    def get_likes(self, obj):
        """Return all of likes"""
        return obj.likes.count()

class GetPostToBookmarksSerializer(ModelSerializer):
    """Get bookmark posts based on user"""
    posts = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Bookmarks
        fields = ['posts']
    
    def get_posts(self, obj):
        return CustomPostSerializer(obj).data