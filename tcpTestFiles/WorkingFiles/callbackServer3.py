#Working callback server.  Used with callbackClient3.py to send data and messages

#TODO: NEED TO FIX LOST CONNECTIONS THING (CHECK CURENT IP AND HOW TO REMOVE FROM DICTFORMAT)

#Written by Michelle Sit
#Many thanks to Vlatko Klabucar for helping me with the HTTP part!

from twisted.internet.protocol import Factory
from twisted.internet import reactor, protocol, defer
import time, sys

from twisted.web.server import Site
from twisted.web.resource import Resource

import cgi

#sets up the Protocol class
class DataFactory(Factory):
	numConnections = 0

	def __init__(self, data=None):
		self.data = data

	def buildProtocol(self, addr):
		return DataProtocol(self, d)

class DataProtocol (protocol.Protocol):
	global dictFormat
	dictFormat = {}

	def __init__(self, factory, d):
		self.factory = factory
		self.d = defer.Deferred()

	def connectionMade(self):
		self.factory.numConnections += 1
		print "Connection made. Number of active connections: {0}".format(self.factory.numConnections)

	def connectionLost(self, reason):
		self.factory.numConnections -= 1
		print dictFormat
		print "Connection lost. Number of active connections: {0}".format(self.factory.numConnections)

	def dataReceived(self, data):
		print "Server received data: {0}".format(data)
		msgFromClient = [data for data in data.split()]
		print msgFromClient
		if msgFromClient[0] == "ip":
			print "FOUND AN IP"
			self.d.addCallback(self.gotIP, msgFromClient[2])
			self.d.addErrback(self.failedIP)
			self.d.callback(msgFromClient[1])
		elif msgFromClient[0] == "Hi":
			print "FOUND A HI"
			reactor.callInThread(a.setImgName, msgFromClient[1])

	def gotIP(self, piGroup, ipAddr):
		print "RUNNING GOTIP"
		print piGroup
		print ipAddr
		if (piGroup in dictFormat) == False:
			#adds key and a list containing IP address
			print "I didn't have this cluster key"
			dictFormat[piGroup] = [ipAddr]
			print dictFormat
			print "finished with adding cluster and IP"
		elif (piGroup in dictFormat) == True:
			#appends new IP to the end of the key's list
			print "it's true! I have this cluster in my keys"
			#print dictFormat[piGroup] #prints out the key values
			dictFormat[piGroup].append(ipAddr)
			print dictFormat
			print "finished with adding new IP to a known cluster"
		else:
			print "Got something that wasn't an IP"
			self.d.errback(ValueError("Couldn't process your IP request"))
		reactor.callInThread(self.checkConnections, piGroup)

	def writeToClient(self, msg):
		print "write message to client"
		self.transport.write(msg)

	def failedIP(self, failure):
		print "FAILURE: NOTIP"
		sys.stderr.write(str(failure))

	#Called in seperate threads	
	def checkConnections(self, dataKey):
		print "This is checkConnections method.  Hello."
		print dataKey
		print len(dictFormat[dataKey])
		numValues = len(dictFormat[dataKey])
		while numValues < 2:
			numValues = len(dictFormat[dataKey])
		else:
			print "SENDING CMDS"
			self.d.addCallback(self.sendCmds)
		 	self.d.addErrback(self.failedSendCmds)

	def failedCheckConnections(self, failure):
		print "FAILURE: failedCheckConnections"
		sys.stderr.write(str(failure))

	def sendCmds(self, data):
		print "sendCmds"
		reactor.callLater(0.1, self.writeToClient, "Okay sendPicName")

#TODO: Put in a timeout to check if the msgs were received
	def failedSendCmds(self, failure):
		print "FAILURE: failedSendCmds"
		sys.stderr.write(str(failure))

#Used for HTTP network.  Receives images and saves them to the server
class UploadImage(Resource):

	def setImgName(self, value):
		global imgName
		imgName = value
		print "This img name will be {0}".format(imgName)

	def render_GET(self, request):
		print "getting"
		return '<html><body><p>This is the server for the MIT SENSEable City Urban Flows Project.'\
		'  It receives images and saves them to the server.</p></body></html>'

	def render_POST(self, request):
		print "Posting: {0}".format(imgName)
		# file = open("uploaded-image.jpg","wb")
		file = open(imgName, "wb")
		file.write(request.content.read())
		return '<html><body>Image uploaded :) </body></html>'
		file.close()

if __name__ == '__main__':
	#HTTP network
	a = UploadImage()
	root = Resource()
	root.putChild("upload-image", a)
	factory = Site(root)
	reactor.listenTCP(8880, factory, 200, 'localhost')

	#TCP network
	d = defer.Deferred()
	reactor.listenTCP(8888, DataFactory(), 200, 'localhost')
	reactor.run()

	#reactor.listenTCP(8888, DataFactory(), 200, '18.111.45.131')