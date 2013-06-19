#!/usr/bin/env python
# -*-coding: utf8 -*-

""" Dummy SAE Storage API
"""

import os
import errno
import mimetypes
from datetime import datetime
from urllib import quote as _quote

DEFAULT_API_URL = 'https://api.sinas3.com'
ACCESS_KEY = SECRET_KEY = APP_NAME = 'x'
DEFAULT_API_VERSION = 'v1'
DEFAULT_RESELLER_PREFIX = 'SAE_'

class Error(Exception): pass

class AttrDict(dict):
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

def q(value, safe='/'):
    value = encode_utf8(value)
    if isinstance(value, str):
        return _quote(value, safe)
    else:
        return value

def encode_utf8(value):
    if isinstance(value, unicode):
        value = value.encode('utf8')
    return value

class Bucket:
    def __init__(self, bucket, conn=None):
        self.conn = conn if conn else Connection()
        self.bucket = bucket

    _s = """
def %s(self, *args, **kws):
    return self.conn.%s_bucket(self.bucket, *args, **kws)
"""
    for _m in ('put', 'post', 'stat', 'delete', 'list'):
        exec _s % (_m, _m)

    _s = """
def %s(self, *args, **kws):
    return self.conn.%s(self.bucket, *args, **kws)
"""
    for _m in ('get_object', 'get_object_contents', 'put_object',
               'post_object', 'stat_object', 'delete_object',
               'generate_url'):
        exec _s % (_m, _m)

    del _m, _s

class Connection(object):
    def __init__(self, accesskey=ACCESS_KEY, secretkey=SECRET_KEY,
                 account=APP_NAME, retries=3, backoff=0.5,
                 api_url=DEFAULT_API_URL,
                 api_version = DEFAULT_API_VERSION,
                 reseller_prefix=DEFAULT_RESELLER_PREFIX,
                 bucket_class=Bucket):
        if accesskey is None or secretkey is None or account is None:
            raise TypeError(
                '`accesskey` or `secretkey` or `account` is missing')
        self.bucket_class = bucket_class

    def list_bucket(self, bucket, prefix=None, delimiter=None,
                    path=None, limit=10000, marker=None):
        if path:
            prefix = path
            delimiter = '/'
        objs = []
        pth = os.path.normpath(self._get_storage_path(bucket))
        for dpath, dnames, fnames in os.walk(pth):
            rpath = dpath[len(pth)+1:]
            objs.extend([os.path.join(rpath, f) for f in fnames])
        last_subdir = None
        startpos = len(prefix) if delimiter and prefix else 0
        for obj in objs:
            if prefix:
                if not obj.startswith(prefix):
                    continue
            if delimiter:
                endpos = obj.find(delimiter, startpos)
                if endpos != -1:
                    subdir = obj[:endpos+1]
                    if subdir != last_subdir:
                        item = AttrDict()
                        item['bytes'] = None
                        item['content_type'] = None
                        item['hash'] = None
                        item['last_modified'] = None
                        item['name'] = subdir
                        yield item
                        last_subdir = subdir
                    continue
            item = AttrDict()
            item['bytes'] = '12'
            item['content_type'] = 'application/octet-stream'
            item['hash'] = 'x' * 40
            item['last_modified'] = '2013-05-23T03:01:59.051030'
            item['name'] = obj
            yield item

    def stat_bucket(self, bucket):
        attrs = AttrDict()
        attrs['acl'] = '.r:*'
        attrs['bytes'] = '10240'
        attrs['objects'] = '10240'
        attrs['metadata'] = {}
        return attrs

    def get_bucket(self, bucket):
        return self.bucket_class(bucket)

    def put_bucket(self, bucket, acl=None, metadata=None):
        path = self._get_storage_path(bucket)
        try:
            os.mkdir(path)
        except OSError, e:
            if e.errno != errno.EEXIST:
                raise Error(500, str(e))

    def post_bucket(self, bucket, acl=None, metadata=None):
        pass

    def delete_bucket(self, bucket):
        path = self._get_storage_path(bucket)
        try:
            os.rmdir(path)
        except OSError, e:
            if e.errno == errno.ENOENT:
                raise Error(404, 'Not Found')
            elif e.errno == errno.ENOTEMPTY:
                raise Error(409, 'Confict')
            else:
                raise Error(500, str(e))

    def get_object(self, bucket, obj, chunk_size=None):
        return self.stat_object(bucket, obj), \
                self.get_object_contents(bucket, obj, chunk_size)

    def get_object_contents(self, bucket, obj, chunk_size=None):
        fname = self._get_storage_path(bucket, obj)
        try:
            resp = open(fname, 'rb')
        except IOError, e:
            if e.errno == errno.ENOENT:
                raise Error(404, 'Not Found')
            else:
                raise Error(500, str(e))
        if chunk_size:
            def _body():
                buf = resp.read(chunk_size)
                while buf:
                    yield buf
                    buf = resp.read(chunk_size)
            return _body()
        else:
            return resp.read()

    def stat_object(self, bucket, obj):
        fname = self._get_storage_path(bucket, obj)
        try:
            st = os.stat(fname)
        except OSError, e:
            if e.errno == errno.ENOENT:
                raise Error(404, 'Not Found')
            else:
                raise Error(500, str(e))
        attrs = AttrDict()
        attrs['bytes'] = str(st.st_size)
        attrs['hash'] = 'x'*40
        attrs['last_modified'] = datetime.utcfromtimestamp(
                float(st.st_mtime)).isoformat()
        attrs['content_type'] = mimetypes.guess_type(obj)[0] or \
                                'application/octet-stream'
        attrs['content_encoding'] = None
        attrs['timestamp'] = str(st.st_mtime)
        attrs['metadata'] = {}
        return attrs

    def put_object(self, bucket, obj, contents,
                   content_type=None, content_encoding=None,
                   metadata=None):
        fname = self._get_storage_path(bucket, obj)
        if hasattr(contents, 'read'):
            contents = contents.read()
        try:
            os.makedirs(os.path.dirname(fname))
        except OSError, e:
            if e.errno != errno.EEXIST:
                raise Error(500, str(e))
        try:
            open(fname, 'wb').write(contents)
        except IOError, e:
            raise Error(500, str(e))

    def post_object(self, bucket, obj,
                    content_type=None, content_encoding=None,
                    metadata=None):
        pass

    def generate_url(self, bucket, obj):
        return 'http://%s/stor-stub/%s/%s' % \
            (os.environ['HTTP_HOST'], bucket, q(obj))

    def delete_object(self, bucket, obj):
        fname = self._get_storage_path(bucket, obj)
        try:
            os.unlink(fname)
        except OSError, e:
            if e.errno == errno.ENOENT:
                raise Error(404, 'Not Found')
        bname = self._get_storage_path(bucket)
        fname = os.path.dirname(fname)
        while fname and len(fname) > len(bname):
            try:
                os.rmdir(fname)
            except OSError, e:
                if e.errno == errno.ENOTEMPTY:
                    break
                else:
                    raise Error(500, str(e))
            fname = os.path.dirname(fname)

    _STORAGE_PATH = os.environ.get('sae.storage.path')
    def _get_storage_path(self, *args):
        if not self._STORAGE_PATH:
            raise RuntimeError(
                "Please specify --storage-path in the command line")
        if not os.path.isdir(self._STORAGE_PATH):
            raise RuntimeError(
                "'%s' directory does not exists" % self._STORAGE_PATH)
        return os.path.join(self._STORAGE_PATH, *args)
