import subprocess
import time

def get_sink_latency(sink_name):
    """Retrieve the latency of a given sink using pacmd."""
    try:
        # Run pacmd command to list sink information
        result = subprocess.run(["pacmd", "list-sinks"], capture_output=True, text=True, check=True)
        output = result.stdout

        # Find the section of the output related to the given sink
        sink_data = output.split("index: ")[1:]  # Split by sink indices
        for sink in sink_data:
            if f"name: <{sink_name}>" in sink:
                # Extract the latency line
                latency_line = next((line for line in sink.splitlines() if "current latency" in line), None)
                if latency_line:
                    # Extract latency value in microseconds
                    latency = int(latency_line.split()[-2])
                    return latency
        return None
    except subprocess.CalledProcessError as e:
        print(f"Error retrieving latency for sink {sink_name}: {e}")
        return None

def adjust_latency(sink_name, offset):
    """Adjust the latency offset of a given sink using pactl."""
    try:
        # Convert the offset to microseconds and apply it
        offset_str = f"{offset * 1000}"  # convert ms to microseconds
        subprocess.run(["pactl", "set-port-latency-offset", sink_name, offset_str], check=True)
        print(f"Adjusted latency of {sink_name} by {offset} ms")
    except subprocess.CalledProcessError as e:
        print(f"Error adjusting latency for sink {sink_name}: {e}")

def monitor_and_adjust_sinks(sinks, check_interval=5):
    """Monitor the latency of each sink and adjust if they drift out of sync."""
    if len(sinks) < 2:
        print("At least two sinks are required to monitor and adjust latency.")
        return

    while True:
        # Get the latencies of all sinks
        latencies = {}
        for sink in sinks:
            latency = get_sink_latency(sink)
            if latency is not None:
                latencies[sink] = latency
            else:
                print(f"Could not retrieve latency for {sink}")

        if len(latencies) < len(sinks):
            print("Skipping adjustment due to missing latency data.")
        else:
            # Calculate the maximum and minimum latency
            max_latency = max(latencies.values())
            min_latency = min(latencies.values())

            # Adjust sinks that are behind
            for sink, latency in latencies.items():
                if latency < max_latency:
                    offset = max_latency - latency
                    adjust_latency(sink, offset / 1000.0)  # convert microseconds to milliseconds

        # Wait for the next check
        time.sleep(check_interval)

# if __name__ == "__main__":
    # Example sinks to monitor and adjust
    # sinks_to_monitor = [
        # "Upstairs_Living_room_speaker_RTP_sink",
        # "Liams_Office_speaker_RTP_sink",
        # "Liams_Bedroom_speaker_RTP_sink"
    # ]
    # 
    # monitor_and_adjust_sinks(sinks_to_monitor)
def monitor_and_adjust_combined_sink(combined_sink_name="Combined_Speaker", slaves=None, check_interval=5):
    """Monitor the combined sink and adjust its latency if the slaves drift out of sync."""
    if slaves is None:
        slaves = [
            "Upstairs_Living_room_speaker_RTP_sink",
            "Liams_Office_speaker_RTP_sink",
            "Liams_Bedroom_speaker_RTP_sink"
        ]

    while True:
        # Monitor individual slave sinks
        latencies = {}
        for sink in slaves:
            latency = get_sink_latency(sink)
            if latency is not None:
                latencies[sink] = latency
            else:
                print(f"Could not retrieve latency for {sink}")

        if len(latencies) < len(slaves):
            print("Skipping adjustment due to missing latency data.")
        else:
            # Calculate the maximum and minimum latency
            max_latency = max(latencies.values())
            min_latency = min(latencies.values())


            # Adjust the combined sink if necessary
            if max_latency - min_latency > 5000:  # Example threshold of 5000 microseconds (5ms)
                adjust_latency(combined_sink_name, (max_latency - min_latency) / 1000.0)

        time.sleep(check_interval)

if __name__ == "__main__":
    # Example combined sink and its slaves
    combined_sink = "Combined_Speaker"
    slaves_to_monitor = [
        "Upstairs_Living_room_speaker_RTP_sink",
        "Liams_Office_speaker_RTP_sink",
        "Liams_Bedroom_speaker_RTP_sink"
    ]

    monitor_and_adjust_combined_sink(combined_sink_name=combined_sink, slaves=slaves_to_monitor)