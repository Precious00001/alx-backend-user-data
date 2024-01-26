#!/usr/bin/env python3
""" UserSession module
"""
from models.base import Base


class UserSession(Base):
    """ UserSession class
    """

    def __init__(self, *args: list, **kwargs: dict):
        """ Initialize a UserSession instance
        """
        # Call the constructor of the parent class (Base)
        super().__init__(*args, **kwargs)

        # Retrieve user_id and session_id from keyword arguments
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
