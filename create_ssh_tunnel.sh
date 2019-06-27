#!/bin/bash
REVERSE_SSH_PORT=50000
createTunnel() {
	sshpass -p '12142448@Nome' ssh -N -R $REVERSE_SSH_PORT:localhost:22 isgreen@isgreen.no-ip.org 
  if [[ $? -eq 0 ]]; then
    echo Tunnel to jumpbox created successfully
  else
    echo An error occurred creating a tunnel to jumpbox. RC was $?
  fi
}
/bin/pidof ssh
if [[ $? -ne 0 ]]; then
  echo Creating new tunnel connection
  createTunnel
fi

