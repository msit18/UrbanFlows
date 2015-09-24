#Written by Vlatko Klabucar.

#TODO: needs to be debugged

mport sys

from twisted.internet import reactor
from twisted.web.client import Agent
from twisted.web.http_headers import Headers

agent = Agent(reactor)

file = open("./cute_otter.jpg", 'rb')

d = agent.request(
    'POST',
    "http://" + sys.argv[1] + ":8880/upload-image",
    Headers({'Content-Type': ['image/jpeg']}),
    file.read())

def cbResponse(response):
    print response
d.addCallback(cbResponse)

def cbShutdown(ignored):
    reactor.stop()
d.addBoth(cbShutdown)

reactor.run()




