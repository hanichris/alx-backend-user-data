#!/usr/bin/env python3
"""Module defining a class to manage api authentication.

This class serves as an extension of the base class `Auth.`
"""
from .auth import Auth
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
