#!/usr/bin/python

#Written by Michelle Sit
#Takes a video on one thread and moves/removes the video file to the masterPi board through zip/tar files to compress

import time
import threading
import Queue
import picamera
import datetime
import glob
import os

global queue
queue = Queue.Queue()

#Takes pictures
class takePictures(threading.Thread):
	def __init__(self, queue):
		threading.Thread.__init__(self)
		self.queue = queue

	def run (self):
		frames = 5
#		with picamera.PiCamera() as camera:
#			camera.resolution = (640,480)
#			camera.framerate = 90
#			for k in range (5):
#				camera.capture_sequence([
#					datetime.datetime.now().strftime ('%d-%m-%Y-%H_%M_%S_%f') + '.jpg'
#					for i in range(frames)
#					], use_video_port=True)
#				print ('Thread 1 Captured %d frames' %(frames))
		with picamera.PiCamera() as camera:
			camera.resolution = (1920, 1080)
			camera.start_recording(datetime.datetime.now().strftime ('%d-%m-%Y-%H_%M_%S_%f') + '.h264')
			camera.wait_recording(60)
			camera.stop_recording()
			self.queue.put('beginT2')
		self.queue.put('T1closeT2')
#		print 'T1 sent close message to T2'

#Checks to see if any pictures have been taken and moves them to the MasterPi board
class queuePictures(threading.Thread):
	def __init__(self, queue):
		threading.Thread.__init__(self)
		self.queue = queue
	
	def run (self):
		while True:
			runThread = self.queue.get()
#			print "T2 runThread " + runThread
			if runThread is 'beginT2':
				picsList = glob.glob('*.jpg')
				while len(picsList) > 0:
					#print picsList
					pics = picsList.pop()
					os.system("mv %(pics)s pastImages/" %locals())
					os.system("cd pastImages/ ; ls; echo 'break'; cd")
				#Error in the next line.  Only the first tar file has images in it.  Need to fix the logic
				#os.system('NAME=$(date "+%Y-%m-%d_%H_%M_%2S_%3N"); zip $NAME pastImages/*.jpg')
				os.system('NAME=$(date "+%Y-%m-%d_%H_%M_%2S_%3N"); TAR=".tar"; NAMEFULL=$NAME$TAR; tar cvfz $NAMEFULL pastImages/*.jpg')
				os.system("sshpass -p 'raspberry' scp /home/pi/*.tar pi@10.0.0.1:/home/pi/" %locals())
				os.system("rm pastImages/*.jpg")
				os.system("rm *.tar")
			elif runThread is 'T1closeT2':
#				print 'T2 recieved close message'
				break

def main():
	pics = []
	t1 = takePictures(queue)
	t2 = queuePictures(queue)
	t1.start()
	t2.start()

if __name__ == '__main__':
	main()
