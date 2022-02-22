from typing import Awaitable, Set
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.base_user import AbstractBaseUser
from django.db.models import Q
from server.jornal_app.models.friends import FriendList, FriendRequest

from channels.db import database_sync_to_async
import json, enum

from server.jornal_app.models.messenger import Messages
from server.jornal_app.services.users import get_user_by_id


class MessageTypes(enum.Enum):
    UserOnline = 'online'
    UserOffline = 'offline'


class LOGGER(enum.Enum):
    message_creation_error = {
        "type":"CreateMessageError",
        "Details":"Can not create this message"
    }


@database_sync_to_async
def send_online_to_users(user: AbstractBaseUser):
    messages = Messages.objects.filter(
            Q(sender=user) | Q(receiver = user)
        )
    arr = []
    for message in messages:
        if message.sender.id == user.id:
            if not message.receiver.id in arr:
                arr.append(message.receiver.id)
        else:
            if not message.sender.id in arr:
                arr.append(message.sender.id)
    return arr

@database_sync_to_async
def set_user_online(user: AbstractBaseUser):
    user = get_user_by_id(user.id)
    user.is_online = True
    user.save()

@database_sync_to_async
def set_user_offline(user: AbstractBaseUser):
    user = get_user_by_id(user.id)
    user.is_online = False
    user.save()

@database_sync_to_async
def create_message(msg: Messages):
    sender = get_user_by_id(int(msg["sender"]))
    receiver = get_user_by_id(int(msg["receiver"]))
    Messages.objects.create(
        sender = sender,
        receiver = receiver,
        text = msg["message"],
    )


class JornalMessageConsumers(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.group_name: str = str(self.user.pk)
        self.sender_username: str = self.user.username
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        await set_user_online(self.user)
        friends = await send_online_to_users(self.user)

        for friend in friends:
            await self.channel_layer.group_send(
                str(friend),{
                    "type": "user_status",
                    "status": MessageTypes.UserOnline.value,
                    "user_pk": str(self.user.pk)
                }
            )

    async def disconnect(self, close_code):

        if close_code != 4001 and getattr(self, 'user', None) is not None:
            await self.channel_layer.group_discard(self.group_name, self.channel_name)
        await set_user_offline(self.user)
        friends = await send_online_to_users(self.user)
        for friend in friends:
            await self.channel_layer.group_send(
                str(friend),{
                    "type": "user_status",
                    "status": MessageTypes.UserOffline.value,
                    "user_pk": str(self.user.pk)
                }
            )
    
    async def receive(self, text_data, bytes_data=None):
        data = json.loads(text_data)
        user_id = data['receiver']
        print(data)

        sending_data = {
            'type'      : None,
            'receiver'  : user_id,
        }

        if 'is_typing' in data:
            sending_data['type'] = 'is_typing'
            sending_data['is_typing'] = data['is_typing']
            await self.channel_layer.group_send(
                str(user_id),sending_data
            )

        else:
            sending_data['type'] = 'message'
            sending_data['message'] = data['message']
            sending_data['sender'] = data['sender']
            
            try:
                await create_message(data)
                await self.channel_layer.group_send(
                    str(user_id),sending_data
                )
            except:
                await self.channel_layer.group_send(
                    str(data['sender']),
                    LOGGER.message_creation_error.value
                )


    async def is_typing(self, event):
        receiver    = event['receiver']
        is_typing   = event['is_typing']
        print(event)
        # Send request to WebSocket
        await self.send(
            text_data=json.dumps(
                {
                    'receiver'  : receiver,
                    'is_typing' : is_typing,
                    'status'    : MessageTypes.UserOnline.value
                }
            )
        )
    
    # Receive message from room group
    async def message(self, event):
        message     = event['message']
        sender      = event['sender']
        receiver    = event['receiver']

        # Send request to WebSocket
        await self.send(
            text_data=json.dumps(
                {
                    'message'   :message,
                    'sender'    :sender,
                    'receiver'  :receiver,
                    'status'    : MessageTypes.UserOnline.value
                }
            )
        )

    # Receive message from room group
    async def user_status(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    'status': event['status'],
                    'user_pk': event['user_pk']
                }
            )
        )

    async def message_creation_error(self, event):
        """Send alert logger to sender, this message connt created"""
        await self.send(text_data=json.dumps(event))