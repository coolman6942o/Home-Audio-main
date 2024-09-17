#!/bin/bash

# Update and upgrade system
apt update && apt upgrade -y

# Install dependencies for Python and system tools
apt install -y build-essential libssl-dev zlib1g-dev libbz2-dev \
libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
xz-utils tk-dev libffi-dev liblzma-dev python-openssl git cargo \
pactl pulseaudio ffmpeg pipewire pipewire-pulse libasound2-dev

# Install pyenv to manage Python versions
curl https://pyenv.run | bash

# Add pyenv to bash so it loads automatically
echo -e '\nexport PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.bashrc
echo -e 'eval "$(pyenv init --path)"' >> ~/.bashrc
echo -e 'eval "$(pyenv init -)"' >> ~/.bashrc
echo -e 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc

# Source bashrc to load pyenv
source ~/.bashrc

# Install latest Python version using pyenv
latest_python_version=$(pyenv install --list | grep -v - | tail -1)
pyenv install $latest_python_version
pyenv global $latest_python_version

# Create a virtual environment
python -m venv ~/python_venv

# Activate virtual environment
source ~/python_venv/bin/activate

# Install default Python packages
pip install --upgrade pip setuptools wheel

# Restart pipewire services to ensure everything works properly
systemctl --user daemon-reload
systemctl --user restart pipewire pipewire-pulse

echo "System setup completed. Now setting up Home-Audio project."

# Clone the Home-Audio repository
git clone https://github.com/coolman6942o/Home-Audio-main.git
cd Home-Audio-main

# Run another system update/upgrade just in case (optional, since it was done earlier)
apt update -y && apt upgrade -y

# Build the Librespot project
cd librespot
cargo build --release

# Go back to the Home-Audio main directory and start the cast script
cd ../cast

# Run the Python script
python run.py

echo "Home-Audio setup completed."
