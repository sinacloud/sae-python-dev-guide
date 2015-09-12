#!/usr/bin/env python
# -*-coding: utf8 -*-

"""Channel API
"""

import time
import json
import os

MAXIMUM_CLIENT_ID_LENGTH = 118

MAXIMUM_TOKEN_DURATION_SECONDS = 24 * 60

MAXIMUM_MESSAGE_LENGTH = 32767

class Error(Exception):
    """Base error class for this module."""

class InvalidChannelClientIdError(Error):
    """Error that indicates a bad client id."""

class InvalidChannelTokenDurationError(Error):
    """Error that indicates the requested duration is invalid."""

class InvalidMessageError(Error):
    """Error that indicates a message is malformed."""

class InternalError(Error):
    """Error that indicates server side error"""

def _validate_client_id(client_id):
    if not isinstance(client_id, basestring):
        raise InvalidChannelClientIdError('"%s" is not a string.' % client_id)

    if isinstance(client_id, unicode):
        client_id = client_id.encode('utf-8')

    if len(client_id) > MAXIMUM_CLIENT_ID_LENGTH:
        msg = 'Client id length %d is greater than max length %d' % (
            len(client_id), MAXIMUM_CLIENT_ID_LENGTH)
        raise InvalidChannelClientIdError(msg)

    return client_id

def create_channel(name, duration=None):
    client_id = _validate_client_id(name)

    if duration is not None:
        if not isinstance(duration, (int, long)):
            raise InvalidChannelTokenDurationError(
                'Argument duration must be integral')
        elif duration < 1:
            raise InvalidChannelTokenDurationError(
                'Argument duration must not be less than 1')
        elif duration > MAXIMUM_TOKEN_DURATION_SECONDS:
            msg = ('Argument duration must be less than %d'
                 % (MAXIMUM_TOKEN_DURATION_SECONDS + 1))
            raise InvalidChannelTokenDurationError(msg)

    _cache[name] = []
    return 'http://%s/_sae/channel/%s' % (os.environ['HTTP_HOST'], name)

def send_message(name, message, async=False):
    client_id = name

    if isinstance(message, unicode):
        message = message.encode('utf-8')
    elif not isinstance(message, str):
        raise InvalidMessageError('Message must be a string')
    if len(message) > MAXIMUM_MESSAGE_LENGTH:
        raise InvalidMessageError(
            'Message must be no longer than %d chars' % MAXIMUM_MESSAGE_LENGTH)

    if name in _cache:
        _cache[name].append(message)
        return 1
    else:
        return 0

_cache = {}

import urllib
import urlparse
import cStringIO

def _channel_wrapper(app):
    def _(environ, start_response):
        if not environ['PATH_INFO'].startswith('/_sae/channel/dev'):
            return app(environ, start_response)

        qs = urlparse.parse_qs(environ['QUERY_STRING'])

        token = qs['channel'][0]
        command = qs['command'][0]

        if token not in _cache:
            start_response('401 forbidden', [])
            return []

        start_response('200 ok', [])

        if command == 'poll':
            try:
                return [_cache[token].pop(0),]
            except IndexError:
                return []
        else:
            qs = urllib.urlencode({'from': token})
            environ['PATH_INFO'] = '/_sae/channel/%sed' % command
            environ['QUERY_STRING'] = ''
            environ['REQUEST_METHOD'] = 'POST'
            environ['HTTP_CONTENT_TYPE'] = 'application/x-www-form-urlencoded'
            environ['HTTP_CONTENT_LENGTH'] = len(qs)
            environ['wsgi.input'] = cStringIO.StringIO(qs)
            try:
                print '[CHANNEL]', [i for i in app(environ, lambda x, y: None)]
            except Exception:
                pass
            return []

    return _ 
