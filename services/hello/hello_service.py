from flask import Flask, request, jsonify
from prometheus_flask_exporter import PrometheusMetrics
from flask_oidc import OpenIDConnect

app = Flask(__name__)
metrics = PrometheusMetrics(app)  # This sets up the /metrics endpoint

app.config.update({
    'SECRET_KEY': 'your_secret_key',
    'TESTING': True,
    'DEBUG': True,
    'OIDC_CLIENT_SECRETS': 'client_secrets.json',
    'OIDC_ID_TOKEN_COOKIE_SECURE': False,
    # 'OIDC_SCOPES': 'openid email profile'.split(),
    # 'OIDC_INTROSPECTION_AUTH_METHOD': 'client_secret_post',
    'OIDC_OPENID_REALM': 'http://172.18.0.5/hello/oidc_callback',
    'OVERWRITE_REDIRECT_URI': 'http://172.18.0.5/hello/oidc_callback'
})

oidc = OpenIDConnect(app)

@app.route('/hello')
def hello_world():

    return 'Hello, World!'

@app.route('/hello/secure')
@oidc.require_login
def secure_hello():
    return jsonify({
        'message': 'Hello, {}!'.format(oidc.user_getfield('preferred_username')),
        'email': oidc.user_getfield('email')
    })

@app.route('/hello/logout')
def logout():
    oidc.logout()
    return redirect(url_for('hello_world'))

@app.route('/healthz', methods=['GET'])
def healthz():
    return jsonify({"status": "ok"}), 200

@app.route('/readiness', methods=['GET'])
def readiness():
    # Implement your readiness check logic here
    return jsonify({"status": "ready"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
