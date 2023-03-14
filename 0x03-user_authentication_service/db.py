#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session

from typing import TypeVar
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Create a new user and save their details to the database.

        Args:
            email (str): email of the new user.
            hashed_password (str): the new user's hashed password.
        Return:
            User
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs):
        """Find the first row found in `users` table.

        Returns exactly one result or raises an exception. Raises
        `sqlalchemy.orm.exc.NoResultFound` if the query selects no
        rows and `sqlalchemy.orm.exc.MultipleResultsFound` if multiple
        object identities are return.
        """
        kwargs_set = set(kwargs)
        users_set = set(User.__dict__)
        if kwargs_set.intersection(users_set) == set():
            raise InvalidRequestError
        user = self._session.query(User).filter_by(**kwargs).first()
        if user is None:
            raise NoResultFound
        return user
