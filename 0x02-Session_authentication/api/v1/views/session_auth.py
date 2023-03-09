#!/usr/bin/env python3
"""Module that handles all routes for Session authentication."""
import os
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User


@app_views.route('/auth_session/login',
                 methods=['POST'], strict_slashes=False)
def login():
    """ POST /auth_session/login/
    JSON body:
        - email
        - password
    Return:
        - Response object.
        - 404 if user isn't found.
    """
    err_msg = None
    email = request.form.get("email", "")
    pwd = request.form.get("password", "")
    if err_msg is None and email == "":
        err_msg = "email missing"
    if err_msg is None and pwd == "":
        err_msg = "password missing"
    if err_msg is None:
        users = User.search({'email': email})
        if users == []:
            return jsonify({'error': 'no user found for this email'}), 404
        for user in users:
            if user.is_valid_password(pwd):
                from api.v1.app import auth
                sess_id = auth.create_session(user.id)
                resp = jsonify(user.to_json())
                sess_name = os.getenv('SESSION_NAME')
                resp.set_cookie(sess_name, sess_id)
                return resp
        return jsonify({'error': 'wrong password'}), 401
    return jsonify({'error': err_msg}), 400


@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def logout():
    """DELETE /api/v1/auth_session/logout."""
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
