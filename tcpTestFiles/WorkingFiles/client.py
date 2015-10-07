#Written by Vlatko Klabucar.  Fixed by Michelle Sit

import sys

from twisted.internet import reactor
from twisted.web.client import Agent
from twisted.web.http_headers import Headers

from StringIO import StringIO
from twisted.web.client import FileBodyProducer

class method(Agent):
	def __init__(self, agent):
		self.agent = agent

	def thing(self):
		#agent = Agent(reactor)
		body = FileBodyProducer(open("./cute_otter.jpg", 'rb'))

		d = agent.request(
		    'POST',
		    "http://localhost:8888/upload-image",
		    Headers({'User-Agent': ['Twisted Web Client Example'],
		    		'Content-Type': ['text/x-greeting']}),
		    body)

		d.addCallback(self.cbResponse)
		d.addBoth(self.cbShutdown)

		#reactor.run()

	def cbResponse(self, response):
	    print response

	def cbShutdown(self, ignored):
	    reactor.stop()

if __name__ == '__main__':
	global agent
	agent = Agent(reactor)

	c = method(agent)
	c.thing()
	reactor.run()


# #Working copy of the program:
# agent = Agent(reactor)

# #file = open("./cute_otter.jpg", 'rb')

# # d = agent.request(
# #     'POST',
# #     "http://" + sys.argv[1] + ":8880/upload-image",
# #     Headers({'Content-Type': ['image/jpeg']}),
# #     file.read())

# body = FileBodyProducer(open("./cute_otter.jpg", 'rb'))

# d = agent.request(
#     'POST',
#     "http://localhost:8888/upload-image",
#     Headers({'User-Agent': ['Twisted Web Client Example'],
#     		'Content-Type': ['text/x-greeting']}),
#     body)

# def cbResponse(response):
#     print response
# d.addCallback(cbResponse)

# def cbShutdown(ignored):
#     reactor.stop()
# d.addBoth(cbShutdown)

# reactor.run()