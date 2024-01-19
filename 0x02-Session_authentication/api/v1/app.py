#!/usr/bin/env python3
"""Route module for the API."""
import os
from os import getenv
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)

from api.v1.views import app_views
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth
from api.v1.auth.session_db_auth import SessionDBAuth
from api.v1.auth.session_exp_auth import SessionExpAuth

# Create a Flask application
app = Flask(__name__)
# Register the Blueprint for API views
app.register_blueprint(app_views)
# Enable Cross-Origin Resource Sharing (CORS) for the entire app
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Initialize auth based on the chosen authentication type
auth = None
auth_type = getenv('AUTH_TYPE', 'auth')
if auth_type == 'auth':
    auth = Auth()
if auth_type == 'basic_auth':
    auth = BasicAuth()
if auth_type == 'session_auth':
    auth = SessionAuth()
if auth_type == 'session_exp_auth':
    auth = SessionExpAuth()
if auth_type == 'session_db_auth':
    auth = SessionDBAuth()

# Define error handlers for 404, 401, and 403 errors
@app.errorhandler(404)
def not_found(error) -> str:
    """Not found handler."""
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(401)
def unauthorized(error) -> str:
    """Unauthorized handler."""
    return jsonify({"error": "Unauthorized"}), 401

@app.errorhandler(403)
def forbidden(error) -> str:
    """Forbidden handler."""
    return jsonify({"error": "Forbidden"}), 403

# Define a function to authenticate the user before processing a request
@app.before_request
def authenticate_user():
    """Authenticates a user before processing a request."""
    if auth:
        # Define paths that do not require authentication
        excluded_paths = [
            "/api/v1/status/",
            "/api/v1/unauthorized/",
            "/api/v1/forbidden/",
            "/api/v1/auth_session/login/",
        ]
        # Check if authentication is required for the current path
        if auth.require_auth(request.path, excluded_paths):
            user = auth.current_user(request)
            # Check if either authorization header or session cookie is present
            if auth.authorization_header(request) is None and \
                    auth.session_cookie(request) is None:
                # If not present, abort with a 401 Unauthorized error
                abort(401)
            # Check if the user is authenticated
            if user is None:
                # If not authenticated, abort with a 403 Forbidden error
                abort(403)
            # Attach the authenticated user to the request
            request.current_user = user

# Run the Flask app if the script is executed
if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)