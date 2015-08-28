from twisted.internet.protocol import Factory
from twisted.internet import reactor, protocol
import time

class DataFactory(Factory):
	numConnections = 0

	def __init__(self, data=None):
		self.data = data

	def buildProtocol(self, addr):
		print "running buildProtocol"
		return sendMessages(self)


class sendMessages (protocol.Protocol):
	def __init__(self,factory):
		self.factory = factory

	def connectionMade(self):
		self.factory.numConnections += 1

	def dataReceived(self, data):
		print "Number of active connections: {0}".format(self.factory.numConnections,)
		print "Received: {0}\nSending: {1}".format(data, self.getData())
		self.transport.write(self.getData())
		time.sleep(2)
		self.updateData(data)

	def connectionLost(self, reason):
		self.factory.numConnections -= 1

	def getData(self):
		print "running getData"
		return self.factory.data

	def updateData(self, data):
		print "running updateData"
		self.factory.data = data

reactor.listenTCP(8888, DataFactory(), 200, '18.111.55.166')
reactor.run()
