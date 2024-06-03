import os
import requests
import logging
from flask import Flask, request, jsonify
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)  # This sets up the /metrics endpoint
logger = logging.getLogger(__name__)

INVENTORY_SERVICE_URL = os.getenv('INVENTORY_SERVICE_URL', 'http://inventory-service')

@app.route('/consume', methods=['POST'])
def consume():
    data = request.json

    # Make a call to the inventory service to update the inventory
    inventory_response = requests.post(f'{INVENTORY_SERVICE_URL}/update', json=data)

    # Check if the inventory update was successful
    if inventory_response.status_code == 200:
        return jsonify({'status': 'success', 'data': data})
    else:
        logger.error('request failed: %s', inventory_response.text)
        return jsonify({'status': 'error', 'message': 'Failed to update inventory'}), 500

@app.route('/healthz', methods=['GET'])
def healthz():
    return jsonify({"status": "ok"}), 200

@app.route('/readiness', methods=['GET'])
def readiness():
    # Implement your readiness check logic here
    return jsonify({"status": "ready"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
