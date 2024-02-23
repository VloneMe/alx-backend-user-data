#!/usr/bin/env python3
"""
Implementation of a Database class using SQLAlchemy.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from user import Base, User
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


class DB:
    """
    Represents a Database class for SQLAlchemy operations.
    """

    def __init__(self):
        """
        Initializes the Database class by creating an engine and session.
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self):
        """
        Creates and provides a session for database operations.
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Adds a new user to the database.

        Parameters:
        - email: str, email address of the user.
        - hashed_password: str, hashed password of the user.

        Returns:
        User: The newly created User object.
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        Finds a user in the database based on provided filters.

        Parameters:
        **kwargs: Arbitrary keyword arguments for filtering.

        Returns:
        User: The user found in the database.

        Raises:
        InvalidRequestError: If the provided filter is invalid.
        NoResultFound: If no user is found based on the provided filters.
        """
        if kwargs is None:
            raise InvalidRequestError
        for k in kwargs.keys():
            if not hasattr(User, k):
                raise InvalidRequestError
        try:
            user = self._session.query(User).filter_by(**kwargs).first()
        except InvalidRequestError:
            raise InvalidRequestError
        if user is None:
            raise NoResultFound
        else:
            return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Updates a user's attributes in the database.

        Parameters:
        - user_id: int, the ID of the user to update.
        **kwargs: Arbitrary keyword arguments representing
          attributes to update.

        Raises:
        ValueError: If an invalid attribute is provided for update.
        """
        user = self.find_user_by(id=user_id)
        for k, v in kwargs.items():
            if not hasattr(user, k):
                raise ValueError
            else:
                setattr(user, k, v)
        self._session.commit()
