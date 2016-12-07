#!/bin/bash

DATE=$(date "+%Y-%m-%d_%H:%M:%2S:%3N")

#takes images
for i in $(seq 5);
do $(raspistill -t 1 -vf -hf -o /home/pi/$DATE.jpg);
#raspistill -t 1 -vf -hf -o /home/pi/$DATE.jpg;

echo $DATE;
echo "pi4";
#move file to masterPi
sshpass -p 'raspberry' scp /home/pi/$DATE.jpg pi@10.0.0.1:/home/pi/;

#echo 'transfered files!';

DATE=$(date "+%Y-%m-%d_%H:%M:%2S:%3N")


done
