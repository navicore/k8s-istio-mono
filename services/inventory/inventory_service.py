from flask import Flask, request, jsonify
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)  # This sets up the /metrics endpoint

inventory = {}

@app.route('/update', methods=['POST'])
def update_inventory():
    data = request.json
    # Logic to update inventory
    return jsonify({'status': 'inventory updated', 'data': data})

# @app.route('/inventory', methods=['POST'])
# def update_inventory():
#     data = request.json
#     sku = data.get('sku')
#     quantity = data.get('quantity')
#     action = data.get('action')
#     
#     if action == 'consume':
#         inventory[sku] = inventory.get(sku, 0) - quantity
#     elif action == 'restock':
#         inventory[sku] = inventory.get(sku, 0) + quantity
#     else:
#         return jsonify({"error": "Invalid action"}), 400
#
#     return jsonify({"sku": sku, "quantity": inventory[sku]}), 200
#
@app.route('/healthz', methods=['GET'])
def healthz():
    return jsonify({"status": "ok"}), 200

@app.route('/readiness', methods=['GET'])
def readiness():
    # Implement your readiness check logic here
    return jsonify({"status": "ready"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
