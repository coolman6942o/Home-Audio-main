# Home-Audio-
Multi Zone home audio controller
## BOOM 3 [Liam's] EC:81:93:76:EE:83 | Liams Office

### Spotify
- librespot -n "Liams Office [Main]" -b 320

- ### Server ###
    ```
    pactl load-module module-null-sink sink_name=Liams_Office_speaker_RTP_sink sink_properties=device.description="Liams_Office_[Main]"
    
    ffmpeg -f pulse -i Liams_Office_speaker_RTP_sink.monitor -ac 2 -ar 48000  -f rtp rtp://192.168.0.127:5000 
    ```
- ### Raspberry Pi ###

    - **RTP config**
        -  Note: The IP4 127.0.0.1 DONT TOUCH | Change the ip in c=IN IP4 192.168.0.127 to the Rpi4 ipaddress 
        ```
        v=0
        o=- 0 0 IN IP4 127.0.0.1
        s=No Name
        c=IN IP4 192.168.0.127
        t=0 0
        a=tool:libavformat 58.76.100
        m=audio 5000 RTP/AVP 97
        b=AS:768
        a=rtpmap:97 PCMU/48000/2

        ```
    - Execute
        ```
        ffplay -protocol_whitelist "file,udp,rtp" -i stream.sdp
        ```

## BOOM 3 [Mums] EC:81:93:74:97:B7 | Upstairs Living Room

### Spotify ###
```
librespot -n "Upstairs Living Room [Main]" -b 320 --format S16
```

- ### Server ###
    ```
    pactl load-module module-null-sink sink_name=Upstairs_Living_room_speaker_RTP_sink sink_properties=device.description="Upstairs_Living_Room_[Main]"
    ```
    ```
    ffmpeg -f pulse -i Upstairs_Living_room_speaker_RTP_sink.monitor -ac 2 -ar 48000 -f rtp rtp://192.168.0.106:5001
    ```
- ### Raspberry Pi ###

    - **RTP config**
        - Note: The IP4 127.0.0.1 DONT TOUCH | Change the ip in c=IN IP4 192.168.0.106 to the Rpi4 ipaddress 
        ```
        v=0 192.168.0.108 to the Rpi4 ipaddress 
        o=- 0 0 IN IP4 127.0.0.1
        s=No Name
        c=IN IP4 192.168.0.106
        t=0 0
        a=tool:libavformat 58.76.100
        m=audio 5001 RTP/AVP 97
        b=AS:768
        a=rtpmap:97 PCMU/48000/2
        ```
    - **Execute**
        ```
        ffplay -protocol_whitelist "file,udp,rtp" -i stream.sdp
        ```
## JBL Horizon B8:D5:0B:17:74:14 | Liam's Bedroom

### Spotify
```
librespot -n "Liams Bedroom [Main]" -b 320
```
- ### Server ###
    ```
    pactl load-module module-null-sink sink_name=Liams_Bedroom_speaker_RTP_sink sink_properties=device.description="Liams_Bedroom_[Main]"

    ```

    ```
    ffmpeg -f pulse -i Liams_Bedroom_speaker_RTP_sink.monitor -ac 2 -ar 48000 -f rtp rtp://192.168.0.74:5004
   
    ```  
- ### Raspberry Pi ###

    - **RTP config**
        - Note: The IP4 127.0.0.1 DONT TOUCH | Change the ip in c=IN IP4 192.168.0.107 to the Rpi4 ipaddress 
        ```
        v=0 192.168.0.108 to the Rpi4 ipaddress 
        o=- 0 0 IN IP4 127.0.0.1
        s=No Name
        c=IN IP4 192.168.0.74
        t=0 0
        a=tool:libavformat 58.76.100
        m=audio 5004 RTP/AVP 97
        b=AS:768
        a=rtpmap:97 PCMU/48000/2
        ```
    - **Execute**
        ```
        ffplay -protocol_whitelist "file,udp,rtp" -i stream.sdp
        ```



# Instrunctions

- **STEP 1** :
    - Execute the Spotify Connect command for each zone
- **STEP 2** :
    - Create a virtual null sink device for each zone
- **STEP 3** : 
    - Create a ffmpeg rtp command to the zone Pi 
        # Note
            make sure that you are have exacuted the command ffplay on the pi 
- **STEP 4 [PARTY MODE]** :
    - when joing more then one out put device exacute this command
    ## PARTY [EXAMPLE] Upstairs_Living_room_speaker_RTP_sink + Liams_Office_speaker_RTP_sink : 
    ```
    pactl load-module module-combine-sink sink_name=Combined_Speaker slaves=Upstairs_Living_room_speaker_RTP_sink,Liams_Office_speaker_RTP_sink
    ```

    ## PARTY [EXAMPLE] All Zones : 
    ```
    pactl load-module module-combine-sink sink_name=Combined_Speaker slaves=Upstairs_Living_room_speaker_RTP_sink,Liams_Office_speaker_RTP_sink, Liams_Bedroom_speaker_RTP_sink
    ```

    ## PARTY [EXAMPLE] Upstairs_Living_room_speaker_RTP_sink + Liams_Bedroom_speaker_RTP_sink: 
    ```
    pactl load-module module-combine-sink sink_name=Combined_Speaker slaves=Upstairs_Living_room_speaker_RTP_sink,Liams_Bedroom_speaker_RTP_sink
    ```
    ### PARTY [EXAMPLE] Liams_Bedroom_speaker_RTP_sink + Liams_Office_speaker_RTP_sink: 
    ```
    pactl load-module module-combine-sink sink_name=Combined_Speaker slaves=Liams_Bedroom_speaker_RTP_sink,Liams_Office_speaker_RTP_sink
    ```

    ### PARTY [EXAMPLE] Upstairs_Living_room_speaker_RTP_sink + Liams_Office_speaker_RTP_sink + Liams_Bedroom_speaker_RTP_sink: 
    ```
    pactl load-module module-combine-sink sink_name=Combined_Speaker slaves=Upstairs_Living_room_speaker_RTP_sink,Liams_Office_speaker_RTP_sink,Liams_Bedroom_speaker_RTP_sink 
    ```





