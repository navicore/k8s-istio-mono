from flask import Flask, redirect, url_for, session, jsonify
from authlib.integrations.flask_client import OAuth
import logging

# Setup logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configure OAuth
oauth = OAuth(app)
oauth.register(
    name='oauth_provider',
    client_id='flask-app',
    client_secret='your-client-secret',
    access_token_url='http://172.18.0.5/auth/realms/flask-realm/protocol/openid-connect/token',
    authorize_url='http://172.18.0.5/auth/realms/flask-realm/protocol/openid-connect/auth',
    authorize_params=None,
    refresh_token_url=None,
    redirect_uri='http://172.18.0.5/hello/authorize',  # Updated to match the new root path
    client_kwargs={'scope': 'openid email profile'},
)

@app.route('/hello')
def homepage():
    user = session.get('user')
    return f'Hello, {user["preferred_username"]}' if user else 'Hello, please <a href="/hello/login">login</a>.'

@app.route('/hello/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    authorization_url = oauth.oauth_provider.authorize_url
    params = {
        'client_id': oauth.oauth_provider.client_id,
        'redirect_uri': redirect_uri,
        'response_type': 'code',
        'scope': 'openid email profile'
    }
    url = authorization_url + '?' + '&'.join([f'{k}={v}' for k, v in params.items()])
    logging.debug(f"Redirecting to {url}")
    return redirect(url)

@app.route('/hello/authorize')
def authorize():
    token = oauth.oauth_provider.authorize_access_token()
    user = oauth.oauth_provider.parse_id_token(token)
    session['user'] = user
    return redirect(url_for('homepage'))

@app.route('/hello/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('homepage'))

@app.route('/hello/secure')
def secure_hello():
    user = session.get('user')
    if user:
        return jsonify({
            'message': f'Hello, {user["preferred_username"]}!',
            'email': user['email']
        })
    return redirect(url_for('login'))

@app.route('/hello/healthz', methods=['GET'])
def healthz():
    return jsonify({"status": "ok"}), 200

@app.route('/hello/readiness', methods=['GET'])
def readiness():
    return jsonify({"status": "ready"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
