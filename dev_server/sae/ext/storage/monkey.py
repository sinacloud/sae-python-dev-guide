
# Copyright (C) 2012-2013 SINA, All rights reserved.

import os.path
import sys
import re
import time
import errno

from sae.storage import Connection, Error

_S_FILEPATH_REGEX = re.compile('^(?:/s|/s/.*)$')
_S_FILENAME_REGEX = re.compile('^(?:/s|/s/([^/]*)/?(.*))$')

def _parse_name(filename):
    m = _S_FILENAME_REGEX.match(os.path.normpath(filename))
    if m:
        return m.groups()
    else:
        raise ValueError('invalid filename')

STORAGE_PATH = os.environ.get('sae.storage.path')

_is_storage_path = lambda n: _S_FILEPATH_REGEX.match(n)
def _get_storage_path(path):
    if not STORAGE_PATH:
        raise RuntimeError(
            "Please specify --storage-path in the command line")
    return STORAGE_PATH + n[2:]

class _File(file):

    def isatty(self):
        return False

    # Unimplemented interfaces below here.

    def flush(self):
        pass

    def fileno(self):
        raise NotImplementedError()

    def next(self):
        raise NotImplementedError()

    def readinto(self):
        raise NotImplementedError()

    def readline(self):
        raise NotImplementedError()

    def readlines(self):
        raise NotImplementedError()

    def truncate(self):
        raise NotImplementedError()

    def writelines(self):
        raise NotImplementedError()

    def xreadlines(self):
        raise NotImplementedError()

import __builtin__

_real_open = __builtin__.open
def open(filename, mode='r', buffering=-1):
    if _is_storage_path(filename):
        filename = _get_storage_path(filename)
    return _real_open(filename, mode, buffering)

import os

_real_os_listdir = os.listdir
def os_listdir(path):
    if _is_storage_path(path):
        path = _get_storage_path(path)
    return _real_os_listdir(path)

_real_os_mkdir = os.mkdir
def os_mkdir(path, mode=0777):
    if _is_storage_path(path):
        path = _get_storage_path(path)
    return _real_os_mkdir(path, mode)

_real_os_open = os.open
def os_open(filename, flag, mode=0777):
    if _is_storage_path(filename):
        filename = _get_storage_path(filename)
    return  _real_os_open(filename, flag, mode)

_real_os_fdopen = getattr(os, 'fdopen', None)
def os_fdopen(fd, mode='r', bufsize=-1):
    return _real_os_fdopen(fd, mode, bufsize)

_real_os_close = os.close
def os_close(fd):
    return _real_os_close(fd)

_real_os_chmod = os.chmod
def os_chmod(path, mode):
    if _is_storage_path(path):
        pass
    else:
        return _real_os_chmod(path, mode)

_real_os_stat = os.stat
def os_stat(path):
    if _is_storage_path(path):
        path = _get_storage_path(path)
    return _real_os_stat(path)

_real_os_unlink = os.unlink
def os_unlink(path):
    if _is_storage_path(path):
        path = _get_storage_path(path)
    return _real_os_unlink(path)

import os.path

_real_os_path_exists = os.path.exists
def os_path_exists(path):
    if _is_storage_path(path):
        path = _get_storage_path(path)
    return _real_os_path_exists(path)

_real_os_path_isdir = os.path.isdir
def os_path_isdir(path):
    if _is_storage_path(path):
        path = _get_storage_path(path)
    return _real_os_path_isdir(path)

_real_os_rmdir = os.rmdir
def os_rmdir(path):
    if _is_storage_path(path):
        path = _get_storage_path(path)
    return _real_os_rmdir(path)

def patch_all():
    __builtin__.open = open
    os.listdir = os_listdir
    os.mkdir = os_mkdir
    os.path.exists = os_path_exists
    os.path.isdir = os_path_isdir
    os.open = os_open
    os.fdopen = os_fdopen
    os.close = os_close
    os.chmod = os_chmod
    os.stat = os_stat
    os.unlink = os_unlink
    os.rmdir = os_rmdir
