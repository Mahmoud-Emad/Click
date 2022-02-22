from server.jornal_app.models.friends import REQUESTFRIENDSTATUS, Following, FriendList, FriendRequest
from server.jornal_app.models.users import User


def get_friend_request_by_id(id: int, status=REQUESTFRIENDSTATUS.SENDING) -> FriendRequest:
    """Return friend request by id from database"""
    try:
        return FriendRequest.objects.get(id = id, status=status)
    except:
        return None

def get_any_friend_request_between_us(sender: User, receiver: User) -> User:
    """Return any friend request has user as sender or receiver from database"""
    try:
        rq = FriendRequest.objects.get(sender = sender, receiver = receiver)
    except:
        try:
            rq = FriendRequest.objects.get(sender = receiver, receiver = sender)
        except:
            # This mean this is the first time user send this request
            rq = FriendRequest.objects.create(
                sender = sender, 
                receiver = receiver, 
                status = REQUESTFRIENDSTATUS.SENDING
            )
    return rq if rq != None else None
    
def list_response(list: list) -> FriendList:
    """Make readable response to friends, black list"""
    arr = []
    for user in list:
        data = {}
        data['User'] = user.email
        data['user_id'] = user.id
        arr.append(data)
    return arr

def get_friends_list(user: User) -> FriendList:
    """Return or create friend list"""
    try:
        return FriendList.objects.get_or_create(user = user)[0]
    except:
        return None

def get_friends_list(user: User) -> FriendList:
    """Return or create friend list"""
    try:
        return FriendList.objects.get_or_create(user = user)[0]
    except:
        return None

def get_follow_list(user: User) -> Following:
    """Return or create Follow list"""
    try:
        return Following.objects.get_or_create(user = user)[0]
    except:
        return None

def custom_friend_request_response(friend_request):
    """Handle friend request status response"""
    data = {
        "Success Sending": {
            'sender': friend_request.sender.email,
            'receiver': friend_request.receiver.email,
            'status': friend_request.status
        }
    }
    return data

def get_mutual_friends(user: User):
    # TODO
    # more than 5 of mutual friends
    friends = []
    my_friend_list                  = FriendList.objects.get(user = user).friends.all()
    friend_friend_list              = FriendList.objects.filter(user__in = my_friend_list)
    for friend in friend_friend_list:
        for friend_ in friend.friends.all():
            friends.append(friend_.id)
    all_of_users                    = User.objects.filter(id__in = friends)
    return all_of_users