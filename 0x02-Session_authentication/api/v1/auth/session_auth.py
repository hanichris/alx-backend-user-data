#!/usr/bin/env python3
"""Module defining a class to manage api authentication.

This class serves as an extension of the base class `Auth.`
"""
from .auth import Auth


class SessionAuth(Auth):
    """Extends the management done by `Auth` class.

    Defines the session authentication protocol.
    """
    pass