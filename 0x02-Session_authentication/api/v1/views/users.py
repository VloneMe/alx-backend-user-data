#!/usr/bin/env python3
"""Module for User views."""

from flask import abort, jsonify, request
from api.v1.views import app_views
from models.user import User

@app_views.route('/users', methods=['GET'], strict_slashes=False)
def view_all_users() -> str:
    """GET /api/v1/users - Retrieve a list of all User objects."""
    all_users = [user.to_json() for user in User.all()]
    return jsonify(all_users)

@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def view_one_user(user_id: str = None) -> str:
    """GET /api/v1/users/:id - Retrieve a specific User object by ID.

    Args:
        user_id (str): The ID of the user to retrieve.

    Returns:
        str: JSON representation of the User object.
    """
    if user_id is None:
        abort(404)
    if user_id == 'me':
        if request.current_user is None:
            abort(404)
        else:
            return jsonify(request.current_user.to_json())
    user = User.get(user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_json())

@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id: str = None) -> str:
    """DELETE /api/v1/users/:id - Delete a specific User object by ID.

    Args:
        user_id (str): The ID of the user to delete.

    Returns:
        str: Empty JSON response.
    """
    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)
    user.remove()
    return jsonify({}), 200

@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user() -> str:
    """POST /api/v1/users - Create a new User object.

    JSON Body:
        - email: Email address of the user.
        - password: Password of the user.
        - first_name (optional): First name of the user.
        - last_name (optional): Last name of the user.

    Returns:
        str: JSON representation of the newly created User object.
    """
    rj = request.get_json()
    if rj is None or not rj.get("email") or not rj.get("password"):
        return jsonify({'error': 'Invalid JSON'}), 400
    try:
        user = User(**rj)
        user.save()
        return jsonify(user.to_json()), 201
    except Exception as e:
        return jsonify({'error': f"Can't create User: {e}"}), 400

@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id: str = None) -> str:
    """PUT /api/v1/users/:id - Update an existing User object.

    Args:
        user_id (str): The ID of the user to update.

    JSON Body:
        - first_name (optional): Updated first name of the user.
        - last_name (optional): Updated last name of the user.

    Returns:
        str: JSON representation of the updated User object.
    """
    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)
    rj = request.get_json()
    if not rj:
        return jsonify({'error': 'Invalid JSON'}), 400
    user.update(**rj)
    user.save()
    return jsonify(user.to_json()), 200
