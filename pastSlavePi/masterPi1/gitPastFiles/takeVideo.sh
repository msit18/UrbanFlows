#!/bin/bash

#Written by Michelle Sit
#Takes a video and sends it to the masterPi

DATE=$(date "+%Y_%m_%d_%H_%M_%2S_%3N")
echo;

raspivid -o /home/pi/$DATE.h264 -t 60000 -w 640 -h 480;

sshpass -p 'raspberry' scp /home/pi/$DATE.h264 pi@10.0.0.1:/home/pi/;

done
