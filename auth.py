from functools import wraps
import base64
from config_loader import config
from flask import Response, request


def check(authorization_header):
    try:
        encoded_uname_pass = authorization_header.split()[-1]
        decoded_uname_pass = base64.b64decode(encoded_uname_pass).decode()
        print("decodee:",decoded_uname_pass)
    except Exception:
        return False

    if decoded_uname_pass == config.APP_CREDENTIALS:
        return True
    else:
        return False


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        authorization_header = request.headers.get('Authorization')
        print("HEADEER?",authorization_header)
        if authorization_header and check(authorization_header):
            return f(*args, **kwargs)
        else:
            resp = Response()
            resp.headers['WWW-Authenticate'] = 'Basic'
            return resp, 401

    return decorated
