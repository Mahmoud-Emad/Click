from server.jornal_app.models.pages import USERTYPE, PageUserPermission, UserPage
from server.jornal_app.models.users import User

def get_page_by_id(page: int) -> UserPage:
    """return page obj if exists"""
    try:
        return UserPage.objects.get(id = page)
    except:
        return None

def get_or_create_user_permission(user: User, user_type = None) -> PageUserPermission:
    """Get or create user with permission to page"""
    if user_type is not None:
        return PageUserPermission.objects.get_or_create(
            user = user, user_type = user_type)[0]
    return PageUserPermission.objects.get_or_create(
        user = user)[0]

def get_admin_user_pages(user: User) -> UserPage:
    """Return pages who user have ADMIN permissions"""
    user = PageUserPermission.objects.filter(
        user = user, user_type = USERTYPE.ADMIN)
    user_pages = UserPage.objects.filter(users__in = user)
    return user_pages if len(user_pages) > 0 else None

def get_any_user_pages(user: User) -> UserPage:
    """Return pages who user have ADMIN permissions"""
    user = PageUserPermission.objects.filter(user = user)
    user_pages = UserPage.objects.filter(users__in = user)
    return user_pages if len(user_pages) > 0 else None