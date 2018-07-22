#!/bin/bash

RHOST="###IPADDR####"
RPORT="22"

### You shouldn't touch anything below ###

RUSER="homeassistant"
RDIR="/home/homeassistant/vacuum/"
SSHCTL="/root/.ssh/ctl-ha-rockrobo"

while true; do
    if $(ls /run/shm/navmap*.ppm 1> /dev/null 2>&1) && $(ls /run/shm/SLAM_fprintf.log 1> /dev/null 2>&1); then
        # If the robot is moving then set the SSH control path session and sync files as fast as possible
        if ! [ -e ${SSHCTL} ]; then
            ssh -p ${RPORT} -qnNf -o ControlMaster=yes -o ControlPath="${SSHCTL}" ${RUSER}@${RHOST}
        fi
        # rsync will handle sparse files to let navmaps be transferred quickier
        rsync -cqrlDS -e "ssh -p ${RPORT} -o 'ControlPath=${SSHCTL}'" --timeout 10 --include="navmap*.ppm" --include="SLAM_fprintf.log" --exclude="*" /run/shm/ ${RUSER}@${RHOST}:${RDIR}
    else
        # If the robot isn't moving then exit from the SSH control path session (if exists) and sleep waiting for the next loop
        if [ -e ${SSHCTL} ]; then
            ssh -p ${RPORT} -qO exit -o ControlPath="${SSHCTL}" ${RUSER}@${RHOST}
        fi
        sleep 5 
    fi
done
