#!/usr/bin/env python3
"""Module defining a class to manage api authentication.

This class serves as an extension of the base class `Auth.`
"""
from .session_auth import SessionAuth
from datetime import datetime, timedelta
from os import getenv


class SessionExpAuth(SessionAuth):
    """Extends the management of `SessionAuth`.

    Adds an expiration date to a Session ID.
    """
    def __init__(self) -> None:
        try:
            self.session_duration = int(getenv("SESSION_DURATION", 0))
        except (TypeError, ValueError):
            self.session_duration = 0

    def create_session(self, user_id: str = None) -> str:
        """Create a session id for a particular user.

        Args:
            user_id (str): id for a particular user.
        Return:
            str: session id for the user with the `user_id`.
        """
        sess_id = super().create_session(user_id)
        if sess_id is None:
            return None
        self.user_id_by_session_id[sess_id] = {'user_id': user_id,
                                               'created_at': datetime.now()}
        return sess_id

    def user_id_for_session_id(self, session_id=None):
        """Obtain the `user_id` referrenced by the `session_id`.

        Args:
            session_id (str): string representation of a session id.
        Return:
            str: string representation of the user's id.
        """
        if session_id is None:
            return None
        sess_dict = self.user_id_by_session_id.get(session_id)
        if sess_dict is None:
            return None
        if self.session_duration <= 0:
            return sess_dict.get('user_id')
        created_at = sess_dict.get('created_at')
        if created_at is None:
            return None
        timeframe = created_at + timedelta(seconds=self.session_duration)
        if timeframe < datetime.now():
            return None
        return sess_dict.get('user_id')
