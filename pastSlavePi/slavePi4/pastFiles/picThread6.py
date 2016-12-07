import time
import threading
import Queue
import picamera
import datetime
import glob
import os
import string

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
			#camera.resolution = (2592,1944)
			camera.resolution = (640, 480)
			camera.framerate = 90
			for k in range (5):
				camera.capture_sequence([
					datetime.datetime.now().strftime ('%d-%m-%Y-%H_%M_%S_%f') + '.jpg'
					for i in range(frames)
					], use_video_port=True)
				#print ('Thread 1 Captured %d frames' %(frames))
				print "10.0.0.2: " + str(k)
				self.queue.put('beginT2')
#				time.sleep(1)
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
					print list
					os.system("sshpass -p 'raspberry' scp %(list)s pi@10.0.0.1:/home/pi/" %locals())
                                	os.system("rm %(list)s" %locals())
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
