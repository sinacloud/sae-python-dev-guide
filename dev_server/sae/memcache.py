#!/usr/bin/env python

"""
Fake client for sae memcached service.

This client keeps all the data in local memory, and the data will be lost once 
the process is down.

This should give you a feel for how this module operates::

    import pylibmc
    mc = pylibmc.Client()

    mc.set("some_key", "Some value")
    value = mc.get("some_key")

    mc.set("another_key", 3)
    mc.delete("another_key")

    mc.set("key", "1")   # note that the key used for incr/decr must be a string.
    mc.incr("key")
    mc.decr("key")

The standard way to use memcache with a database is like this::

    key = derive_key(obj)
    obj = mc.get(key)
    if not obj:
        obj = backend_api.get(...)
        mc.set(key, obj)

    # we now have obj, and future passes through this code
    # will use the object from the cache.

Detailed Documentation
======================

More detailed documentation is available in the L{Client} class.
"""

import sys
import os
import re
import time
import pickle

SERVER_MAX_KEY_LENGTH = 250
#  Storing values larger than 1MB requires recompiling memcached.  If you do,
#  this value can be changed by doing "memcache.SERVER_MAX_VALUE_LENGTH = N"
#  after importing this module.
SERVER_MAX_VALUE_LENGTH = 1024*1024

class _Error(Exception):
    pass

class _ConnectionDeadError(Exception):
    pass

class _CacheEntry(object):
    
    def __init__(self, value, flags, expiration):
        self.value = value
        self.flags = flags
        self.created_time = time.time()
        self.will_expire = expiration != 0
        self.locked = False
        self._set_expiration(expiration)

    def _set_expiration(self, expiration):
        if expiration > (86400 * 30):
            self.expiration = expiration
        else:
            self.expiration = self.created_time + expiration

    def is_expired(self):
        return self.will_expire and time.time() > self.expiration

class local(object):
    pass

_DEAD_RETRY = 30  # number of seconds before retrying a dead server.
_SOCKET_TIMEOUT = 3  #  number of seconds before sockets timeout.

_cache = {}

