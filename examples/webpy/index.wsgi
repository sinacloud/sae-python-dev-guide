import os

import sae
import web
        
urls = (
    '/', 'Hello'
)

app_root = os.path.dirname(__file__)
templates_root = os.path.join(app_root, 'templates')
render = web.template.render(templates_root)

class Hello:        
    def GET(self):
        return render.hello()

app = web.application(urls, globals()).wsgifunc()

application = sae.create_wsgi_app(app)
