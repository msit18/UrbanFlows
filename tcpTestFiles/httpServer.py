#Written by Michelle Sit
#Many thanks to Vlatko Klabucar for helping me with the HTTP part!  Also many thanks to Nahom Marie
#for helping me with the architecture of this system!

from twisted.internet.protocol import Factory
from twisted.internet import reactor, protocol, defer
import time, sys

from twisted.web.server import Site
from twisted.web.resource import Resource

import cgi

#sets up the Protocol class
class HTTPDataFactory(Factory):
	numConnections = 0

	def __init__(self, data=None):
		self.data = data

	def buildProtocol(self, addr):
		root = Resource()
		root.putChild("upload-image", c)
		factory = Site(root)
		return HTTPDataProtocol(self, d)

class HTTPDataProtocol (protocol.Protocol):

	def __init__(self, factory, d):
		self.factory = factory
		self.d = defer.Deferred()
		self.imgName = ""

	def connectionMade(self):
		self.factory.numConnections += 1
		print "Connection made. Number of active connections: {0}".format(self.factory.numConnections)

	def connectionLost(self, reason):
		self.factory.numConnections -= 1
		print dictFormat
		print "Connection lost. Number of active connections: {0}".format(self.factory.numConnections)

	def dataReceived(self, data):
		print "Server received data: {0}".format(data)
		self.transport.write("Thanks!")

	def render_GET(self, request):
		print "getting"
		return '<html><body><p>This is the server for the MIT SENSEable City Urban Flows Project.'\
		'  It receives images and saves them to the server.</p></body></html>'

	def render_POST(self, request):
		print "Posting: {0}".format(self.imgName)
		# file = open("uploaded-image.jpg","wb")
		# file = open(imgName, "wb")
		# file.write(request.content.read())
		return '<html><body>Image uploaded :) </body></html>'

if __name__ == '__main__':
	d = defer.Deferred()
	b = HTTPDataFactory()
	c = HTTPDataProtocol(HTTPDataFactory, d)

	#reactor.listenTCP(8888, b, 200, 'localhost')

	# root = Resource()
	# root.putChild("upload-image", c)
	# factory = Site(root)
	#reactor.listenTCP(8880, b, 200, 'localhost')

	reactor.run()

	reactor.listenTCP(8000, DataFactory(), 200, '10.0.0.6')
