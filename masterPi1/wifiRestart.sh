#!/bin/bash
#Test it several times and figure out how to deal with the stalling problem
COUNT=0

while [ $COUNT -lt 4 ] ; do
	python /home/pi/flash.py wifiConnect
	if ping -c 4 google.com | grep '64 bytes'; then
		echo "found"
		python /home/pi/sysinfo2.py
		python3 /home/pi/readPiFace4.py
		COUNT=8
	else
		if [ $COUNT -lt 2 ] ; then
			sudo ifdown wlan0
			sudo ifup wlan0
			COUNT=$((COUNT+1))
			echo "not found"
			echo $COUNT
		else
			echo "else running"
			python /home/pi/flash.py wifiError
			python3 /home/pi/readPiFace4.py
			COUNT=8
		fi
	fi
done
