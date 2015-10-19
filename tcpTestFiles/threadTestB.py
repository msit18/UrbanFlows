import threading
import Queue

class thread2(threading.Thread):
	def __init__(self, queue):
		threading.Thread.__init__(self)
		self.queue = queue

	def run (self):
		runThread = self.queue.get()
		if runThread != "end":
			print "Thread 2: {0}".format(runThread)
		else:
			print "closing threadTestB"
			thread.exit()