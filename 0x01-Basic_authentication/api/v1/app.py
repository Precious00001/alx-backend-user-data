#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None
if os.getenv('AUTH_TYPE') == 'auth':
    from api.v1.auth.auth import Auth
    auth = Auth()
elif os.getenv('AUTH_TYPE') == 'basic_auth':
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """Handles unauthorized access.

    Args:
        error: The error object.

    Returns:
        str: JSON response indicating unauthorized access.
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """Handles forbidden access.

    Args:
        error: The error object.

    Returns:
        str: JSON response indicating forbidden access.
    """
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def before_request() -> None:
    """Executed before handling each request.

    Checks for authentication and authorization
    before processing the request.

    Returns:
        None: Continues processing the request if authorized;
        otherwise, aborts with 401 or 403 error.
    """
    # Paths that do not require authentication
    paths = ['/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/']

    # Skip authentication for certain paths
    if not auth:
        return None

    # Allow access to paths without authentication
    if not auth.require_auth(request.path, paths):
        return None

    # Check for presence of authorization header
    if not auth.authorization_header(request):
        abort(401)

    # Check current user authorization
    if not auth.current_user(request):
        abort(403)


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
