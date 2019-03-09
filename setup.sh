#!/bin/bash

apt-get -y update
apt-get -y dist-upgrade
apt-get -y install sshfs
apt-get -y install python3-pip
apt-get -y install python3-lxml
pip3 install spidev
pip3 install RPi.GPIO
mkdir ngsct
cd ngsct/
git clone https://github.com/vicdelacruz/sct.git
cd sct
git checkout dev
python3 setup.py install
