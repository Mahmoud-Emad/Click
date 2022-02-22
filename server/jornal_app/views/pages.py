from rest_framework.generics import GenericAPIView

from server.jornal_app.api.permissions import AdminPage, AuthorPage, EditorPage, IsUser
from server.jornal_app.api.response import CustomResponse
from server.jornal_app.models.pages import USERTYPE, Permissions, UserPage
from server.jornal_app.models.posts import Post
from server.jornal_app.serializers.pages import AddUserToPageSerializer, PagePostsSerializer, UserPageSerializer
from server.jornal_app.serializers.posts import CustomPostSerializer
from server.jornal_app.services.friends import get_friends_list
from server.jornal_app.services.pages import get_any_user_pages, get_or_create_user_permission, get_page_by_id, get_admin_user_pages
from server.jornal_app.services.posts import get_post_by_id
from server.jornal_app.services.users import get_user_by_id

class CreatePageApiVeiw(GenericAPIView):
    """Create page for user"""
    permission_classes = [IsUser,]
    serializer_class = UserPageSerializer
    def post(self, request, format=None):
        serializer = UserPageSerializer(data=request.data)
        if serializer.is_valid():
            user = get_or_create_user_permission(request.user, user_type = USERTYPE.ADMIN)
            user.permissions.add(*Permissions.objects.all())
            page = serializer.save()
            page.users.add(user)
            user.pages.add(page)
            return CustomResponse.success(message='Successfully created', data = serializer.data)
        return CustomResponse.bad_request(message='Make sure that you entered a valid data', error=serializer.errors)

class GetePageApiVeiw(GenericAPIView):
    """get page for any user"""
    permission_classes = [IsUser,]
    serializer_class = UserPageSerializer
    def get(self, request, page_id, format=None):
        page = get_page_by_id(int(page_id))
        if page is not None:
            return CustomResponse.success(message='Successfully', data = UserPageSerializer(page).data)
        return CustomResponse.not_found(message='Page Not Found')

class AddUserToPageApiVeiw(GenericAPIView):
    """Only admin user who have page can add users to his page"""
    permission_classes = [IsUser, AdminPage,]
    serializer_class = AddUserToPageSerializer
    def put(self, request, page_id, format=None):
        """Add user to your page"""
        serializer = AddUserToPageSerializer(data=request.data)
        if serializer.is_valid():
            user_pages = get_admin_user_pages(request.user)
            page = get_page_by_id(int(page_id))
            added_user = get_user_by_id(serializer.validated_data.get('user').id)
            create_user = get_or_create_user_permission(
                added_user, user_type = serializer.validated_data.get('user_type')
            )
            if page is not None:
                if page in user_pages:
                    user_in_page = page.users.all().filter(user__id = added_user.id)
                    if len(user_in_page) > 0:
                        if added_user.id == user_in_page[0].user.id:
                            page.users.remove(user_in_page[0])
                            user_in_page[0].pages.remove(page)
                    page.users.add(create_user)
                    create_user.pages.add(page)
                    create_user.permissions.add(*Permissions.objects.filter(
                        user_type = serializer.validated_data.get('user_type')
                    ))
                    return CustomResponse.success(
                        message="Successfully Add User", 
                        data = UserPageSerializer(page).data)
                return CustomResponse.bad_request(message="You do not have permission to perform this action.")
            return CustomResponse.not_found(message="Page Not Found")
        return CustomResponse.bad_request(message="Make sure that you entered a valid date", error=serializer.errors)

class RemoveUserFromPageApiVeiw(GenericAPIView):
    """Only admin user who have page can use this endpoint"""
    permission_classes = [IsUser, AdminPage,]
    def delete(self, request, page_id, user_id, format=None):
        """Remove user from page"""
        user_pages = get_admin_user_pages(request.user)
        page = get_page_by_id(int(page_id))
        removed_user = get_user_by_id(int(user_id))
        if removed_user is not None:
            if page in user_pages:
                user_in_page = page.users.all().filter(user__id = removed_user.id)
                if len(user_in_page) > 0 and removed_user.id == user_in_page[0].user.id:
                    page.users.remove(user_in_page[0])
                    user_in_page[0].pages.remove(page)
                    return CustomResponse.success(message="Successfully Add User", data = UserPageSerializer(page).data)
                return CustomResponse.not_found(message="User Is Not In Page")
            return CustomResponse.not_found(message="Page Not Found")
        return CustomResponse.not_found(message=f"User with id {user_id} dose not exist")

