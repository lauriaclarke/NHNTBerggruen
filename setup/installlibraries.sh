#! usr/bin/bash

echo "-------------------------------------------"
echo "INSTALLING LIBRARIES for NHNT"
echo "-------------------------------------------"

echo "-------------------------------------------"
echo "updating system: "
sudo apt update
sudo apt upgrade -y

# echo "-------------------------------------------"
# echo "librosa dependencies: "
# sudo apt-get install make build-essential libportaudio0 libportaudio2 libportaudiocpp0 portaudio19-dev libatlas-base-dev -y
# sudo apt install software-properties-common -y
# sudo apt install libatlas3-base libgfortran5 -y
# sudo pip3 install scipy==1.7.3
# sudo apt install libblas-dev llvm llvm-dev -y
# export LLVM_CONFIG=/usr/bin/llvm-config
# pip3 install llvmlite
# pip3 install numba
# pip3 install librosa
# pip3 install numpy==1.23.0
                                                  
echo "-------------------------------------------"
echo "the rest: "
pip3 install ggwave
# pip3 install gtts
pip3 install sounddevice
pip3 install audio2numpy
pip3 install pyyaml
pip3 install openai
# pip3 install pyttsx3
# pip3 install pydub

echo "-------------------------------------------"
echo "linux installs: "
sudo apt install vim -y
# sudo apt install ffmpeg -y
sudo apt install git -y
# sudo apt install espeak

echo "-------------------------------------------"
echo "i2s microphone setup: "
cd ~
sudo pip3 install --upgrade adafruit-python-shell
wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/i2smic.py
sudo python3 i2smic.py

echo "please reboot now"
