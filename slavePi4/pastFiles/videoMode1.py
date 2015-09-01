#/!/usr/bin/python

#Written by Michelle Sit
#Edited from manualPic.py on pi@10.0.0.5 to take arguments from readPiFace.  Takes pictures on one thread
#and moves/removes them to the masterPi.  Picture resolution and total time process runs (in seconds) is controlled
#by the inputs from the piFace.  It additionally triggers flash.py on the MasterPi to provide user feedback.

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
			print "manual pic TTA1: " + str(sys.argv[1])
			print "manual pic VTA2: " + str(sys.argv[5])
			print "manual pic RW: " + str(sys.argv[2])
			print "manual pic RH: " + str(sys.argv[3])
			print "manual pic FR: " + str(sys.argv[4])
#			totalTime = int(sys.argv[1])*60
			vidTime = int(float(sys.argv[5])*60)
#			print "manual pic TT: " + str(totalTime)
			print "manual pic VT: " + str(vidTime)
#			numCycles = totalTime/vidTime
#			print "manual pic CYC: " + str(numCycles)
			with picamera.PiCamera() as camera:
				camera.resolution = (int(sys.argv[2]), int(sys.argv[3]))
				camera.framerate = int(sys.argv[4])
				for filename in camera.record_sequence([
					datetime.datetime.now().strftime('%d-%m-%Y-%H_%M_%S_%f') + '_TT' + str(sys.argv[1]) + '_VT' + str(sys.argv[5]) + '_RW' + str(sys.argv[2]) + '_FR' + str(sys.argv[4]) + ".h264"]):
#					for k in range(numCycles)]):
					camera.wait_recording(vidTime)
#					print ("10.0.0.4: " + str(k))
					self.queue.put('beginT2')
			self.queue.put('T1closeT2')
			camera.close()
		except (picamera.exc.PiCameraError, picamera.exc.PiCameraMMALError):
			print "caught error"
			self.queue.put('exit')
			time.sleep(1)
			os.system("sshpass -p 'raspberry' ssh pi@10.0.0.1 -o StrictHostKeyChecking=no python flash.py camError 4")
		except:
			self.queue.put('exit')
			time.sleep(1)
			os.system("sshpass -p 'raspberry' ssh pi@10.0.0.1 -o StrictHostKeyChecking=no python flash.py error 4")

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
				print '10.4 T2 recieved close message'
				break
			elif runThread is 'exit':
				print "10.4 broken"
				break

def main():
	t1 = takePictures(queue)
	t2 = queuePictures(queue)
	t1.start()
	t2.start()

if __name__ == '__main__':
	main()