class UpdatePageInfoAPIView(GenericAPIView):
    """Only admin user who have page can access this endpoint"""
    permission_classes = [IsUser, AdminPage,]
    serializer_class = UserPageSerializer
    def put(self, request, page_id, format=None):
        """An endpoint to update page informations"""
        page = get_page_by_id(int(page_id))
        if page is not None:
            user_pages = get_admin_user_pages(request.user)
            if page in user_pages:
                serializer = UserPageSerializer(page, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return CustomResponse.success(message="Successfully update page", data = serializer.data)
                return CustomResponse.bad_request(message='Make sure that you entered a valid data', error=serializer.errors)
            return CustomResponse.bad_request(message="You do not have permission to perform this action.")
        return CustomResponse.not_found(message="Page Not Found")

class DeletePageAPIView(GenericAPIView):
    """Only admin user who have page can access this endpoint"""
    permission_classes = [IsUser, AdminPage,]
    serializer_class = UserPageSerializer
    def delete(self, request, page_id, format=None):
        """An endpoint to delete page"""
        page = get_page_by_id(int(page_id))
        if page is not None:
            user_pages = get_admin_user_pages(request.user)
            if page in user_pages:
                page.delete()
                return CustomResponse.success(message="Successfully deleted", data = {}, status_code=204)
            return CustomResponse.bad_request(message="You do not have permission to perform this action.")
        return CustomResponse.not_found(message="Page Not Found")

class FollowPageAPIView(GenericAPIView):
    """Any user can access this endpoint"""
    permission_classes = [IsUser,]
    def post(self, request, page_id, format=None):
        """An endpoint to follow page"""
        page = get_page_by_id(int(page_id))
        user = get_user_by_id(request.user.id)
        if page is not None:
            if user in page.followers.all():
                page.followers.remove(user)
            else:
                page.followers.add(user)
            return CustomResponse.success(message="Successfully followed.", data=UserPageSerializer(page).data)
        return CustomResponse.not_found(message="Page Not Found")

class PagePostAPIView(GenericAPIView):
    """Any [ADMIN, AUTHOR, EDITOR] can access this endpoint"""
    permission_classes = [IsUser, AdminPage, EditorPage, AuthorPage]
    serializer_class = CustomPostSerializer
    def post(self, request, page_id, format=None):
        """Make post in page endpoint"""
        page = get_page_by_id(int(page_id))
        if page is not None:
            user_pages = get_any_user_pages(request.user)
            if page in user_pages:
                serializer = CustomPostSerializer(data=request.data)
                if serializer.is_valid():
                    post = serializer.save(author = request.user)
                    page.posts.add(post)
                    return CustomResponse.success(message="Successfully Posted", data = serializer.data)
                return CustomResponse.bad_request(message="Make sure that you entered a valid data.", error=serializer.errors)
            return CustomResponse.bad_request(message="You do not have permission to perform this action.")
        return CustomResponse.not_found(message="Page Not Found.")

class DeletePagePostAPIView(GenericAPIView):
    """Any [ADMIN, EDITOR] can access this endpoint"""
    permission_classes = [IsUser, AdminPage, EditorPage]
    def delete(self, request, page_id, post_id, format=None):
        """Delete post in page endpoint"""
        page = get_page_by_id(int(page_id))
        post = get_post_by_id(int(post_id))
        if page is not None:
            user_pages = get_any_user_pages(request.user)
            if page in user_pages:
                if post is not None and post in page.posts.all():
                    post.delete()
                    return CustomResponse.success(message="Successfully deleted")
                return CustomResponse.not_found(message="Post Not Found.")
            return CustomResponse.bad_request(message="You do not have permission to perform this action.")
        return CustomResponse.not_found(message="Page Not Found.")

class PagePostsAPIView(GenericAPIView):
    """Get all of posts from page"""
    permission_classes = [IsUser,]
    serializer_class = PagePostsSerializer
    def get(self, request, page_id, format=None):
        """Get all of posts in page endpoint"""
        page = get_page_by_id(int(page_id))
        if page is not None:
            data = PagePostsSerializer(page).data
            return CustomResponse.success(message='Successfully', data = data)
        return CustomResponse.not_found(message='Page Not Found')

class PagePostsWithVideoAPIView(GenericAPIView):
    """Get all of posts has videos from page"""
    permission_classes = [IsUser,]
    serializer_class = PagePostsSerializer
    def get(self, request, page_id, format=None):
        """Get all of posts in page endpoint"""
        page = get_page_by_id(int(page_id))
        if page is not None:
            import operator
            from django.db.models import Q
            from functools import reduce
            posts = Post.objects.filter(reduce(operator.or_, (Q(media__contains=video) for video in ['MOV','avi','mp4','webm','mkv'])))
            data = CustomPostSerializer(posts, many=True).data
            return CustomResponse.success(message='Successfully', data = data)
        return CustomResponse.not_found(message='Page Not Found')