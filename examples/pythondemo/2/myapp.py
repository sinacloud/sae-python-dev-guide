
import MySQLdb
from flask import Flask, g, request

app = Flask(__name__)
app.debug = True

from sae.const import (MYSQL_HOST, MYSQL_HOST_S,
    MYSQL_PORT, MYSQL_USER, MYSQL_PASS, MYSQL_DB
)

@app.before_request
def before_request():
    appinfo = sae.core.Application()
    g.db = MySQLdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASS,
                           MYSQL_DB, port=int(MYSQL_PORT))

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'): g.db.close()

@app.route('/')
def hello():
    return "Hello, world! - Flask"

@app.route('/demo', methods=['GET', 'POST'])
def greeting():
    html = ''

    if request.method == 'POST':
        c = g.db.cursor()
        c.execute("insert into demo(text) values(%s)", (request.form['text']))

    html += """
    <form action="" method="post">
        <div><textarea cols="40" name="text"></textarea></div>
        <div><input type="submit" /></div>
    </form>
    """
    c = g.db.cursor()
    c.execute('select * from demo')
    msgs = list(c.fetchall())
    msgs.reverse()
    for row in msgs:
        html +=  '<p>' + row[-1] + '</p>'

    return html

