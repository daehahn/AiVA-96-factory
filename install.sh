#!/bin/bash
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install -y python3 vim audacity
sudo apt install -y python3-pip
#python3 -m pip install --upgrade pip
sudo apt-get install python3-setuptools
pip3 install setuptools --upgrade
pip3 install wheel
pip3 install pyusb
pip3 install pyqt5
pip3 install pyserial

# 단축 아이콘 복사
sudo cp shortcuts/*.desktop /usr/share/applications/
sudo cp shortcuts/*.desktop ~/바탕화면
sudo chmod 755 ~/바탕화면/*.desktop
sudo cp rules/*  /etc/udev/rules.d/

echo "cd /home/roy/workspace/utils/XMOS/xTIMEcomposer/Community_14.3.1" | tee -a ~/.bashrc > /dev/null
echo "source ./SetEnv" | tee -a ~/.bashrc > /dev/null
echo "cd ~" | tee -a ~/.bashrc > /dev/null
echo "PATH=$PATH:~/workspace/utils/XMOS/xTIMEcomposer/Community_14.3.1/bin" | tee -a ~/.bashrc > /dev/null

while [[ -z $IsReboot ]] ; do
    echo ""
    echo ""
    echo "====================================="
    echo "Type yes, reboot the system"
    echo "====================================="
    read IsReboot
done

if [ ${IsReboot,,} == "yes" ]; then
    sudo shutdown -r
fi

