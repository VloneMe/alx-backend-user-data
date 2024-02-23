#!/usr/bin/env python3
"""Password Hashing"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _hash_password(password: str) -> str:
    """
    Hashes the input password using bcrypt.

    Args:
        password: A string representing the password to be hashed.

    Returns:
        A string representing the salted hash of the input password.
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def _generate_uuid() -> str:
    """
    Generates a string representation of a new UUID.

    Returns:
        A string representing a new UUID.
    """
    return str(uuid.uuid4())


class Auth:
    """
    Auth class to interact with the authentication database.
    """

    def __init__(self):
        """
        Initializes an instance of the Auth class.
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Registers a new user with the provided email and password.

        Args:
            email: A string representing the email of the user.
            password: A string representing the password of the user.

        Returns:
            An instance of the User class representing the registered user.
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError('User {} already exists'.format(email))
        except NoResultFound:
            hpassword = _hash_password(password)
            user = self._db.add_user(email, hpassword)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """
        Checks if the provided password is correct for the given email.

        Args:
            email: A string representing the email of the user.
            password: A string representing the password to be checked.

        Returns:
            A boolean value indicating whether the login is valid or not.
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                return bcrypt.checkpw(
                        password.encode(),
                        user.hashed_password.encode()
                        )
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """
        Creates a session for the user with the provided email.

        Args:
            email: A string representing the email of the user.

        Returns:
            A string representing the session ID for the user.
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                session_id = _generate_uuid()
                self._db.update_user(user.id, session_id=session_id)
                return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> str:
        """
        Returns the corresponding user for the given session ID.

        Args:
            session_id: A string representing the session ID.

        Returns:
            An instance of the User class corresponding to the session ID.
        """
        if not session_id:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except Exception as e:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Destroys the session for the user with the given user ID.

        Args:
            user_id: An integer representing the ID of the user.
        """
        self._db.update_user(user_id, session_id=None)
        return None

    def get_reset_password_token(self, email: str) -> str:
        """
        Generates a reset token for the user with the provided email.

        Args:
            email: A string representing the email of the user.

        Returns:
            A string representing the reset token for the user.
        """
        if not email:
            return None
        try:
            user = self._db.find_user_by(email=email)
            token = _generate_uuid()
            self._db.update_user(user.id, reset_token=token)
            return token
        except Exception as e:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Updates the password for the user with the provided reset token.

        Args:
            reset_token: A string representing the reset token.
            password: A string representing the new password for the user.
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            new_password = _hash_password(password)
            self._db.update_user(
                    user.id,
                    hashed_password=new_password,
                    reset_token=None
                    )
            return None
        except Exception as e:
            raise ValueError
