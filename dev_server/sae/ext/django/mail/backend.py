"""send mail via sae's mail service"""

import threading

from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend

from email.mime.base import MIMEBase

from sae.mail import EmailMessage, Error

class EmailBackend(BaseEmailBackend):
    def __init__(self, host=None, port=None, username=None, password=None,
                 use_tls=None, fail_silently=False, **kwargs):
        super(EmailBackend, self).__init__(fail_silently=fail_silently)
        self.host = host or settings.EMAIL_HOST
        self.port = port or settings.EMAIL_PORT
        if username is None:
            self.username = settings.EMAIL_HOST_USER
        else:
            self.username = username
        if password is None:
            self.password = settings.EMAIL_HOST_PASSWORD
        else:
            self.password = password
        if use_tls is None:
            self.use_tls = settings.EMAIL_USE_TLS
        else:
            self.use_tls = use_tls
        self.smtp = (self.host, self.port, self.username, self.password,
                     self.use_tls)
        self._lock = threading.RLock()

    def send_messages(self, email_messages):
        if not email_messages:
            return
        with self._lock:
            num_sent = 0
            for message in email_messages:
                sent = self._send(message)
                if sent:
                    num_sent += 1
        return num_sent

    def _send(self, email_message):
        if not email_message.recipients():
            return False
        attachments = []
        for attach in email_message.attachments:
            if isinstance(attach, MIMEBase):
                if not self.fail_silently:
                    raise NotImplemented()
                else:
                    return False
            else:
                attachments.append((attach[0], attach[1]))
        try:
            message = EmailMessage()
            message.to = email_message.recipients()
            message.from_addr = email_message.from_email
            message.subject = email_message.subject
            message.body = email_message.body
            message.smtp = self.smtp
            if attachments:
                message.attachments = attachments
            message.send()
        except Error, e:
            if not self.fail_silently:
                raise
            return False
        return True
