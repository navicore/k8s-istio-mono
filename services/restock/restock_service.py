from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/restock', methods=['POST'])
def restock():
    data = request.json
    sku = data.get('sku')
    quantity = data.get('quantity')
    # Logic to handle restock event
    return jsonify({"message": f"Restocked {quantity} of SKU {sku}"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
