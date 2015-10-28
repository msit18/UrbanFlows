#/!/usr/bin/python

#Written by Michelle Sit

#Edited from manualPic4.py to take arguments from readPiFace.py.  Takes pictures on
#one thread and on another thread moves/removes them to the MasterPi.  Picture resolution,
#fps, and time is controlled by the inputs from the MasterPi piface
#Sends errors to flash.py on the MasterPi

#Update: also provides updates every twenty minutes (CURRENTLY SET TO EVERY 10 MINUTES) on
#the program's fps progress while the program is running

#sys.argv[1] = totalTime duration (in seconds)
#sys.argv[2] = resolution width
#sys.argv[3] = resolution height
#sys.argv[4] = number of pictures to take (fps)
#sys.argv[5] = time interval (seconds) for frames to be taken in (fps)
#sys.argv[6] = framerate of picamera

import time
import threading
import Queue
import picamera
import datetime
import glob
import os
import string
import sys
import numpy as np
import RPi.GPIO as gp

#Setup for the pi camera, taken from the 'ivport_capture_sequence_A.py' file
gp.setwarnings(False)
gp.setmode(gp.BOARD)

gp.setup(7, gp.OUT)
gp.setup(11, gp.OUT)
gp.setup(12, gp.OUT)

gp.output(7, False)
gp.output(11, False)
gp.output(12, True)

#More for testing purposes for now; number of pictures to be taken. 
frames = 30

#Begins the camera on picamera 1
cam = 1

#Switches cameras. Taken from 'ivport_capture_sequence_A.py'
#ACTUAL PORTS FOR THE PI CAMERAS TBD 
def cam_change():
	global cam
	gp.setmode(gp.BOARD)
	if cam == 1:
	        # CAM 1 for A Jumper Setting
	        #first output number was first 7
	        gp.output(7, False)
	        gp.output(11, False)
	        gp.output(12, True)
	elif cam == 2:
	        # CAM 2 for A Jumper Setting
	        gp.output(7, True)
	        gp.output(11, False)
	        gp.output(12, True)
	elif cam == 3:
	    	# CAM 3 for A Jumper Setting
	        gp.output(7, False)
	        gp.output(11, True)
	        gp.output(12, False)
	elif cam == 4:
	        # CAM 4 for A Jumper Setting
	        gp.output(7, True)
	        gp.output(11, True)
	        gp.output(12, False)
	cam += 1
	if cam > 4:
		cam = 1

	#Changes cameras and names the written files; SHOULD BE MORE SUBSTANTIVELY NAMED. 
def filenames():
    	frame = 0
	while frame < frames:
		time.sleep(0.007)    # SD Card Bandwidth Correction Delay,
		cam_change()        # Switching Camera
        	time.sleep(0.007)   # SD Card Bandwidth Correction Delay
        	yield 'image%02d.jpg' % frame
        	frame += 1
        	
# Multiplexer architecture capturing sequence
with picamera.PiCamera() as camera:
	camera.resolution = (640, 480)
	#How quickly pictures will be taken
	camera.framerate = 30
	camera.start_preview()

	# Optional Camera LED OFF
	#gp.setmode(gp.BCM)
	#camera.led = False

	time.sleep(2)    # Camera Initialize
	startTime = time.time()
	camera.capture_sequence(filenames(), use_video_port=True)
	finishTime = time.time()
	timeRan = finishTime - startTime
	print 'Captured %d frames at total %.2ffps' % (frames, frames / timeRan)
	print 'Finished running in %.02f seconds' % timeRan
        


#Takes pictures based inputted fps options (while loops control total run time and how many 
#pictures are taken in the specified time frame (fps).

