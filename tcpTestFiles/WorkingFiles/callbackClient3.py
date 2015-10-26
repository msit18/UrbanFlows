#Working TCP client that runs with callbackServer3

#TODO: Integration with manualPic and videoMode

#Written by Michelle Sit
#Many thanks to Vlatko Klabucar for helping me with the HTTP part!  Also many thanks to Nahom Marie
#for helping me with the architecture of this system!

#TCP
from twisted.internet import reactor, protocol
import subprocess
#HTTP
from twisted.web.client import Agent
from twisted.web.http_headers import Headers
from twisted.web.client import FileBodyProducer
#Threading for picture transfer
import threading
import Queue
import os
import glob
import time
#import manualPic_capturePhotos

#TCP network portion
class DataClientFactory(protocol.ClientFactory):
	def __init__(self, data):
		self.data = data

	def buildProtocol(self, addr):
		return myProtocol(self)

	def clientConnectionFailed(self, connector, reason):
		print 'connection failed:', reason.getErrorMessage()
		reactor.stop()

	def clientConnectionLost(self, connector, reason):
		print 'connection lost:', reason.getErrorMessage()
		reactor.stop()

class myProtocol(protocol.Protocol):
	def __init__(self, factory):
		self.factory = factory
		self.fileList = []
		self.name = ""
		self.tag = True

	def connectionMade(self):
		ip_address = subprocess.check_output("hostname --all-ip-addresses", shell=True).strip()
		msg = "ip piGroup1 {0}".format(ip_address)
		self.transport.write(msg)

	def dataReceived(self, data):
		print "data Received from Server: {0}".format(data)
		msgFromServer = [data for data in data.split()]
		# print msgFromServer[0]
		# print msgFromServer[1]
		if msgFromServer[1] == "startTakingPictures":
			#STARTS IMAGE TAKING PROCESS
			print "GOT A STARTTAKINGPICTURES"
			#INSERT COMMAND TO START TAKING PICTURES
			#(below) STARTS GATHERING PICTURES TO SEND OVER
			self.getList()
		elif msgFromServer[1] == "gotNameSendImg":
			print "RECEIVED GOTNAMESENDIMG"
			self.sendImg()
		elif msgFromServer[1] == "End":
			self.tag = False
		else:
			print "Didn't write hi success.jpg to server"

	def getList(self):
		if len(self.fileList) <= 0:
			self.fileList = glob.glob('*.jpg')
			print self.fileList
			self.sendName()
		else:
			self.sendName()

	def sendName(self):
		print self.fileList
		self.name = self.fileList.pop(0)
		print "Sending name over: {0}".format(self.name)
		reactor.callLater(1, self.transport.write, " imgName {0}".format(self.name))

# #HTTP network portion
# class sendHTTPImage():
	def sendImg(self):
		print "RUNNING SENDIMG"
		print self.name
		agent = Agent(reactor)
		body = FileBodyProducer(open("/home/michelle/gitFolder/UrbanFlows/tcpTestFiles/WorkingFiles/{0}".format(self.name), 'rb'))
		postImg = agent.request(
		    'POST',
		    "http://localhost:8880/upload-image",
		    Headers({'User-Agent': ['Twisted Web Client Example'],
		    		'Content-Type': ['text/x-greeting']}),
		    body)
		os.system('rm {0}'.format(self.name))
		if self.tag == True:
			self.getList()
		else:
			pass

if __name__ == '__main__':
	#reactor.connectTCP('18.111.45.131', 8888, DataClientFactory(data), timeout=200)

	#manualPic setup
	queue = Queue.Queue()
	f = open('manualPic5Output.txt', 'w')
	# t1 = manualPic_capturePhotos.takePictures(queue, f)
	#t2 = queuePictures(queue, f)
	
	#TCP network.  Connects on port 8888
	data = "first data"
	reactor.connectTCP('localhost', 8888, DataClientFactory(data), timeout=200)

	#HTTP network.  Connects on port 8880
	# c = sendHTTPImage()

	reactor.run()