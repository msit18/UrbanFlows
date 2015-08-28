from twisted.internet.protocol import Factory
from twisted.internet import reactor, protocol
import time

#sets up the Protocol class
class DataFactory(Factory):
	numConnections = 0

	def __init__(self, data=None):
		self.data = data

	def buildProtocol(self, addr):
		print "running buildProtocol"
		return DataProtocol(self)

class DataProtocol (protocol.Protocol):
	def __init__(self,factory):
		self.factory = factory

	def connectionMade(self):
		self.factory.numConnections += 1

	def dataReceived(self, data):
		print "Number of active connections: {0}".format(self.factory.numConnections,)
		print "Server received data: {0}".format(data)
		self.transport.write("Thanks I got your data")
	#	self.updateData(data)

	def connectionLost(self, reason):
		self.factory.numConnections -= 1

#Stores data to send to the client next time it connects
	# def updateData(self, data):
	# 	print "running updateData"
	# 	self.factory.data = "Server manipulation: {0}".format(data)
	# 	print "The next message Server will send is: {0}".format(self.factory.data)

#reactor.listenTCP(8888, DataFactory(), 200, '18.111.45.131')
reactor.listenTCP(8888, DataFactory(), 200, 'localhost')
reactor.run()
