import sae
from renrenoauth import app

application = sae.create_wsgi_app(app)
