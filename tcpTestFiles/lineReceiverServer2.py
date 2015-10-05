#Working callback server.  Used with callbackClient.py to send data and messages

#Written by Michelle Sit

from twisted.internet.protocol import Factory
from twisted.internet import reactor, protocol, defer
import time, sys
from twisted.protocols.basic import LineReceiver

#sets up the Protocol class
class DataFactory(Factory):
	numConnections = 0
	dictFormat = {'piGroup1': ['10.0.0.4']}

	def __init__(self, data=None):
		self.data = data

	def buildProtocol(self, addr):
		print "running buildProtocol"
#		return DataProtocol(self, d)
		return DataProtocol(self)

#class DataProtocol (protocol.Protocol):
class DataProtocol (LineReceiver):
#	def __init__(self,factory, d):
#		self.factory = factory
	def __init__(self, d):
		self.d = defer.Deferred()

	def connectionMade(self):
#		self.factory.numConnections += 1
#		print "Connection made. Number of active connections: {0}".format(self.factory.numConnections)
		print "Connection made"

	def connectionLost(self, reason):
#		self.factory.numConnections -= 1
		print "connection closed"
#		print self.factory.dictFormat
#		print "Connection lost. Number of active connections: {0}".format(self.factory.numConnections)

#	def dataReceived(self, data):
	def dataReceived(self, line):
		data = line
		print "Server received data: {0}".format(data)
		d.addCallback(self.gotIP)
		d.addErrback(self.notIP)
		# d.addCallback(self.checkConnections)
		# d.addErrback(self.failedCheckConnections)
		# d.addCallback(self.thirdMethod)
		# d.addErrback(self.failedThirdMethod)
#		d.callback(data)
		d.callback(line)
		print "fin"

#	def gotIP(self, data):
	def gotIP(self, line):
		self.sendLine("This is LineReceiver")
		time.sleep(1)
		self.sendLine ("I waited a second before sending this message")
# 		print "got data"
# 		data = line ##added for line receiver
# 		dataSplit = [data for data in data.split() if data.strip()]
# 		#dataSplit[0] = piGroup1
# 		#dataSplit[1] = IP address
# 		print dataSplit[0] in self.factory.dictFormat
# 		if (dataSplit[0] in self.factory.dictFormat) == False:
# 			#adds key and a list containing IP address
# 			print "I didn't have this cluster key"
# 			genList = [dataSplit[1]]
# 			self.factory.dictFormat[dataSplit[0]] = genList
# 			print self.factory.dictFormat
# #			self.transport.write("Added your IP \n")
# 			self.sendLine("Added your IP")
# 			print "finished with adding cluster and IP"
# 			#d.callback(data)
# 		elif (dataSplit[0] in self.factory.dictFormat) == True:
# 			#appends new IP to the end of the key's list
# 			print "it's true! I have this cluster in my keys"
# 			print self.factory.dictFormat[dataSplit[0]] #prints out the key values
# 			addIPList = self.factory.dictFormat[dataSplit[0]]
# 			addIPList.append(dataSplit[1])
# 			print addIPList
# 			print self.factory.dictFormat
# 			self.transport.write("Added your IP \r\n")
# 			print "finished with adding new IP to a known cluster"
# 		else:
# 			print "didn't find anything.  Sorry"
# 			d.errback(ValueError("Couldn't process your IP request"))
# 		self.transport.write("IP received \r\n")
		# if data == "true":
		# 	d.callback("True!")
		# else:
		# 	d.errback(ValueError("Nope sorry"))
		#print data

	def notIP(self, failure):
		print "RUNNING NOTIP"
		#sys.stderr.write(str(failure))

	#Need to run through a time expire loop
	def checkConnections(self, data):
		print "This is checkConnections method.  Hello."
		print len(zip(*self.factory.dictFormat.values()))
		numValues = len(zip(*self.factory.dictFormat.values()))
		while numValues < 1:
			numValues = len(zip(*self.factory.dictFormat.values()))
		else:
			print "running checkConnections method"

	def failedCheckConnections(self, failure):
		print "RUNNING failedCheckConnections"
		sys.stderr.write(str(failure))
		print "end of failedCheckConnections"

	def thirdMethod(self, data):
		print "thirdmethod"
		self.transport.write("This is from thirdMethod from the Server \r\n")

	def failedThirdMethod(self, failure):
		print "RUNNING failedThirdMethod"
		sys.stderr.write(str(failure))
		print "end of failedThirdMethod"

if __name__ == '__main__':
	d = defer.Deferred()

	#reactor.listenTCP(8888, DataFactory(), 200, '18.111.45.131')
	reactor.listenTCP(8888, DataFactory(), 200, 'localhost')
	reactor.run()
