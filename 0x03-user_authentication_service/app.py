#!/usr/bin/env python3
"""Basic Flask app"""
from auth import Auth
from flask import Flask, jsonify, request, abort, redirect, url_for

AUTH = Auth()
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def index() -> str:
    """Index page of the web application."""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def register_user():
    """POST /users"""
    email = request.form.get('email')
    pwd = request.form.get('password')
    try:
        user = AUTH.register_user(email, pwd)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    return jsonify({"email": f"{user.email}", "message": "user created"})


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login_user():
    """POST /sessions"""
    email = request.form.get('email')
    pwd = request.form.get('password')
    if not AUTH.valid_login(email, pwd):
        abort(401)
    sess_id = AUTH.create_session(email)
    resp = jsonify({"email": f"{email}",
                    "message": "logged in"})
    resp.set_cookie('session_id', sess_id)
    return resp


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout_user():
    """DELETE /sessions"""
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect(url_for('index'))


@app.route('/profile', strict_slashes=False)
def display_profile():
    """GET /profile"""
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    return jsonify({"email": f"{user.email}"})


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """POST /reset_password"""
    email = request.form.get('email')
    try:
        reset_pwd_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)
    return jsonify({"email": f"{email}", "reset_token": f"{reset_pwd_token}"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
