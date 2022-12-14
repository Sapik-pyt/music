from src.oauth.serializers import GoogleAuth
from google.oauth2 import id_token
from google.auth.transport import requests
from rest_framework.exceptions import AuthenticationFailed
from src.oauth.models import AuthUser
from src.oauth.services import base_auth
from django.conf import settings

def check_google_auth(google_user):
    try:
        id_token.verify_oauth2_token(google_user['tokem'], requests.Request(), settings.GOOGLE_CLIENT_ID)
    except ValueError:
        raise AuthenticationFailed(code=403, detail='Bad token Google')

    user, _ = AuthUser.objects.get_or_create(email=google_user['email'])

    return base_auth.create_token(user.id)