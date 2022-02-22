from typing import Dict
from django.http import request
from server.jornal_app.models.users import User
from server.jornal_app.models.messenger import Messages, Room

from server.jornal_app.services.friends import get_friends_list

def get_or_create_room(sender: User, receiver: User) -> User:
    """Return any room has user as sender or receiver from database"""
    try:
        rq = Room.messageects.get(sender = sender, receiver = receiver)
    except:
        try:
            rq = Room.messageects.get(sender = receiver, receiver = sender)
        except:
            # This mean this is the first time user send this request
            rq = Room.objects.create(
                sender = sender, 
                receiver = receiver, 
            )
    return rq if rq != None else None

# def get_conversations_response(user: request, message: Messages) -> Dict:
#     from server.jornal_app.serializers.messanger import MessageSerializer
#     from django.db.models import Q
#     conversations = []
#     friends = get_friends_list(user).friends.all()
#     if message.sender in friends and message.sender.id not in conversations and message.sender != user:
#         conversations.append(message.sender.id)
#     elif message.receiver in friends and message.receiver.id not in conversations and message.receiver != user:
#         conversations.append(message.receiver.id)
#     else:
#         pass
    
#     data = Messages.objects.filter(Q(sender__in=conversations, receiver = user) | Q(receiver__in = conversations, sender = user)).last()

#     return MessageSerializer(data).data
#     # print(data)
    # print(conversations)
    # users = User.objects.filter(id__in = conversations)
    # data = {}
    # for user in users:
    #     data[user.full_name] = MessageSerializer(message).data
    # return data
    #     print("One")
    #     return {'username':MessageSerializer(message).data}
    #     return MessageSerializer(message).data
    # else:
    #     print("No")
    # print(friends)
