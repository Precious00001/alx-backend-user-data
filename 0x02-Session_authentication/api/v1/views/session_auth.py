#!/usr/bin/env python3
""" Module of session auth views """

# Import necessary modules and classes
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from os import getenv


# Route for user login
@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """ POST /auth_session/login
    Return:
     - User instance based on email
    """
    # Get email and password from the request form
    email = request.form.get('email')
    password = request.form.get('password')

    # Check if email and password are provided
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    try:
        # Search for users with the given email
        users = User.search({'email': email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404

    # Check if any users are found
    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    # Validate password for each user
    for u in users:
        if not u.is_valid_password(password):
            return jsonify({"error": "wrong password"}), 401

        # Create a session and set the session ID as a cookie
        from api.v1.app import auth
        session_id = auth.create_session(u.id)
        out = jsonify(u.to_json())
        out.set_cookie(getenv('SESSION_NAME'), session_id)
        return out

    return jsonify({"error": "no user found for this email"}), 404


# Route for user logout
@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def logout():
    """ DELETE /auth_session/logout
    Return:
     - Empty JSON
    """
    from api.v1.app import auth
    # Destroy the user session (logout) and return an empty JSON object
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
