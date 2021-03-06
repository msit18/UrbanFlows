#Still being written: TCP client that runs with callbackServer3

#Written by Michelle Sit
#Many thanks to Vlatko Klabucar for helping me with the HTTP part!  Also many thanks to Nahom Marie
#for helping me with the architecture of this system!

#TCP
from twisted.internet import reactor, protocol, defer, threads
import subprocess
#HTTP
from twisted.web.client import Agent
from twisted.web.http_headers import Headers
from twisted.web.client import FileBodyProducer

#Threading for picture transfer
from manualPic_capturePhotos import takePictures
#from doSomeRandom import doSomeRandom
import os
import glob
import time
import sys

#TCP network portion
class DataClientFactory(protocol.ReconnectingClientFactory):
	def __init__(self, data):
		self.data = data

	def buildProtocol(self, addr):
		return myProtocol(self)

	def clientConnectionFailed(self, connector, reason):
		print >>f, 'Connection failed at {0}:'.format(time.strftime("%Y-%m-%d-%H:%M:%S")), reason.getErrorMessage()
		ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)
		#reactor.stop()

	def clientConnectionLost(self, connector, reason):
		print >>f, 'Connection lost at {0}:'.format(time.strftime("%Y-%m-%d-%H:%M:%S")), reason.getErrorMessage()
		reactor.stop()

class myProtocol(protocol.Protocol):
	def __init__(self, factory):
		self.factory = factory
		self.fileList = []
		self.name = ""
		self.tag = False
		self.clientParams = ""

	def connectionMade(self):
		ip_address = subprocess.check_output("hostname --all-ip-addresses", shell=True).strip()
		msg = "ip piGroup1 {0}".format(ip_address)
		print >>f, msg
		self.transport.write(msg)

	def dataReceived(self, data):
		print >>f, "Data received from Server: {0}".format(data)
		msgFromServer = [data for data in data.split()]
		if msgFromServer[1] == "startTakingPictures":
			print "GOT A STARTTAKINGPICTURES"
			#TAKING PICTURES IN SEPARATE THREAD. Has errback handling here
			#added callback to notify when finished
			if msgFromServer[2] == "camera":
				self.clientParams = "{0} {1} {2} {3} {4} {5} {6}".format(\
				msgFromServer[2], msgFromServer[3], msgFromServer[4],\
				msgFromServer[5], msgFromServer[6], msgFromServer[7], msgFromServer[8])
			elif msgFromServer[2] == "video":
				self.clientParams = "{0} {1} {2} {3} {4}".format(\
				msgFromServer[2], msgFromServer[3], msgFromServer[4],\
				msgFromServer[5], msgFromServer[6])
			print >>f, self.clientParams
			#result = threads.deferToThread(y.capturePictures)
			result = threads.deferToThread(t1.run)
			result.addCallback(self.getFinStatus)
			result.addErrback(self.failedMethod)
			#STARTS GATHERING PICTURES TO SEND OVER
			self.getList("thing")
		elif msgFromServer[1] == "gotNameSendImg":
			print "RECEIVED GOTNAMESENDIMG"
			e = self.sendImg()
			e.addCallback(self.getList)
			e.addErrback(self.failedMethod)
			e.callback("thing")
		else:
			print "Didn't write hi success.jpg to server"

	def getFinStatus(self, second):
		print "running GETFINSTATUS"
		print second #end Token for capturePicture thread
		self.tag = second

	def failedMethod(self,failure):
		print >>f, "FAILURE: ERROR WITH PICTURE TAKING METHOD"
		#TODO: FIGURE OUT HOW TO DISTINGUISH BETWEEN DIFFERENT PICAM ERRORS
		self.transport.write("ERROR PICAMERA")
		sys.stderr.write(str(failure))

	def getTagStatus(self):
		print "running GETTAGSTATUS"
		print "SELF TAG: {0}".format(self.tag)
		return self.tag

	def getList(self, second):
		self.fileList = glob.glob('*.jpg')
		self.tag = self.getTagStatus()
		if len(self.fileList) > 0:
			print "GLOB HAS PICTURES. SENDING NAME"
			self.sendName()
		else:
			#len has no pictures and self tag is false
			while self.tag == False:
				print "GLOB HAS NO PICTURES AND TAG IS FALSE. RUNNING CHECK"
				self.fileList = glob.glob('*.jpg')
				self.tag = self.getTagStatus() #TODO: Will this work for Raspi?
			#len has no pictures and self tag is true
			else:
				print "GLOB HAS NO PICTURES AND TAG IS TRUE. SLEEP"
				self.fileList = glob.glob('*.jpg')
				if len(self.fileList) > 0:
					print "UP DATE FOUND PICTURES. SENDING NAME"
					self.sendName()
				elif len(self.fileList) <= 0:
					print "UP DATE DIDN'T FIND ANYTHING. REACTOR STOP"
					print "FINISHED WRITING IMAGE"
					self.transport.write("finished")

	def sendName(self):
		print self.fileList
		self.name = self.fileList.pop(0)
		print "Sending name over: {0}".format(self.name)
		print "fileLen is: {0}".format(len(self.fileList))
		reactor.callLater(0.1, self.transport.write, "imgName {0}".format(self.name))

	def sendImg(self):
		print "RUNNING SENDIMG"
		e = defer.Deferred()
		print self.name
		agent = Agent(reactor)
		body = FileBodyProducer(open("/home/pi/UrbanFlows/tcpTestFiles/WorkingFiles/{0}".format(self.name), 'rb'))
		postImg = agent.request(
		    'POST',
		    "http://localhost:8880/upload-image",
		    Headers({'User-Agent': ['Twisted Web Client Example'],
		    		'Content-Type': ['text/x-greeting']}),
		    body)
		os.system('rm {0}'.format(self.name))
		print 'finished writing img'
		return e

if __name__ == '__main__':
	f = open('ClientLog-{0}.txt'.format(time.strftime("%Y-%m-%d-%H:%M:%S")), 'w')
	t1 = takePictures()
	
	#TCP network. Connects on port 8888. HTTP network. Connects on port 8880
	data = "start"
	reactor.connectTCP('18.111.103.156', 8888, DataClientFactory(data), timeout=200)

	#y = doSomeRandom()

	reactor.run()

	
