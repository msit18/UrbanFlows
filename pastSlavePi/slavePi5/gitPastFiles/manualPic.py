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
class takePictures(threading.Thread):
	def __init__(self, queue):
		threading.Thread.__init__(self)
		self.queue = queue

	def run (self):
#		try:
		frames = int(sys.argv[4])
		print "manual pic ST: " + str(sys.argv[1])
		print "manual pic RW: " + str(sys.argv[2])
		print "manual pic RH: " + str(sys.argv[3])
		print "manual pic FR: " + str(sys.argv[4])
		timeFrames = int(sys.argv[1])*5
		print "manual pic TF: " + str(timeFrames)
		with picamera.PiCamera() as camera:
			camera.resolution = (int(sys.argv[2]), int(sys.argv[3]))
			camera.framerate = int(sys.argv[4])
			start = time.time()
			for k in range (timeFrames):
				camera.capture_sequence([
					datetime.datetime.now().strftime ('%d-%m-%Y-%H_%M_%S_%f') + '_ST' + str(sys.argv[1]) + '_RW' + str(sys.argv[2]) + '_FR' + str(sys.argv[4]) + '.jpg'
					for i in range(frames)
					], use_video_port=True)
				print ('Thread 1 Captured %d frames' %(frames))
				self.queue.put('beginT2')
			finish = time.time()
			print ('Captured %d at %2ffps' %(frames, (finish-start)))
		print "the queue is closing"
		self.queue.put('T1closeT2')
		camera.close()
#		except picamera.exc.PiCameraError:
#			print ("Caught error")
#			self.queue.put("exit")
#			time.sleep(1)
#			os.system("sshpass -p 'raspberry' ssh pi@10.0.0.1 -o StrictHostKeyChecking=no python flash.py camError 5")
#		except picamera.exc.PiCameraMMALError:
#			print ("Caught mmal error")
#			self.queue.put("exit")
#			time.sleep(1)
#			os.system("sshpass -p 'raspberry' ssh pi@10.0.0.1 -o StrictHostKeyChecking=no python flash.py error 5")
#		except:
#			print ("Caught random error")
#			self.queue.put("exit")
#			time.sleep(1)
#			os.system("sshpass -p 'raspberry' ssh pi@10.0.0.1 -o StrictHostKeyChecking=no python flash.py error 5")

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
				pass
#				print "running second thread"
#				picsList = glob.glob('*.jpg')
#				while len(picsList) > 0:
#					list = ' '.join(picsList)
#					print (list)
#					os.system("sshpass -p 'raspberry' scp -o StrictHostKeyChecking=no %(list)s pi@10.0.0.1:/home/pi/pastImages/"%locals())
#					os.system("rm %(list)s"%locals())
#					picsList = []
			elif runThread is 'T1closeT2':
				print '10.5: T2 recieved close message'
				os.system("sshpass -p 'raspberry' ssh pi@10.0.0.1 -o StrictHostKeyChecking=no python flash.py fin {0} {1} {2} {3}".format(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]))
				break 
			elif runThread is 'exit':
				print "10.5 broken"
				break

def main():
	global t1, t2
	t1 = takePictures(queue)
	t2 = queuePictures(queue)
	t1.start()
	t2.start()

if __name__ == '__main__':
	main()
