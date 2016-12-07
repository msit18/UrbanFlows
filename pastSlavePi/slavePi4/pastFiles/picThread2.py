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

class takePictures(threading.Thread):
	def __init__(self, queue):
		threading.Thread.__init__(self)
		self.queue = queue

	def run (self):
		frames = 5
		with picamera.PiCamera() as camera:
			camera.resolution = (640,480)
			camera.framerate = 90
		#take pictures
			for k in range (5):
				camera.capture_sequence([
					datetime.datetime.now().strftime ('%d-%m-%Y-%H_%M_%S_%f') + '.jpg'
					for i in range(frames)
					], use_video_port=True)
				print ('Captured %d frames' %(frames))
		#retrieve the pics from the folder
			picsList = glob.glob('*.jpg')
			while len(picsList) > 0:
#				print picsList
				pics = picsList.pop()
				self.queue.put(pics)
#				queue.put(pics)
		self.queue.put('finished')

class movePictures(threading.Thread):
	def __init__(self, queue):
		threading.Thread.__init__(self)
		self.queue = queue

	def run (self):
		while True:
			pics = self.queue.get()
			print pics
			if pics is 'finished':
				break
				#self.queue.task_done()
			else:
				os.system("sshpass -p 'raspberry' scp %(pics)s pi@10.0.0.1:/home/pi/" %locals())
				os.system('rm %(pics)s' %locals())

def main():
	pics = []
	#global queue
	#queue = Queue.Queue()
	t1 = takePictures(queue)
	t2 = movePictures(queue)
	t1.start()
	t2.start()

if __name__ == '__main__':
	main()
