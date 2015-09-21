import sys

from twisted.internet import reactor
from twisted.web.client import Agent
from twisted.web.http_headers import Headers

from stringprod import StringProducer

agent = Agent(reactor)

file = open("/home/michelle/gitFolder/UrbanFlows/tcpTestFiles/cute_otter.jpg", 'rb')

d = agent.request(
    'POST',
    "http://" + sys.argv[1] + ":8000/upload-image",
    Headers({'Content-Type': ['image/jpeg']}),
    file.read())

def cbResponse(response):
	print "Yes this is response"
	print response
#d.addCallback(cbResponse)

def cbShutdown(ignored):
    reactor.stop()
#d.addBoth(cbShutdown)

body = StringProducer("this is my own script")

e = agent.request(
	'GET',
    "http://localhost:8000/upload-image",
    Headers({'User-Agent': ['Twisted Web Client Example'],
            'Content-Type': ['text/x-greeting']}),
    None)

e.addCallback(cbResponse)
e.addBoth(cbShutdown)

reactor.run()