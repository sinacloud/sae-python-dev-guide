#!/usr/bin/env python
# -*-coding: utf8 -*-

"""SAE Mail API

Provides functions for application developers to deliver mail messages 
for their applications. Currently we only support send mail through SMTP 
asynchronously.

Examle:

1. Send a simple plain-text message.

    from sae.mail import send_mail

    send_mail('recipient@sina.com', 'subject', 'plain text',
              ('smtp.sina.com', 25, 'me@sina.com', 'password', False))

2. Send a HTML-format message.

    from sae.mail import EmailMessage

    m = EmailMessage()
    m.to = 'recipient@sina.com'
    m.subject = 'unforgivable sinner'
    m.html = '<b>darling, please, please forgive me...</b>'
    m.smtp = ('smtp.sina.com', 25, 'me@sina.com', 'password', False)
    m.send()
"""

__all__ = ['Error', 'InternalError', 'InvalidAttachmentTypeError', 
           'InvalidRequestError', 'MailTooLargeError', 'MissingBodyError', 
           'MissingRecipientError', 'MissingSMTPError', 'MissingSubjectError',
           'ServiceUnavailableError', 'MAX_EMAIL_SIZE', 'EmailMessage', 
           'send_mail']

import base64
import json
import time
import urllib
import urllib2

import core
import conf
import util

class Error(Exception):
    """Base-class for all errors in this module"""

class InternalError(Error):
    """There was an internal error while sending message, it should be 
    temporary, it problem continues, please contact us"""

class InvalidRequestError(Error):
    """The request we send to the mail backend is illengal."""

class MissingRecipientError(Error):
    """No recipient specified in message"""

class MissingSubjectError(Error):
    """No subject specified in message"""

class MissingBodyError(Error):
    """No body content specified in the message"""

class MissingSMTPError(Error):
    """No smtp server configuration is provided."""

class InvalidAttachmentTypeError(Error):
    """The type of the attachment is not permitted."""

class MailTooLargeError(Error):
    """The email is too large, """

class ServiceUnavailableError(Error):
    """The application has reached its service quota or has no permission."""

_ERROR_MAPPING = {3: InvalidRequestError, 500: InternalError, 999: InternalError,
                  999: ServiceUnavailableError}

_MAIL_BACKEND = "http://mail.sae.sina.com.cn/index.php"

MAX_EMAIL_SIZE = 1048576 # bytes (1M)

class EmailMessage(object):
    """Main interface to SAE Mail Service
    """
    _properties = ['to', 'subject', 'body', 'html', 'attachments', 'smtp', 'from_addr']
    _ext_to_disposition = {
        'bmp':  'I', 'css':  'A',
        'csv':  'A', 'gif':  'I',
        'htm':  'I', 'html': 'I',
        'jpeg': 'I', 'jpg':  'I',
        'jpe':  'I', 'pdf':  'A',
        'png':  'I', 'rss':  'I',
        'text': 'A', 'txt':  'A',
        'asc':  'A', 'diff': 'A',
        'pot':  'A', 'tiff': 'A',
        'tif':  'A', 'wbmp': 'I',
        'ics':  'I', 'vcf':  'I'
    }

    def __init__(self, **kwargs):
        """Initializer"""
        self.initialize(**kwargs)

    def initialize(self, **kwargs):
        """Sets fields of the email message
        
        Args:
          to: The recipient's email address.
          subject: The subject of the message.
          body: The content of the message, plain-text only.
          html: Use this field when you want to send html-encoded message.
          smtp: This is a five-element tuple of your smtp server's configuration
            (smtp_host, smtp_port, smtp_username, smtp_password, smtp_tls).
          attachments: The file attachments of the message, as a list of 
            two-value tuples, one tuple for each attachment. Each tuple contains
            a filename as the first element, and the file contents as the second
            element.
        """
        for name, value in kwargs.iteritems():
            setattr(self, name, value)

    def send(self):
        """Sends the email message.
        
        This method just post the message to the mail delivery queue.
        """
        message = self._to_proto()
        #print message
        self._remote_call(message)

    def check_initialized(self):
        if not hasattr(self, 'to'):
            raise MissingRecipientError()

        if not hasattr(self, 'subject'):
            raise MissingSubjectError()

        if not hasattr(self, 'smtp'):
            raise MissingSMTPError()

        if not hasattr(self, 'body') and not hasattr(self, 'html'):
            raise MissingBodyError()

    def _check_email_valid(self, address):
        if not isinstance(address, basestring):
            raise TypeError()

        # TODO: validate email address

    def _check_smtp_valid(self, smtp):
        if not isinstance(smtp, tuple) or len(smtp) != 5:
            raise TypeError()

    def _check_attachments(self, attachments):
        for a in attachments:
            if not isinstance(a, tuple) or len(a) != 2:
                raise TypeError()

    def __setattr__(self, attr, value):
        if attr not in self._properties:
            raise AttributeError("'EmailMessage' has no attribute '%s'" % attr)

        if not value:
            raise ValueError("May not set empty value for '%s'" % attr)

        if attr == 'to':
            if isinstance(value, list):
                for v in value:
                    self._check_email_valid(v)
                to = ','.join(value)
                super(EmailMessage, self).__setattr__(attr, to) 
                return

            self._check_email_valid(value)
        elif attr == 'smtp':
            self._check_smtp_valid(value)
        elif attr == 'attachments':
            self._check_attachments(value)

        super(EmailMessage, self).__setattr__(attr, value)

    def _to_proto(self):
        """Convert mail mesage to protocol message"""
        self.check_initialized()

        args = {'from':          getattr(self, 'from_addr', self.smtp[2]),
                'to':            self.to,
                'subject':       self.subject,
                'smtp_host':     self.smtp[0],
                'smtp_port':     self.smtp[1],
                'smtp_username': self.smtp[2],
                'smtp_password': self.smtp[3],
                'tls':           self.smtp[4]}

        size = 0

        if hasattr(self, 'body'):
            args['content'] = self.body
            args['content_type'] = 'TEXT'
            size = size + len(self.body)
        elif hasattr(self, 'html'):
            args['content'] = self.html
            args['content_type']  = 'HTML'
            size = size + len(self.html)

        if hasattr(self, 'attachments'):
            for attachment in self.attachments:
                ext = attachment[0].split('.')[-1]

                disposition = self._ext_to_disposition.get(ext)
                if not disposition:
                    raise InvalidAttachmentTypeError()

                key = 'attach:' + attachment[0] + ':B:' + disposition
                args[key] = base64.encodestring(attachment[1])

                size = size + len(attachment[1])

        if size > MAX_EMAIL_SIZE:
            raise MailTooLargeError()

        message = {'saemail': json.dumps(args)}
        return message

    def _remote_call(self, message):
        args = json.loads(message['saemail'])

        # just print the message on console
        print '[SAE:MAIL] Sending new mail'
        import pprint
        pprint.pprint(args)

    def _get_headers(self):
        access_key = core.get_access_key()
        secret_key = core.get_secret_key()

        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        msg = 'ACCESSKEY' + access_key + 'TIMESTAMP' + timestamp
        headers = {'TimeStamp': timestamp,
                   'AccessKey': access_key,
                   'Signature': util.get_signature(secret_key, msg)}

        return headers

def send_mail(to, subject, body, smtp, **kwargs):
    """A shortcut for sending mail"""
    kwargs['to'] = to
    kwargs['subject'] = subject
    kwargs['body'] = body
    kwargs['smtp'] = smtp
    
    EmailMessage(**kwargs).send()

