import subprocess
import os
import multiprocessing
import time

def run_librespot_processes_in_background(names=None):
    if names is None:
        # Default list of names
        names = [
            "Upstairs Living Room [Main]",
            "Liams Office [Main]",
            "Liams Bedroom [Main]"
        ]

    def run_processes_in_background(names):
        # Path to the librespot executable
        librespot_path = os.path.expanduser("~/Home-Audio-main/librespot/target/release/librespot")

        # Directory to save log files
        log_dir = os.path.expanduser("~/Home-Audio-main/cast/librespot_logs")
        os.makedirs(log_dir, exist_ok=True)

        # List to keep track of subprocesses
        processes = []

        for name in names:
            try:
                # Construct the command
                cmd = [librespot_path, "-n", name, "-b", "320"]
                
                # Log file paths
                log_file_path = os.path.join(log_dir, f"{name.replace(' ', '_').replace('[','').replace(']','')}.log")
                
                # Open the log file
                with open(log_file_path, "w") as log_file:
                    # Start the subprocess, redirecting stdout and stderr to the log file
                    process = subprocess.Popen(
                        cmd,
                        stdout=log_file,
                        stderr=subprocess.STDOUT,
                        universal_newlines=True,
                        bufsize=1
                    )
                    
                    # Append the process to the list
                    processes.append((process, name))
                    
                    print(f"Started librespot for '{name}', logging to {log_file_path}")
                
            except Exception as e:
                print(f"Failed to start librespot for '{name}': {e}")

        # Wait for all subprocesses to complete
        for process, name in processes:
            try:
                process.wait()
                print(f"librespot process for '{name}' completed with return code {process.returncode}")
            except Exception as e:
                print(f"Error while waiting for process '{name}': {e}")

    # Start the librespot processes as a daemon process
    background_process = multiprocessing.Process(target=run_processes_in_background, args=(names,))
    background_process.daemon = True  # Set the process as a daemon
    background_process.start()
    
    # Give the daemon process some time to start and create log files
    time.sleep(5)  # Increase the delay to give enough time for the processes to start

    # Ensure that log files are created
    log_dir = os.path.expanduser("~/Home-Audio-main/cast/librespot_logs")
    for name in names:
        log_file_path = os.path.join(log_dir, f"{name.replace(' ', '_').replace('[','').replace(']','')}.log")
        if not os.path.exists(log_file_path):
            print(f"Warning: Log file {log_file_path} has not been created yet.")

    print(f"Started librespot processes in the background with PID {background_process.pid}")


def create_virtual_audio_sources(sink_names=None, sink_desc=None):
    # Default list of sink names and descriptions
    if sink_names is None:
        sink_names = [
            "Upstairs_Living_room_speaker_RTP_sink",
            "Liams_Office_speaker_RTP_sink",
            "Liams_Bedroom_speaker_RTP_sink"
        ]
    
    if sink_desc is None:
        sink_desc = [
            "device.description='Upstairs_Living_Room_[Main]'",
            "device.description='Liams_Office_[Main]'",
            "device.description='Liams_Bedroom_[Main]'"
        ]

    # Ensure the two lists have the same length
    if len(sink_names) != len(sink_desc):
        raise ValueError("The length of sink_names and sink_desc must be the same.")

    # Directory to save log files
    log_dir = os.path.expanduser("~/Home-Audio-main/cast/virtual_audio_source_logs")
    os.makedirs(log_dir, exist_ok=True)

    # Log file path
    log_file_path = os.path.join(log_dir, "virtual_audio_sources.log")

    processes = []
    with open(log_file_path, "w") as log_file:
        for name, desc in zip(sink_names, sink_desc):
            cmd = [
                "pactl",
                "load-module",
                "module-null-sink",
                f"sink_name={name}",
                f"sink_properties={desc}"
            ]
            
            try:
                # Start each command as a subprocess and capture the output
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                
                # Store the process and command in the processes list
                processes.append((process, name))
                
                log_file.write(f"Started virtual audio source '{name}', logging to {log_file_path}\n")
                print(f"Started virtual audio source '{name}', logging to {log_file_path}")
            
            except Exception as e:
                log_file.write(f"Failed to start virtual audio source '{name}': {e}\n")
                print(f"Failed to start virtual audio source '{name}': {e}")

        # Wait for all processes to complete
        for process, name in processes:
            try:
                process.wait()
                log_file.write(f"Virtual audio source process for '{name}' completed with return code {process.returncode}\n")
                print(f"Virtual audio source process for '{name}' completed with return code {process.returncode}")
            except Exception as e:
                log_file.write(f"Error while waiting for process '{name}': {e}\n")
                print(f"Error while waiting for process '{name}': {e}")


