#!/bin/bash

#Written by Michelle Sit
#Triggers the video taking sequence in each of the slavePies

echo;

sshpass -p 'raspberry' ssh pi@10.0.0.2 /home/pi/takeVideo.sh & sshpass -p 'raspberry' ssh pi@10.0.0.3 /home/pi/takeVideo.sh & sshpass -p 'raspberry' ssh pi@10.0.0.4 /home/pi/takeVideo.sh & sshpass -p 'raspberry' ssh pi@10.0.0.5 /home/pi/takeVideo.sh;

done
