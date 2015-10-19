import threading
import Queue
import glob
import time
from twisted.internet import defer

from twisted.web.client import Agent
from twisted.web.http_headers import Headers
from twisted.web.client import FileBodyProducer
from twisted.internet import reactor, protocol

class thread1(threading.Thread):
	def __init__(self, queue):
		threading.Thread.__init__(self)
		self.queue = queue

	def run (self):
		fileList = glob.glob('*.jpg')
		print fileList
		print len(fileList)
		while len(fileList) > 0:
			global name
			name = fileList.pop()
			print name
			self.sendImg(name)
		self.queue.put('end')

	def sendImg(self, imgName):
		print "running sendImg"
		agent = Agent(reactor)
		body = FileBodyProducer(open('{0}'.format(imgName), 'rb'))
		postImg = agent.request(
		    'POST',
		    "http://localhost:8880/upload-image",
		    Headers({'User-Agent': ['Twisted Web Client Example'],
		    		'Content-Type': ['text/x-greeting']}),
		    body)

		# for i in range(len(fileList)):
		# 	if i > len(fileLis):
		# 		print "closing threadTestA"
		# 		self.queue.put('end')
		# 	else:
		# 		name = fileList[i]
		# 		print name
		# 		self.queue.put('{0}'.format(name))
		# 		time.sleep(0.5)