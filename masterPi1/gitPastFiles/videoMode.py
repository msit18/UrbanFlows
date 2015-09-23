#/!/usr/bin/python

#Written by Michelle Sit
#Edited from picThread6.py to take arguments from readPiFace and globalVariables.  Takes pictures on one thread
#and moves/removes them to the masterPi.  Picture resolution and total time process runs (in seconds) is controlled
#by the inputs from the piFace

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
#TODO: FIX CAMERA-RECORD SEQUENCE.  NOT FUNCTIONAL RIGHT NOW
class takePictures(threading.Thread):
	def __init__(self, queue):
		threading.Thread.__init__(self)
		self.queue = queue

	def run (self):
		#frames = 5
		print "manual pic ST: " + str(sys.argv[1])
		print "manual pic RW: " + str(sys.argv[2])
		print "manual pic RH: " + str(sys.argv[3])
		print "manual pic FR: " + str(sys.argv[4])
		timeFrames = int(sys.argv[1])*60
		print "manual pic TF: " + str(timeFrames)
		with picamera.PiCamera() as camera:
			camera.resolution = (int(sys.argv[2]), int(sys.argv[3]))
			for filename in camera.record_sequence(
				[datetime.datetime.now().strftime ('%d-%m-%Y-%H_%M_%S_%f') + '.h264'] for i in range(timeFrames)):
				camera.wait_recording(int(sys.argv[4]))
		#	for k in range (timeFrames):
		#		camera.capture_sequence([
		#			datetime.datetime.now().strftime ('%d-%m-%Y-%H_%M_%S_%f') + '.jpg'
		#			for i in range(frames)
		#			], use_video_port=True)
			print ("10.0.0.2: " + str(k))
			self.queue.put('beginT2')
			time.sleep(1)
		self.queue.put('T1closeT2')

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
				picsList = glob.glob('*.jpg')
				while len(picsList) > 0:
					list = ' '.join(picsList)
					print (list)
					os.system("sshpass -p 'raspberry' scp %(list)s pi@10.0.0.1:/home/pi/"%locals())
					os.system("rm %(list)s"%locals())
					picsList = []
			elif runThread is 'T1closeT2':
#				print 'T2 recieved close message'
				break

def main():
	t1 = takePictures(queue)
	t2 = queuePictures(queue)
	t1.start()
	t2.start()

if __name__ == '__main__':
	main()
