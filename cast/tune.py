import subprocess

# Function to get the list of active sink inputs and their details
def get_sink_inputs():
    try:
        # Run pactl command to list all sink inputs
        result = subprocess.run(['pactl', 'list', 'short', 'sink-inputs'], stdout=subprocess.PIPE, text=True)
        lines = result.stdout.splitlines()
        
        sink_inputs = []
        
        for line in lines:
            # Each line contains: <sink_input_id> <sink_id> <module_id> <client_id> <format>
            parts = line.split('\t')
            sink_input_id = parts[0]
            sink_id = parts[1]
            client_name = parts[3]  # In some cases, the client name can help identify the stream
            
            # Add the sink input ID and associated sink ID to the list
            sink_inputs.append((sink_input_id, sink_id, client_name))
        
        return sink_inputs
    except subprocess.CalledProcessError as e:
        print(f"Failed to retrieve sink inputs: {e}")
        return []

# Function to move sink inputs to the correct sink
def move_sink_input(sink_input_id, sink_name):
    try:
        cmd = ['pactl', 'move-sink-input', str(sink_input_id), sink_name]
        subprocess.run(cmd, check=True)
        print(f"Moved sink input {sink_input_id} to {sink_name}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to move sink input {sink_input_id}: {e}")

# Function to map sink-inputs to the correct sink names
def map_sink_inputs_to_sinks(sink_inputs):
    # Mapping client name to corresponding sink
    sink_mapping = {
        'Liams_Office': 'Liams_Office_speaker_RTP_sink',
        'Upstairs_Living_room': 'Upstairs_Living_room_speaker_RTP_sink',
        'Liams_Bedroom': 'Liams_Bedroom_speaker_RTP_sink'
    }
    
    # Move each input to its appropriate sink
    for sink_input_id, sink_id, client_name in sink_inputs:
        # Dynamically find the right sink based on the client name
        for keyword, sink_name in sink_mapping.items():
            if keyword in client_name:
                move_sink_input(sink_input_id, sink_name)

# Main process
if __name__ == "__main__":
    # Get all active sink inputs
    sink_inputs = get_sink_inputs()

    # Map the detected sink inputs to the correct sinks
    if sink_inputs:
        map_sink_inputs_to_sinks(sink_inputs)
    else:
        print("No active sink inputs detected.")
