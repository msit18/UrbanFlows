#!/bin/bash

echo "uploading..."
# while true
# do
/usr/bin/flock --nonblock --wait 5 /tmp/fcj.lockfile python /home/pi/UrbanFlows/slavePi/uploadScript.py $1 $2
# done