class Client(local):
    """
    Object representing a pool of memcache servers.

    See L{memcache} for an overview.

    In all cases where a key is used, the key can be either:
        1. A simple hashable type (string, integer, etc.).
        2. A tuple of C{(hashvalue, key)}.  This is useful if you want to avoid
        making this module calculate a hash value.  You may prefer, for
        example, to keep all of a given user's objects on the same memcache
        server, so you could use the user's unique id as the hash value.

    @group Setup: __init__, set_servers, forget_dead_hosts, disconnect_all, debuglog
    @group Insertion: set, add, replace, set_multi
    @group Retrieval: get, get_multi
    @group Integers: incr, decr
    @group Removal: delete, delete_multi
    @sort: __init__, set_servers, forget_dead_hosts, disconnect_all, debuglog,\
           set, set_multi, add, replace, get, get_multi, incr, decr, delete, delete_multi
    """
    _FLAG_PICKLE  = 1<<0
    _FLAG_INTEGER = 1<<1
    _FLAG_LONG    = 1<<2
    _FLAG_COMPRESSED = 1<<3

    _SERVER_RETRIES = 10  # how many times to try finding a free server.

    # exceptions for Client
    class MemcachedKeyError(Exception):
        pass
    class MemcachedKeyLengthError(MemcachedKeyError):
        pass
    class MemcachedKeyCharacterError(MemcachedKeyError):
        pass
    class MemcachedKeyNoneError(MemcachedKeyError):
        pass
    class MemcachedKeyTypeError(MemcachedKeyError):
        pass
    class MemcachedStringEncodingError(Exception):
        pass

    def __init__(self, servers=[], debug=0, pickleProtocol=0,
                 pickler=pickle.Pickler, unpickler=pickle.Unpickler,
                 pload=None, pid=None,
                 server_max_key_length=SERVER_MAX_KEY_LENGTH,
                 server_max_value_length=SERVER_MAX_VALUE_LENGTH,
                 dead_retry=_DEAD_RETRY, socket_timeout=_SOCKET_TIMEOUT,
                 cache_cas = False):
        """
        Create a new Client object with the given list of servers.

        @param servers: C{servers} is passed to L{set_servers}.
        @param debug: whether to display error messages when a server can't be
        contacted.
        @param pickleProtocol: number to mandate protocol used by (c)Pickle.
        @param pickler: optional override of default Pickler to allow subclassing.
        @param unpickler: optional override of default Unpickler to allow subclassing.
        @param pload: optional persistent_load function to call on pickle loading.
        Useful for cPickle since subclassing isn't allowed.
        @param pid: optional persistent_id function to call on pickle storing.
        Useful for cPickle since subclassing isn't allowed.
        @param dead_retry: number of seconds before retrying a blacklisted
        server. Default to 30 s.
        @param socket_timeout: timeout in seconds for all calls to a server. Defaults
        to 3 seconds.
        @param cache_cas: (default False) If true, cas operations will be
        cached.  WARNING: This cache is not expired internally, if you have
        a long-running process you will need to expire it manually via
        "client.reset_cas(), or the cache can grow unlimited.
        @param server_max_key_length: (default SERVER_MAX_KEY_LENGTH)
        Data that is larger than this will not be sent to the server.
        @param server_max_value_length: (default SERVER_MAX_VALUE_LENGTH)
        Data that is larger than this will not be sent to the server.
        """
        local.__init__(self)
        self.debug = debug
        self.cache_cas = cache_cas
        self.reset_cas()

        # Allow users to modify pickling/unpickling behavior
        self.server_max_key_length = server_max_key_length
        self.server_max_value_length = server_max_value_length

        _cache = {}

        self.reset_stats()

    def reset_stats(self):
        self._get_hits = 0
        self._get_misses = 0
        self._cmd_set = 0
        self._cmd_get = 0

    def reset_cas(self):
        """
        Reset the cas cache.  This is only used if the Client() object
        was created with "cache_cas=True".  If used, this cache does not
        expire internally, so it can grow unbounded if you do not clear it
        yourself.
        """
        self.cas_ids = {}

    def set_servers(self, servers):
        """
        Set the pool of servers used by this client.

        @param servers: an array of servers.
        Servers can be passed in two forms:
            1. Strings of the form C{"host:port"}, which implies a default weight of 1.
            2. Tuples of the form C{("host:port", weight)}, where C{weight} is
            an integer weight value.
        """
        pass

    def get_stats(self, stat_args = None):
        '''Get statistics from each of the servers.

        @param stat_args: Additional arguments to pass to the memcache
            "stats" command.

        @return: A list of tuples ( server_identifier, stats_dictionary ).
            The dictionary contains a number of name/value pairs specifying
            the name of the status field and the string value associated with
            it.  The values are not converted from strings.
        '''

        total_bytes= 0
        for k, e in _cache.iteritems():
            total_bytes += len(str(e.value))

        curr_items = len(_cache)

        name = '10.67.15.110:9211 (0)'
        stats = {
            'bytes': str(total_bytes),
            'bytes_read': '920852',
            'bytes_written': '3615514',
            'cmd_get': str(self._cmd_get),
            'cmd_set': str(self._cmd_set),
            'connection_structures': '676',
            'curr_connections': '3',
            'curr_items': str(curr_items),
            'evictions': '0',
            'get_hits': str(self._get_hits),
            'get_misses': str(self._get_misses),
            'limit_maxbytes': '1048576',
            'pid': '24925',
            'pointer_size': '64',
            'rusage_system': '38237.950000',
            'rusage_user': '53464.940000',
            'threads': '0',
            'time': str(int(time.time())),
            'total_connections': '350149607',
            'total_items': str(curr_items),
            'uptime': '2541642',
            'version': '1.4.5'
        }

        return [(name, stats),]

    def flush_all(self):
        'Expire all data currently in the memcache servers.'
        _cache.clear()

    def debuglog(self, str):
        if self.debug:
            sys.stderr.write("MemCached: %s\n" % str)

    def forget_dead_hosts(self):
        """
        Reset every host in the pool to an "alive" state.
        """
        pass

    def disconnect_all(self):
        pass

    def delete_multi(self, keys, time=0, key_prefix=''):
        '''
        Delete multiple keys in the memcache doing just one query.

        >>> notset_keys = mc.set_multi({'key1' : 'val1', 'key2' : 'val2'})
        >>> mc.get_multi(['key1', 'key2']) == {'key1' : 'val1', 'key2' : 'val2'}
        1
        >>> mc.delete_multi(['key1', 'key2'])
        1
        >>> mc.get_multi(['key1', 'key2']) == {}
        1


        This method is recommended over iterated regular L{delete}s as it reduces total latency, since
        your app doesn't have to wait for each round-trip of L{delete} before sending
        the next one.

        @param keys: An iterable of keys to clear
        @param time: number of seconds any subsequent set / update commands should fail. Defaults to 0 for no delay.
        @param key_prefix:  Optional string to prepend to each key when sending to memcache.
            See docs for L{get_multi} and L{set_multi}.

        @return: 1 if no failure in communication with any memcacheds.
        @rtype: int

        '''
        for key in keys:
            _key = key_prefix + str(key)
            try:
                del _cache[_key]
            except KeyError:
                pass

        return True

    def delete(self, key):
        '''Deletes a key from the memcache.

        @return: Nonzero on success.
        '''
        if key not in _cache:
            return False
        del _cache[key]
        return True

    def incr(self, key, delta=1):
        """
        Sends a command to the server to atomically increment the value
        for C{key} by C{delta}, or by 1 if C{delta} is unspecified.
        Returns None if C{key} doesn't exist on server, otherwise it
        returns the new value after incrementing.

        Note that the value for C{key} must already exist in the memcache,
        and it must be the string representation of an integer.

        >>> mc.set("counter", "20")  # returns 1, indicating success
        1
        >>> mc.incr("counter")
        21
        >>> mc.incr("counter")
        22

        Overflow on server is not checked.  Be aware of values approaching
        2**32.  See L{decr}.

        @param delta: Integer amount to increment by (should be zero or greater).
        @return: New value after incrementing.
        @rtype: int
        """
        return self._incrdecr("incr", key, delta)

    def decr(self, key, delta=1):
        """
        Like L{incr}, but decrements.  Unlike L{incr}, underflow is checked and
        new values are capped at 0.  If server value is 1, a decrement of 2
        returns 0, not -1.

        @param delta: Integer amount to decrement by (should be zero or greater).
        @return: New value after decrementing.
        @rtype: int
        """
        return self._incrdecr("decr", key, delta)

    def _incrdecr(self, cmd, key, delta):
        self.check_key(key)

        if key not in _cache:
            return False

        if cmd == 'decr':
            delta = - delta

        value = int(_cache[key].value) + delta
        if value < 0: value = 0
        _cache[key].value = value

        return value

    def add(self, key, val, time = 0, min_compress_len = 0):
        '''
        Add new key with value.

        Like L{set}, but only stores in memcache if the key doesn't already exist.

        @return: Nonzero on success.
        @rtype: int
        '''
        return self._set("add", key, val, time, min_compress_len)

    def append(self, key, val, time=0, min_compress_len=0):
        '''Append the value to the end of the existing key's value.

        Only stores in memcache if key already exists.
        Also see L{prepend}.

        @return: Nonzero on success.
        @rtype: int
        '''
        return self._set("append", key, val, time, min_compress_len)

    def prepend(self, key, val, time=0, min_compress_len=0):
        '''Prepend the value to the beginning of the existing key's value.

        Only stores in memcache if key already exists.
        Also see L{append}.

        @return: Nonzero on success.
        @rtype: int
        '''
        return self._set("prepend", key, val, time, min_compress_len)

    def replace(self, key, val, time=0, min_compress_len=0):
        '''Replace existing key with value.

        Like L{set}, but only stores in memcache if the key already exists.
        The opposite of L{add}.

        @return: Nonzero on success.
        @rtype: int
        '''
        return self._set("replace", key, val, time, min_compress_len)

    def set(self, key, val, time=0, min_compress_len=0):
        '''Unconditionally sets a key to a given value in the memcache.

        The C{key} can optionally be an tuple, with the first element
        being the server hash value and the second being the key.
        If you want to avoid making this module calculate a hash value.
        You may prefer, for example, to keep all of a given user's objects
        on the same memcache server, so you could use the user's unique
        id as the hash value.

        @return: Nonzero on success.
        @rtype: int
        @param time: Tells memcached the time which this value should expire, either
        as a delta number of seconds, or an absolute unix time-since-the-epoch
        value. See the memcached protocol docs section "Storage Commands"
        for more info on <exptime>. We default to 0 == cache forever.
        @param min_compress_len: The threshold length to kick in auto-compression
        of the value using the zlib.compress() routine. If the value being cached is
        a string, then the length of the string is measured, else if the value is an
        object, then the length of the pickle result is measured. If the resulting
        attempt at compression yeilds a larger string than the input, then it is
        discarded. For backwards compatability, this parameter defaults to 0,
        indicating don't ever try to compress.
        '''
        return self._set("set", key, val, time, min_compress_len)


    def cas(self, key, val, time=0, min_compress_len=0):
        '''Sets a key to a given value in the memcache if it hasn't been
        altered since last fetched. (See L{gets}).

        The C{key} can optionally be an tuple, with the first element
        being the server hash value and the second being the key.
        If you want to avoid making this module calculate a hash value.
        You may prefer, for example, to keep all of a given user's objects
        on the same memcache server, so you could use the user's unique
        id as the hash value.

        @return: Nonzero on success.
        @rtype: int
        @param time: Tells memcached the time which this value should expire,
        either as a delta number of seconds, or an absolute unix
        time-since-the-epoch value. See the memcached protocol docs section
        "Storage Commands" for more info on <exptime>. We default to
        0 == cache forever.
        @param min_compress_len: The threshold length to kick in
        auto-compression of the value using the zlib.compress() routine. If
        the value being cached is a string, then the length of the string is
        measured, else if the value is an object, then the length of the
        pickle result is measured. If the resulting attempt at compression
        yeilds a larger string than the input, then it is discarded. For
        backwards compatability, this parameter defaults to 0, indicating
        don't ever try to compress.
        '''
        return self._set("cas", key, val, time, min_compress_len)

    def set_multi(self, mapping, time=0, key_prefix='', min_compress_len=0):
        '''
        Sets multiple keys in the memcache doing just one query.

        >>> notset_keys = mc.set_multi({'key1' : 'val1', 'key2' : 'val2'})
        >>> mc.get_multi(['key1', 'key2']) == {'key1' : 'val1', 'key2' : 'val2'}
        1


        This method is recommended over regular L{set} as it lowers the number of
        total packets flying around your network, reducing total latency, since
        your app doesn't have to wait for each round-trip of L{set} before sending
        the next one.

        @param mapping: A dict of key/value pairs to set.
        @param time: Tells memcached the time which this value should expire, either
        as a delta number of seconds, or an absolute unix time-since-the-epoch
        value. See the memcached protocol docs section "Storage Commands"
        for more info on <exptime>. We default to 0 == cache forever.
        @param key_prefix:  Optional string to prepend to each key when sending to memcache. Allows you to efficiently stuff these keys into a pseudo-namespace in memcache:
            >>> notset_keys = mc.set_multi({'key1' : 'val1', 'key2' : 'val2'}, key_prefix='subspace_')
            >>> len(notset_keys) == 0
            True
            >>> mc.get_multi(['subspace_key1', 'subspace_key2']) == {'subspace_key1' : 'val1', 'subspace_key2' : 'val2'}
            True

            Causes key 'subspace_key1' and 'subspace_key2' to be set. Useful in conjunction with a higher-level layer which applies namespaces to data in memcache.
            In this case, the return result would be the list of notset original keys, prefix not applied.

        @param min_compress_len: The threshold length to kick in auto-compression
        of the value using the zlib.compress() routine. If the value being cached is
        a string, then the length of the string is measured, else if the value is an
        object, then the length of the pickle result is measured. If the resulting
        attempt at compression yeilds a larger string than the input, then it is
        discarded. For backwards compatability, this parameter defaults to 0,
        indicating don't ever try to compress.
        @return: List of keys which failed to be stored [ memcache out of memory, etc. ].
        @rtype: list

        '''
        self._cmd_set += 1

        for key, value in mapping.iteritems():
            if isinstance(key, basestring):
                flags = 0
            else:
                flags = 1
            _key = key_prefix + str(key)
            self.check_key(_key)
            _cache[_key] = _CacheEntry(value, flags, time)

        return []
        

    def _set(self, cmd, key, val, time, min_compress_len = 0):
        self.check_key(key)

        self._cmd_set += 1

        key_exists = key in _cache

        if ((cmd == 'add' and key_exists) or
            (cmd == 'replace' and not key_exists) or
            (cmd == 'prepend' and not key_exists) or
            (cmd == 'append' and not key_exists)):
            return False

        if cmd == 'prepend':
            new_val = val + _cache[key].value
        elif cmd == 'append':
            new_val = _cache[key].value + val
        else:
            new_val = val

        _cache[key] = _CacheEntry(new_val, 0, time)
        return True

    def _get(self, cmd, key):
        self.check_key(key)

        self._cmd_get += 1

        if key in _cache:
            entry = _cache[key]
            if not entry.is_expired():
                self._get_hits += 1
                return entry.value
        self._get_misses += 1
        return None

    def get(self, key):
        '''Retrieves a key from the memcache.

        @return: The value or None.
        '''
        return self._get('get', key)

    def gets(self, key):
        '''Retrieves a key from the memcache. Used in conjunction with 'cas'.

        @return: The value or None.
        '''
        return self._get('gets', key)

    def get_multi(self, keys, key_prefix=''):
        '''
        Retrieves multiple keys from the memcache doing just one query.

        >>> success = mc.set("foo", "bar")
        >>> success = mc.set("baz", 42)
        >>> mc.get_multi(["foo", "baz", "foobar"]) == {"foo": "bar", "baz": 42}
        1
        >>> mc.set_multi({'k1' : 1, 'k2' : 2}, key_prefix='pfx_') == []
        1

        This looks up keys 'pfx_k1', 'pfx_k2', ... . Returned dict will just have unprefixed keys 'k1', 'k2'.
        >>> mc.get_multi(['k1', 'k2', 'nonexist'], key_prefix='pfx_') == {'k1' : 1, 'k2' : 2}
        1

        get_mult [ and L{set_multi} ] can take str()-ables like ints / longs as keys too. Such as your db pri key fields.
        They're rotored through str() before being passed off to memcache, with or without the use of a key_prefix.
        In this mode, the key_prefix could be a table name, and the key itself a db primary key number.

        >>> mc.set_multi({42: 'douglass adams', 46 : 'and 2 just ahead of me'}, key_prefix='numkeys_') == []
        1
        >>> mc.get_multi([46, 42], key_prefix='numkeys_') == {42: 'douglass adams', 46 : 'and 2 just ahead of me'}
        1

        This method is recommended over regular L{get} as it lowers the number of
        total packets flying around your network, reducing total latency, since
        your app doesn't have to wait for each round-trip of L{get} before sending
        the next one.

        See also L{set_multi}.

        @param keys: An array of keys.
        @param key_prefix: A string to prefix each key when we communicate with memcache.
            Facilitates pseudo-namespaces within memcache. Returned dictionary keys will not have this prefix.
        @return:  A dictionary of key/value pairs that were available. If key_prefix was provided, the keys in the retured dictionary will not have it present.

        '''
        self._cmd_get += 1

        retvals = {}
        for key in keys:
            _key = key_prefix + str(key)
            try:
                entry = _cache[_key]
            except KeyError:
                self._get_misses += 1
                continue

            if entry.is_expired():
                self._get_misses += 1
                continue
            if entry.flags ==  1:
                key = int(key)
            retvals[key] = entry.value
            self._get_hits += 1

        return retvals

    def check_key(self, key, key_extra_len=0):
        """Checks sanity of key.  Fails if:
            Key length is > SERVER_MAX_KEY_LENGTH (Raises MemcachedKeyLength).
            Contains control characters  (Raises MemcachedKeyCharacterError).
            Is not a string (Raises MemcachedStringEncodingError)
            Is an unicode string (Raises MemcachedStringEncodingError)
            Is not a string (Raises MemcachedKeyError)
            Is None (Raises MemcachedKeyError)
        """
        if isinstance(key, tuple): key = key[1]
        if not key:
            raise Client.MemcachedKeyNoneError("Key is None")
        if isinstance(key, unicode):
            raise Client.MemcachedStringEncodingError(
                    "Keys must be str()'s, not unicode.  Convert your unicode "
                    "strings using mystring.encode(charset)!")
        if not isinstance(key, str):
            raise Client.MemcachedKeyTypeError("Key must be str()'s")

        if isinstance(key, basestring):
            if self.server_max_key_length != 0 and \
                len(key) + key_extra_len > self.server_max_key_length:
                raise Client.MemcachedKeyLengthError("Key length is > %s"
                         % self.server_max_key_length)
            for char in key:
                if ord(char) < 33 or ord(char) == 127:
                    raise Client.MemcachedKeyCharacterError(
                            "Control characters not allowed")

