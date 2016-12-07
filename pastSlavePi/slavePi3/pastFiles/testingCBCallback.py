from twisted.internet import reactor
from twisted.internet.defer import Deferred, DeferredList
from twisted.internet.protocol import Protocol
from twisted.web.client import Agent, HTTPConnectionPool

class IgnoreBody(Protocol):
    def __init__(self, deferred):
        self.deferred = deferred

    def dataReceived(self, bytes):
        pass

    def connectionLost(self, reason):
        self.deferred.callback(None)


def cbRequest(response):
    print 'Response code:', response.code
    finished = Deferred()
    response.deliverBody(IgnoreBody(finished))
    return finished

pool = HTTPConnectionPool(reactor)
agent = Agent(reactor, pool=pool)

def requestGet(url):
    d = agent.request('GET', url)
    d.addCallback(cbRequest)
    return d

# Two requests to the same host:
d = requestGet('http://localhost:8880/upload-image').addCallback(
    lambda ign: requestGet("http://localhost:8880/upload-image"))
def cbShutdown(ignored):
    reactor.stop()
d.addCallback(cbShutdown)

reactor.run()