import sae
from mysite import wsgi

application = sae.create_wsgi_app(wsgi.application)
