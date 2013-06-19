
# Copyright (C) 2012-2013 SINA, All rights reserved.

from _mysql_exceptions import *

"""An proxy for the MySQL C API
Translate the _mysql C API call into restfull call
"""

import types
import pickle
import urllib2

from release import __version__, version_info

import logging
logger = logging.getLogger('sae._mysql')

NULL = 'NULL'
_SAE_MYSQL_API_BACKEND = 'http://2.python.sinaapp.com/api/mysql/'

# refs:
# http://www.python.org/dev/peps/pep-0249
# http://mysql-python.sourceforge.net/MySQLdb.html#mysql

class connection(object):
    def __init__(self, *args, **kwargs):
        self.converter = kwargs.pop('conv', {})
        self._conn_args = args
        self._conn_kwargs = kwargs
        self._conn_id = None
        self._rows = None
        self._description = None
        self._description_flags = None
        self._rowcount = None
        self._warnings = None
        self._info = None
        self._lastrowid = None
        self._open_connection()

    def open(self):
        pass

    def close(self):
        self._conn_id = None

    def shutdown(self):
        pass

    def select_db(self, *args):
        self._request('select_db', args)

    def change_user(self):
        pass

    def character_set_name(self):
        if not hasattr(self, '_charset'):
            self._charset = self._request('character_set_name')
        return self._charset

    def set_character_set(self, charset):
        if getattr(self, '_charset', None) != charset:
            self._request('set_character_set', charset)
        self._charset = charset

    def set_server_option(self, *args, **kws):
        logging.warning('Ignored set_server_option: %s, %s', args, kws)

    def query(self, query):
        retval = self._request('query', query=query)
        self._rows = retval['rows']
        self._description = retval['description']
        self._description_flags = retval['description_flags']
        self._rowcount = retval['rowcount']
        self._warnings = retval['warnings']
        self._info = retval['info']
        self._lastrowid = retval['lastrowid']

    def commit(self):
        pass

    def rollback(self):
        pass

    def autocommit(self, value):
        pass

    def use_result(self):
        return self.store_result()

    def store_result(self):
        if self._rows:
            return StoreResult(self, self._rows, self.converter,
                               self._description, self._description_flags)
        else:
            return None

    def next_result(self, *args, **kws):
        # TODO
        return -1

    def affected_rows(self):
        return self._rowcount

    def insert_id(self):
        return self._lastrowid

    def info(self):
        return self._info

    def get_host_info(self):
        return self._host_info

    def get_proto_info(self):
        return self._proto_info

    def get_server_info(self):
        return self._server_info

    def ping(self):
        pass

    def escape(self, item, dct=None):
        return escape(item, dct or self.converter)
        
    def escape_string(self, str):
        return escape_string(str)

    def string_literal(self, obj):
        return '\'%s\'' % escape_string(str(obj)) 

    def _open_connection(self):
        retval = self._request('open', *self._conn_args, **self._conn_kwargs)
        self._conn_id = retval['connection_id']
        self._host_info = retval['host_info']
        self._proto_info = retval['proto_info']
        self._server_info = retval['server_info']
        self.server_capabilities = retval['server_capabilities']

    def _request(self, op, *args, **kwargs):
        req = {
            'connection_id': self._conn_id,
            'op': op, 'args': args, 'kwargs': kwargs
        }
        logger.debug('REQ: %s', req)
        payload = pickle.dumps(req)
        body = urllib2.urlopen(_SAE_MYSQL_API_BACKEND, payload).read()
        rep = pickle.loads(body)
        logger.debug('REP: %s', rep)
        if rep.get('sql_exception'):
            raise rep.get('sql_exception')
        return rep.get('result')

def _mysql_rows_to_python(rows, conv, field_info, how):
    def row_to_python0(row):
        nrow = []
        for i, v in enumerate(row):
            # XXX: NULL is always converted to None, so here we
            # do not need to do it again.
            nrow.append(None if v is None else conv[i](v))
        return tuple(nrow)
    def row_to_python1(row):
        nrow = {}
        for i, v in enumerate(row):
            # XXX: NULL is always converted to None, so here we
            # do not need to do it again.
            nrow[field_info[i][0]] = None if v is None else conv[i](v)
        return nrow
    if how:
        return tuple(row_to_python1(r) for r in rows)
    else:
        return tuple(row_to_python0(r) for r in rows)

class StoreResult:
    def __init__(self, conn, rows, conv, description, description_flags):
        self.conn = conn
        self.current = 0
        self.description = description
        self.description_flags = description_flags
        self._cached = rows
        self._init_conv(conv)

    def _init_conv(self, conv):
        # _mysql.c:_mysql_ResultObject_Initialize
        self.converter = []
        for n, i in enumerate(self.description):
            c = conv.get(i[1], str)     # search by field.type
            if isinstance(c, list):
                nc = None
                mask = self.description_flags[n]
                for j in c:
                    if isinstance(j[0], int):
                        if mask & j[0]: # search by field.flags
                            nc = j[1]
                            break
                    else:
                        nc = j[1]
                        break           # wildcard
                c = nc if nc is not None else str
            self.converter.append(c)

    def fetch_row(self, maxrows=1, how=0):
        if maxrows == 0:
            retval = self._cached
            self._cached = ()
        else:
            retval = self._cached[self.current:maxrows]
            self.current += maxrows
        return _mysql_rows_to_python(retval, self.converter, self.description, how)

    def describe(self):
        return self.description

    def field_flags(self):
        return self.description_flags

connect = connection

def get_client_info():
    return '5.1.67'


def escape(item, dct):
    return _escape_item(item, dct)
    
def _escape_item(val, dct):
    d = dct.get(type(val)) or dct.get(types.StringType)
    return d(val, dct)

# Copied from pymysql
# See: https://github.com/petehunt/PyMySQL/blob/master/pymysql/converters.py
import re
ESCAPE_REGEX = re.compile(r"[\0\n\r\032\'\"\\]", re.IGNORECASE)
def escape_string(value):
    def rep(m):
        n = m.group(0)
        if n == "\0":
            return "\\0"
        elif n == "\n":
            return "\\n"
        elif n == "\r":
            return "\\r"
        elif n == "\032":
            return "\\Z"
        else:
            return "\\"+n
    s = re.sub(ESCAPE_REGEX, rep, value)
    return s

def string_literal(obj):
    return '\'%s\'' % escape_string(str(obj)) 

def escape_dict(val, dct):
    n = {}
    for k, v in val.items():
        quoted = _escape_item(v)
        n[k] = quoted
    return n

def escape_sequence(val, dct):
    return tuple(_escape_item(v, dct) for v in val)
