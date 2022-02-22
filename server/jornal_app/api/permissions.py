from rest_framework import permissions
from django.core.exceptions import PermissionDenied
from rest_framework.request import Request
from rest_framework.views import APIView
from django.http import HttpResponse

from server.jornal_app.models.pages import USERTYPE, PageUserPermission, UserPage


class IsUser(permissions.BasePermission):
    """
    return this endpoint only for normal user
    """
    def has_permission(self, request : Request, view:APIView) -> bool:
        if request.user.is_authenticated and request.user.groups.filter(name='Users'):
            return True
        raise PermissionDenied


class IsSystemUser(permissions.BasePermission):
    """
    return this endpoint only for a system user
    """
    def has_permission(self, request : Request, view:APIView) -> bool:
        if request.user.is_authenticated and request.user.groups.filter(name='System Users') and request.user.is_superuser:
            return True
        raise PermissionDenied

class AdminPage(permissions.BasePermission):
    """
    return this endpoints only for any user have pages
    """
    def has_permission(self, request : Request, view:APIView) -> bool:
        user = PageUserPermission.objects.filter(user = request.user, user_type = USERTYPE.ADMIN)
        page_user = UserPage.objects.filter(users__in = user)
        if request.user.is_authenticated and page_user:
            return True
        raise PermissionDenied

class EditorPage(permissions.BasePermission):
    """
    return this endpoints only for any user have pages
    """
    def has_permission(self, request : Request, view:APIView) -> bool:
        user = PageUserPermission.objects.filter(user = request.user).exclude(user_type = USERTYPE.AUTHOR)
        page_user = UserPage.objects.filter(users__in = user)
        if request.user.is_authenticated and page_user:
            return True
        raise PermissionDenied

class AuthorPage(permissions.BasePermission):
    """
    return this endpoints only for any user have pages
    """
    def has_permission(self, request : Request, view:APIView) -> bool:
        user = PageUserPermission.objects.filter(user = request.user)
        page_user = UserPage.objects.filter(users__in = user)
        if request.user.is_authenticated and page_user:
            return True
        raise PermissionDenied
