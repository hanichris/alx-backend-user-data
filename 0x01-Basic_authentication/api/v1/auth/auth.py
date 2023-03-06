#!/usr/bin/env python3
"""Module defining a class to manage api authentication."""
from flask import request
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
        return not (path in excluded_paths)

    def authorization_header(self, request=None) -> str:
        """Include the authorization header to the request being made."""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Get's the current user making a request."""
        return None
