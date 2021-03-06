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
import threading
import Queue
import picamera
import datetime
import glob
import os
import string
import sys
import numpy as np

#Takes pictures based inputted fps options (while loops control total run time and how many pictures are taken in the specified time frame (fps).
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

			print >>self.f, "Capturing {0}p for a total time of {1} min ({2} secs) at {3} frames per {4} second (({5} mins) at {6} framerate "\
				.format(str(resH), str(totalTimeMin), str(totalTimeSec), str(numPics), str(timeInterval), str(float(timeInterval/60)), str(frameRate) )
			print >>self.f, "TimePlusTwenty = {0}".format(str(timePlusTwentyMins) )

			numPicArray = []
			fpsArray = []
			timeAvg = []

			while timeNow < timePlusTwentyMins and timeNow < timeEnd:
				timeNow = time.time()
				if timeNow >= timePlusTwentyMins:
					endTwenty = time.time()
					twentyTime = endTwenty-timeStart
					twentyFPS = sum(numPicArray)/twentyTime
					print >>self.f, "10.2 Twenty Min Update: Total number of pictures is {0}, total time elapsed is {1}, totalFPS is {2}".format(str(sum(numPicArray)), str(twentyTime), str(twentyFPS) )
					timePlusTwentyMins = time.time()+600
				else:
					while timeNow > timePlusInt:
						timePlusInt = timeNow + timeInterval
						start=time.time()
						with picamera.PiCamera() as camera:
							camera.resolution = (resW, resH)
							camera.framerate = frameRate
							camera.capture_sequence([
								datetime.datetime.now().strftime ('%d-%m-%Y-%H_%M_%S_%f') + '_TT' + str(sys.argv[1]) + '_RES' + str(resH) + '_PIC'\
												 + str(numPics) + '_TI' + str(timeInterval) + '_FR' + str(frameRate) + '.jpg'
								for i in range(numPics)
								], use_video_port=True)
						finish = time.time()
						#Analyzing time and frames
						fpsTime = (finish-start)
						fps = numPics/fpsTime
						numPicArray.append(numPics)
						fpsArray.append(fps)
						timeAvg.append(fpsTime)
						print >>self.f, 'Captured {0} frames at {1}fps in {2}secs'.format( str(sum(numPicArray)), str(numPics/(finish-start)), str(finish-start))
						self.queue.put('beginT2')
			endTime = time.time()
			totalTime = endTime-timeStart
			totalFPS = sum(numPicArray)/totalTime
			print >>self.f, "10.2: Captured {0} total pictures.  Total time was {1}, total FPS is {2}".format(str(sum(numPicArray)), str(totalTime), str(totalFPS) )
			camera.close()
			self.queue.put('T1closeT2')
		except (picamera.exc.PiCameraError, picamera.exc.PiCameraMMALError):
			print >>self.f, "PiCameraError or MMALError"
			self.queue.put('exit')
			time.sleep(1)
			os.system("sshpass -p 'raspberry' ssh pi@10.0.0.1 -o StrictHostKeyChecking=no python flash.py camError 2")
		except:
			print >>self.f, "other error"
			self.queue.put('exit')
			time.sleep(1)
			os.system("sshpass -p 'raspberry' ssh pi@10.0.0.1 -o StrictHostKeyChecking=no python flash.py error 2")


#Checks to see if any pictures have been taken and moves/removes them to the MasterPi
#Checks the folder to see if there are any pictures, sends that group to the MasterPi, removes them, checks again, repeat
#picsList is an arrray, list is a string
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
#					os.system("sshpass -p 'raspberry' scp -o StrictHostKeyChecking=no {0} pi@10.0.0.1:/home/pi/pastImages/".format(list) )
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

def main():
	queue = Queue.Queue()
	f = open('manualPic3Output.txt', 'w')
	t1 = takePictures(queue, f)
	t2 = queuePictures(queue, f)
	t1.start()
	t2.start()

if __name__ == '__main__':
	main()
