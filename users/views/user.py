from django.contrib.auth import get_user_model
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, status
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.services.user import UserService

User = get_user_model()


class UserLogin(GenericAPIView):
    """User login View"""

    class InputSerializer(serializers.Serializer):
        """DRF Serializer for login"""
        username = serializers.CharField(required=True)
        password = serializers.CharField(required=True)

        class Meta:
            """Meta Class"""
            ref_name = None

    class OutputSerializer(serializers.ModelSerializer):
        """DRF serializer for login endpoint response."""
        key = serializers.CharField(help_text="Created token key")

        class Meta:
            """Meta Class"""
            model = Token
            fields = ("key",)
            ref_name = None

    @swagger_auto_schema(
        request_body=InputSerializer,
        responses={201: openapi.Response('Returns token key', OutputSerializer)})
    def post(self, request):
        """User login endpoint"""
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = UserService.user_login(serializer.data['username'], serializer.data['password'])
        return Response(
            self.OutputSerializer(token, many=False).data,
            status=status.HTTP_201_CREATED
        )


class UserLogout(GenericAPIView):
    """User logout endpoint"""
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        request_body=serializers.Serializer,
        responses={200: openapi.Response("User active Token is deleted", status=200)})
    def post(self, request):
        """User logout endpoint"""
        UserService.user_logout(request.user)
        return Response(
            status=status.HTTP_200_OK
        )
