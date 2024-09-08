import json
from flask_socketio import emit
import subprocess

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
        if device["zone"] == device_name:
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

def update_bluetooth_status(device_name, bluetooth_name, new_status):

    # Load the JSON data
    with open('/home/liam/Downloads/Home-Audio-main/API/config/devices.json', 'r') as f:
        data = json.load(f)

    # Find and update the Bluetooth device status
    for device in data["Devices"]:
        if device["zone"] == device_name:
            for audio in device["Audio"]:
                for speaker in audio["Speakers"]:
                    for bluetooth in speaker["Bluetooth"]:
                        if bluetooth["name"] == bluetooth_name:
                            # if bluetooth["Status"][1] == new_status[0]:
                            #     print(new_status[0])
                            #     return False
                            
                            # elif bluetooth["Status"][0] == new_status[1]:
                            #     print(new_status[1])
                            #     return False
                            
                            if bluetooth["Status"][0] == new_status[1] and bluetooth["Status"][1] == new_status[0]:
                                print(new_status[1])
                                print(new_status[0])
                                return False
                            
                            if bluetooth["Status"][1] != new_status[0] and bluetooth["Status"][0] != new_status[1]:
                                print(f"Bluetooth device '{bluetooth_name}' status set to '{new_status[0]}' on device '{device_name} which is turned {new_status[1]}'.")
                                bluetooth["Status"][1] = new_status[0]
                                bluetooth["Status"][0] = new_status[1]
                            
                                # Save the updated JSON data back to the file
                                with open('/home/liam/Downloads/Home-Audio-main/API/config/devices.json', 'w') as f:
                                    json.dump(data, f, indent=4)
                 

                                print(type(data))
                                return data
                            
                            if bluetooth["Status"][1] != new_status[0]:
                                print(f"Bluetooth device '{bluetooth_name}' status set to '{new_status[0]}' on device '{device_name} which is turned {bluetooth["Status"][0]}.")
                                bluetooth["Status"][1] = new_status[0]
                                with open('/home/liam/Downloads/Home-Audio-main/API/config/devices.json', 'w') as f:
                                    json.dump(data, f, indent=4)
                                

                                print(type(data))
                                return data
                                
                            if bluetooth["Status"][0] != new_status[1]:
                                bluetooth["Status"][0] = new_status[1]
                                print(f"Bluetooth device '{bluetooth_name}' status {bluetooth["Status"][1]}  on device '{device_name} which is turned {new_status[1]}'.")

                                with open('/home/liam/Downloads/Home-Audio-main/API/config/devices.json', 'w') as f:
                                    json.dump(data, f, indent=4)
                                
  
                                print(type(data))
                                return data

    print(f"Bluetooth device '{bluetooth_name}' not found on device '{device_name}'.")
    return False

#data = {'zone':'Pi1','speaker':'MegaBoom 3 (1)','Status':['Connected','OFF']}
#updatedData= update_bluetooth_status(device_name=data["zone"], bluetooth_name=data["speaker"],new_status=data["Status"])
#print(updatedData)


def zoneSearch(zone=None):
    try:
        if zone is not None:
            with open('/home/liam/Downloads/Home-Audio-main/API/config/devices.json', 'r') as f:
                data = json.load(f)

    # Find and update the Bluetooth device status
            for device in data["Devices"]:
                if device["name"] == zone:
                    for audio in device["Audio"]:
                        return audio["pulseaudio"]
    except Exception as e:
        print("Error" + str(e))        
        

import subprocess

def combine_zones(data, name="Party"):
    # Step 1: List all sinks and check for existing combined sink
    result = subprocess.run(['pactl', 'list', 'sinks', 'short'], capture_output=True, text=True)
    
    if "combined" in result.stdout:
        return "Error: A combined zone already exists."

    # Step 2: Get the sinks to combine from the zones in the data dictionary
    zone_sinks = [zone['name'] for zone in data['zones'] if zone['state'] == 'RUNNING']
    
    if not zone_sinks:
        return "Error: No running sinks available to combine."
    groupZoneName = " + ".join(zone_sinks)  # Combine the names with " + " in between
    

    # Step 3: Create the combined sink using the sink names
    sink_names = ",".join(zone_sinks)
    subprocess.run(['pactl', 'load-module', 'module-combine-sink', f'slaves={sink_names}', f'sink_name={name}'])
    
    print(f"Combined zone '{name}' created successfully.")
    return groupZoneName


def unload_combined_sink(name=None):
    # Step 1: Get the sink name from the list of loaded modules
    result = subprocess.run(['pactl', 'list', 'short', 'modules'], capture_output=True, text=True)
    
    # Look for the combined sink matching the given name
    combined_sink = None
    for line in result.stdout.splitlines():
        if f"{name}" in line:
            combined_sink = line.split()[0]  # Get the module ID
    
    if not combined_sink:
        return f"Error: Combined sink '{name}' not found."

    # Step 2: Unload the combined sink module
    subprocess.run(['pactl', 'unload-module', combined_sink])
    
    return f"Combined zone '{name}' unloaded successfully."


def zoneManipulation(zones=None, CmpZnName=None):
    try:
        print(zones)
        pulseaudio_sinks = []
        matching_sinks = {"zones":[]}
        for zone in zones:
            found = zoneSearch(zone)
            if found:
                pulseaudio_sinks.append(found)

        # Run the pactl command to list all sinks
        result = subprocess.run(['pactl', 'list', 'sinks'], stdout=subprocess.PIPE)

        # Decode the output and split it by lines
        sinks_data = result.stdout.decode('utf-8').splitlines()
        
        # Extract sink name, state, and owner module information
        sink_names = [line.strip("\t") for line in sinks_data if 'Name' in line]
        sink_states = [line.strip("\t") for line in sinks_data if 'State' in line]
        sink_owner_module_ids = [line.strip("\t") for line in sinks_data if 'Owner Module' in line]
        
        # Returning the results as a dictionary
        rsp = {
            "sink_names": sink_names,
            "sink_states": sink_states,
            "sink_owner_module_ids": sink_owner_module_ids
        }
        for audioSource in pulseaudio_sinks:
            for name,state,mdlId in zip(rsp['sink_names'], rsp['sink_states'], rsp['sink_owner_module_ids']):
                if audioSource == name.strip("Name: "):
                    sink = {
                        "name":name.strip("Name: "),
                        "state":state.strip("State: "),
                        "id": mdlId.strip("Owner Module: ")
                    }
                    matching_sinks["zones"].append(sink)
        print(matching_sinks)
        return combine_zones(data=matching_sinks,name=CmpZnName)
         
    except Exception as e:
        print("Error: " + str(e))
        return {}

# Example usage
#data = ["Upstairs Living Room", "Liams Office"]

#rsp = zoneManipulation(data, "test")
#print(rsp)

# Example usage:


# Example usage:
#data = {"zones":[{'name': 'Upstairs_Living_room_speaker_RTP_sink', 'state': 'RUNNING', 'id': '536870913'}, 
#                {'name': 'Liams_Office_speaker_RTP_sink', 'state': 'RUNNING', 'id': '536870914'}]}
#print(combine_zones(data, name="test"))
# 
#print(unload_combined_sink(name="None"))