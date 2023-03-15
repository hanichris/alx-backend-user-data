#!/usr/bin/env python3
"""Working with the `db.py` module"""
from sqlalchemy.orm.exc import NoResultFound

import bcrypt
from typing import TypeVar

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
