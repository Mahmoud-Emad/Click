from django.contrib.auth.models import Group
from rest_framework.generics import GenericAPIView
from django.shortcuts import render

from server.jornal_app.api.response import CustomResponse
from server.jornal_app.models.users import User
from server.jornal_app.serializers.users import ForgetPasswordUser, UserLoginSerializer, UserRegisterInfoSerializer
from server.jornal_app.services.users import get_user_by_email_for_login, get_user_by_phone_for_login
from server.jornal_app.utils.auth import get_tokens_for_user, validate_email



class UserLoginApiView(GenericAPIView):
    """endpoint for user login"""
    serializer_class = UserLoginSerializer
    
    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            login_field = serializer.validated_data.get('login_field')
            password = serializer.validated_data.get('password')
            validator = validate_email(login_field)
            if validator:
                try:
                    user_email = get_user_by_email_for_login(login_field)
                    if user_email.check_password(password):
                        return CustomResponse.success(message = "Valid email in our system.", data=get_tokens_for_user(user_email))
                except:
                    return CustomResponse.bad_request(message = 'Wrong Credential!')
            else:
                try:
                    user_phone = get_user_by_phone_for_login(login_field)
                    if user_phone.check_password(password):
                        return CustomResponse.success(message = "Valid phone number in our system.", data=get_tokens_for_user(user_phone))
                except:
                    return CustomResponse.bad_request(message = 'Wrong Credential!')
            return CustomResponse.bad_request(message = 'Make sure that you entered a valid data')
        return CustomResponse.bad_request(message = 'Make sure that you entered a valid data')


class UserRegisternIfoAPIView(GenericAPIView):
    """register a new user endpoint"""
    serializer_class = UserRegisterInfoSerializer
    def post(self, request, format=None):
        serializer = UserRegisterInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            normal_data = serializer.data
            normal_data["password"] = "*" * len(normal_data["password"])

            user_group, created  = Group.objects.get_or_create(name='Users')
            user = User.objects.get(email = normal_data["email"])
            user_group.user_set.add(user)

            return CustomResponse.success(data = normal_data)
        return CustomResponse.bad_request(message = "Cant Creat User", error = serializer.errors)



class PasswordResetAPIView(GenericAPIView):
    """
    An end point to send a reset password email
    """
    serializer_class = ForgetPasswordUser
    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                user = get_user_by_email_for_login(serializer.validated_data.get('email'))
                # We can contanue this after setting email confgeration 
                return CustomResponse.success(message="If this email rught you should receive message contain new password")
            except:
                return CustomResponse.not_found(message="There are no user with this email")
        return CustomResponse.bad_request(message="Make sure that you entered a valid data")


def login_view(request):
    return render(request, "registration/login.html")