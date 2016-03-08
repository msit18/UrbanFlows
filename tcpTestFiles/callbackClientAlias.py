#Working TCP client that runs with callbackServer3
#Works to test callbacks

#Written by Michelle Sit
#Many thanks to Vlatko Klabucar for helping me with the HTTP part!

from twisted.internet import reactor, protocol
import subprocess
import time
import os

import sys

from twisted.web.client import Agent
from twisted.web.http_headers import Headers

from twisted.web.client import FileBodyProducer

#TCP network portion
#Sets up the Protocol class
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

	def connectionMade(self):
		ip_address = subprocess.check_output("hostname --all-ip-addresses", shell=True).strip()
		msg = "ip piGroup1 {0}".format(ip_address)
		self.transport.write(msg)

	def dataReceived(self, data):
		print "data Received from Server: {0}".format(data)
		msgFromServer = [data for data in data.split()]
		print msgFromServer[0]
		print msgFromServer[1]
		if msgFromServer[1] == "sendPicName":
			self.transport.write("Hi success2.jpg filler")
			self.sendImg()
		else:
			print "Didn't write hi success.jpg to server"

# #HTTP network portion
# class sendHTTPImage():

	def sendImg(self):
		agent = Agent(reactor)
		body = FileBodyProducer(open("./cute_bird.jpg", 'rb'))
		postImg = agent.request(
		    'POST',
		    "http://localhost:8880/upload-image",
		    Headers({'User-Agent': ['Twisted Web Client Example'],
		    		'Content-Type': ['text/x-greeting']}),
		    body)

	def writeToServer(self, msg):
		self.transport.write(msg)

	def cbShutdown(self, ignored):
	    reactor.stop()

if __name__ == '__main__':
	#reactor.connectTCP('18.111.45.131', 8888, DataClientFactory(data), timeout=200)
	
	#TCP network.  Connects on port 8888
	data = "first data"
	reactor.connectTCP('localhost', 8888, DataClientFactory(data), timeout=200)

	#HTTP network.  Connects on port 8880
	# c = sendHTTPImage()

	reactor.run()