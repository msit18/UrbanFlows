#Working TCP server.  Used with tcpClient4.py to send data and messages

#Written by Michelle Sit

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
		print "Connection made. Number of active connections: {0}".format(self.factory.numConnections)

#Need to write method that updates IP addresses of the pies at first.
#Then switches to accepting error messages
	def dataReceived(self, data):
		print "Server received data: {0}".format(data)
		storage = [data for data in data.split() if data.strip()]
		print storage
		piInfo = [storage[1], storage[2]]
		listOfAll = [piInfo]
		dictFormat = {storage[0]: listOfAll}
		print dictFormat
		print dictFormat.keys()
		listOfAll.append(['10.189.49.150', '19:01:10'])
		print dictFormat
		for x in listOfAll:
			print x[1]
		self.transport.write("Thanks I got your data")
	#	self.updateData(data)

	def _acceptIP(self, data):
		print "running acceptIP.  Received: {0}".format(data)
		self.transport.write("Thanks I got your IP address")

	def _acceptMSG(self, data):
		print "running acceptMSG.  Received: {0}".format(data)
		self.transport.write("Thanks I got your message")

	def connectionLost(self, reason):
		self.factory.numConnections -= 1
		print "Connection lost. Number of active connections: {0}".format(self.factory.numConnections)


#reactor.listenTCP(8888, DataFactory(), 200, '18.111.45.131')
reactor.listenTCP(8888, DataFactory(), 200, 'localhost')
reactor.run()
