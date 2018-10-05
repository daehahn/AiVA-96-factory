#!/bin/bash
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install python3
sudo apt install -y python3-pip
#python3 -m pip install --upgrade pip
sudo apt-get install python3-setuptools
pip3 install setuptools --upgrade
pip3 install wheel
pip3 install pyusb
pip3 install pyqt5
