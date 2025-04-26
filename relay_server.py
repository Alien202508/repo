from flask import Flask, request, jsonify
import socket
import os

app = Flask(__name__)

# إعداد الاتصال عبر Socket مع سيرفر Metasploit
HOST = '127.0.0.1'  # عنوان السيرفر الفعلي أو IP العميل
PORT = 12345  # نفس المنفذ الذي يعمل عليه سيرفر Metasploit

def socket_server_connection(command):
    """الاتصال مع سيرفر Metasploit عبر Socket"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(command.encode())  # إرسال الأمر
            data = s.recv(1024)  # استلام الرد
            return data.decode()
    except Exception as e:
        return f"خطأ في الاتصال: {e}"

@app.route('/')
def index():
    return 'Relay Server is Running!'

@app.route('/send_to_client', methods=['POST'])
def send_to_client():
    """استقبال أوامر من Metasploit عبر HTTP"""
    data = request.json
    command = data.get('command', '')
    
    # إرسال الأمر إلى العميل عبر socket أو مباشرة
    response = socket_server_connection(command)
    
    return jsonify({"status": "Command received", "response": response})

@app.route('/get_from_client', methods=['GET'])
def get_from_client():
    """إرسال أمر إلى العميل (مثل إرسال صورة)"""
    command = {"command": "send_image"}  # مثال لأمر
    return jsonify(command)

if __name__ == '__main__':
    # تأكد من أن المجلد الذي يحتوي على الملفات موجود
    if not os.path.exists("uploaded_files"):
        os.makedirs("uploaded_files")
    app.run(host='0.0.0.0', port=10000)
