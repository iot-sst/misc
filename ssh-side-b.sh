#!/bin/bash

sudo pacman --noconfirm -S sshpass glibc
wget https://iot-sst.github.io/misc/ilstunnelsshB.service
sudo mv ./ilstunnelsshB.service /etc/systemd/system/ilstunnelssh.service
sudo systemctl start ilstunnelssh
sudo systemctl enable ilstunnelssh

