#Michelle Sit playing around with example code.  Attempting to see if you can
#connect multiple clients to a server in one code (You can't)

#Used as a basis for other tcp files

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


class secondDataClientFactory(protocol.ClientFactory):
	def __init__(self, data):
		self.data = data

	def buildProtocol(self, addr):
		return secondProtocol(self)

	def clientConnectionFailed(self, connector, reason):
		print 'connection failed:', reason.getErrorMessage()
		reactor.stop()

	def clientConnectionLost(self, connector, reason):
		print 'connection lost:', reason.getErrorMessage()
		reactor.stop()



# class DataProtocol(protocol.Protocol):
# 	def __init__(self, factory):
# 		self.factory = factory

# 	def connectionMade(self):
# 		self.sendData()

# 	def sendData(self):
# 		self.transport.write(self.factory.data)
# 		time.sleep(2)

# 	def dataReceived(self, data):
# 		print "Received data:", data
# 		self.transport.loseConnection()


class myProtocol(protocol.Protocol):
	def __init__(self, factory):
		self.factory = factory

	def connectionMade(self):
		ip = subprocess.check_output("hostname --all-ip-addresses", shell=True).decode('utf-8')
		msg = "attempting something method: My IP address is {0}".format(ip)
		print "client is sending this  msg: {0}".format(msg)
		self.transport.write(msg)

	def dataReceived(self, data):
		print "data Received from Server from first protocol: {0}".format(data)
		reactor.connectTCP('localhost', 8888, secondDataClientFactory(secondData), timeout=200)
		# self.transport.loseConnection()


class secondProtocol(protocol.Protocol):
	def __init__(self, factory):
		self.factory = factory

	def connectionMade(self):
		time.sleep(5)
		secondMsg = "Second protocol message"
		print "second protocol client is sending message: {0}".format(secondMsg)
		self.transport.write(secondMsg)

	def dataReceived(self, data):
		print "data Received from Server from second protocol: {0}".format(data)
		#self.transport.loseConnection()
		reactor.stop()


if __name__ == '__main__':
	#datas = ["sending data 1", "sending data 2", msg]

	#data_counter = len(datas)

	#for data in datas:
		#reactor.connectTCP('18.111.45.131', 8888, DataClientFactory(data), timeout=200)
	#	reactor.connectTCP('localhost', 8888, DataClientFactory(data), timeout=200)
	
	data = "first data"
	secondData = "seonc data"

	reactor.connectTCP('localhost', 8888, DataClientFactory(data), timeout=200)

	reactor.run()