#!/usr/bin/env python3
"""Module declaring a `User` mapping."""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String


Base = declarative_base()


class User(Base):
    """Maps to the table `users` that stores the records for users.

    The columns of the table `users` are:
        id, email, hashed_password, session_id, reset_token
    Id is the primary key of the table while `session_id` and `reset_token`
    are columns that can contain NULL values. The rest cannot.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250))
    reset_token = Column(String(250))
