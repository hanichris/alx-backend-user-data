#!/usr/bin/env python3
"""Basic Flask app"""
from auth import Auth
from flask import Flask, jsonify, request

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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
