from flask import Flask, request, jsonify
from prometheus_flask_exporter import PrometheusMetrics
from flask_oidc import OpenIDConnect
import json

app = Flask(__name__)
metrics = PrometheusMetrics(app)  # This sets up the /metrics endpoint

app.config.update({
    'SECRET_KEY': 'your-client-secret',
    'TESTING': True,
    'OIDC_CLIENT_SECRETS': 'client_secrets.json',
    'OIDC_RESOURCE_SERVER_ONLY': True,
    'OIDC_SCOPES': ['openid', 'email', 'profile'],
    'OIDC_INTROSPECTION_AUTH_METHOD': 'client_secret_post',
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
    app.run(host='0.0.0.0', port=5000)
