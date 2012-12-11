import tornado.wsgi

import sae

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world! - Tornado")

app = tornado.wsgi.WSGIApplication([
    (r"/", MainHandler),
])

application = sae.create_wsgi_app(app)
