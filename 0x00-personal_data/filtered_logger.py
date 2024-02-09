#!/usr/bin/env python3
"""
Provides functions for encrypting and validating passwords using bcrypt.
"""

import bcrypt
from typing import Union


def hash_password(password: str) -> bytes:
    """
    Hashes the provided password using bcrypt.

    Args:
        password: A string representing the password to be hashed.

    Returns:
        A byte string representing the hashed password.
    """
    encoded = password.encode()
    hashed = bcrypt.hashpw(encoded, bcrypt.gensalt())
    return hashed


def is_valid(hashed_password: Union[str, bytes], password: str) -> bool:
    """
    Validates the provided password against the hashed password.

    Args:
        hashed_password: A string or
        bytes object representing the hashed password.
        password: A string representing the password to be validated.

    Returns:
        True if the provided password matches
        the hashed password, False otherwise.
    """
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode()

    encoded = password.encode()
    return bcrypt.checkpw(encoded, hashed_password)
