from django.db import models
from server.jornal_app.models.users import User

from server.jornal_app.models.abstracts import TimeStampedModel


class REQUESTFRIENDSTATUS(models.TextChoices):
    SENDING     = "SENDING", "SENDING"
    DECLINING   = "DECLINING", "DECLINING"
    ACCEPRING   = "ACCEPRING", "ACCEPRING"
    REMOVED     = "REMOVED", "REMOVED"


class FriendList(TimeStampedModel):
    user            = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
    friends         = models.ManyToManyField(User, related_name='friends')
    blooking_users  = models.ManyToManyField(User, related_name='black_list')
    
    def __str__(self) -> isinstance:
        """Return string of instance"""
        return self.user.email

class FriendRequest(TimeStampedModel):
    sender      = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    status      = models.CharField(max_length=50, choices=REQUESTFRIENDSTATUS.choices)

    def __str__(self) -> isinstance:
        """Return string of instance"""
        return self.sender.email

class Following(TimeStampedModel):
    user            = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_follow')
    following       = models.ManyToManyField(User, related_name='following')
    followers       = models.ManyToManyField(User, related_name='followers')

    def __str__(self) -> isinstance:
        """Return string of instance"""
        return self.user.email