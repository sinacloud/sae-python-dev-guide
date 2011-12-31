#!/usr/bin/env python

"""Simple development server

Make sure you're use python 2.6 for developing

"""
import sys
import os
import imp
from werkzeug.serving import run_simple

import sae.core

def main(app_root):

    try:
        index = imp.load_source('index', 'index.wsgi')
    except IOError:
        print "Seems you don't have an index.wsgi"
        sys.exit(-1)

    if not hasattr(index, 'application'):
        print "application not found in index.wsgi"
        sys.exit(-1)

    if not callable(index.application):
        print "application is not a callable"
        sys.exit(-1)

    statics = { '/static': os.path.join(app_root,  'static'),
              '/media': os.path.join(app_root,  'media'),
             '/favicon.ico': os.path.join(app_root,  'favicon.ico'),
             }

    # FIXME: All files under current directory
    files = ['index.wsgi']

    try:
        run_simple('localhost', 8080, index.application,
                    use_reloader = True,
                    use_debugger = True,
                    extra_files = files,
                    static_files = statics)

    except KeyboardInterrupt:
        print "OK"

if __name__ == '__main__':
    cwd = os.getcwd()
    if cwd not in sys.path:
        sys.path.insert(0, cwd)

    try:
        import app
        sae.core.Application = app.Application
    except:
        print 'MySQL config not found: app.py'

    main(cwd)
