import SimpleHTTPServer
import SocketServer
from zope.interface import implements
from twisted.internet.defer import succeed
from twisted.web.iweb import IBodyProducer

class StringProducer(object):
	implements(IBodyProducer)

	def __init__(self, body):
		print "hi I'm running the StringProducer"
		self.body = body
		self.length = len(body)

	def startProducing(self, consumer):
	    print "hi self"
	    #consumer.write(self.body)
	    consumer.write("hi.  This is the server")
	    clientIP = consumer.getClientIP(self)
	    print clientIP
	    return succeed(None)

	def pauseProducing(self):
		print "running pauseProducing"
		pass

	def stopProducing(self):
		print "running stopProducing"
		pass

PORT = 8000
Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

httpd = SocketServer.TCPServer(("", PORT), Handler)

print "serving at port", PORT
httpd.serve_forever()
httpd.getClientIP()
StringProducer(httpd)