#Still being written: callback server.  Used with testUploadSpeed2.py to send data and messages

#TODO: Not implemented: A scaleable method of keeping track of the clusters. Nahom proposed
#having a team leader pi who is responsible for pinging its teammates when the server detects
#that a connection has been lost. Instead of pinging all of the clients, just ping 1/4 (the
#team leaders) who then ping their team members and report back if they have lost someone.

#Written by Michelle Sit
#Many thanks to Vlatko Klabucar for helping me with the HTTP part!  Also many thanks to Nahom Marie
#for helping me with the architecture of this system!

from twisted.internet.protocol import Factory
from twisted.internet import reactor, protocol, defer, threads
import sys, time
from masterVariables2 import MasterVariables

from twisted.web.server import Site
from twisted.web.resource import Resource

import cgi
import subprocess

#sets up the Protocol class
class DataFactory(Factory):
	numConnections = 0

	def __init__(self, data=None):
		self.data = data
		self.ipDictionary = {}
		self.checkCamPi = 0
		self.finished = 0

	def buildProtocol(self, addr):
		return DataProtocol(self, d)

class DataProtocol (protocol.Protocol):

	def __init__(self, factory, d):
		self.factory = factory
		self.d = defer.Deferred()
		self.name = None

	def connectionMade(self):
		self.factory.numConnections += 1
		print "Connection made at {0}. Number of active connections: {1}".format(time.strftime("%Y-%m-%d-%H:%M:%S"), self.factory.numConnections)

	def connectionLost(self, reason):
		self.factory.numConnections -= 1
		if self.name in self.factory.ipDictionary:
			del self.factory.ipDictionary[self.name]
		print "Echoers: ", self.factory.ipDictionary
		print "Connection lost at {0}. Number of active connections: {1}".format(time.strftime("%Y-%m-%d-%H:%M:%S"), self.factory.numConnections)

	def dataReceived(self, data):
		print "DATARECEIVED. Server received data: {0}".format(data)
		msgFromClient = [data for data in data.split()]
		if msgFromClient[0] == "ip":
			print "FOUND AN IP"
			self.name = msgFromClient[2]
			self.factory.ipDictionary[self.name] = self
			print "Echoers: ", self.factory.ipDictionary
			print "RUNNING CHECKCONNECTIONS"
			if len(self.factory.ipDictionary) > (totalNumRaspies-1): #Set value to total number of Raspies -1
				self.verifyConnections()
		elif msgFromClient[0] == 'CAMERROR':
			print "ERROR FROM {1} PICAMERA at {0}".format(time.strftime("%Y-%m-%d-%H:%M:%S"), msgFromClient[1])

		elif msgFromClient[0] == 'checkCamPi':
			self.factory.checkCamPi += 1
			if self.factory.checkCamPi > (totalNumRaspies-1):
				print "All raspies are ready to start process"
				print "Running send cmds"
				self.startProgram()
			else:
				print "Still waiting on other raspies to connect. {0} raspies are ready".format(self.factory.checkCamPi)

		elif msgFromClient[0] == 'finished':
			self.factory.finished += 1
			if self.factory.finished > (totalNumRaspies-1):
				print "All raspies are finished"
			else:
				print "Still waiting on other raspies to finish taking or uploading pictures. {0} raspies are finished".format(self.factory.finished)

		else:
			print "Time: {0}. I don't know what this is: {1}".format(time.strftime("%Y-%m-%d-%H:%M:%S"), data)

	#USE THIS FOR THE LARGER SCALEABLE SYSTEM
	# def updatingIPDictionary(self, dictionary, piGroup, ipAddr):
	# 	print "RUNNING GOTIP"
	# 	#adds key and a list containing IP address
	# 	if (piGroup in dictionary) == False:
	# 		print "I didn't have this cluster key for {0}".format(dictionary)
	# 		dictionary[piGroup] = [ipAddr]
	# 	#appends new IP to the end of the key's list
	# 	elif (piGroup in dictionary) == True:
	# 		print "it's true! I have this cluster in my keys for {0}".format(dictionary)
	# 		dictionary[piGroup].append(ipAddr)
	# 	else:
	# 		print "Got something that wasn't an IP. Adding to dict anyway for {0}".format(dictionary)
	# 		dictionary[piGroup] = [ipAddr]
	# 	print dictionary

	def verifyConnections(self):
		for echoer in self.factory.ipDictionary:
			sendMsg = "checkCamera " + time.strftime("%x %X")
			print "sendMsg for verify ", sendMsg
			self.factory.ipDictionary[echoer].transport.write(sendMsg)

	def startProgram(self):
		print "STARTTAKINGPICTURES"
		for echoer in self.factory.ipDictionary:
			sendMsg = "startProgram {0}".format(f.getParam())
			print sendMsg
			self.factory.ipDictionary[echoer].transport.write(sendMsg)

#TODO: Put in a timeout to check if the msgs were received
	def failedSendCmds(self,failure):
		print "FAILURE: failedSendCmds"
		sys.stderr.write(str(failure))

#Used for HTTP network.  Receives images and saves them to the server
class UploadImage(Resource):

	def render_GET(self, request):
		print "RENDER GETTING"
		return '<html><body><p>This is the server for the MIT SENSEable City Urban Flows Project.'\
		'  It receives images and saves them to the server.</p></body></html>'

	def render_POST(self, request):
		name = request.getHeader('filename')
		print "RENDER Posting: {0}".format(name)
		with open(name, "wb") as file:
			file.write(request.content.read())
		print "finished writing file"
		return '<html><body>Image uploaded :) </body></html>'

if __name__ == '__main__':
	#log = open('ServerLog-{0}.txt'.format(time.strftime("%Y-%m-%d-%H:%M:%S")), 'w')
	f = MasterVariables()
	f.userInput()

	ip_address = subprocess.check_output("hostname --all-ip-addresses", shell=True).strip()
	serverIP = ip_address.split()[1]
	totalNumRaspies = 2

	#TCP network
	d = defer.Deferred()
	b = DataFactory()
	reactor.listenTCP(8888, b, 200, serverIP)

	#HTTP network
	a = UploadImage()
	root = Resource()
	root.putChild("upload-image", a)
	factory = Site(root)
	reactor.listenTCP(8880, factory, 200, serverIP)

	print "SERVER IP IS: ", serverIP

	reactor.run()
