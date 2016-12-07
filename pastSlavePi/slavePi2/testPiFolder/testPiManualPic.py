#/!/usr/bin/python

#Written by Michelle Sit

#Edited from manualPic3.py to take arguments from readPiFace.py.  Takes pictures on one thread and on another thread
#moves/removes them to the MasterPi.  Picture resolution, fps, and time is controlled by the inputs from the MasterPi piface
#Sends errors to flash.py on the MasterPi

#Update: also provides updates every twenty minutes (CURRENTLY SET TO EVERY 10 MINUTES) on the program's fps progress while the program is running

#sys.argv[1] = totalTime duration (in seconds)
#sys.argv[2] = resolution width
#sys.argv[3] = resolution height
#sys.argv[4] = number of pictures to take (fps)
#sys.argv[5] = time interval (seconds) for frames to be taken in (fps)
#sys.argv[6] = framerate of picamera

import time
import picamera
import datetime
import os
import string
import sys
import numpy as np

#Takes pictures based inputted fps options (while loops control total run time and how many pictures are taken in the specified time frame (fps).
#Time is also updated on each run through)

def run ():
	resW = int(sys.argv[2])
	resH = int(sys.argv[3])
	numPics = int(sys.argv[4])
	timeInterval = int(sys.argv[5])
	frameRate = int(sys.argv[6])

	timeStart = time.time() #When the program began
	totalTimeSec = int(sys.argv[1])
	totalTimeMin = int(sys.argv[1])/60
	timeNow = time.time() #Used to keep track of current time
	timeEnd = totalTimeSec+timeNow #When the program ends
	timePlusInt = timeNow #Keeps track of time increments

	timePlusTwentyMins = timeNow+300

	print >>f, "Capturing {0}p for a total time of {1} min ({2} secs) at {3} frames per {4} second (({5} mins) at {6} framerate "\
		.format(str(resH), str(totalTimeMin), str(totalTimeSec), str(numPics), str(timeInterval), str(float(timeInterval/60)), str(frameRate) )
	print >>f, "TimePlusTwenty = {0}".format(str(timePlusTwentyMins) )

	numPicArray = []

	while timeNow < timePlusTwentyMins and timeNow < timeEnd:
		timeNow = time.time()
		if timeNow >= timePlusTwentyMins:
			endTwenty = time.time()
			twentyTime = endTwenty-timeStart
			twentyFPS = sum(numPicArray)/twentyTime
			print >>f, "10.2 Five Min Update: Total number of pictures is {0}, total time elapsed is {1}, totalFPS is {2}".format(str(sum(numPicArray)), str(twentyTime), str(twentyFPS) )
			timePlusTwentyMins = time.time()+300
		else:
			while timeNow > timePlusInt:
				timePlusInt = timeNow + timeInterval
				start=time.time()
				with picamera.PiCamera() as camera:
					camera.resolution = (resW, resH)
					camera.framerate = frameRate
					camera.capture_sequence([
						datetime.datetime.now().strftime ('%H%M%S%f') + '.jpg'
						for i in range(numPics)
						], use_video_port=True)
				finish = time.time()
				#Analyzing time and frames
				fpsTime = (finish-start)
				fps = numPics/fpsTime
				numPicArray.append(numPics)
				print >>f, 'Captured {0} frames at {1}fps in {2}secs'.format( str(sum(numPicArray)), str(numPics/(finish-start)), str(finish-start))
	endTime = time.time()
	totalTime = endTime-timeStart
	totalFPS = sum(numPicArray)/totalTime
	print >>f, "10.2: Captured {0} total pictures.  Total time was {1}, total FPS is {2}".format(str(sum(numPicArray)), str(totalTime), str(totalFPS) )
	with open("master.txt", 'a') as myfile:
		myfile.write("{0}TotalPictures {1}totalFps {2}totalTime {3}frames {4}p\n".format(str(sum(numPicArray)), str(totalFPS), str(totalTime), str(numPics), str(resH)))
	camera.close()
	f.close()

if __name__ == '__main__':
	f = open('{0}p_{1}fps_FR{2}_PRGMLOG.txt'.format(sys.argv[3], sys.argv[4], sys.argv[6]), 'w')
	run()