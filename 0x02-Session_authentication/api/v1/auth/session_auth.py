#!/usr/bin/env python3
"""Module defining a class to manage api authentication.

This class serves as an extension of the base class `Auth.`
"""
from .auth import Auth
from models.user import User
from typing import TypeVar
import uuid


class SessionAuth(Auth):
    """Extends the management done by `Auth` class.

    Defines the session authentication protocol.
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Create a session id for a particular user.

        Args:
            user_id (str): id for a particular user.
        Return:
            str: session id for the user with the `user_id`.
        """
        if user_id is None:
            return None
        if type(user_id) is not str:
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Obtain the `user_id` referrenced by the `session_id`.

        Args:
            session_id (str): string representation of a session id.
        Return:
            str: string representation of the user's id.
        """
        if session_id is None:
            return None
        if type(session_id) is not str:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> TypeVar('User'):
        """Obtain a `User` instance based on the cookie `_my_session_id`.

        Args:
            request (request): request that was made.
        Return:
            User: instance of User class.
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        return User.get(user_id)

    def destroy_session(self, request=None):
        """Delete the user session (log the user out)."""
        if request is None:
            return False
        cookie = self.session_cookie(request)
        if cookie is None:
            return False
        if self.user_id_for_session_id(cookie) is None:
            return False
        del self.user_id_by_session_id[cookie]
        return True
