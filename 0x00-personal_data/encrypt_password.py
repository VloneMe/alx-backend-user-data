#!/usr/bin/env python3
"""Provides functions for hashing and validating passwords using bcrypt."""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Returns the salted and hashed password as a byte string.

    Args:
        password: A string representing the password to be hashed.

    Returns:
        A byte string representing the hashed password.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validates the provided password against the hashed password.

    Args:
        hashed_password: A byte string representing the hashed password.
        password: A string representing the password to be validated.

    Returns:
        True if the provided password matches
        the hashed password, False otherwise.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
