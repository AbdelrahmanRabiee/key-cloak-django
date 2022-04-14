from rest_framework import mixins, status
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet

from users import serializers
from users.models import User
from users.permissions import IsAdmin


class AdminUserViewSet(ReadOnlyModelViewSet):
    """
    This endpoint is only for admin user
    """
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAdmin]

    def get_queryset(self):
        return User.objects.filter(keycloak_id=self.request.user.keycloak_id)


class NormalUserViewSet(ReadOnlyModelViewSet):
    """
    This endpoint is for users and admins
    """
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(keycloak_id=self.request.user.keycloak_id)


class LoginViewSet(mixins.CreateModelMixin, GenericViewSet):
    """This login endpoint for both admin and user to get access token"""
    serializer_class = serializers.LoginSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)