from rest_framework import serializers

from users.models import User
from dj_rest_keycloak.utils import get_keycloak_openid, convert_keycloack_auth_error_to_json


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=False)
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        keycloak_openid = get_keycloak_openid()
        try:
            token = keycloak_openid.token(email, password)
        except Exception as e:
            raise serializers.ValidationError(convert_keycloack_auth_error_to_json(e))
        return token
