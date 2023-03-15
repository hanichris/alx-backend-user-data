#!/usr/bin/env python3
"""Basic Flask app"""
from flask import Flask, jsonify


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def index() -> str:
    """Index page of the web application."""
    return jsonify({"message": "Bienvenue"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
