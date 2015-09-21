from pprint import pformat

from twisted.internet import reactor
from twisted.internet.defer import Deferred
from twisted.internet.protocol import Protocol
from twisted.web.client import Agent
from twisted.web.http_headers import Headers

class BeginningPrinter(Protocol):
    def __init__(self, finished):
        self.finished = finished
        self.remaining = 1024 * 10

    def connectionMade(self):
        print "I made a connection with the server"

    def dataReceived(self, bytes):
        print "running dataReceived"
        if self.remaining:
            display = bytes[:self.remaining]
            print 'Some data received:'
            print display
            self.remaining -= len(display)

    def connectionLost(self, reason):
        print 'Finished receiving body:', reason.getErrorMessage()
        self.finished.callback(None)

def cbRequest(response):
    print 'Response version:', response.version
    print 'Response code:', response.code
    print 'Response phrase:', response.phrase
    print 'Response headers:'
    print pformat(list(response.headers.getAllRawHeaders()))
    finished = Deferred()
    response.deliverBody(BeginningPrinter(finished))
    return finished

def cbShutdown(ignored):
    reactor.stop()

if __name__ == '__main__':
    #beginning of the code
    agent = Agent(reactor)
    #file = open("cute_otter.jpg", 'rb')
    #print file
    d = agent.request(
        'OTHER',
        'http://localhost:8880/upload-image',
        Headers({'User-Agent': ['Twisted Web Client Example']}),
        None)
    # d = agent.request(
    #     'POST',
    #     "http://localhost:8880/upload-image",
    #      Headers({'User-Agent': ['Twisted Web Client Example'],
    #         'Content-Type': ['image/jpg']}),
    #     file.read())
    d.addCallback(cbRequest)
    d.addBoth(cbShutdown)
    reactor.run()