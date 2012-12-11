import tornado.web
from tornado.httpclient import AsyncHTTPClient

class MainHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        http = tornado.httpclient.AsyncHTTPClient()
        http.fetch("http://wiki.westeros.org", callback=self._callback)
        self.write("Hello to the Tornado world! ")
        self.flush()

    def _callback(self, response):
        self.write(response.body)
        self.finish()

settings = {
    "debug": True,
}

# application should be an instance of `tornado.web.Application`,
# and don't wrap it with `sae.create_wsgi_app`
application = tornado.web.Application([
    (r"/", MainHandler),
], **settings)
