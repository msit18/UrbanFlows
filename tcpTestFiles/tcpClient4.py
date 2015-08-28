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
		ip = subprocess.check_output("hostname --all-ip-addresses", shell=True).decode('utf-8')
		msg = "attempting something method: My IP address is {0}".format(ip)
		print "client is sending this msg: {0}".format(msg)
		self.transport.write(msg)
		self.stateMachine()

	def dataReceived(self, data):
		print "data Received from Server: {0}".format(data)

	def stateMachine(self):
		print "running stateMachine"
		if self.state == "runFirst":
			self.runFirst()
		else:
			self.runElse()

	def runFirst(self):
		print "running runFirst"
		cmd = "Running runFirst method"
		self.transport.write(cmd)
		self.state = "runElse"
		self.stateMachine()

	def runElse(self):
		print "running runElse"
		cmd2 = "Running runElse method"
		self.transport.write(cmd2)
		self.transport.loseConnection()


if __name__ == '__main__':
	#reactor.connectTCP('18.111.45.131', 8888, DataClientFactory(data), timeout=200)
	
	data = "first data"

	reactor.connectTCP('localhost', 8888, DataClientFactory(data), timeout=200)

	reactor.run()