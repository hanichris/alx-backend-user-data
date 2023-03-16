#!/usr/bin/env python3
"""Perform an end-to-end integration test of user authentication."""
import requests


URL = "http://localhost:5000"
EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email: str, password: str) -> None:
    """Test the `/users endpoint` of the application.

    Args:
        email (str): user's email.
        password (str): user's password.
    """
    payload = {'email': email, 'password': password}
    resp = requests.post(f"{URL}/users", data=payload)
    if resp.status_code == 200:
        assert resp.json() == {"email": f"{email}", "message": "user created"}
    else:
        assert resp.status_code == 400
        assert resp.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    """Test login functionality having provided the wrong credentials.

    Args:
        email (str): user's email address.
        password (str): user's password.
    """
    payload = {'email': email, 'password': password}
    resp = requests.post(f'{URL}/sessions', data=payload)
    assert resp.status_code == 401


def log_in(email: str, password: str) -> str:
    pass


def profile_unlogged() -> None:
    pass


def profile_logged(session_id: str) -> None:
    pass


def log_out(session_id: str) -> None:
    pass


def reset_password_token(email: str) -> str:
    pass


def update_password(email: str, reset_token: str, new_password: str) -> None:
    pass


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    # log_in_wrong_password(EMAIL, NEW_PASSWD)
    # profile_unlogged()
    # session_id = log_in(EMAIL, PASSWD)
    # profile_logged(session_id)
    # log_out(session_id)
    # reset_token = reset_password_token(EMAIL)
    # update_password(EMAIL, reset_token, NEW_PASSWD)
    # log_in(EMAIL, NEW_PASSWD)
