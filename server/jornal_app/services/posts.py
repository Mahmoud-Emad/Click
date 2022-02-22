from typing import Dict
from server.jornal_app.models import *
from server.jornal_app.services.users import get_user_profile_by_id, user_info_response
from server.jornal_app.utils.translations import translate_method


def get_post_by_id(id: int) -> Post:
    """Return single post"""
    try:
        return Post.objects.get(id = id)
    except Post.DoesNotExist:
        return None

def get_comment_by_id(id: int) -> Comment:
    """Return single post"""
    try:
        return Comment.objects.get(id = id)
    except Comment.DoesNotExist:
        return None

def get_reply_by_id(id: int) -> Reply:
    """Return single post"""
    try:
        return Reply.objects.get(id = id)
    except Reply.DoesNotExist:
        return None

def custom_translate_response(post: Post, code:str) -> Dict:
    tr = translate_method(post.body, code)
    return {
        'orignal': post.body,
        'translate':tr
    }

def get_posts_from_bookmark_based_on_user(user: User) -> Post:
    """Get posts from user bookmark"""
    try:
        return Bookmarks.objects.get(user = user).posts.all()
    except:
        return None

def get_bookmark_by_user(user: User) -> Post:
    """Get bookmark by user"""
    try:
        return Bookmarks.objects.get(user = user)
    except:
        return None

def get_or_creqate_bookmark_by_user(user: User) -> Post:
    """Get or create bookmark to user"""
    try:
        return Bookmarks.objects.get(user = user)
    except:
        return Bookmarks.objects.create(user = user)