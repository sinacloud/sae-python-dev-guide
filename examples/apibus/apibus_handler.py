#-*-coding: utf8 -*-

"""
urllib2 handler for SAE APIBus Service

Usage:

import urllib2
from apibus_handler import APIBusHandler
opener = urllib2.build_opener(APIBusHandler(ACCESSKEY, SECRETKEY))

Then you can use *opener* to request sae internal service such as segement,
sms as you want.
"""

import hmac
import base64
import hashlib
import time
from urllib2 import BaseHandler, Request

_APIBUS_ENDPOINT = 'http://g.apibus.io'

class APIBusHandler(BaseHandler):
    # apibus handler must be in front
    handler_order = 100

    def __init__(self, accesskey, secretkey):
        self.accesskey = accesskey
        self.secretkey = secretkey

    def _signature(self, headers):
        msg = ''.join([k + v for k, v in headers])
        h = hmac.new(self.secretkey, msg, hashlib.sha256).digest()
        return base64.b64encode(h)

    def http_request(self, req):
        orig_url = req.get_full_url()
        timestamp = str(int(time.time()))
        headers = [
            ('Fetchurl', orig_url),
            ('Timestamp', timestamp),
            ('Accesskey', self.accesskey),
        ]
        headers.append(('Signature', self._signature(headers)))
        # Create a new request
        _req = Request(_APIBUS_ENDPOINT, req.get_data(), origin_req_host=orig_url)
        _req.headers.update(req.header_items())
        _req.headers.update(headers)
        _req.timeout = req.timeout
        return _req

    https_request = http_request

