#!/bin/bash

sudo pacman --noconfirm -Syy sshpass glibc
wget https://iot-sst.github.io/misc/supervisor.py
wget https://iot-sst.github.io/misc/ilstunnelssh.service
sudo mv ./ilstunnelssh.service /etc/systemd/system/ilstunnelssh.service
sudo systemctl start ilstunnelssh
sudo systemctl enable ilstunnelssh

