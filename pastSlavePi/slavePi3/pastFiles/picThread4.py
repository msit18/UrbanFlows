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
		with picamera.PiCamera() as camera:
			camera.resolution = (2592,1944)
			camera.framerate = 90
			for k in range (60):
				camera.capture_sequence([
					datetime.datetime.now().strftime ('%d-%m-%Y-%H_%M_%S_%f') + '.jpg'
					for i in range(frames)
					], use_video_port=True)
				#print ('Thread 1 Captured %d frames' %(frames))
				print "10.0.0.2: " + str(k)
				self.queue.put('beginT2')
				time.sleep(1)
		self.queue.put('T1closeT2')
#		print 'T1 sent close message to T2'

#Checks to see if any pictures have been taken and pushes them to the queue if so
class queuePictures(threading.Thread):
	def __init__(self, queue):
		threading.Thread.__init__(self)
		self.queue = queue
	
	def run (self):
		print "run once"
		while True:
			#os.system("sshpass -p 'raspberry' ssh pi@10.0.0.1")
			runThread = self.queue.get()
#			print "T2 runThread " + runThread
			if runThread is 'beginT2':
				picsList = glob.glob('*.jpg')
				while len(picsList) > 0:
					#print picsList
					pics = picsList.pop()
					os.system("sshpass -p 'raspberry' scp %(pics)s pi@10.0.0.1:/home/pi/" %locals())
					os.system("rm %(pics)s" %locals())

					#move all the picture files into a zip file.   Send all images in one large zip file.
			elif runThread is 'T1closeT2':
#				print 'T2 recieved close message'
				print "end"
				break
		print "end two"

def main():
	pics = []
	t1 = takePictures(queue)
	t2 = queuePictures(queue)
	t1.start()
	t2.start()

if __name__ == '__main__':
	main()
