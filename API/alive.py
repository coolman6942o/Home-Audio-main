import os
import platform
import time
import json
from flask_socketio import SocketIO, emit
import requests

API_ENDPOINT = "http://192.168.0.179:8000/status"

def send_api_request(api_endpoint, data):
    """Send an API request to the specified endpoint."""
    try:
        headers = {"Content-Type": "application/json"}
        
        response = requests.post(api_endpoint, json=data, headers=headers)
        response.raise_for_status()
        print("API request sent successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Error sending API request: {e}")


def updateDeviceStatus(host, status):
    with open("/home/liam/Downloads/Home-Audio-main/API/config/devices.json","r") as f:
        data = json.load(f)

    for device in data["Devices"]:
        if device["host"] == host:
            if device["status"] == status:    
                print(f"{host} is {status}")
            else:
                print(f"{host} changed status to {status}")
                device["status"] = status
            # Save the updated JSON data back to the file
                with open('/home/liam/Downloads/Home-Audio-main/API/config/devices.json', 'w') as f:
                    json.dump(data, f, indent=4)
                send_api_request(API_ENDPOINT, data)
                print(f"{host} is {status}")

    
def ping_host(host):
    # Determine the command based on the operating system
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    
    # Build the command to ping only once
    command = f'ping {param} 1 {host}'

    # Redirect output to null to suppress command output
    if platform.system().lower() == 'windows':
        command += ' > NUL 2>&1'
    else:
        command += ' > /dev/null 2>&1'
    
    # Execute the command
    response = os.system(command)
    
    # Check the response
    if response == 0:
        status = {"host":host,"status":"Online"}
        return status
    else:
        status = {"host":host,"status":"Offline"}
        return status
if __name__ == "__main__":
    # List of hosts to ping
    hosts_to_ping = ['192.168.0.106', '192.168.0.74', '192.168.0.127']
    # Ping each host in the list
    while True:
        for host in hosts_to_ping:
            notice = ping_host(host)
            updateDeviceStatus(host=notice["host"], status=notice["status"])
                
        time.sleep(5)