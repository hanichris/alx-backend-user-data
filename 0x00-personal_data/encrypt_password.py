#!/usr/bin/env python3
"""Ensures passwords aren't stored in plaintext within the database."""
import bcrypt


def hash_password(password: str) -> bytes:
    """Generate a salted, hashed password for the plaintext password.

    Args:
        password (str): password in plaintext.
    Return
        bytes: salted, hashed password.
    """
    password = password.encode()
    return bcrypt.hashpw(password, bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Validate the plaintext password.

    Args:
        hashed_password (bytes): the `hashed_password` stored in the db.
        password (str): plaintext password entered by user.
    Return:
        bool: whether entered password matches the stored password.
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
