import time
import threading
import Queue
import subprocess

class takePictures(threading.Thread):
	def __init__(self, queue):
		threading.Thread.__init__(self)
		self.queue = queue

	def run (self):
		print "hi"
		while True:
			pic = subprocess.call("./takePicture2.sh", shell=True)
			self.queue.put(pic)
			print 'took picture!'
			time.sleep(1)

class movePictures(threading.Thread):
	def __init__(self, queue):
		threading.Thread.__init__(self)
		self.queue = queue

	def run (self):
		while True:
			pic = self.queue.get()
			#insert python code that will mvoe the file
			print pic
			self.queue.task_done()

def main():
	pic = []
	queue = Queue.Queue()
	t1 = takePictures(queue)
	t2 = movePictures(queue)
	t1.start()
	t2.start()

if __name__ == '__main__':
	main()

