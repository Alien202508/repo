from flask import Flask, request, jsonify
import os

app = Flask(__name__)
client_to_server = []
server_to_client = []

@app.route('/send_to_server', methods=['POST'])
def send_to_server():
    data = request.json
    client_to_server.append(data)
    return jsonify({"status": "received"})

@app.route('/get_from_client', methods=['GET'])
def get_from_client():
    if client_to_server:
        return jsonify(client_to_server.pop(0))
    else:
        return jsonify({})

@app.route('/send_to_client', methods=['POST'])
def send_to_client():
    data = request.json
    server_to_client.append(data)
    return jsonify({"status": "sent"})

@app.route('/get_from_server', methods=['GET'])
def get_from_server():
    if server_to_client:
        return jsonify(server_to_client.pop(0))
    else:
        return jsonify({})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
