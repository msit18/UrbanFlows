import time
import threading
import Queue
import subprocess
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
		with picamera.PiCamera() as camera:
			camera.resolution = (640,480)
			camera.framerate = 90
			for k in range (2):
				camera.capture_sequence([
					datetime.datetime.now().strftime ('%d-%m-%Y-%H_%M_%S_%f') + '.jpg'
					for i in range(frames)
					], use_video_port=True)
				print ('Thread 1 Captured %d frames' %(frames))
				self.queue.put('remaining')
				time.sleep(4)
		self.queue.put('finished')

#Checks to see if any pictures have been taken and pushes them to the queue if so
class queuePictures(threading.Thread):
	def __init__(self, queue):
		threading.Thread.__init__(self)
		self.queue = queue
	
	def run (self):
		while True:
			runThread = self.queue.get()
#			print "T2 runThread " + runThread
			if runThread is 'remaining':
				picsList = glob.glob('*.jpg')
				while len(picsList) > 0:
					print picsList
					pics = picsList.pop()
					#move all the picture files into a zip file.   Send all images in one large zip file.
					self.queue.put(pics)
					#print "queue size: " + str(self.queue.qsize())
			elif runThread is 'finished':
#				print 'T2 finishedT1 recieved, sent finished to T3'
				self.queue.put('finished')
				break
			else:
				self.queue.put(runThread)

#Moves the pictures in the queue to the MasterPi.  Removes the picture from the SlavePi after it has been moved.
class movePictures(threading.Thread):
	def __init__(self, queue):
		threading.Thread.__init__(self)
		self.queue = queue

	def run (self):
		while True:
			pics = self.queue.get()
#			print "T3: " + pics
			if pics is 'finished':
				print 'ending thread 3'
				break
			elif pics is 'remaining':
				print "T3 sent remaining back into queue"
				self.queue.put('remaining')
			elif pics is 'finishedT1':
				print 'T3 continuing on'
				continue
			else:
				print 'T3 removed picture'
				os.system("sshpass -p 'raspberry' scp %(pics)s pi@10.0.0.1:/home/pi/" %locals())
				os.system("rm %(pics)s" %locals())				

def main():
	pics = []
	t1 = takePictures(queue)
	t2 = queuePictures(queue)
	t3 = movePictures(queue)
	t1.start()
	t2.start()
	t3.start()

if __name__ == '__main__':
	main()
