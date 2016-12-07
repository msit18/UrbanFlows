#!/bin/bash

DATE=$(date "+%Y-%m-%d_%H_%M_%2S_%3N")

#takes images
for i in $(seq 5);
do $(raspistill -t 1 -vf -hf -o /home/pi/$DATE.jpg);
#raspistill -t 1 -vf -hf -o /home/pi/$DATE.jpg;

echo $DATE;

#move file to masterPi
#sshpass -p 'raspberry' scp /home/pi/*.jpg pi@10.0.0.1:/home/pi/;

DATE=$(date "+%Y-%m-%d_%H_%M_%2S_%3N")


done
