from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO, emit
import json

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/devices')
def get_devices():
    with open('/home/liam/Downloads/Home-Audio-main/API/config/devices.json', 'r') as f:
        data = json.load(f)
    return jsonify(data)

@app.route('/devices/update', methods=["POST"])
def update_devices():
    responseData = request.get_json()
    print(responseData)
    # Emit the updated data to all connected clients
    socketio.emit('update_device_status', responseData, to='/')
    return "200"

if __name__ == '__main__':
    socketio.run(app, debug=True)
