#!/bin/bash

#Written by Michelle Sit
#Moves all picture files in the immediate floor to the MasterPi

sshpass -p 'raspberry' scp *.jpg pi@10.0.0.1:/home/pi/
