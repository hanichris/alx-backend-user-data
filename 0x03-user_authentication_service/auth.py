#!/usr/bin/env python3
"""Working with the `db.py` module"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """Return the computed salt hash of the input password.

    Args:
        password (str): input password in plaintext.
    Return:
        bytes: salt hash of the input password.
    """
    password = password.encode()
    return bcrypt.hashpw(password, bcrypt.gensalt())
