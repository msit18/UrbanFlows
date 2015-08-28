#!/bin/bash

#Written by Michelle Sit
#Uses raspistill to take a picture (can be customized to take multiple pictures of a period of specified time and different resolutions).  Sends the image to the MasterPi

DATE=$(date "+%Y-%m-%d_%H:%M:%2S:%3N")

#takes images
for i in $(seq 5);
do $(raspistill -t 1 -vf -hf -o /home/pi/$DATE.jpg);
#raspistill -t 1 -vf -hf -o /home/pi/$DATE.jpg;

echo $DATE;

#move file to masterPi
sshpass -p 'raspberry' scp /home/pi/$DATE.jpg pi@10.0.0.1:/home/pi/;

#echo 'transfered files!';

DATE=$(date "+%Y-%m-%d_%H:%M:%2S:%3N")


done
