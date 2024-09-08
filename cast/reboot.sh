#!/bin/bash
pulseaudio -k && pulseaudio --start
pkill librespot
systemctl --user restart pipewire
systemctl --user restart pipewire-pulse

pkill ffplay
pkill spotify
/home/liam/Downloads/Home-Audio-main/venv/bin/python /home/liam/Downloads/Home-Audio-main/cast/run.py
spotify