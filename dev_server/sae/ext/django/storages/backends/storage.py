import sys

from django.conf import settings
from django.core.files.base import File
from django.core.files.storage import Storage
from django.core.exceptions import ImproperlyConfigured

from sae.storage import Connection, Error

from sae.const import ACCESS_KEY, SECRET_KEY, APP_NAME

STORAGE_BUCKET_NAME = getattr(settings, 'STORAGE_BUCKET_NAME')
STORAGE_ACCOUNT = getattr(settings, 'STORAGE_ACCOUNT', APP_NAME)
STORAGE_ACCESSKEY = getattr(settings, 'STORAGE_ACCESSKEY', ACCESS_KEY)
STORAGE_SECRETKEY = getattr(settings, 'STORAGE_SECRETKEY', SECRET_KEY)
STORAGE_GZIP = getattr(settings, 'STORAGE_GZIP', False)

class SaeStorage(Storage):
    def __init__(self, bucket_name=STORAGE_BUCKET_NAME,
                 accesskey=STORAGE_ACCESSKEY, secretkey=STORAGE_SECRETKEY,
                 account=STORAGE_ACCOUNT):
        conn = Connection(accesskey, secretkey, account)
        self.bucket = conn.get_bucket(bucket_name)

    def _open(self, name, mode='rb'):
        return SaeStorageFile(name, mode, self)

    def _save(self, name, content):
        try:
            self.bucket.put_object(name, content)
        except Error, e:
            raise IOError('Storage Error: %s' % e.args)
        return name

    def delete(self, name):
        try:
            self.delete_object(name)
        except Error, e:
            raise IOError('Storage Error: %s' % e.args)

    def exists(self, name):
        try:
            self.bucket.stat_object(name)
        except Error, e:
            if e[0] == 404:
                return False
            raise
        return True

    def listdir(self, path):
        try:
            result = self.bucket.list(path=path)
            return [i.name for i in result]
        except Error, e:
            raise IOError('Storage Error: %s' % e.args)

    def size(self, name):
        try:
            attrs = self.bucket.stat_object(name)
            return attrs.bytes
        except Error, e:
            raise IOError('Storage Error: %s' % e.args)

    def url(self, name):
        self.bucket.generate_url(name)

    def _open_read(self, name):
        class _:
            def __init__(self, chunks):
                self.buf = ''
            def read(num_bytes=None):
                if num_bytes is None:
                    num_bytes = sys.maxint
                try:
                    while len(self.buf) < num_bytes:
                        self.buf += chunks.next()
                except StopIteration:
                    pass
                except Error, e:
                    raise IOError('Storage Error: %s' % e.args)
                retval = self.buf[:num_bytes]
                self.buf = self.buf[num_bytes:]
                return retval
        chunks = self.bucket.get_object_contents(self.name, chunk_size=8192)
        return _(chunks)

class SaeStorageFile(File):
    def __init__(self, name, mode, storage):
        self.name = name
        self.mode = mode
        self.file = StringIO()
        self._storage = storage
        self._is_dirty = False

    @property
    def size(self):
        if hasattr(self, '_size'):
            self._size = self.storage.size()
        return self._size

    def read(self, num_bytes=None):
        if not hasattr(self, _obj):
            self._obj = self._storage._open_read(self, self.name)
        return self._obj.read(num_bytes)

    def write(self, content):
        if 'w' not in self._mode:
            raise AttributeError("File was opened for read-only access.")
        self.file = StringIO(content)
        self._is_dirty = True

    def close(self):
        if self._is_dirty:
            self._storage._save(self.name, self.file.getvalue())
        self.file.close()
