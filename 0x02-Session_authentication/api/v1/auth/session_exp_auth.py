#!/usr/bin/env python3
"""
SessionExpAuth class to manage API authentication
"""
from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """SessionExpAuth class to manage API authentication"""

    def __init__(self):
        """Initialize SessionExpAuth
        """
        try:
            # Attempt to get the session duration from environment variable
            self.session_duration = int(getenv('SESSION_DURATION'))
        except Exception:
            # Set session duration to 0 if an exception occurs
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Create session
        """
        # Call the create_session method from the parent class
        session_id = super().create_session(user_id)
        if session_id:
            # Store user_id and creation timestamp in
            # the user_id_by_session_id dictionary
            SessionAuth.user_id_by_session_id[session_id] = {
                'user_id': user_id, 'created_at': datetime.now()}
            return session_id

    def user_id_for_session_id(self, session_id=None):
        """Get user ID from session
        """
        # Check if session_id is provided
        if not session_id:
            return None

        # Get the session dictionary from user_id_by_session_id
        session_dict = SessionExpAuth.user_id_by_session_id.get(session_id)

        # Check if session_dict is available
        if not session_dict:
            return None

        # Check if session_duration is set to 0 (indicating no expiration)
        if self.session_duration <= 0:
            return session_dict['user_id']

        # Check if 'created_at' is present in the session_dict
        if 'created_at' not in session_dict:
            return None

        # Calculate the expiration time based on session_duration
        delta = timedelta(seconds=self.session_duration)

        # Check if the session has expired
        if session_dict['created_at'] + delta < datetime.now():
            return None

        # Return the user_id if the session is still valid
        return session_dict['user_id']
