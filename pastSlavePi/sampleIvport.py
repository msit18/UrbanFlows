#!/usr/bin/env python
import time 
from datetime import datetime

def mockCam():
	SystemNum = "Sys1" #+ str(1)
	for i in range (1,5):
		currentTime = datetime.now()
		final = str(currentTime) + "_camera%d_" %i + str(SystemNum)
		print final

def NinetyShots(SysNum):
	SystemNum = "Sys" + str(SysNum)
	shots = 1
	cameraNum = 1
	while (shots < 90):
		timeStamp = datetime.now()
		imgName = str(SystemNum) + "_camera" + str(cameraNum) + "_" + str(timeStamp)
		print imgName
		#update values
		shots += 1
		cameraNum += 1
		if (cameraNum > 4):
			cameraNum = 1

def filenames(SysNum):
	frames = 90
	frame = 0
	SystemNum = "Sys" + str(SysNum)
	global cam
	cam = 1

	while frame < frames:
		time.sleep(0.007)   # SD Card Bandwidth Correction Delay
		#cam_change()        # Switching Camera
		time.sleep(0.007)   # SD Card Bandwidth Correction Delay
		timeStamp = datetime.now()
		#yield 'image%02d.jpg' % frame
		yield str(SystemNum) + "_camera" + str(cam) + "_" + str(timeStamp)
		frame += 1
		cam += 1
		if cam > 4:
			cam = 1

if __name__ == '__main__':
	print (filenames(1))
	for i in filenames(1):
		print(i)
