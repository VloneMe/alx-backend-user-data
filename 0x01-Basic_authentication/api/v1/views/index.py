#!/usr/bin/env python3
"""Module for Index views."""
from flask import jsonify, abort
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """Return the status of the API.

    Returns:
        str: JSON response indicating the status of the API.
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats/', strict_slashes=False)
def stats() -> str:
    """Return the number of each object.

    Returns:
        str: JSON response containing the number of each object.
    """
    from models.user import User
    stats = {}
    stats['users'] = User.count()
    return jsonify(stats)


@app_views.route('/unauthorized/', strict_slashes=False)
def unauthorized() -> None:
    """Return an Unauthorized error.

    Returns:
        None
    """
    abort(401)


@app_views.route('/forbidden/', strict_slashes=False)
def forbidden() -> None:
    """Return a Forbidden error.

    Returns:
        None
    """
    abort(403)
