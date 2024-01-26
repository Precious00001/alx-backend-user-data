#!/usr/bin/env python3
"""
User model
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer

# Create a declarative base for defining the User class
Base = declarative_base()


class User(Base):
    """User model

    Args:
        Base (class): Declarative base from sqlalchemy
    """

    # Define the table name in the database
    __tablename__ = 'users'

    # Define columns for the 'users' table
    id = Column(Integer, primary_key=True)
    # Primary key column
    email = Column(String(250), nullable=False)
    # Email column, not nullable
    hashed_password = Column(String(250), nullable=False)
    # Hashed password column, not nullable
    session_id = Column(String(250), nullable=True)
    # Session ID column, nullable
    reset_token = Column(String(250), nullable=True)
    # Reset token column, nullable
