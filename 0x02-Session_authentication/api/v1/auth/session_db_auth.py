#!/usr/bin/env python3
"""
SessionDBAuth class to manage API authentication
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from os import getenv
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """SessionDBAuth class to manage API authentication"""

    def create_session(self, user_id=None):
        """Create session
        """
        # Call the create_session method from the parent class
        if user_id:
            session_id = super().create_session(user_id)

            # Create a UserSession instance and save it to the file
            us = UserSession(user_id=user_id, session_id=session_id)
            us.save()
            UserSession.save_to_file()
            return session_id

    def user_id_for_session_id(self, session_id=None):
        """Get user ID from session
        """
        # Check if session_id is provided
        if not session_id:
            return None

        # Load UserSession data from file
        UserSession.load_from_file()

        # Search for UserSession entries with the given session_id
        users = UserSession.search({'session_id': session_id})

        # Check if any users are found
        for u in users:
            # Calculate expiration time based on session_duration
            delta = timedelta(seconds=self.session_duration)

            # Check if the session has expired
            if u.created_at + delta < datetime.now():
                return None

            # Return the user_id if the session is still valid
            return u.user_id

    def destroy_session(self, request=None):
        """Delete the user session / log out
        """
        if request:
            # Get session_id from the request's cookie
            session_id = self.session_cookie(request)

            # Check if session_id is present
            if not session_id:
                return False

            # Check if user_id is associated with the session_id
            if not self.user_id_for_session_id(session_id):
                return False

            # Search for UserSession entries with the given session_id
            users = UserSession.search({'session_id': session_id})

            # Remove the UserSession entry, save to file, and return True
            for u in users:
                u.remove()
                UserSession.save_to_file()
                return True
        return False
