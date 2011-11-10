
from flask import Flask, request, redirect, session
from weibopy import OAuthHandler, oauth, API

app = Flask(__name__)
app.debug = True
app.secret_key = 'test'

consumer_key = '199***'
consumer_secret = 'a1f8****'

def get_referer():
    return request.headers.get('HTTP_REFERER', '/')

def get_weibo_user():
    auth = OAuthHandler(consumer_key, consumer_secret)
    # Get currrent user access token from session
    access_token = session['oauth_access_token']
    auth.setToken(access_token.key, access_token.secret)
    api = API(auth)
    # Get info from weibo
    return api.me()

def login_ok(f):
    def login_wrapper(*args, **kw):
        if 'oauth_access_token' not in session:
            return redirect('/login')
        return f(*args, **kw)
    return login_wrapper

@app.route('/')
@login_ok
def hello():
    user = get_weibo_user()
    return "Hello, %d <img src=%s>" % (user.screen_name, user.profile_image_url)

@app.route('/login')
def login():
    session['login_ok_url'] = get_referer()
    callback = 'http://appstack.sinaapp.com/login_callback'

    auth = OAuthHandler(consumer_key, consumer_secret, callback)
    # Get request token and login url from the provider
    url = auth.get_authorization_url()
    session['oauth_request_token'] = auth.request_token
    # Redirect user to login
    return redirect(url)

@app.route('/login_callback')
def login_callback():
    # This is called by the provider when user has granted permission to your app
    verifier = request.args.get('oauth_verifier', None)
    auth = OAuthHandler(consumer_key, consumer_secret)
    request_token = session['oauth_request_token']
    del session['oauth_request_token']
    
    # Show the provider it's us really
    auth.set_request_token(request_token.key, request_token.secret)
    # Ask for a temporary access token
    session['oauth_access_token'] = auth.get_access_token(verifier)
    return redirect(session.get('login_ok_url', '/'))

@app.route('/logout')
def logout():
    del session['oauth_access_token']
    return redirect(get_referer())
