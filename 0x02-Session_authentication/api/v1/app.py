#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)

# Create a Flask application
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# Register the Blueprint for the API views
app.register_blueprint(app_views)

# Enable CORS for the entire application
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Initialize authentication based on the specified AUTH_TYPE
auth = None
auth_type = getenv('AUTH_TYPE')
if auth_type == 'auth':
    from api.v1.auth.auth import Auth
    auth = Auth()
elif auth_type == 'basic_auth':
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
elif auth_type == 'session_auth':
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()
elif auth_type == 'session_exp_auth':
    from api.v1.auth.session_exp_auth import SessionExpAuth
    auth = SessionExpAuth()
elif auth_type == 'session_db_auth':
    from api.v1.auth.session_db_auth import SessionDBAuth
    auth = SessionDBAuth()


# Error handler for 404 - Not Found
@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


# Error handler for 401 - Unauthorized
@app.errorhandler(401)
def unauthorized(error) -> str:
    """ Request unauthorized
    """
    return jsonify({"error": "Unauthorized"}), 401


# Error handler for 403 - Forbidden
@app.errorhandler(403)
def forbidden(error) -> str:
    """ Request forbidden
    """
    return jsonify({"error": "Forbidden"}), 403


# Before each request, perform authentication
# and set current_user in the request object
@app.before_request
def before_request():
    """ Before request
    """
    excluded_paths = ['/api/v1/status/', '/api/v1/unauthorized/',
                      '/api/v1/forbidden/', '/api/v1/auth_session/login/']
    if auth and auth.require_auth(request.path, excluded_paths):
        if (not auth.authorization_header(request) and
                not auth.session_cookie(request)):
            # Abort with 401 Unauthorized if no authorization
            # header or session cookie is present
            abort(401)
        if not auth.current_user(request):
            # Abort with 403 Forbidden if the current user cannot be determined
            abort(403)
        # Set the current_user in the request object for further use
        request.current_user = auth.current_user(request)


# Start the Flask application if this script is executed directly
if __name__ == "__main__":
    # Get host and port from environment variables or use default values
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    # Run the Flask application
    app.run(host=host, port=port)
