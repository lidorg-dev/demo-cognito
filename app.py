from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
import os
 
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Use a secure random key in production
oauth = OAuth(app)

oauth.register(
  name='oidc',
  authority='https://cognito-idp.us-east-1.amazonaws.com/us-east-1_IX3G0TMok',
  client_id='',
  client_secret='',
  server_metadata_url='https://cognito-idp.us-east-1.amazonaws.com/us-east-1_IX3G0TMok/.well-known/openid-configuration',
  client_kwargs={'scope': 'email openid phone'}
)
@app.route('/')
def index():
    user = session.get('user')
    if user:
        return  f'Hello, {user["email"]}. <a href="/logout">Logout</a>'
    else:
        return f'Welcome! Please <a href="/login">Login</a>.'


@app.route('/login')
def login():
    # Alternate option to redirect to /authorize
    # redirect_uri = url_for('authorize', _external=True)
    # return oauth.oidc.authorize_redirect(redirect_uri)
    return oauth.oidc.authorize_redirect('https://localhost:5000')

@app.route('/authorize')
def authorize():
    token = oauth.oidc.authorize_access_token()
    user = token['userinfo']
    session['user'] = user
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run('0.0.0.0', debug=True, port=5000, ssl_context='adhoc')