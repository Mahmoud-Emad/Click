from rest_framework.generics import GenericAPIView

from server.jornal_app.api.permissions import IsSystemUser, IsUser
from server.jornal_app.api.response import CustomResponse
from server.jornal_app.models.pages import USERTYPE, Permissions
from server.jornal_app.models.users import User, UserProfile
from server.jornal_app.services.users import get_all_permissions, get_user_by_id
from server.jornal_app.serializers.users import (
    PermissionSerializers,
    UpdateUserProfileSerializer, 
    UserSerializer
)


class GetUserInfoApiView(GenericAPIView):
    """Normal endpoint return single user"""
    serializer_class = UpdateUserProfileSerializer
    permission_classes = [IsUser,]
    def get(self, request, id, format=None):
        from itertools import chain
        try:
            user = get_user_by_id(id)
            data = {}
            for f in chain(user._meta.concrete_fields, user._meta.private_fields):
                data[f.name] = f.value_from_object(user)
                data["password"] = "*********"
            return CustomResponse.success(message = "Success Response", data = data)
        except:
            return CustomResponse.not_found(message = f"Cant Find Any User With ID {id}")
    
    def put(self, request, id, format=None):
        try:
            user = get_user_by_id(id)
            serializer = UpdateUserProfileSerializer(user, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return CustomResponse.success(message="Success Update", data = serializer.data)
            return CustomResponse.bad_request(message = "Cant Update User", error = serializer.errors)
        except User.DoesNotExist:
            return CustomResponse.not_found(message = f"Cant Find Any User With ID {id}")


class GetUserLogedInApiView(GenericAPIView):
    """Normal endpoint return who user login now"""
    permission_classes = [IsUser,]
    def get(self, request, format=None):
        if not request.user.is_anonymous:
            from itertools import chain
            user = get_user_by_id(request.user.id)
            data = {}
            for f in chain(user._meta.concrete_fields, user._meta.private_fields):
                data[f.name] = f.value_from_object(user)
                data["password"] = "*********"
            return CustomResponse.success(message = "Success Response", data = data)
        return CustomResponse.bad_request(message ="Make Sure That You Loged In Our System.", error= "User Type Is Anonymous User.")


class GetAllUsersApiView(GenericAPIView):
    """endpoint return all users an our system"""
    permission_classes = [IsUser,]
    def get(self, request, format=None):
        users = User.objects.order_by('pk')
        serializer = UserSerializer(users, many=True)
        try:
            for user in serializer.data:
                try:
                    get_user = UserProfile.objects.get(id = user.get("id"))
                    user["phone_nummber"]   = get_user.phone_nummber
                    user["gender"]          = get_user.gender
                    user["country"]         = get_user.country.name
                except UserProfile.DoesNotExist:
                    continue
                
            return CustomResponse.success(message = "Success Response", data = serializer.data)
        except:
            return CustomResponse.bad_request(message ="Make Sure That You permation to use this endpoint.", error= "User Type Is Normal User.")


class SetPagesAndGroupPermission(GenericAPIView):
    serializer_class = PermissionSerializers
    permission_classes = [IsSystemUser,]
    def post(self, request, format=None):
        """You have to use this endpoint if there are no permission in database"""
        if not len(Permissions.objects.all()) > 0:
            set_permissions = get_all_permissions(USERTYPE.values)
            serializers = PermissionSerializers(set_permissions, many=True)
            return CustomResponse.success(message="Message Success Setting Permissions", data = serializers.data)
        return CustomResponse.bad_request(
            message="You can't set all permissions again please don't use this endpoint wheel there are permissions in database",
            data=PermissionSerializers(Permissions.objects.all(), many=True).data)