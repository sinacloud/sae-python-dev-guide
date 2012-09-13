#!/usr/bin/env python
# -*-coding: utf8 -*-

""" SAE Storage API
"""

import json
import urllib
import urllib2
import random
import string
import errno
from sae.const import (
    ACCESS_KEY, SECRET_KEY, APP_NAME
)

# Check the settings
import os
_stor_path = os.environ.get('STORAGE_PATH', None)
if not _stor_path:
    raise RuntimeError("Please specify --storage-path in the command line")
if not os.path.isdir(_stor_path):
    raise RuntimeError("'%s' directory does not exists" % _stor_path)

class Error(Exception):
    """Base-class of errors in this module"""

class InternalError(Error):
    """Something unexpected happened, it should be temporary."""

class PermissionDeniedError(Error):
    """The requested operation is not allowed for this app"""

class DomainNotExistsError(Error):
    """The requested domain does not exists"""

class ObjectNotExistsError(Error):
    """The requested object does not exists"""

_ERROR_MAPPING = {-3: PermissionDeniedError, 
    -7: DomainNotExistsError, -18: ObjectNotExistsError
}

_STOR_BACKEND = 'http://stor.sae.sina.com.cn/storageApi.php'

_META_MAPPING = {
    'expires': 'expires',
    'content_type': 'type',
    'content_encoding': 'encoding',
}

class Object:
    def __init__(self, data, **kwargs):
        """
        Args:
          data: The content of the object.
          expires: Set the expires time of the object. The same format as
            apache's expires directive.
          content_encoding: Set a Content-Encoding header on the object.
          content_type: Set a Content-Type header on the object.
        """
        self.data = data
        self.meta = {}
        for k, v in kwargs.iteritems():
            if k in _META_MAPPING:
                self.meta[k] = v

class PostDataHandler(urllib2.BaseHandler):
    handler_order = urllib2.HTTPHandler.handler_order-10 

    def http_request(self, request):
        data = request.get_data()
        if data is not None and type(data) != str:
            objs = []
            vars = []
            try:
                 for key, value in data.items():
                     if isinstance(value, Object):
                         objs.append((key, value))
                     else:
                         vars.append((key, value))
            except TypeError:
                raise TypeError("sequence or mapping object required")

            if len(objs) == 0:
                data = urllib.urlencode(vars, 1)
            else:
                boundary, data = self.encode(vars, objs)
                content_type = 'multipart/form-data; boundary=%s' % boundary
                request.add_unredirected_header('Content-Type', content_type)
            request.add_data(data)
        return request

    def encode(self, vars, objs, boundary = None):
        if boundary is None:
            boundary = ''.join([
                random.choice(string.letters) for i in range(20)
            ])
        buffer = ''

        for key, value  in vars:
            buffer += '--%s\r\n' % boundary \
                + 'Content-Disposition: form-data; name="%s"\r\n' % key \
                + '\r\n' + value + '\r\n'

        for key, obj  in objs:
            buffer += '--%s\r\n' % boundary \
                + 'Content-Disposition: form-data; name="%s"; filename="x"\r\n' % key \
                + 'Content-Type: application/octet-stream\r\n' \
                + '\r\n' + obj.data + '\r\n'

        buffer += '--%s--\r\n\r\n' % boundary

        return boundary, buffer

    https_request = http_request

class Client:

    def __init__(self, accesskey=ACCESS_KEY, \
            secretkey=SECRET_KEY, prefix=APP_NAME):
        pass

    def put(self, domain, key_name, object):
        """Put an object in the specified domain.

        Args:
          domain: The domain to put the object.
          key_name: The name of the object.
          object: The object will be putted.
        Returns: The url of the object.
        """
        if not isinstance(object, Object):
            raise TypeError("Only Object is allowed")

        path = os.path.join(_stor_path, domain)
        self._ensure_dir_exists(path)

        fullpath = os.path.join(path, key_name)

        try:
            open(fullpath, 'wb').write(object.data)
        except OSError, e:
            raise InternalError()

        return self.url(domain, key_name)

    def get(self, domain, key_name):
        """Get an object from the specified domain.

        Args:
          domain: The domain from which the obect will be getted.
          key_name: The name of the object
        """
        fullpath = os.path.join(_stor_path, domain, key_name)

        try:
            data = open(fullpath, 'rb').read()
        except IOError, e:
            if e.errno == errno.ENOENT:
                raise ObjectNotExistsError()
            else:
                raise InternalError()
            
        return Object(data)

    def stat(self, domain, key_name):
        """Get an object's attributes

        Args:
          domain: The domain from which the obect will be getted.
          key_name: The name of the object
        """
        fullpath = os.path.join(_stor_path, domain, key_name)

        try:
            st = os.stat(fullpath)
        except OSError, e:
            if e.errno == errno.ENOENT:
                raise ObjectNotExistsError()
            else:
                raise InternalError()

        d = {'name': key_name, 'length': st[6], 'datetime': st[8]}
                
        return d

    def delete(self, domain, key_name):
        """Delete an object from the specified domain.

        Args:
          domain: The domain where the object is in.
          key_name: The name of the object.
        """
        fullpath = os.path.join(_stor_path, domain, key_name)

        try:
            os.unlink(fullpath)
        except OSError, e:
            if e.errno == errno.ENOENT:
                raise ObjectNotExistsError()
            else:
                raise InternalError()

    def list(self, domain):
        """List the objects in a domain.

        Args:
          domain: Which domain to list.
        Returns: A list of all the  objects' attributes.
        """
        path = os.path.join(_stor_path, domain)
        self._ensure_dir_exists(path)

        data = []
        for f in os.listdir(path):
            filepath = os.path.join(path, f)

            try:
                st = os.stat(filepath)
            except OSError:
                raise InternalError()

            data.append({
                'name': f,
                'length': st[6],
                'datetime': st[8],
            })

        return data

    def create_domain(self, domain, **attrs):
        """Create a domain.

        Args:
          domain: The name of the domain.
        """
        raise NotImplementedError()

    def delete_domain(self, domain):
        """Delete a domain.

        Args:
          domain: The name of the domain.
        """
        raise NotImplementedError()

    def list_domain(self):
        """List all the domains.

        Returns: A list of all the domains.
        """
        domains = []
        for f in os.listdir(_stor_path):
            fullpath = os.path.join(_stor_path, f)
            if os.path.isdir(fullpath):
                domains.append(unicode(f))
        return domains

    def url(self, domain, key_name):
        """Get an object's public url.
        """
        return 'http://%s/stor-stub/%s/%s' % \
            (os.environ['HTTP_HOST'], domain, urllib.quote(key_name))

    def _ensure_dir_exists(self, path):
        try:
            os.mkdir(path)
        except OSError, e:
            if e.errno == errno.EPERM:
                raise PermissionDeniedError()
            elif e.errno != errno.EEXIST:
                raise InternalError()
            

