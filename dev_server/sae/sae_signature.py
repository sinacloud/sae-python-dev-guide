
import os
import base64
import hmac
import hashlib

def get_signature(key, msg):
    h = hmac.new(key, msg, hashlib.sha256)
    return base64.b64encode(h.digest())

def get_signatured_headers(headers):
    """Given a list of headers, return a signatured dict
    Becareful of the order of headers when signaturing
    """
    d = {}
    msg = ''
    for k, v in headers:
        d[k] = v
        msg += k + v

    secret = os.environ.get('SECRET_KEY', '')
    d['Signature'] = get_signature(secret, msg)
    return d
