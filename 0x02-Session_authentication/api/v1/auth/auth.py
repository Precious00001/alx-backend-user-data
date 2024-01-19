#!/usr/bin/env python3
"""
Manage API authentication
"""

# Import necessary modules and classes
from flask import request
from typing import List, TypeVar
from os import getenv


class Auth:
    """ Manage API authentication """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Check if the path is in the list of excluded paths """
        if not path or not excluded_paths:
            return True
        if path[-1] != '/':
            path += '/'
        for p in excluded_paths:
            if path[:p.find('*')] in p[:p.find('*')]:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """ Return the authorization header """
        if not request:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """ Return None """
        return None

    def session_cookie(self, request=None):
        """ Return a cookie value from a request """
        if request:
            return request.cookies.get(getenv('SESSION_NAME'))
