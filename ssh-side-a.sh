#!/bin/bash

sudo pacman --noconfirm -S sshpass glibc
wget https://iot-sst.github.io/misc/ilstunnelsshA.service
sudo mv ./ilstunnelsshA.service /etc/systemd/system/ilstunnelssh.service
sudo systemctl start ilstunnelssh
sudo systemctl enable ilstunnelssh

