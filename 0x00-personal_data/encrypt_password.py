#!/usr/bin/env python3
"""
    Encryption Password
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt.

    Args:
        password (str): The plaintext password.

    Returns:
        bytes: The salted, hashed password as a byte string.
    """
    # Check if the password is provided
    if password:
        # Encode the password and generate a salted hash
        return bcrypt.hashpw(str.encode(password), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Validates a password against its hashed version.

    Args:
        hashed_password (bytes): The hashed password.
        password (str): The plaintext password for validation.

    Returns:
        bool: True if the password is valid, False otherwise.
    """
    # Check if both hashed_password and password are provided
    if hashed_password and password:
        # Check if the plaintext password matches the hashed password
        return bcrypt.checkpw(str.encode(password), hashed_password)
