"""SAE Python

Jaime Chen<chenzheng2@staff.sina.com.cn> 2011
"""

import core

def create_wsgi_app(app):

    def new_app(environ, start_response):
        import os

        os.environ['HTTP_HOST'] = environ['HTTP_HOST']

        return app(environ, start_response)

    return new_app

def dev_server(conf):
    core.environ = conf
