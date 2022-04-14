import json
from keycloak import KeycloakOpenID
from keycloak.exceptions import KeycloakAuthenticationError

from django.conf import settings


def get_keycloak_openid() -> KeycloakOpenID:
    try:
        return KeycloakOpenID(
            server_url=settings.KEYCLOAK_CONFIG.get('KEYCLOAK_SERVER_URL'),
            realm_name=settings.KEYCLOAK_CONFIG.get('KEYCLOAK_REALM'),
            client_id=settings.KEYCLOAK_CONFIG.get('KEYCLOAK_CLIENT_ID'),
            client_secret_key=settings.KEYCLOAK_CONFIG.get('KEYCLOAK_CLIENT_SECRET_KEY')
        )
    except KeyError as e:
        raise KeyError(
            f'invalid settings: {e}'
        )

def convert_keycloack_auth_error_to_json(exception: KeycloakAuthenticationError) -> dict:
    """
    convert keycloak authentication error exception to json format
    {"error":"invalid_grant","error_description":"Invalid user credentials"}
    """

    response_body = exception.__dict__.get('response_body').decode('utf-8')
    error = json.loads(response_body)

    return error

