from main import *
import os 

run_librespot_processes_in_background()
create_virtual_audio_sources()
run_ffmpeg_processes_in_background()

os.system("pactl load-module module-combine-sink sink_name=Combined_Speaker slaves=Upstairs_Living_room_speaker_RTP_sink,Liams_Office_speaker_RTP_sink,Liams_Bedroom_speaker_RTP_sink")


