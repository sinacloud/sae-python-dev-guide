"""Core functions of SAE

environ    A copy of the environ passed to your wsgi app, should not be used directly

"""

import os

import conf

class Application:
    """Information class for sae app"""

    def __init__(self):
        self.access_key = environ.get('HTTP_ACCESSKEY', '')
        self.secret_key = environ.get('HTTP_SECRETKEY', '')
        self.name = environ.get('HTTP_APPNAME', '')
        self.version = environ.get('HTTP_VERSION', '')
        self.hash = environ.get('HTTP_HASH', '')

        self.mysql_db = '_'.join(['app', self.name])
        self.mysql_user = self.access_key
        self.mysql_pass = self.secret_key
        self.mysql_host = conf.SAE_MYSQL_HOST_M
        self.mysql_host_s = conf.SAE_MYSQL_HOST_S
        self.mysql_port = conf.SAE_MYSQL_PORT

def get_access_key():
    """Return access_key of your app"""
    return environ.get('HTTP_ACCESSKEY', '')

def get_secret_key():
    """Return secret_key of your app"""
    return environ.get('HTTP_SECRETKEY', '')

def get_trusted_hosts():
    return [host for host in environ.get('TRUSTED_HOSTS', '').split() if host]

environ = {}
