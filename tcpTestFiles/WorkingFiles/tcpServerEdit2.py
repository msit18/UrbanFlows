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
		#dataSplit[0] = piGroup1
		#dataSplit[1] = IP address
		print dataSplit[0] in self.factory.dictFormta
		if dataSplit[0] == "msg":
			pass #run cmd
		elif dataSplit[0] == "time":

		elif (dataSplit[0] in self.factory.dictFormat) == False:
			#adds key and a list containing IP address
			print "I didn't have this key"
			genList = [dataSplit[1]]
			self.factory.dictFormat[dataSplit[0]] = genList
			print self.factory.dictFormat
		elif (dataSplit[0] in self.factory.dictFormat) == True:
			#appends new IP to the end of the key's list
			print "it's true! I have this IP in my keys"
			print self.factory.dictFormat[dataSplit[0]] #prints out the key values
			addIPList = self.factory.dictFormat[dataSplit[0]]
			addIPList.append(dataSplit[1])
			print addIPList
			print self.factory.dictFormat
		else:
			print "didn't find anything.  Sorry"
		self.transport.write("IP received")
	#	self.updateData(data)

#	def takeIP(self, data):

	def compareTime(self):
		for x in self.factory.dictFormat[dataSplit[0]]:
			

	def connectionLost(self, reason):
		self.factory.numConnections -= 1
		print "connection closed"
		print self.factory.dictFormat
		print "Connection lost. Number of active connections: {0}".format(self.factory.numConnections)


#reactor.listenTCP(8888, DataFactory(), 200, '18.111.45.131')
reactor.listenTCP(8888, DataFactory(), 200, 'localhost')
reactor.run()
