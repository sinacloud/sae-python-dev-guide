"""SAE Python

Jaime Chen<chenzheng2@staff.sina.com.cn> 2011
"""

import core

from werkzeug.debug import DebuggedApplication

def create_wsgi_app(app):
    return DebuggedApplication(app)

def dev_server(conf):
    core.environ = conf
