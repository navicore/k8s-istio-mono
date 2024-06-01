from flask import Flask, request, jsonify

app = Flask(__name__)

inventory = {}

@app.route('/inventory', methods=['POST'])
def update_inventory():
    data = request.json
    sku = data.get('sku')
    quantity = data.get('quantity')
    action = data.get('action')
    
    if action == 'consume':
        inventory[sku] = inventory.get(sku, 0) - quantity
    elif action == 'restock':
        inventory[sku] = inventory.get(sku, 0) + quantity
    else:
        return jsonify({"error": "Invalid action"}), 400

    return jsonify({"sku": sku, "quantity": inventory[sku]}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
