# app_auth/views.py
from datetime import datetime

from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics

from app_auth.models.agent_profile import AgentProfile
from app_auth.models.user import CustomUser  # Correct path to the CustomUser model
from app_auth.serializers.users import CustomUserSerializer, PermissionSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from app_auth.models.user import CustomUser  # Adjust this import if necessary
from django.contrib.auth.models import Group
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


class CustomTokenObtainPairView(TokenObtainPairView):

    @swagger_auto_schema(operation_summary="Login")
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        print("email, password", email, password)

        try:
            # Retrieve user by email
            user = CustomUser.objects.get(email=email)

            # Check if the provided password matches the stored password
            if user.check_password(password):
                # Generate tokens
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                # New user
                # new_user = user.new_user
                # user_profile = AgentProfile.objects.filter(user=user)
                # if new_user and user_profile.exists():
                #     user.new_user = False
                #     user.save()

                # Get user groups
                groups = user.groups.all().values_list('name', flat=True)
                permissions = user.user_permissions.all()

                # permission_serializers = PermissionSerializer(permissions, many=True)
                return Response({
                    'refresh': str(refresh),
                    'access': access_token,
                    'groups': list(groups),
                    # 'permissions': permission_serializers
                }, status=status.HTTP_200_OK)
                # If password is correct, proceed to issue the token
                # return super().post(request, *args, **kwargs)
            else:
                # If password is incorrect, return an error response
                return Response({'detail': 'Invalid password'}, status=status.HTTP_401_UNAUTHORIZED)

        except CustomUser.DoesNotExist:
            # If the user does not exist, return an error response
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class CustomTokenRefreshView(TokenRefreshView):

    @swagger_auto_schema(operation_summary="Refresh Token Generator")
    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get('refresh')

        if refresh_token is None:
            return Response({'detail': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)

            return Response({
                'access': access_token,
            }, status=status.HTTP_200_OK)

        except TokenError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
