#TCP client code

from twisted.internet import reactor, protocol
import subprocess
import time

#Sets up the Protocol class
class DataClientFactory(protocol.ClientFactory):
	def __init__(self, data):
		self.data = data

	def buildProtocol(self, addr):
		return DataProtocol(self)

	def clientConnectionFailed(self, connector, reason):
		print 'connection failed:', reason.getErrorMessage()
		maybeStopReactor()

	def clientConnectionLost(self, connector, reason):
		print 'connection lost:', reason.getErrorMessage()
		maybeStopReactor()


class DataProtocol(protocol.Protocol):
	def __init__(self, factory):
		self.factory = factory

	def connectionMade(self):
		self.sendData()

	def sendData(self):
		self.transport.write(self.factory.data)
		time.sleep(2)

	def dataReceived(self, data):
		print "Received data:", data
		self.transport.loseConnection()

#Helper method to shutdown process
def maybeStopReactor():
	global data_counter
	data_counter -= 1
	if not data_counter:
		reactor.stop()

def findIPAddress():
	global msg
	print "running findIPAddress"
	ip = subprocess.check_output("hostname --all-ip-addresses", shell=True).decode('utf-8')
	msg = "My IP address is {0}".format(ip)

if __name__ == '__main__':
	findIPAddress()
	datas = ["sending data 1", "sending data 2", msg]

	data_counter = len(datas)

	for data in datas:
		#reactor.connectTCP('18.111.45.131', 8888, DataClientFactory(data), timeout=200)
		reactor.connectTCP('localhost', 8888, DataClientFactory(data), timeout=200)
	reactor.run()