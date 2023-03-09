#!/usr/bin/env python3
"""Module defining a class to manage api authentication."""
from flask import request
from os import getenv
from typing import List, TypeVar


class Auth:
    """Manages API authentication."""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """checks which endpoint requires authentication to access."""
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        path = f"{path}/" if path[-1] != '/' else path
        if path in excluded_paths:
            return False
        for entry in excluded_paths:
            if entry[-1] == '*' and path.startswith(entry[:-1]):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """Obtain the value of the authorization key from the request."""
        if request is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """Get's the current user making a request."""
        return None

    def session_cookie(self, request=None):
        """Obtain cookie value from a request."""
        if request is None:
            return None
        cookie = getenv("SESSION_NAME")
        return request.cookies.get(cookie)
