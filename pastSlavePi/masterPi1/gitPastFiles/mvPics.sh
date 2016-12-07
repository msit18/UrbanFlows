#/!/bin/bash

#Written by Michelle Sit
#Triggers all moveFiles in the slavePies.  Moves all picture files in the home/specified folder and move them to the MasterPi

echo "MasterPi moving files bash script";
date "+%H:%M:%2S:%3N";

sshpass -p 'raspberry' ssh pi@10.0.0.2 /home/pi/moveFiles.sh & sshpass -p 'raspberry' ssh pi@10.0.0.3 /home/pi/moveFiles.sh & sshpass -p 'raspberry' ssh pi@10.0.0.4 /home/pi/moveFiles.sh & sshpass -p 'raspberry' ssh pi@10.0.0.5 /home/pi/moveFiles.sh;

echo "MasterPi finish moving files";
date "+%H:%M:%2S:%3N";

done
