from rest_framework import (
    authentication,
    exceptions,
)
from django.conf import settings
from django.contrib.auth.models import update_last_login
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from dj_rest_keycloak.utils import get_keycloak_openid
from users.choices import ROLE

User = get_user_model()



class KeycloakOpenIDAuthentication(authentication.TokenAuthentication):
        keyword = settings.KEYCLOAK_CONFIG.get('KEYCLOAK_AUTH_HEADER_PREFIX')
        keycloak_openid = None

        def __init__(self):
            self.keycloak_openid = get_keycloak_openid()

        def authenticate(self, request):
            credentials = super().authenticate(request)
            if credentials:
                user, decoded_token = credentials
                request.roles = decoded_token['realm_access']['roles']
            return credentials

        def authenticate_credentials(self, token: str):
            try:
                decoded_token = self._get_decoded_token(token)
                self._verify_token_active(decoded_token)
                user = self._get_or_create_local_user(decoded_token)
                return user, decoded_token

            except Exception:
                raise exceptions.AuthenticationFailed()

        def _get_decoded_token(self, token: str) -> dict:
            """
            make a call to keycloak server to verify the token
            if it's valid return dict of user information
            if not return dict is {'active': False}.
            """
            try:
                return self.keycloak_openid.introspect(token)
            except Exception as e:
                raise Exception(e)

        def _verify_token_active(self, decoded_token: dict) -> None:
            """raise exception is decoded_token.active is False"""
            is_active = decoded_token.get('active', False)
            if not is_active:
                raise exceptions.AuthenticationFailed(
                    'invalid or expired token'
                )

        def _get_or_create_local_user(self, decoded_token: dict) -> User:
            """
            get user from local database or create it if it doesnt exist
            """
            django_uuid_field = settings.KEYCLOAK_CONFIG.get('KEYCLOAK_DJANGO_USER_UUID_FIELD')
            django_fields = self._map_keycloak_to_django_fields(decoded_token)
            sub = decoded_token['sub']

            user = None
            try:
                user = User.objects.get(**{django_uuid_field: sub})
                self._update_user(user, django_fields)
            except ObjectDoesNotExist:
                pass

            if user is None:
                django_fields.update(**{django_uuid_field: sub})
                user = User.objects.create_user(**django_fields)

            update_last_login(sender=None, user=user)
            return user

        def _map_keycloak_to_django_fields(self, decoded_token: dict) -> dict:
            """
            map fields between keycloak and user model
            """
            django_fields = {}
            if 'given_name' in decoded_token:
                django_fields['first_name'] = decoded_token['given_name']

            if 'family_name' in decoded_token:
                django_fields['last_name'] = decoded_token['family_name']

            if 'email' in decoded_token:
                django_fields['email'] = decoded_token['email']

            if 'email_verified' in decoded_token:
                django_fields['is_email_verified'] = decoded_token['email_verified']

            if ROLE.__getitem__("admin") in decoded_token['realm_access']['roles']:
                django_fields['role'] = ROLE.admin

            if ROLE.__getitem__("normal_user") in decoded_token['realm_access']['roles']:
                django_fields['role'] = ROLE.normal_user

            return django_fields

        def _update_user(self, user: User, django_fields: dict) -> None:
            """update user fields and save it on database"""
            save_model = False
            for key, value in django_fields.items():
                try:
                    if getattr(user, key) != value:
                        setattr(user, key, value)
                        save_model = True
                except Exception:
                    pass

            if save_model:
                user.save()
            return user

