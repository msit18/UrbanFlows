#/!/bin/bash
#Restarts wifi if wifi is down and Pi is connected by ethernet

#Written by Michelle Sit

sudo ifdown eth0
sudo ifdown wlan0
sudo ifup wlan0
sudo ifup eth0
