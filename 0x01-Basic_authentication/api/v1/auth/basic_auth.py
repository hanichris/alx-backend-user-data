#!/usr/bin/env python3
"""Module defining a class to manage api authentication.

This class serves as an extension of the base class `Auth.`
"""
from .auth import Auth
import base64
import binascii
from models.user import User
from typing import Tuple, TypeVar


class BasicAuth(Auth):
    """Extends the management done by the `Auth` class"""
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Obtain the Base64 part of the Authorization header.

        Args:
            authorization_header (str): key in request header.
        Return:
            str: base64 encoding of the value stored in authorization_header.
        """
        if authorization_header is None:
            return None
        if type(authorization_header) is not str:
            return None
        auth_value = authorization_header.split()
        if auth_value == [] or auth_value[0] != "Basic":
            return None
        return auth_value[1]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """Decode the value of the base64 string.

        Args:
            base64_authorization_header (str): base64 encoded credentials.
        Return:
            str: decoded string.
        """
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) is not str:
            return None
        try:
            decoded_value = base64_authorization_header.encode()
            decoded_value = base64.b64decode(decoded_value)
        except binascii.Error:
            return None
        else:
            return decoded_value.decode('utf-8')

    def extract_user_credentials(self, decoded_base64_authorization_header:
                                 str) -> Tuple[str, str]:
        """Return the username and email from a decoded base64 string.

        Args:
            decoded_base64_authorization_header (str): decoded base64 string.
        Return
            tuple(str, str): username, password
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if type(decoded_base64_authorization_header) is not str:
            return None, None
        values_list = decoded_base64_authorization_header.split(':',
                                                                maxsplit=1)
        if len(values_list) != 2:
            return None, None
        return values_list[0], values_list[1]

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """Return the `User` instance based on their password & email.

        Args:
            user_email (str): user's email.
            user_pwd (str): user's password.
        Return:
            TypeVar('User'): instance of the user with the given name
                             and password.
        """
        if user_email is None or type(user_email) is not str:
            return None
        if user_pwd is None or type(user_pwd) is not str:
            return None
        try:
            users = User.search({'email': user_email})
            if users == []:
                return None
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
            return None
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Return the `User` instance for a request."""
        auth_header = self.authorization_header(request)
        print(f"I've been called!!!!\n{auth_header}")
        if auth_header is not None:
            encoded = self.extract_base64_authorization_header(auth_header)
            if encoded is not None:
                decoded = self.decode_base64_authorization_header(encoded)
                if decoded is not None:
                    email, pwd = self.extract_user_credentials(decoded)
                    if email and pwd:
                        return self.user_object_from_credentials(email, pwd)
