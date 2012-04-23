#!/usr/bin/env python
#coding=utf-8
# 
# Copyright 2010 RenRen
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""A demo SAE application that uses RenRen for login.

This application is modified from the offical renren oauth sdk for python.

This application uses OAuth 2.0 directly rather than relying on renren's
JavaScript SDK for login. It also accesses the RenRen API directly
using the Python SDK. It is designed to illustrate how easy
it is to use the renren Platform without any third party code.

Befor runing the demo, you have to register a RenRen Application and modify the root domain.
e.g. If you specify the redirect_rui as "http://www.example.com/example_uri". The root domain must be "example.com"

@Author 414nch4n <chenfeng2@staff.sina.com.cn>

"""

# Replace these keys with your own one.
RENREN_APP_API_KEY = "06c0673d123240e7acd75e181cb5e40c"
RENREN_APP_SECRET_KEY = "a11b055a759241bd8bc6af9d99aacbd4"


RENREN_AUTHORIZATION_URI = "http://graph.renren.com/oauth/authorize"
RENREN_ACCESS_TOKEN_URI = "http://graph.renren.com/oauth/token"
RENREN_SESSION_KEY_URI = "http://graph.renren.com/renren_api/session_key"
RENREN_API_SERVER = "http://api.renren.com/restserver.do"



import base64
import Cookie
import email.utils
import hashlib
import hmac
import logging
import os.path
import time
import urllib

# Find a JSON parser
try:
    import json
    _parse_json = lambda s: json.loads(s)
except ImportError:
    try:
        import simplejson
        _parse_json = lambda s: simplejson.loads(s)
    except ImportError:
        from django.utils import simplejson
        _parse_json = lambda s: simplejson.loads(s)

import tornado.web
import tornado.wsgi
import tornado.database

from sae.const import (MYSQL_HOST, MYSQL_HOST_S,
    MYSQL_PORT, MYSQL_USER, MYSQL_PASS, MYSQL_DB
)

_db = tornado.database.Connection(
   ':'.join([MYSQL_HOST, MYSQL_PORT]), MYSQL_DB, MYSQL_USER, MYSQL_PASS,
   max_idle_time = 5
)

class User:
    def __init__(self, uid=None, name=None, avatar=None, access_token=None):
        self.uid = uid
        self.name = name
        self.avatar = avatar
        self.access_token = access_token

    @classmethod
    def get(cls, uid):
        user = cls()
        row = _db.get("""
            select * from users where uid = %s
        """, uid)
        user.uid = row.uid
        user.name = row.name
        user.avatar = row.avatar
        user.access_token = row.access_token
        return user

    def put(self):
        _db.execute("""
            insert into users(uid, name, avatar, access_token)
            values(%s, %s, %s, %s) on duplicate key update
            name = %s, avatar = %s, access_token = %s
        """, self.uid, self.name, self.avatar, self.access_token,
        self.name, self.avatar, self.access_token)

class BaseHandler(tornado.web.RequestHandler):
    @property
    def current_user(self):
        """Returns the logged in renren user, or None if unconnected."""
        if not hasattr(self, "_current_user"):
            self._current_user = None
            user_id = parse_cookie(self.get_secure_cookie("renren_user"))
            if user_id:
                logging.info("renren_user in cookie is: %s", user_id)
                self._current_user = User.get(user_id)
        return self._current_user

class HomeHandler(BaseHandler):
    def get(self):
        template_file = os.path.join(os.path.dirname(__file__), 
                                     'oauth.html')
        self.render(template_file, current_user=self.current_user)

class LoginHandler(BaseHandler):
    def get(self):
        verification_code = self.get_argument("code", None)
        # FIXME: use path_url from the request to construct the redirect_uri
        args = dict(client_id=RENREN_APP_API_KEY, redirect_uri='http://%s/auth/login' % self.request.host)
        
        error = self.get_argument("error", None)
        
        if error:
            args["error"] = error
            args["error_description"] = self.get_argument("error_description", '')
            args["error_uri"] = self.get_argument("error_uri", '')
            path = os.path.join(os.path.dirname(__file__), "error.html")
            args = dict(error=args)
            self.render(path, **args)
        elif verification_code:
            scope = self.get_argument("scope", "")
            scope_array = str(scope).split("[\\s,+]")
            logging.info("returning scope is :" + str(scope_array))
            response_state = self.get_argument("state", "")
            logging.info("returning state is :" + response_state)
            args["client_secret"] = RENREN_APP_SECRET_KEY
            args["code"] = verification_code
            args["grant_type"] = "authorization_code"
            logging.info(RENREN_ACCESS_TOKEN_URI + "?" + urllib.urlencode(args))
            response = urllib.urlopen(RENREN_ACCESS_TOKEN_URI + "?" + urllib.urlencode(args)).read()
            logging.info(response)
            access_token = _parse_json(response)["access_token"]
            logging.info("obtained access_token is: " + access_token)
            
            '''Obtain session key from the Resource Service.'''
            session_key_request_args = {"oauth_token": access_token}
            response = urllib.urlopen(RENREN_SESSION_KEY_URI + "?" + urllib.urlencode(session_key_request_args)).read()
            logging.info("session_key service response: " + str(response))
            session_key = str(_parse_json(response)["renren_token"]["session_key"])
            logging.info("obtained session_key is: " + session_key)
            
            '''Requesting the Renren API Server obtain the user's base info.'''
            params = {"method": "users.getInfo", "fields": "name,tinyurl"}
            api_client = RenRenAPIClient(session_key, RENREN_APP_API_KEY, RENREN_APP_SECRET_KEY)
            response = api_client.request(params);
            
            if type(response) is list:
                response = response[0]
            
            user_id = response["uid"]#str(access_token).split("-")[1]
            name = response["name"]
            avatar = response["tinyurl"]
            
            user = User(uid=user_id, name=name, avatar=avatar, access_token=access_token)
            user.put()
            
            set_cookie(self, "renren_user", str(user_id),
                       expires=time.time() + 30 * 86400)
            self.redirect("/")
        else:
            args["response_type"] = "code"
            args["scope"] = "publish_feed email status_update"
            args["state"] = "1 23 abc&?|."
            self.redirect(
                RENREN_AUTHORIZATION_URI + "?" +
                urllib.urlencode(args))


class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie('renren_user')
        self.redirect("/")

class RenRenAPIClient(object):
    def __init__(self, session_key = None, api_key = None, secret_key = None):
        self.session_key = session_key
        self.api_key = api_key
        self.secret_key = secret_key
    def request(self, params = None):
        """Fetches the given method's response returning from RenRen API.

        Send a POST request to the given method with the given params.
        """
        params["api_key"] = self.api_key
        params["call_id"] = str(int(time.time() * 1000))
        params["format"] = "json"
        params["session_key"] = self.session_key
        params["v"] = '1.0'
        sig = self.hash_params(params);
        params["sig"] = sig
        
        post_data = None if params is None else urllib.urlencode(params)
        
        #logging.info("request params are: " + str(post_data))
        
        file = urllib.urlopen(RENREN_API_SERVER, post_data)
        
        try:
            s = file.read()
            logging.info("api response is: " + s)
            response = _parse_json(s)
        finally:
            file.close()
        if type(response) is not list and response["error_code"]:
            logging.info(response["error_msg"])
            raise RenRenAPIError(response["error_code"], response["error_msg"])
        return response
    def hash_params(self, params = None):
        hasher = hashlib.md5("".join(["%s=%s" % (self.unicode_encode(x), self.unicode_encode(params[x])) for x in sorted(params.keys())]))
        hasher.update(self.secret_key)
        return hasher.hexdigest()
    def unicode_encode(self, str):
        """
        Detect if a string is unicode and encode as utf-8 if necessary
        """
        return isinstance(str, unicode) and str.encode('utf-8') or str
    
class RenRenAPIError(Exception):
    def __init__(self, code, message):
        Exception.__init__(self, message)
        self.code = code

def set_cookie(response, name, value, domain=None, path="/", expires=None):
    """Generates and signs a cookie for the give name/value"""
    # Now we just ignore domain, path and expires
    response.set_secure_cookie(name, value)
    logging.info("set cookie as " + name + ", value is: " + value)

def parse_cookie(value):
    """Parses and verifies a cookie value from set_cookie"""
    if not value: return None
    return value

settings = {
  "debug": True,
  "cookie_secret": "c19e4cc825adee8ab0928244186538aca2821425",
  "static_path": os.path.join(os.path.dirname(__file__))
}

app = tornado.wsgi.WSGIApplication([
    (r"/", HomeHandler),
    (r"/auth/login", LoginHandler),
    (r"/auth/logout", LogoutHandler),
], **settings)

if __name__ == '__main__':
    import wsgiref.simple_server
    httpd = wsgiref.simple_server.make_server('', 8080, app)
    httpd.serve_forever()
