#Working callback server.  Used with callbackClient.py to send data and messages

#Written by Michelle Sit

from twisted.internet.protocol import Factory
from twisted.internet import reactor, protocol, defer
import time

#sets up the Protocol class
class DataFactory(Factory):
	numConnections = 0
	dictFormat = {}

	def __init__(self, data=None):
		self.data = data

	def buildProtocol(self, addr):
		print "running buildProtocol"
		return DataProtocol(self, d)

class DataProtocol (protocol.Protocol):
	dictFormat = {}
	def __init__(self,factory, d):
		self.factory = factory
		self.d = defer.Deferred()

	def connectionMade(self):
		self.factory.numConnections += 1
		print "Connection made. Number of active connections: {0}".format(self.factory.numConnections)

	def dataReceived(self, data):
		print "Server received data: {0}".format(data)
		d.addCallback(self.gotIP)
		d.addErrback(self.notIP)
		d.callback(data)
		print "fin"

	def connectionLost(self, reason):
		self.factory.numConnections -= 1
		print "connection closed"
		print self.factory.dictFormat
		print "Connection lost. Number of active connections: {0}".format(self.factory.numConnections)

	def gotIP(self, data):
		print "got data"
		if data == "true":
			d.callback("True!")
		else:
			d.errback(ValueError("Nope sorry"))
		#print data

	def notIP(self, failure):
		print "running notIP"
		import sys
		sys.stderr.write(str(failure))

if __name__ == '__main__':
	d = defer.Deferred()

	#reactor.listenTCP(8888, DataFactory(), 200, '18.111.45.131')
	reactor.listenTCP(8888, DataFactory(), 200, 'localhost')
	reactor.run()
