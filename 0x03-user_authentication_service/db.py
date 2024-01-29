#!/usr/bin/env python3
"""
DB class
"""

from sqlalchemy import create_engine
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from typing import TypeVar
from user import Base, User  # Assuming there is an import for the User model

DATA = ['id', 'email', 'hashed_password', 'session_id', 'reset_token']


class DB:
    """Database class for managing user data"""

    def __init__(self):
        """Initialize the DB class"""
        # Create a SQLite database engine
        self._engine = create_engine("sqlite:///a.db", echo=False)

        # Drop and create all tables defined in the Base class
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)

        # Initialize the session to None
        self.__session = None

    @property
    def _session(self):
        """Property to get the database session"""
        if self.__session is None:
            # Create a session if it doesn't exist
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add user to the database

        Args:
            email (string): Email of the user
            hashed_password (string): Hashed password of the user
        Returns:
            User: User object created
        """
        if not email or not hashed_password:
            return  # If either email or hashed_password is missing, do nothing

        # Create a new User instance
        user = User(email=email, hashed_password=hashed_password)

        # Add the user to the session and commit the changes
        session = self._session
        session.add(user)
        session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """Find user by specified arguments

        Returns:
            User: User found or raises NoResultFound if not found
        """
        user = self._session.query(User).filter_by(**kwargs).first()
        if not user:
            raise NoResultFound
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update user by ID

        Args:
            user_id (int): ID of the user to be updated
        """
        # Find the user by ID
        user = self.find_user_by(id=user_id)

        # Update user attributes based on provided kwargs
        for key, val in kwargs.items():
            if key not in DATA:
                raise ValueError(f"Invalid key: {key}")
            setattr(user, key, val)

        # Commit the changes to the database
        self._session.commit()
        return None
