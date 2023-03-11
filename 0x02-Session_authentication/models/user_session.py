#!/usr/bin/env python3
""" UserSession module
"""
from .base import Base


class UserSession(Base):
    """User Session that enables storage of session IDs in db."""
    def __init__(self, *args: list, **kwargs: dict):
        """Initialize a UserSession instance."""
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
