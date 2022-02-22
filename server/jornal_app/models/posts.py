from django.db import models

from server.jornal_app.models.abstracts import PostAbc, TimeStampedModel
from server.jornal_app.models.users import User

class PRIVECYSTATUS(models.TextChoices):
    Public   = "Public", "Public"
    Friends  = "Friends", "Friends"
    OnlyMe   = "Only me", "Only me"

class Post(PostAbc):
    """DataBase table [Post] for post"""
    author  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    body    = models.TextField(max_length = 500, null=True, blank=True)
    privecy = models.CharField(max_length=50, choices = PRIVECYSTATUS.choices, default = PRIVECYSTATUS.Public)
    shered_post = models.ForeignKey('Post', on_delete=models.CASCADE, null=True, blank=True)
    likes = models.ManyToManyField(User, related_name="post_likes")

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_type_valid",
                check=models.Q(privecy__in=PRIVECYSTATUS.values),
            )
        ]

    def __str__(self) -> isinstance:
        """Return string of instance"""
        return self.body

class Comment(PostAbc):
    """DataBase table [Comment] for comment"""
    author  = models.ForeignKey(User, on_delete=models.CASCADE)
    post    = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments')
    body    = models.TextField(max_length=250)
    likes   = models.ManyToManyField(User, related_name="comment_likes")

    def __str__(self) -> isinstance:
        """Return string of instance"""
        return str(self.body)

class Reply(PostAbc):
    """DataBase table [Reply] for comment"""
    author  = models.ForeignKey(User, on_delete=models.CASCADE)
    body    = models.TextField(max_length=250)
    likes   = models.ManyToManyField(User, related_name="reply_likes")
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="comment")

    def __str__(self) -> isinstance:
        """Return string of instance"""
        return str(self.body)

class Bookmarks(TimeStampedModel):
    posts = models.ManyToManyField(Post, related_name='saved_posts')
    user = models.OneToOneField(User, related_name='user_saved_posts', on_delete=models.CASCADE)
    
    def __str__(self) -> isinstance:
        """Return string of instance"""
        return str(self.user.email)
