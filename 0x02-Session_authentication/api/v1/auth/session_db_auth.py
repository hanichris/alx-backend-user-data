#!/usr/bin/env python3
"""Module defining a class to manage api authentication.

This class serves as an extension of the base class `Auth.`
"""
from .session_exp_auth import SessionExpAuth
from datetime import datetime, timedelta
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """Extends the management of `SessionExpAuth`.

    Stores the session id for a given user to a database.
    """
    def create_session(self, user_id: str = None) -> str:
        """Create a session id for the user with id `user_id`.

        Args:
            user_id (str): id for a particular user.
        Return:
            str: the session id for the user.
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        user = UserSession(**{'user_id': user_id,
                              'session_id': session_id})
        user.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Obtain the `user_id` referrenced by the `session_id`.

        Args:
            session_id (str): string representation of a session id.
        Return:
            str: string representation of the user's id.
        """
        if session_id is None or type(session_id) is not str:
            return None
        users = UserSession.search({'session_id': session_id})
        if users == []:
            return None
        created_at = users[0].created_at
        if created_at is None:
            return None
        timeframe = created_at + timedelta(seconds=self.session_duration)
        if timeframe < datetime.now():
            return None
        return users[0].user_id

    def destroy_session(self, request=None):
        """Destroy the user session based on the `session` id.

        Args:
            request (request): current request that has been made.
        """
        if request is None:
            return False
        cookie = self.session_cookie(request)
        if cookie is None:
            return False
        users = UserSession.search({'session_id': cookie})
        if users == []:
            return False
        users[0].remove()
        return True
