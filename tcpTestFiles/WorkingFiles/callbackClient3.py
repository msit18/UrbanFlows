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
import threading
import Queue
import os
import glob
import time
import sys
#import manualPic_capturePhotos
from doSomeRandom import doSomeRandom

#TCP network portion
class DataClientFactory(protocol.ClientFactory):
	def __init__(self, data):
		self.data = data

	def buildProtocol(self, addr):
		return myProtocol(self)

	def clientConnectionFailed(self, connector, reason):
		print 'connection failed:', reason.getErrorMessage()
		reactor.stop()

	def clientConnectionLost(self, connector, reason):
		print 'connection lost:', reason.getErrorMessage()
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
		self.transport.write(msg)

	def dataReceived(self, data):
		print "data Received from Server: {0}".format(data)
		msgFromServer = [data for data in data.split()]
		if msgFromServer[1] == "startTakingPictures":
			#STARTS IMAGE TAKING PROCESS
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
			print self.clientParams
			result = threads.deferToThread(y.capturePictures)
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

	def failedMethod(self,failure):
		print "FAILURE: failedMethod"
		sys.stderr.write(str(failure))

	def getFinStatus(self, second):
		print "running GETFINSTATUS"
		print second #end Token for capturePicture thread
		self.tag = second

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
		else: #len has no pictures
			#len has no pictures and self tag is false
			while self.tag == False:
					print "GLOB HAS NO PICTURES AND TAG IS FALSE. RUNNING CHECK"
					self.fileList = glob.glob('*.jpg')
					self.tag = self.getTagStatus()
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
		reactor.callLater(0.1, self.transport.write, " imgName {0}".format(self.name))

	def sendImg(self):
		print "RUNNING SENDIMG"
		e = defer.Deferred()
		print self.name
		agent = Agent(reactor)
		body = FileBodyProducer(open("/home/michelle/gitFolder/UrbanFlows/tcpTestFiles/WorkingFiles/{0}".format(self.name), 'rb'))
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
	#HTTP network.  Connects on port 8880

	#reactor.connectTCP('18.111.45.131', 8888, DataClientFactory(data), timeout=200)

	#manualPic setup
	f = open('manualPic5Output.txt', 'w')
	# t1 = manualPic_capturePhotos.takePictures(queue, f)
	
	#TCP network.  Connects on port 8888
	data = "first data"
	reactor.connectTCP('localhost', 8888, DataClientFactory(data), timeout=200)

	y = doSomeRandom()

	reactor.run()