#-*-coding: utf8 -*-

"""
SAE API auth handler for urllib2 and requests

urllib2:

>>> import urllib2
>>> apibus_handler = SaeApibusAuthHandler(ACCESSKEY, SECRETKEY)
>>> opener = urllib2.build_opener(apibus_handler)
>>> print opener.open('http://g.sae.sina.com.cn/log/http/2015-06-18/1-access.log').read()

requests:

>>> import requests
>>> print requests.get('http://g.sae.sina.com.cn/log/http/2015-06-18/1-access.log?head/0/10|fields/ /1/2/3/4', auth=SaeApibusAuth(ACCESSKEY, SECRETKEY)).content
"""

import hmac
import base64
import hashlib
import time
import urllib
from urllib2 import BaseHandler, Request

_APIBUS_URL_PREFIX = 'http://g.sae.sina.com.cn/'

class SaeApibusAuthHandler(BaseHandler):
    # apibus handler must be in front
    handler_order = 100

    def __init__(self, accesskey, secretkey):
        self.accesskey = accesskey
        self.secretkey = secretkey

    def http_request(self, req):
        orig_url = req.get_full_url()
        if not orig_url.startswith(_APIBUS_URL_PREFIX):
            return req

        timestamp = str(int(time.time()))
        headers = [
            ('x-sae-timestamp', timestamp),
            ('x-sae-accesskey', self.accesskey),
        ]
        req.headers.update(headers)

        method = req.get_method()
        resource = urllib.unquote(req.get_full_url()[len(_APIBUS_URL_PREFIX)-1:])
        sae_headers = [(k.lower(), v.lower()) for k, v in req.headers.items() if k.lower().startswith('x-sae-')]
        req.add_header('Authorization', _signature(self.secretkey, method, resource, sae_headers))
        return req

    https_request = http_request

try:
    from requests.auth import AuthBase

    class SaeApibusAuth(AuthBase):
        """Attaches HTTP Basic Authentication to the given Request object."""
        def __init__(self, accesskey, secretkey):
            self.accesskey = accesskey
            self.secretkey = secretkey

        def __call__(self, r):
            timestamp = str(int(time.time()))
            r.headers['x-sae-timestamp'] = timestamp
            r.headers['x-sae-accesskey'] = self.accesskey
            resource = urllib.unquote(r.url[len(_APIBUS_URL_PREFIX)-1:])
            #resource = r.url[len(_APIBUS_URL_PREFIX)-1:]
            sae_headers = [(k.lower(), v.lower()) for k, v in r.headers.items() if k.lower().startswith('x-sae-')]
            r.headers['Authorization'] = _signature(self.secretkey, r.method, resource, sae_headers)
            return r
except ImportError:
    # requests was not present!
    pass

def _signature(secret, method, resource, headers):
    msgToSign = "\n".join([
        method, resource,
        "\n".join([(k + ":" + v) for k, v in sorted(headers)]),
    ])
    return "SAEV1_HMAC_SHA256 " + base64.b64encode(hmac.new(secret, msgToSign, hashlib.sha256).digest())

