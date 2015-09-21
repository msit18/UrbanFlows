from twisted.internet import reactor
from twisted.web.client import Agent
from twisted.web.http_headers import Headers

from stringprod import StringProducer

agent = Agent(reactor)

d = agent.request("GET", "http://localhost:8880/upload-image")

#body = StringProducer("hello, world")
# d = agent.request(
#     'GET',
#     'http://localhost:8880/upload-image',
#     Headers({'User-Agent': ['Twisted Web Client Example'],
#              'Content-Type': ['text/x-greeting']}),
#     body)

# def cbResponse(ignored):
#     print 'Response received'
def cbResponse(response):
	print response

d.addCallback(cbResponse)

def cbShutdown(ignored):
    reactor.stop()
d.addBoth(cbShutdown)

reactor.run()