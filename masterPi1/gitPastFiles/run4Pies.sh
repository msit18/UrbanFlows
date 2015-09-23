#!/bin/bash

#Written by Michelle Sit
#Triggers the picture taking sequence in each of the slavePies.  Beginning and ending times are printed to check how long the execution time is.

echo "Date on MasterPi";
date "+%H:%M:%2S:%3N";

sshpass -p 'raspberry' ssh pi@10.0.0.2 python /home/pi/picThread6.py & sshpass -p 'raspberry' ssh pi@10.0.0.3 python /home/pi/picThread6.py & sshpass -p 'raspberry' ssh pi@10.0.0.4 python /home/pi/picThread6.py & sshpass -p 'raspberry' ssh pi@10.0.0.5 python /home/pi/picThread6.py;

echo "End date on MasterPi";
date "+%H:%M:%2S:%3N";

done
