#!/usr/bin/env python3

"""This maps declarations for SQLAlchemy"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """
    SQLAlchemy model representing a user table in the database.

    Attributes:
    - id: Integer, primary key for the user.
    - email: String, email address of the user.
    - hashed_password: String, hashed password of the user.
    - session_id: String, session ID of the user's current session.
    - reset_token: String, token used for password reset.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
