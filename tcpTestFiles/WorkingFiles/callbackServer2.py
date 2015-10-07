#Working callback server.  Used with callbackClient2.py to send data and messages

#TODO: NEED TO FIX CALLBACK TIMES BECAUSE THEY MIGHT CALL AT THE SAME TIME
#TODO: NEED TO FIX LOST CONNECTIONS THING (CHECK CURENT IP AND HOW TO REMOVE FROM DICTFORMAT)

#Written by Michelle Sit

from twisted.internet.protocol import Factory
from twisted.internet import reactor, protocol, defer
import time, sys

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
		self.d.addCallback(self.gotIP)
		self.d.addErrback(self.failedIP)
		self.d.callback(data)

	def gotIP(self, data):
		dataSplit = [data for data in data.split() if data.strip()]
		#dataSplit[0] = piGroup1
		#dataSplit[1] = IP address
		print dataSplit[0] in dictFormat
		if (dataSplit[0] in dictFormat) == False:
			#adds key and a list containing IP address
			print "I didn't have this cluster key"
			dictFormat[dataSplit[0]] = [dataSplit[1]]
			print dictFormat
			reactor.callLater(0.1, self.writeToClient, "ls")
			print "finished with adding cluster and IP"
		elif (dataSplit[0] in dictFormat) == True:
			#appends new IP to the end of the key's list
			print "it's true! I have this cluster in my keys"
#			print dictFormat[dataSplit[0]] #prints out the key values
			dictFormat[dataSplit[0]].append(dataSplit[1])
			print dictFormat
			reactor.callLater(0.1, self.writeToClient, "ls")
			print "finished with adding new IP to a known cluster"
		else:
			self.d.errback(ValueError("Couldn't process your IP request"))
		reactor.callInThread(self.checkConnections, dataSplit[0])

	def writeToClient(self, msg):
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
		while numValues < 0:
			numValues = len(dictFormat[dataKey])
		else:
			self.d.addCallback(self.sendCmds)
		 	self.d.addErrback(self.failedSendCmds)

	def failedCheckConnections(self, failure):
		print "FAILURE: failedCheckConnections"
		sys.stderr.write(str(failure))

	def sendCmds(self, data):
		print "sendCmds"
		#reactor.callLater(0.3, self.writeToClient, "ls")

#TODO: Put in a timeout to check if the msgs were received
	def failedSendCmds(self, failure):
		print "FAILURE: failedSendCmds"
		sys.stderr.write(str(failure))

if __name__ == '__main__':
	d = defer.Deferred()

	#reactor.listenTCP(8888, DataFactory(), 200, '18.111.45.131')
	reactor.listenTCP(8888, DataFactory(), 200, 'localhost')
	reactor.run()
