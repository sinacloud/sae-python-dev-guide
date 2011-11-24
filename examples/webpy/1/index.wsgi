
import sae
import web
        
urls = (
    '/', 'Hello'
)

class Hello:        
    def GET(self):
        web.header("Content-Type", "text/plain")
        return 'Hello, Webpy!'

app = web.application(urls, globals()).wsgifunc()

application = sae.create_wsgi_app(app)
