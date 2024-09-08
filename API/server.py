from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO, emit
import json
from Actions.functions import * 

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/devices')
def get_devices():
    with open('/home/liam/Downloads/Home-Audio-main/API/config/devices.json', 'r') as f:
        data = json.load(f)
    return jsonify(data)
@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@app.route('/devices/update', methods=["POST"])
def update_devices():
    responseData = request.data.decode('utf-8') 
    data = json.loads(responseData)

    #print(data["zone"], data["speaker"], data["Status"][0])

    # Emit the updated data to all connected clients
    #updatedData = update_bluetooth_status(data["zone"], data["speaker"], data["Status"][0])
    updatedData = update_bluetooth_status(data["zone"], data["speaker"], data["Status"])
    print(updatedData)
    if updatedData is False:
        with open('/home/liam/Downloads/Home-Audio-main/API/config/devices.json', 'r') as f:
            OG_data = json.load(f)  # Use json.load() to load JSON data from a file

        # Emit the updated data to all connected clients
        socketio.emit('update_device_status', OG_data)
    else:
        #socketio.emit('update_device_status', updatedData)
        socketio.emit('update_device_status', updatedData)
    return "200"
@app.route('/zone', methods=["POST"])
def createZone():
    responseData = request.get_json()
    print(responseData)
    li = []
    for zones in responseData["zones"]:
        for zone in zones:
            li.append(zone)
    print(len(li))
    if len(li) == 0:
        print("working")
        removeStatus = unload_combined_sink(name="None")
        print(removeStatus)
    # turn list into str then create a name using the names for the list to make it look like one eg name 1 + name 2
    else:
        status = zoneManipulation(li)
        print(status)
    return "200"

@app.route('/status', methods=["POST"])
def status():
    responseData = request.data.decode('utf-8') 
    data = json.loads(responseData)

    socketio.emit('update_device_status', data)
    return "200"
if __name__ == '__main__':
    socketio.run(app , debug=True, host="0.0.0.0", port=8000)

#    update_bluetooth_status(responseData["zone"], "MegaBoom 3 (1)", responseData["status"][0])
