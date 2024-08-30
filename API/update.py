import subprocess
import requests
from Actions.functions import *
import time
# Set the MAC address of the Bluetooth device
DEVICE_MAC = "10:94:97:22:EA:6B"

# Set the expected name of the sink (as it would appear in pactl list short sinks)
EXPECTED_SINK = f"bluez_sink.{DEVICE_MAC.replace(':', '_')}"

# Set the API endpoint and the data to send
API_ENDPOINT = "http://127.0.0.1:5000/devices/update"

DATA = {"message": "Bluetooth device is connected and sink is active"}

def is_bluetooth_device_connected(device_mac):
    """Check if the Bluetooth device is connected using bluetoothctl."""
    try:
        result = subprocess.run(["bluetoothctl", "info", device_mac],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if "Connected: yes" in result.stdout:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error checking Bluetooth device: {e}")
        return False

def is_sink_active(expected_sink):
    """Check if the expected sink appears in the pactl list short sinks."""
    try:
        result = subprocess.run(["pactl", "list", "short", "sinks"],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if expected_sink in result.stdout:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error checking PulseAudio sinks: {e}")
        return False

def send_api_request(api_endpoint, data):
    """Send an API request to the specified endpoint."""
    try:
        headers = {"Content-Type": "application/json"}
        
        response = requests.post(api_endpoint, json=data, headers=headers)
        response.raise_for_status()
        print("API request sent successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Error sending API request: {e}")

def main():
    # Check if the Bluetooth device is connected
    if is_bluetooth_device_connected(DEVICE_MAC):
        print(f"Bluetooth device {DEVICE_MAC} is connected.")
        
        # Check if the sink is active
        if is_sink_active(EXPECTED_SINK):
            print(f"Sink {EXPECTED_SINK} is active.")
            # Send API request if both conditions are met
            send_api_request(API_ENDPOINT, "{'name':'PI 2','Status':['Connected','ON']}")
        else:
            send_api_request(API_ENDPOINT, "{'name':'PI 2','Status':['Connected','OFF']}")
            print(f"Sink {EXPECTED_SINK} is not active.")
    else:
        print(f"Bluetooth device {DEVICE_MAC} is not connected.")
        send_api_request(API_ENDPOINT, "{'name':'PI 2','Status':['Not Connected','OFF']}")

if __name__ == "__main__":
    while True:
        main()
        time.sleep(15)