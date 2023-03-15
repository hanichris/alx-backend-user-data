#!/usr/bin/env python3
"""Working with the `db.py` module"""
from sqlalchemy.orm.exc import NoResultFound

import bcrypt
from typing import Union
from uuid import uuid4

from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """Return the computed salt hash of the input password.

    Args:
        password (str): input password in plaintext.
    Return:
        bytes: salt hash of the input password.
    """
    password = password.encode()
    return bcrypt.hashpw(password, bcrypt.gensalt())


def _generate_uuid() -> str:
    """Generate and return string representation of a UUID"""
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Create a new user while enforcing unique email addresses.

        Args:
            email (str): user's email address.
            password (str): user's password.
        Return:
            User: the created user.
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_pwd = _hash_password(password)
            new_user = self._db.add_user(email, hashed_pwd)
            return new_user
        raise ValueError(f'User {email} already exists')

    def valid_login(self, email: str, password: str) -> bool:
        """Validates the user's credentials.

        Validation first confirms the existence of a user by the supplied
        email then confirms that the supplied password matches the hashed
        password stored in the database.
        Args:
            email (str): user's email.
            password (str): user's password.
        Return:
            bool: whether the supplied credentials are valid.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        return bcrypt.checkpw(password.encode(), user.hashed_password)

    def create_session(self, email: str) -> Union[str, None]:
        """Create a session id for the supplied email.

        Args:
            email (str): user's email address.
        Return:
            str: session id for the email.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        sess_id = _generate_uuid()
        self._db.update_user(user.id, session_id=sess_id)
        return sess_id
