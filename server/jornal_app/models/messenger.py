from typing import Any, Optional
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.db.models import Q


from server.jornal_app.models.abstracts import TimeStampedModel
from server.jornal_app.models.users import User
import uuid

class Messages(models.Model):
    """Defines a single chat message."""
    sender = models.ForeignKey(User, related_name="me_sender", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="me_receiver", on_delete=models.CASCADE)
    text = models.TextField()
    is_read = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self) -> isinstance:
        """Return string of instance"""
        return str(self.sender)

class Room(models.Model):
    room_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(User, related_name='author_room', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='friend_room', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> isinstance:
        """Return string of instance"""
        return str(self.sender)

class DialogsModel(TimeStampedModel):
    id = models.BigAutoField(primary_key=True)
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+", db_index=True)
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+", db_index=True)

    class Meta:
        unique_together = (('user1', 'user2'), ('user2', 'user1'))

    def __str__(self) -> isinstance:
        """Return string of instance"""
        return ("Dialog between ") + f"{self.user1_id}, {self.user2_id}"

    @staticmethod
    def dialog_exists(u1: AbstractBaseUser, u2: AbstractBaseUser) -> Optional[Any]:
        return DialogsModel.objects.filter(Q(user1=u1, user2=u2) | Q(user1=u2, user2=u1)).first()

    @staticmethod
    def create_if_not_exists(u1: AbstractBaseUser, u2: AbstractBaseUser):
        res = DialogsModel.dialog_exists(u1, u2)
        if not res:
            DialogsModel.objects.create(user1=u1, user2=u2)

    @staticmethod
    def get_dialogs_for_user(user: AbstractBaseUser):
        return DialogsModel.objects.filter(Q(user1=user) | Q(user2=user)).values_list('user1__pk', 'user2__pk')