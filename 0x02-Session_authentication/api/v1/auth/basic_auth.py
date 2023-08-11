#!/usr/bin/env python3
"""Basic Auth implementation module
"""


from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """Basic Auth Class"""
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
        Performs base64 encoding on the authorization_header
        extract base64 of authorization header after "Basic "
        """
        if authorization_header is None or type(authorization_header) != str:
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split("Basic ")[1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        Decodes a base64 string return base64 of string
        """
        if base64_authorization_header is None or \
           type(base64_authorization_header) != str:
            return None

        try:
            return base64.b64decode(base64_authorization_header).\
                decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        extract user credentials from the Base64 decoded value
        returns the user email and password
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        user_credentials = decoded_base64_authorization_header.split(':', 1)
        return user_credentials[0], user_credentials[1]

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """ return User instance based on their email and password
        """
        if user_email is None or type(user_email) != str:
            return None
        if user_pwd is None or type(user_pwd) != str:
            return None

        try:
            users = User.search({'email': user_email})
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """retrieves the User instance for a request
        """
        auth_header = self.authorization_header(request)
        b64Header = self.extract_base64_authorization_header(auth_header)
        decoded = self.decode_base64_authorization_header(b64Header)
        credentials = self.extract_user_credentials(decoded)
        user = self.user_object_from_credentials(
            credentials[0], credentials[1])
        return user
