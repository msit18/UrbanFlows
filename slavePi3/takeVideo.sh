#!/bin/bash

#Written by Michelle Sit
#Takes video, sends it to the MasterPi, and sends a finished msg to flash.py

DATE=$(date "+%Y_%m_%d_%H_%M_%2S_%3N")
echo;

raspivid -o /home/pi/$DATE.h264 -t 10000 -w 1920 -h 1080;

sshpass -p 'raspberry' scp /home/pi/$DATE.h264 pi@10.0.0.1:/home/pi/;

sshpass -p 'raspberry' ssh pi@10.0.0.1 python flash.py fin

done
