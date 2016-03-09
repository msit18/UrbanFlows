#Working TCP server.  Used with tcpClient4.py to send data and messages

#Written by Michelle Sit

from twisted.internet.protocol import Factory
from twisted.internet import reactor, protocol
import time

#sets up the Protocol class
class DataFactory(Factory):
	numConnections = 0
	dictFormat = {}

	def __init__(self, data=None):
		self.data = data

	def buildProtocol(self, addr):
		print "running buildProtocol"
		return DataProtocol(self)

class DataProtocol (protocol.Protocol):
	dictFormat = {}
	def __init__(self,factory):
		self.factory = factory

	def connectionMade(self):
		self.factory.numConnections += 1
		print "Connection made. Number of active connections: {0}".format(self.factory.numConnections)

#Need to write method that updates IP addresses of the pies at first.
#Then switches to accepting error messages
	def dataReceived(self, data):
		print "Server received data: {0}".format(data)
		dataSplit = [data for data in data.split() if data.strip()]
		print dataSplit[0]
		print dataSplit[0] in self.factory.dictFormat
		if dataSplit[0] == "msg":
			pass #run cmd
		elif (dataSplit[0] in self.factory.dictFormat) == False:
			piInfo = [dataSplit[1], dataSplit[2]]
			listOfAll = [piInfo]
			self.factory.dictFormat = {dataSplit[0]: listOfAll}
			print "dictFormat:"
			print self.factory.dictFormat
			print "keys of dictoFormat"
			print self.factory.dictFormat.keys()
			listOfAll.append(['10.189.49.150', '19:01:10'])
			print self.factory.dictFormat
			for x in listOfAll:
				print x[1]
		elif (dataSplit[0] in self.factory.dictFormat) == True:
			print "it's true! I have this IP in my keys already"
		else:
			print "didn't find anything.  Sorry"
		self.transport.write("Thanks I got your data")
	#	self.updateData(data)

	def connectionLost(self, reason):
		self.factory.numConnections -= 1
		print "connection closed"
		print self.factory.dictFormat
		print "Connection lost. Number of active connections: {0}".format(self.factory.numConnections)


#reactor.listenTCP(8888, DataFactory(), 200, '18.111.45.131')
reactor.listenTCP(8888, DataFactory(), 200, 'localhost')
reactor.run()
