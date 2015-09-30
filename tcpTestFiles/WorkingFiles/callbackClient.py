#Working TCP client that runs with callbackServer
#Works to test callbacks

#Written by Michelle Sit

from twisted.internet import reactor, protocol
import subprocess
import time

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
		print msg
		self.transport.write(msg)

	def dataReceived(self, data):
		print "data Received from Server: {0}".format(data)

if __name__ == '__main__':
	#reactor.connectTCP('18.111.45.131', 8888, DataClientFactory(data), timeout=200)
	
	data = "first data"
	reactor.connectTCP('localhost', 8888, DataClientFactory(data), timeout=200)
	reactor.run()