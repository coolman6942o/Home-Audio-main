#from main import *
from fixed import *  
import os 

run_librespot_processes_in_background()
create_virtual_audio_sources()
run_ffmpeg_processes_in_background()
#os.system("bluetoothctl connect 5C:C1:D7:ED:68:EF")
#time.sleep(1)
#os.system("pactl load-module module-combine-sink sink_name=Combined_Speaker slaves=Upstairs_Living_room_speaker_RTP_sink,Liams_Office_speaker_RTP_sink,Liams_Bedroom_speaker_RTP_sink,bluez_output.5C_C1_D7_ED_68_EF.1")
os.system("pactl load-module module-combine-sink sink_name=Combined_Speaker slaves=Upstairs_Living_room_speaker_RTP_sink,Liams_Office_speaker_RTP_sink,Liams_Bedroom_speaker_RTP_sink")



     