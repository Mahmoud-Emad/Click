from server.jornal_app.models.friends import Following, FriendList
from server.jornal_app.models.posts import PRIVECYSTATUS, Post


def get_time_line_friends_list(friends_list: FriendList) -> Post:
    """Return any post posted by author in friends list and privecy not only me"""
    return Post.objects.filter(
        author__in = friends_list
        ).exclude(
            privecy = PRIVECYSTATUS.OnlyMe
        )
        
def get_time_line_following_list(following_list: Following) -> Post:
    """Return any post posted by author in following list and privecy Publice"""
    return Post.objects.filter(
        author__in = following_list,
        privecy = PRIVECYSTATUS.Public
        )
        