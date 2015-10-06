#Written by Vlatko Klabucar.

#TODO: needs to be debugged

import sys

from twisted.internet import reactor
from twisted.web.client import Agent
from twisted.web.http_headers import Headers

from StringIO import StringIO
from twisted.web.client import FileBodyProducer

agent = Agent(reactor)

#file = open("./cute_otter.jpg", 'rb')

# d = agent.request(
#     'POST',
#     "http://" + sys.argv[1] + ":8880/upload-image",
#     Headers({'Content-Type': ['image/jpeg']}),
#     file.read())

body = FileBodyProducer(open("./cute_otter.jpg", 'rb'))

d = agent.request(
    'POST',
    "http://localhost:8880/upload-image",
    Headers({'User-Agent': ['Twisted Web Client Example'],
    		'Content-Type': ['text/x-greeting']}),
    body)

def cbResponse(response):
    print response
d.addCallback(cbResponse)

def cbShutdown(ignored):
    reactor.stop()
d.addBoth(cbShutdown)

reactor.run()




