#/!/usr/bin/python

#Written by Michelle Sit
#Edited from videoMode1.py to take arguments from readPiFace.  Takes video on one thread
#and moves/removes them to the masterPi.  Picture resolution and total time process runs (in seconds) is controlled
#by the inputs from the piFace.  It additionally triggers flash.py on the MasterPi to provide user feedback.

#sys.argv[1] = individual video time (seconds)
#sys.argv[2] = resolution width
#sys.argv[3] = resolution height
#sys.argv[4] = total time (not enabled right now)
#sys.argv[5] = framerate

import time
import threading
import Queue
import picamera
import datetime
import glob
import os
import string
import sys

global queue
queue = Queue.Queue()

#Takes pictures
class takePictures(threading.Thread):
	def __init__(self, queue):
		threading.Thread.__init__(self)
		self.queue = queue

	def run (self):
		try:
			vidTime = int(sys.argv[1])
			resW = int(sys.argv[2])
			resH = int(sys.argv[3])
			totalTime = int(sys.argv[4])*60
			frameRate = int(sys.argv[5])
#			numCycles = totalTime/vidTime
			with picamera.PiCamera() as camera:
				camera.resolution = (resW, resH)
				camera.framerate = frameRate
				for filename in camera.record_sequence([
					datetime.datetime.now().strftime('%d-%m-%Y-%H_%M_%S_%f') + '_TT' + str(sys.argv[4]) + '_VT' + str(sys.argv[1]) + '_RH' + str(sys.argv[3]) + '_FR' + str(sys.argv[5]) + ".h264"]):
#					for k in range(numCycles)]):
					camera.wait_recording(vidTime)
					self.queue.put('beginT2')
			self.queue.put('T1closeT2')
		except (picamera.exc.PiCameraError, picamera.exc.PiCameraMMALError):
			print "caught error"
			self.queue.put('exit')
			time.sleep(1)
			os.system("sshpass -p 'raspberry' ssh pi@10.0.0.1 -o StrictHostKeyChecking=no python flash.py camError 2")
		except:
			self.queue.put('exit')
			time.sleep(1)
			os.system("sshpass -p 'raspberry' ssh pi@10.0.0.1 -o StrictHostKeyChecking=no python flash.py error 2")

#Checks to see if any pictures have been taken and moves/removes them to the MasterPi
class queuePictures(threading.Thread):
	def __init__(self, queue):
		threading.Thread.__init__(self)
		self.queue = queue
	
	def run (self):
		list = ""
		while True:
			runThread = self.queue.get()
			if runThread is 'beginT2':
				picsList = glob.glob('*.h264')
				while len(picsList) > 0:
					list = ' '.join(picsList)
#					print (list)
					os.system("sshpass -p 'raspberry' scp -o StrictHostKeyChecking=no %(list)s pi@10.0.0.1:/home/pi/pastImages/"%locals())
					os.system("rm %(list)s"%locals())
					picsList = []
			elif runThread is 'T1closeT2':
				print '10.5 T2 recieved close message'
				os.system("sshpass -p 'raspberry' ssh pi@10.0.0.1 -o StrictHostKeyChecking=no python flash.py fin {0} {1} {2} {3} {4}".format(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]) )
				break
			elif runThread is 'exit':
				print "10.5 broken"
				break

def main():
	t1 = takePictures(queue)
	t2 = queuePictures(queue)
	t1.start()
	t2.start()

if __name__ == '__main__':
	main()
