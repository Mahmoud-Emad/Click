from server.jornal_app.models.pages import Category, Permissions
from server.jornal_app.models.pages import USERTYPE
from server.jornal_app.models.users import User, UserProfile


def get_user_by_id(id: int) -> User:
    """Normal function return single user"""
    try:
        return User.objects.get(id = id)
    except User.DoesNotExist:
        return None

def get_user_profile_by_id(id: int) -> UserProfile:
    """Normal function return single user"""
    try:
        return UserProfile.objects.get(id = id)
    except UserProfile.DoesNotExist:
        return None

def get_user_by_email_for_login(email: str) -> User:
    """Normal function return user by email"""
    try:
        return User.objects.get(email = email)
    except User.DoesNotExist:
        return None

def get_all_users() -> User:
    """Normal function return all users"""
    return User.objects.all()

def get_user_by_phone_for_login(phone: str) -> UserProfile:
    """Normal function return user by phone"""
    try:
        return UserProfile.objects.get(phone_nummber = phone)
    except UserProfile.DoesNotExist:
        return None

def user_info_response(user) -> User:
    user_obj = {
        'id':vars(user).get('id'),
        'email':vars(user).get('email'),
        'username':vars(user).get('username'),
        'first_name':vars(user).get('first_name'),
        'last_name':vars(user).get('last_name'),
        'fuulname':vars(user).get('fuulname'),
        'phone_nummber':vars(user).get('phone_nummber'),
        'profile_image':vars(user).get('profile_image.url'),
        'profile_cover':vars(user).get('profile_cover.url'),
    }
    return user_obj

def get_all_permissions(users_type: list[str]) -> Permissions:
    admin_permissions = [
        "Can Add User","Can Delete User",
        "Can Add Post","Can Delete Post",
        "Can Open Comments","Can Stop Comments",
        "Can Update Page","Can Delete Page",
        "Can Update Group","Can Delete User",]
    editor_permissions = [
        "Can Add User",
        "Can Add Post","Can Delete Post",
        "Can Stop User"
        ]
    author_permissions = [
        "Can Add Post","Can Delete Post",
        ]
    for user in users_type:
        if user == USERTYPE.ADMIN:
            for permission in admin_permissions:
                Permissions.objects.create(
                    permission = permission,
                    user_type = USERTYPE.ADMIN
                )
        elif user == USERTYPE.EDITOR:
            for permission in editor_permissions:
                Permissions.objects.create(
                    permission = permission,
                    user_type = USERTYPE.EDITOR
                )
        elif user == USERTYPE.AUTHOR:
            for permission in author_permissions:
                Permissions.objects.create(
                    permission = permission,
                    user_type = USERTYPE.AUTHOR
                )
    return Permissions.objects.all()