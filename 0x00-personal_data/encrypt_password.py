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
