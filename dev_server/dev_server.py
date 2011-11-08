#!/usr/bin/python

"""Simple development server

Make sure you're use python 2.6 for developing

"""
import sys
import os
import imp
from wsgiref.simple_server import make_server

import sae.core

def main():

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

    server = make_server("", 8080, index.application)
    print "Start development server on http://localhost:8080/"
    try:
        server.serve_forever()
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

    main()
