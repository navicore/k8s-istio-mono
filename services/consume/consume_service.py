from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/consume', methods=['POST'])
def consume():
    data = request.json
    sku = data.get('sku')
    quantity = data.get('quantity')
    # Logic to handle consume event
    return jsonify({"message": f"Consumed {quantity} of SKU {sku}"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
