"""Core functions of SAE

environ    A copy of the environ passed to your wsgi app, should not be used directly

"""

def get_access_key():
    """Return access_key of your app"""
    return environ.get('HTTP_ACCESSKEY', '')

def get_secret_key():
    """Return secret_key of your app"""
    return environ.get('HTTP_SECRETKEY', '')

def get_trusted_hosts():
    return [host for host in environ.get('TRUSTED_HOSTS', '').split() if host]

environ = {}
