import sae
import cStringIO
from bottle import Bottle, request, response

app = Bottle()

@app.route('/')
def index():
    return """
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <title>matplotlib shell</title>
  </head>
  <body>
    <form action="/plot" method="POST">
      <div id="code">
        <input type="submit" value="RUN"/>
        <hr>
        <textarea rows="25" cols="80" name="code"></textarea>
      </div>
      <hr/>
    </form>
    <div id="quotes" class="clearfix">
    </div>
  </body>
</html>
"""

@app.route('/plot', method='POST')
def plot():
    code = request.forms['code']

    import matplotlib.pyplot as plt
    #import pylab as plt
    __f__ = cStringIO.StringIO()
    
    dct = dict()
    dct['__name__'] = '__main__'
    exec code in dct
    plt.savefig(__f__)
    data = __f__.getvalue()
    __f__.close()

    response.content_type = 'image/png'
    return data

import bottle
bottle.debug(True)

application = sae.create_wsgi_app(app)
