#!/usr/bin/env python3
""" SessionAuth class to manage API authentication """

# Import necessary modules and classes
from api.v1.auth.auth import Auth
from models.user import User
import uuid


class SessionAuth(Auth):
    """ SessionAuth class to manage API authentication """

    # Dictionary to store user_id mapped to session_id
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Create a Session ID for a user_id """
        if isinstance(user_id, str):
            # Generate a unique session ID using uuid
            session_id = str(uuid.uuid4())
            # Map the session_id to the user_id in the dictionary
            SessionAuth.user_id_by_session_id[session_id] = user_id
            return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Retrieve user_id for a given session_id """
        if isinstance(session_id, str):
            return SessionAuth.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """ Return a User instance based on a cookie value """
        return User.get(
            self.user_id_for_session_id(self.session_cookie(request)))

    def destroy_session(self, request=None):
        """ Delete the user session / log out """
        if request:
            session_id = self.session_cookie(request)
            if not session_id:
                return False
            if not self.user_id_for_session_id(session_id):
                return False
            # Remove the session_id from the dictionary
            self.user_id_by_session_id.pop(session_id)
            return True
