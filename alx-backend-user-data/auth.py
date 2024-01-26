#!/usr/bin/env python3
"""
Auth module
"""
from db import DB
from uuid import uuid4
from user import User
from bcrypt import hashpw, gensalt, checkpw
from typing import TypeVar
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> str:
    """Hash a password for a user

    Args:
        password (str): Password of the user

    Returns:
        str: Hashed password
    """
    return hashpw(password.encode('utf-8'), gensalt())


def _generate_uuid() -> str:
    """Generate a UUID

    Returns:
        str: Representation of a new UUID
    """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Initialize the Auth class"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a user

        Args:
            email (str): Email of the user
            password (str): Password of the user

        Returns:
            User: User registered
        """
        try:
            # Check if the user already exists
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))

    def valid_login(self, email: str, password: str) -> bool:
        """Validate login credentials of a user

        Args:
            email (str): Email of the user
            password (str): Password of the user

        Returns:
            bool: True if login is valid, False otherwise
        """
        try:
            # Find the user by email
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        return checkpw(password.encode('utf-8'), user.hashed_password)

    def create_session(self, email: str) -> str:
        """Create a new session for a user

        Args:
            email (str): Email of the user

        Returns:
            str: String representation of session ID
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            # Update the user's session ID in the database
            self._db.update_user(user.id, session_id=session_id)
        except NoResultFound:
            return

    def get_user_from_session_id(self, session_id: str) -> str:
        """Get user email from session ID

        Args:
            session_id (str): Session ID of the user

        Returns:
            str: User email
        """
        if session_id is None:
            return
        try:
            # Find the user by session ID
            user = self._db.find_user_by(session_id=session_id)
            return user.email
        except NoResultFound:
            return

    def destroy_session(self, user_id: int) -> None:
        """Destroy session for a user

        Args:
            user_id (int): User ID
        """
        try:
            # Find the user by ID and update their session ID to None
            user = self._db.find_user_by(id=user_id)
            self._db.update_user(user.id, session_id=None)
        except NoResultFound:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """Get reset password token for a user

        Args:
            email (str): User email

        Raises:
            ValueError: If the user is not found

        Returns:
            str: Reset token
        """
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            # Update the user's reset token in the database
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """Update user password using reset token

        Args:
            reset_token (str): Reset token
            password (str): User password

        Raises:
            ValueError: If the user is not found
        """
        try:
            # Find the user by reset token and update
            # their password and reset token
            user = self._db.find_user_by(reset_token=reset_token)
            self._db.update_user(user.id,
                                 hashed_password=_hash_password(password),
                                 reset_token=None)
        except NoResultFound:
            raise ValueError
