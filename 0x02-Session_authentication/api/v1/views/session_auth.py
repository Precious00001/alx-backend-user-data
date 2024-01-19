#!/usr/bin/env python3
"""Module of session authenticating views."""
import os
from typing import Tuple
from flask import abort, jsonify, request

from models.user import User
from api.v1.views import app_views


# Route for user login
@app_views.route('/auth_session/login',
                 methods=['POST'], strict_slashes=False)
def login() -> Tuple[str, int]:
    """POST /api/v1/auth_session/login
    Return:
      - JSON representation of a User object.
    """
    not_found_res = {"error": "no user found for this email"}

    # Get email and password from the request form
    email = request.form.get('email')
    if email is None or len(email.strip()) == 0:
        return jsonify({"error": "email missing"}), 400
    password = request.form.get('password')
    if password is None or len(password.strip()) == 0:
        return jsonify({"error": "password missing"}), 400

    try:
        # Search for users with the given email
        users = User.search({'email': email})
    except Exception:
        return jsonify(not_found_res), 404

    # Check if user with the given email exists
    if len(users) <= 0:
        return jsonify(not_found_res), 404

    # Validate the password
    if users[0].is_valid_password(password):
        from api.v1.app import auth
        # Create a session and set the session ID as a cookie
        session_id = auth.create_session(getattr(users[0], 'id'))
        res = jsonify(users[0].to_json())
        res.set_cookie(os.getenv("SESSION_NAME"), session_id)
        return res

    # Return error if the password is incorrect
    return jsonify({"error": "wrong password"}), 401


# Route for user logout
@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def logout() -> Tuple[str, int]:
    """DELETE /api/v1/auth_session/logout
    Return:
      - An empty JSON object.
    """
    from api.v1.app import auth
    # Destroy the user session (logout) and return an empty JSON object
    is_destroyed = auth.destroy_session(request)
    if not is_destroyed:
        abort(404)
    return jsonify({})