def _doctest():
    import doctest, memcache
    servers = ["127.0.0.1:11211"]
    mc = Client(servers, debug=1)
    globs = {"mc": mc}
    return doctest.testmod(memcache, globs=globs)

if __name__ == "__main__":
    failures = 0
    print "Testing docstrings..."
    _doctest()
    print "Running tests:"
    print
    serverList = [["127.0.0.1:11211"]]
    if '--do-unix' in sys.argv:
        serverList.append([os.path.join(os.getcwd(), 'memcached.socket')])

    for servers in serverList:
        mc = Client(servers, debug=1)

        def to_s(val):
            if not isinstance(val, basestring):
                return "%s (%s)" % (val, type(val))
            return "%s" % val
        def test_setget(key, val):
            global failures
            print "Testing set/get {'%s': %s} ..." % (to_s(key), to_s(val)),
            mc.set(key, val)
            newval = mc.get(key)
            if newval == val:
                print "OK"
                return 1
            else:
                print "FAIL"; failures = failures + 1
                return 0


        class FooStruct(object):
            def __init__(self):
                self.bar = "baz"
            def __str__(self):
                return "A FooStruct"
            def __eq__(self, other):
                if isinstance(other, FooStruct):
                    return self.bar == other.bar
                return 0

        test_setget("a_string", "some random string")
        test_setget("an_integer", 42)
        if test_setget("long", long(1<<30)):
            print "Testing delete ...",
            if mc.delete("long"):
                print "OK"
            else:
                print "FAIL"; failures = failures + 1
            print "Checking results of delete ..."
            if mc.get("long") == None:
                print "OK"
            else:
                print "FAIL"; failures = failures + 1
        print "Testing get_multi ...",
        print mc.get_multi(["a_string", "an_integer"])

        #  removed from the protocol
        #if test_setget("timed_delete", 'foo'):
        #    print "Testing timed delete ...",
        #    if mc.delete("timed_delete", 1):
        #        print "OK"
        #    else:
        #        print "FAIL"; failures = failures + 1
        #    print "Checking results of timed delete ..."
        #    if mc.get("timed_delete") == None:
        #        print "OK"
        #    else:
        #        print "FAIL"; failures = failures + 1

        print "Testing get(unknown value) ...",
        print to_s(mc.get("unknown_value"))

        f = FooStruct()
        test_setget("foostruct", f)

        print "Testing incr ...",
        x = mc.incr("an_integer", 1)
        if x == 43:
            print "OK"
        else:
            print "FAIL"; failures = failures + 1

        print "Testing decr ...",
        x = mc.decr("an_integer", 1)
        if x == 42:
            print "OK"
        else:
            print "FAIL"; failures = failures + 1
        sys.stdout.flush()

        # sanity tests
        print "Testing sending spaces...",
        sys.stdout.flush()
        try:
            x = mc.set("this has spaces", 1)
        except Client.MemcachedKeyCharacterError, msg:
            print "OK"
        else:
            print "FAIL"; failures = failures + 1

        print "Testing sending control characters...",
        try:
            x = mc.set("this\x10has\x11control characters\x02", 1)
        except Client.MemcachedKeyCharacterError, msg:
            print "OK"
        else:
            print "FAIL"; failures = failures + 1

        print "Testing using insanely long key...",
        try:
            x = mc.set('a'*SERVER_MAX_KEY_LENGTH, 1)
        except Client.MemcachedKeyLengthError, msg:
            print "FAIL"; failures = failures + 1
        else:
            print "OK"
        try:
            x = mc.set('a'*SERVER_MAX_KEY_LENGTH + 'a', 1)
        except Client.MemcachedKeyLengthError, msg:
            print "OK"
     
