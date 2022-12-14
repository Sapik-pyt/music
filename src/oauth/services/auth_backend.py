import jwt
from datetime import datetime
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from src.oauth.models import AuthUser


class AuthBackend(authentication.BaseAuthentication):
    authentication_header_prefix = "Token"

    def authenticate(self, request, token=None, **kwargs):
        auth_header = authentication.get_authorization_header(request).split()

        if not auth_header or auth_header[0].lower() != b'token':
            return None

        if len(auth_header) == 1:
            raise AuthenticationFailed("Invalid token")

        elif len(auth_header) > 2:
            raise AuthenticationFailed(
                "Invalid token header. Token strimg should not contain spaces"
            )

        try:
            token = auth_header[1].decode('utf-8')
        except UnicodeError:
            raise AuthenticationFailed(
                "Invalid token header. Tokin string should contain invalid charaster"
            )

        return self.authenticate_credential(token)


    def authenticate_credential(self, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        except jwt.PyJWTError:
            raise AuthenticationFailed("Invalid authetnication. Could not decode token")
        token_exp = datetime.fromtimestamp(payload['exp'])
        if token_exp < datetime.utcnow():
            raise AuthenticationFailed("Token expired")

        try:
            user = AuthUser.objects.get(id=payload["user_id"])
        except AuthUser.DoesNotExist:
            raise AuthenticationFailed("No user matching this token")

        return user, None