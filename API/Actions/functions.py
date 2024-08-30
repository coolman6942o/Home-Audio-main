import json
from flask_socketio import emit

def set_bluetooth_status(device_name, bluetooth_name, new_status):
    """
    Set the status of a Bluetooth device in the provided JSON structure.

    Args:
        device_name (str): The name of the device (e.g., "PI 1").
        bluetooth_name (str): The name of the Bluetooth device (e.g., "Boom3 (1)").
        new_status (str): The new status to set (e.g., "Connected", "Not Connected").

    Returns:
        bool: True if the operation was successful, False otherwise.
    """

    # Load the JSON data
    with open('/home/liam/Downloads/Home-Audio-main/API/config/devices.json', 'r') as f:
        data = json.load(f)

    # Find and update the Bluetooth device status
    for device in data["Devices"]:
        if device["name"] == device_name:
            for audio in device["Audio"]:
                for speaker in audio["Speakers"]:
                    for bluetooth in speaker["Bluetooth"]:
                        if bluetooth["name"] == bluetooth_name:
                            if bluetooth["Status"][1] == new_status:
                                return False
                            else:
                                print(f"Bluetooth device '{bluetooth_name}' status set to '{new_status}' on device '{device_name}'.")
                                bluetooth["Status"][1] = new_status
                                
                                # Save the updated JSON data back to the file
                                with open('/home/liam/Downloads/Home-Audio-main/API/config/devices.json', 'w') as f:
                                    json.dump(data, f, indent=4)
                                
                                # Emit the updated data to all connected clients
                                emit('update_device_status', data, broadcast=True)
                                
                                return True

    print(f"Bluetooth device '{bluetooth_name}' not found on device '{device_name}'.")
    return False

# Example usage:
status = set_bluetooth_status("PI 1", "Boom3 (1)", "Not Connected")
print(status)