def run_ffmpeg_processes_in_background(sinks=None, ips=None, ports=None):
    if sinks is None:
        # Default list of sink monitors
        sinks = [
            "Upstairs_Living_room_speaker_RTP_sink.monitor",
            "Liams_Bedroom_speaker_RTP_sink.monitor",
            "Liams_Office_speaker_RTP_sink.monitor"
        ]

    if ips is None:
        # Default list of IP addresses
        ips = [
            "192.168.0.74",
            "192.168.0.106",
            "192.168.0.127"
        ]

    if ports is None:
        # Default list of ports
        ports = [
            "5004",
            "5001",
            "5000"
        ]

    # Ensure that the lengths of the lists match
    if len(sinks) != len(ips) or len(sinks) != len(ports):
        raise ValueError("The length of sinks, ips, and ports must be the same.")

    def run_processes_in_background(sinks, ips, ports):
        # Directory to save log files
        log_dir = os.path.expanduser("~/Home-Audio-main/cast/ffmpeg_logs")
        os.makedirs(log_dir, exist_ok=True)

        # List to keep track of subprocesses
        processes = []

        for sink, ip, port in zip(sinks, ips, ports):
            try:
                # Construct the command
                cmd = [
                    "ffmpeg",
                    "-f", "pulse",
                    "-i", sink,
                    "-ac", "2",
                    "-ar", "48000",
                    "-f", "rtp",
                    f"rtp://{ip}:{port}"
                ]
                
                # Log file path
                log_file_path = os.path.join(log_dir, f"{sink.replace(' ', '_').replace('[','').replace(']','')}.log")
                
                # Open the log file
                with open(log_file_path, "w") as log_file:
                    # Start the subprocess, redirecting stdout and stderr to the log file
                    process = subprocess.Popen(
                        cmd,
                        stdout=log_file,
                        stderr=subprocess.STDOUT,
                        universal_newlines=True,
                        bufsize=1
                    )
                    
                    # Append the process to the list
                    processes.append((process, sink))
                    
                    print(f"Started ffmpeg for '{sink}', streaming to {ip}:{port}, logging to {log_file_path}")
                
            except Exception as e:
                print(f"Failed to start ffmpeg for '{sink}': {e}")

        # Wait for all subprocesses to complete
        for process, sink in processes:
            try:
                process.wait()
                print(f"ffmpeg process for '{sink}' completed with return code {process.returncode}")
            except Exception as e:
                print(f"Error while waiting for process '{sink}': {e}")

    # Start the ffmpeg processes as a daemon process
    background_process = multiprocessing.Process(target=run_processes_in_background, args=(sinks, ips, ports))
    background_process.daemon = True  # Set the process as a daemon
    background_process.start()
    
    # Give the daemon process some time to start and create log files
    time.sleep(5)  # Increase the delay to give enough time for the processes to start

    # Ensure that log files are created
    log_dir = os.path.expanduser("~/Home-Audio-main/cast/ffmpeg_logs")
    for sink in sinks:
        log_file_path = os.path.join(log_dir, f"{sink.replace(' ', '_').replace('[','').replace(']','')}.log")
        if not os.path.exists(log_file_path):
            print(f"Warning: Log file {log_file_path} has not been created yet.")

    print(f"Started ffmpeg processes in the background with PID {background_process.pid}")

