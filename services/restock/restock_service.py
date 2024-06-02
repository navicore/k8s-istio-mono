from flask import Flask, request, jsonify
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)  # This sets up the /metrics endpoint

@app.route('/restock', methods=['POST'])
def restock():
    data = request.json
    sku = data.get('sku')
    quantity = data.get('quantity')
    # Logic to handle restock event
    return jsonify({"message": f"Restocked {quantity} of SKU {sku}"}), 200

@app.route('/healthz', methods=['GET'])
def healthz():
    return jsonify({"status": "ok"}), 200

@app.route('/readiness', methods=['GET'])
def readiness():
    # Implement your readiness check logic here
    return jsonify({"status": "ready"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
