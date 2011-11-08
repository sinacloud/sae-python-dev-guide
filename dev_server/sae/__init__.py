"""SAE Python

Jaime Chen<chenzheng2@staff.sina.com.cn> 2011
"""

import core

def create_wsgi_app(app):
    return app

def dev_server(conf):
    core.environ = conf
