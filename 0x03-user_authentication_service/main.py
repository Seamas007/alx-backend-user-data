#!/usr/bin/env python3
""" Principal function """
import requests

URL = "http://localhost:5000"
EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email: str, password: str) -> None:
    """ Register User

        args:
            email: to look
            password: to look

        return
            assert of the values
    """
    reg_user = {
        "email": email,
        "password": password,
    }
    req = requests.post(f'{URL}/users', data=reg_user)

    response = {"email": EMAIL, "message": "user created"}
    assert req.status_code == 200
    assert req.json() == response


def log_in_wrong_password(email: str, password: str) -> None:
    """ Login with error

        args:
            email: to look
            password: to look

        return
            assert of the values
    """
    reg_user = {
        "email": email,
        "password": password,
    }
    req = requests.post(f'{URL}/sessions', data=reg_user)

    assert req.status_code == 401


def profile_unlogged() -> None:
    """ Login with error

        args:
            email: to look
            password: to look

        return
            assert of the values
    """
    req = requests.delete(f'{URL}/sessions')

    assert req.status_code == 403


def log_in(email: str, password: str) -> str:
    """ Login correctly

        args:
            email: to look
            password: to look

        return
            assert of the values
    """
    reg_user = {
        "email": email,
        "password": password,
    }
    req = requests.post(f'{URL}/sessions', data=reg_user)

    response = {
        "email": email,
        "message": "logged in"
    }
    assert req.status_code == 200
    assert req.json() == response

    return (req.cookies['session_id'])


def profile_logged(session_id: str) -> None:
    """ Profile logged

        args:
            session_id: Session identificator

        return
            assert of the values
    """
    cookie = {
        "session_id": session_id
    }
    req = requests.get(f'{URL}/profile', cookies=cookie)

    response = {
        "email": EMAIL,
    }

    assert req.status_code == 200
    assert req.json() == response


def log_out(session_id: str) -> None:
    """ Logout profile

        args:
            session_id: Session identificator

        return
            assert of the values
    """
    cookie = {
        "session_id": session_id
    }
    req = requests.delete(f'{URL}/sessions', cookies=cookie)

    assert req.status_code == 200


def reset_password_token(email: str) -> str:
    """ Reset password token

        args:
            email: Email to identify user

        return
            assert of the values
    """
    reg_user = {
        "email": email
    }
    req = requests.post(f'{URL}/reset_password', data=reg_user)

    token = req.json().get('reset_token', None)
    response = {"email": email, "reset_token": token}

    assert req.status_code == 200
    assert req.json() == response

    return token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """ Reset password token

        args:
            email: Email to identify user
            reset_token: Identifier to reset the password
            new_password: To change

        return
            assert of the values
    """
    reg_user = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password,
    }
    req = requests.put(f'{URL}/reset_password', data=reg_user)

    response = {"email": email, "message": "Password updated"}

    assert req.status_code == 200
    assert req.json() == response


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
