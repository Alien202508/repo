from flask import Flask, request, jsonify

app = Flask(__name__)

# تخزين الرسائل
server_to_client = []
client_to_server = []

@app.route('/')
def index():
    return 'Relay Server is Running'

@app.route('/send_to_client', methods=['POST'])
def send_to_client():
    data = request.json
    server_to_client.append(data)
    return jsonify({"status": "Command received"})

@app.route('/get_from_client', methods=['GET'])
def get_from_client():
    if server_to_client:
        return jsonify(server_to_client.pop(0))
    else:
        return jsonify({})

@app.route('/send_to_server', methods=['POST'])
def send_to_server():
    data = request.json
    client_to_server.append(data)
    return jsonify({"status": "Output received"})

@app.route('/get_from_server', methods=['GET'])
def get_from_server():
    if client_to_server:
        return jsonify(client_to_server.pop(0))
    else:
        return jsonify({})
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