#Time is also updated on each run through)
class takePictures(threading.Thread):
	def __init__(self, queue, f):
		threading.Thread.__init__(self)
		self.queue = queue
		self.f = f

	def run (self):
		try:
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

			timePlusTwentyMins = timeNow+600

			print >>self.f, "Capturing {0}p for a total time of {1} min ({2} secs) at {3} "\
			"frames per {4} second (({5} mins) at {6} framerate ".format(str(resH), \
				str(totalTimeMin), str(totalTimeSec), str(numPics), str(timeInterval), \
				str(float(timeInterval/60)), str(frameRate) )
			print >>self.f, "TimePlusTwenty = {0}".format(str(timePlusTwentyMins) )

			numPicArray = []
			fpsArray = []
			timeAvg = []

			#This outerloop checks to make sure the whole taking pictures time frame doesn't
			#go over the specified time limit (timeNow < timeEnd)
			#(timeNow < timePlusTwentyMins) also checks to make sure the process doesn't end
			#before the end of the last camera cycle (I think?)
			while timeNow < timePlusTwentyMins and timeNow < timeEnd:
				#takes the current time at the beginning of each loop to check in statements
				timeNow = time.time()
				#This process outprints statements every 20 mins (currently set to something
				#faster for testing purposes)
				if timeNow >= timePlusTwentyMins:
					endTwenty = time.time()
					twentyTime = endTwenty-timeStart
					twentyFPS = sum(numPicArray)/twentyTime
					print >>self.f, "10.2 Twenty Min Update: Total number of pictures is {0},"\
					" total time elapsed is {1}, totalFPS is {2}".format(str(sum(numPicArray)),\
					 str(twentyTime), str(twentyFPS) )
					timePlusTwentyMins = time.time()+600
				else:
					#This loop ensures that pictures are taken within the time frame
					#To make sure the processes are running at xfps, the camera cannot take pictures
					#before the start of the next appropriate time (ex - 3 frames per 5 seconds.  Cannot
					#take 3 frames whenever the process finishes.  It has to wait until 5 seconds have
					#passed)
					#For the multiplexer, this is an important factor that I can explain next time
					#we meet.  tl;dr: the four cameras have to take simultaneous pictures so the loop
					#needs to take that into consideration.
					while timeNow > timePlusInt:
						timePlusInt = timeNow + timeInterval
						start=time.time()
						with picamera.PiCamera() as camera:
							camera.resolution = (resW, resH)
							camera.framerate = frameRate
							camera.capture_sequence([
								datetime.datetime.now().strftime ('%d-%m-%Y-%H_%M_%S_%f') + '_TT'\
								 + str(sys.argv[1]) + '_RES' + str(resH) + '_PIC' + str(numPics) +\
								  '_TI' + str(timeInterval) + '_FR' + str(frameRate) + '.jpg'
								for i in range(numPics)
								], use_video_port=True)
						finish = time.time()
						#Analyzing time and frames
						fpsTime = (finish-start)
						fps = numPics/fpsTime
						numPicArray.append(numPics)
						fpsArray.append(fps)
						timeAvg.append(fpsTime)
						print >>self.f, 'Captured {0} frames at {1}fps in {2}secs'\
						.format( str(sum(numPicArray)), str(numPics/(finish-start)), str(finish-start))
						self.queue.put('beginT2')
			endTime = time.time()
			totalTime = endTime-timeStart
			totalFPS = sum(numPicArray)/totalTime
			print >>self.f, "10.2: Captured {0} total pictures.  Total time was {1}, total FPS is {2}"\
			.format(str(sum(numPicArray)), str(totalTime), str(totalFPS) )
			camera.close()
			self.queue.put('T1closeT2')
		except (picamera.exc.PiCameraError, picamera.exc.PiCameraMMALError):
			print >>self.f, "PiCameraError or MMALError"
			self.queue.put('exit')
			time.sleep(1)
			os.system("sshpass -p 'raspberry' ssh pi@10.0.0.1 -o StrictHostKeyChecking=no python"\
			"flash.py camError 2")
		except:
			print >>self.f, "other error"
			self.queue.put('exit')
			time.sleep(1)
			os.system("sshpass -p 'raspberry' ssh pi@10.0.0.1 -o StrictHostKeyChecking=no python"\
			" flash.py error 2")


#Checks to see if any pictures have been taken and moves/removes them to the MasterPi
#Checks the folder to see if there are any pictures, sends that group to the MasterPi, removes them,
#checks again, repeat picsList is an arrray, list is a string
class queuePictures(threading.Thread):
	def __init__(self, queue, f):
		threading.Thread.__init__(self)
		self.queue = queue
		self.f = f

	def run (self):
		list = ""
		while True:
			runThread = self.queue.get()
			if runThread is 'beginT2':
				picsList = glob.glob('*.jpg')
				pass
#				while len(picsList) > 0:
#					list = ' '.join(picsList)
#					print (list)
#					os.system("sshpass -p 'raspberry' scp -o StrictHostKeyChecking=no {0}"\
#					" pi@10.0.0.1:/home/pi/pastImages/".format(list) )
#					os.system("rm {0}".format(list) )
#					picsList = []
			elif runThread is 'T1closeT2':
				print >>self.f, '10.2: T2 recieved close message'
#				self.f.close()
				break
			elif runThread is 'exit':
				print >>self.f, "10.2 broken"
#				self.f.close()
				break

if __name__ == '__main__':
	#queue = Queue.Queue()
	#f = open('manualPic5Output.txt', 'w')
	#t1 = takePictures(queue, f)
	#t2 = queuePictures(queue, f)
	#t1.start()
	#t2.start()
	pass
