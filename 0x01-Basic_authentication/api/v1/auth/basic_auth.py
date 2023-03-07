#!/usr/bin/env python3
"""Module defining a class to manage api authentication.

This class serves as an extension of the base class `Auth.`
"""
from .auth import Auth
import base64
import binascii
from typing import Tuple


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
            decoded_value = base64.b64decode(base64_authorization_header)
        except binascii.Error:
            return None
        else:
            return decoded_value.decode('utf-8')

    def extract_user_credentials(self, decoded_base64_authorization_header:
                                 str) -> Tuple[str, str]:
        """Return the username and email from a decoded base64 string.

        Args:
            decoded_base64_authorization_header (str): decode base64 string.
        Return
            tuple(str, str): username, password
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if type(decoded_base64_authorization_header) is not str:
            return None, None
        values_list = decoded_base64_authorization_header.split(':')
        if len(values_list) != 2:
            return None, None
        return values_list[0], values_list[1]
