#!/usr/bin/env python3
"""Module defining a class to manage api authentication.

This class serves as an extension of the base class `Auth.`
"""
from .auth import Auth
import base64


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
