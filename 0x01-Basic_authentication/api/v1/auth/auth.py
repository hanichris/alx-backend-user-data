#!/usr/bin/env python3
"""Module defining a class to manage api authentication."""
from flask import request
from typing import List, TypeVar


class Auth:
    """Manages API authentication."""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """checks which endpoint requires authorization to access."""
        return False

    def authorization_header(self, request=None) -> str:
        """Include the authorization header to the request being made."""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Get's the current user making a request."""
        return None
