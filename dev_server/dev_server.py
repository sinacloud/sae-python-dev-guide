#!/usr/bin/env python

"""Simple development server

Make sure you're use python 2.7 for developing

"""
import sys
import os
import os.path
import re
import imp
import yaml
from optparse import OptionParser

app_root = os.getcwd()

def setup_sae_environ(conf):
    # Add dummy pylibmc module
    import sae.memcache
    sys.modules['pylibmc'] = sae.memcache

    # Save kvdb data in this file else the data will lost
    # when the dev_server.py is down
    if conf.kvdb:
        print 'KVDB: ', conf.kvdb
        os.environ['kvdb_file'] = conf.kvdb

    # Add app_root to sys.path
    cwd = os.getcwd()
    if cwd not in sys.path:
        sys.path.insert(0, cwd)

    appname = str(conf.name)
    appversion = str(conf.version)

    if conf.mysql:
        import sae.const

        p = re.compile('^(.+):(.+)@(.+):(\d+)$')
        m = p.match(conf.mysql)
        if not m:
            raise Exception("Invalid mysql configuration")

        user, password, host, port = m.groups()
        dbname = 'app_' + appname
        sae.const.MYSQL_DB = dbname
        sae.const.MYSQL_USER = user
        sae.const.MYSQL_PASS = password
        sae.const.MYSQL_PORT = port
        sae.const.MYSQL_HOST = host

        print 'MySQL: %s.%s' % (conf.mysql, dbname)
    else:
        print 'MySQL config not found'

    if conf.storage:
        os.environ['STORAGE_PATH'] = os.path.abspath(conf.storage)
        
    # Add custom environment variable
    os.environ['HTTP_HOST'] = '%s:%d' % (conf.host, conf.port)
    os.environ['APP_NAME'] = appname
    os.environ['APP_VERSION'] = appversion

class Worker:
    def __init__(self, conf, app):
        self.conf = conf
        self.application = app
        self.collect_statifiles()

    def collect_statifiles(self):
        self.static_files = {}
        if hasattr(self.conf, 'handlers'):
            for h in self.conf.handlers:
                url = h['url']
                if h.has_key('static_dir'):
                    self.static_files[url] = os.path.join(app_root, h['static_dir'])
                elif h.has_key('static_path'):
                    self.static_files[url] = os.path.join(app_root, h['static_path'])
        if not len(self.static_files):
            self.static_files.update({
                '/static': os.path.join(app_root,  'static'),
                '/media': os.path.join(app_root,  'media'),
                '/favicon.ico': os.path.join(app_root,  'favicon.ico'),
            })

        if self.conf.storage:
            # stor dispatch: for test usage only
            self.static_files['/stor-stub/'] = os.path.abspath(self.conf.storage)

    def run(self):
        raise NotImplementedError()

class WsgiWorker(Worker):
    def run(self):
        # FIXME: All files under current directory
        files = ['index.wsgi']

        from werkzeug.serving import run_simple
        run_simple(self.conf.host, self.conf.port, self.application,
                   use_reloader = True,
                   use_debugger = True,
                   extra_files = files,
                   static_files = self.static_files)

class TornadoWorker(Worker):
    def run(self):
        import tornado.autoreload
        tornado.autoreload.watch('index.wsgi')

        import re
        from tornado.web import URLSpec, StaticFileHandler
        # The user should not use `tornado.web.Application.add_handlers`
        # since here in SAE one application only has a single host, so here
        # we can just use the first host_handers.
        handlers = self.application.handlers[0][1]
        for prefix, path in self.static_files.iteritems():
            pattern = re.escape(prefix) + r"(.*)"
            handlers.insert(0, URLSpec(pattern, StaticFileHandler, {"path": path}))

        import tornado.ioloop
        from tornado.httpserver import HTTPServer
        server = HTTPServer(self.application, xheaders=True)
        server.listen(self.conf.port, self.conf.host)
        tornado.ioloop.IOLoop.instance().start()

def main(options):
    conf_path = os.path.join(app_root, 'config.yaml')
    conf = yaml.load(open(conf_path, "r"))
    options.__dict__.update(conf)
    conf = options

    # if env `WERKZEUG_RUN_MAIN` is not defined, then we are in 
    # the reloader process.
    # if os.environ.get('WERKZEUG_RUN_MAIN', False):

    setup_sae_environ(conf)

    try:
        index = imp.load_source('index', 'index.wsgi')
    except IOError:
        print >>sys.stderr, "Seems you don't have an index.wsgi"
        return
    if not hasattr(index, 'application'):
        print >>sys.stderr, "application not found in index.wsgi"
        return
    if not callable(index.application):
        print >>sys.stderr, "application is not a callable"
        return

    application = index.application

    cls_name = getattr(conf, 'worker', 'wsgi').capitalize() + 'Worker'
    try:
        globals().get(cls_name, WsgiWorker)(conf, application).run()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-p", "--port", type="int", dest="port", default="8080",
                      help="Which port to listen")
    parser.add_option("--host", dest="host", default="localhost",
                      help="Which host to listen")
    parser.add_option("--mysql", dest="mysql", help="Mysql configuration: user:password@host:port")
    parser.add_option("--storage-path", dest="storage", help="Directory used as local stoarge")
    parser.add_option("--kvdb-file", dest="kvdb", help="File to save kvdb data")
    (options, args) = parser.parse_args()

    main(options)
