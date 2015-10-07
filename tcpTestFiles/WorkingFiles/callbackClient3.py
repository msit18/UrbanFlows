#Working TCP client that runs with callbackServer3
#Works to test callbacks

#Written by Michelle Sit

from twisted.internet import reactor, protocol
import subprocess
import time
import os

import sys

from twisted.web.client import Agent
from twisted.web.http_headers import Headers

from twisted.web.client import FileBodyProducer

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
		self.state = "runFirst"

	def connectionMade(self):
		ip_address = subprocess.check_output("hostname --all-ip-addresses", shell=True).strip()
		msg = "piGroup1 {0}".format(ip_address)
		self.transport.write(msg)

	def dataReceived(self, data):
		print "data Received from Server: {0}".format(data)
		os.system(data)

class sendHTTPImage():

	def sendImg(self):
		agent = Agent(reactor)
		body = FileBodyProducer(open("./cute_otter.jpg", 'rb'))

		postImg = agent.request(
		    'POST',
		    "http://localhost:8880/upload-image",
		    Headers({'User-Agent': ['Twisted Web Client Example'],
		    		'Content-Type': ['text/x-greeting']}),
		    body)

		postImg.addCallback(self.cbResponse)
		#postImg.addBoth(self.cbShutdown)

	def cbResponse(self, response):
	    print response

	def cbShutdown(self, ignored):
	    reactor.stop()

if __name__ == '__main__':
	#reactor.connectTCP('18.111.45.131', 8888, DataClientFactory(data), timeout=200)
	
	#TCP network
	data = "first data"
	reactor.connectTCP('localhost', 8888, DataClientFactory(data), timeout=200)

	#HTTP network.  Connects on port 8880
	c = sendHTTPImage()
	c.sendImg()

	reactor.run()