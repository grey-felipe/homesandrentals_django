import jwt
import os
from django.conf import settings
from rest_framework import authentication, exceptions
from .models import User


class JWTAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = 'Bearer'

    def authenticate(self, request):
        request.user = None
        auth_header = authentication.get_authorization_header(request).split()
        auth_header_prefix = self.authentication_header_prefix.lower()

        if not auth_header:
            return None

        if len(auth_header) <= 1:
            return None

        if len(auth_header) > 2:
            return None

        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')

        if prefix.lower() != authentication_header_prefix:
            return None

        return _authenticate_credentials(request, token)

    def _authenticate_credentials(self, request, token):
        try:
            payload = jwt.decode(token, os.environ['APP_SECRET_KEY'])
        except:
            raise exceptions.AuthenticationFailed('Authentication failed!')

        try:
            user = User.objects.get(pk=payload['id'])
        except:
            raise exceptions.AuthenticationFailed('User not recognised.')

        if not user.isActive:
            raise exceptions.AuthenticationFailed('This user is deactivated!')

        data = (user, token)
        
        return data
