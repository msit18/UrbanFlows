#/!/bin/bash

#Written by Michelle Sit
#Triggers removePics on all slavePies.  Removes all jpg files from the home/specified folder
#TODO: Needs to be changed to reflect current folders

sshpass -p 'raspberry' ssh pi@10.0.0.2 /home/pi/removePics.sh & sshpass -p 'raspberry' ssh pi@10.0.0.3 /home/pi/removePics.sh & sshpass -p 'raspberry' ssh pi@10.0.0.4 /home/pi/removePics.sh & sshpass -p 'raspberry' ssh pi@10.0.0.5 /home/pi/removePics.sh;

done
