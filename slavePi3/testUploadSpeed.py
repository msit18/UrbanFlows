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
#from manualPic_capturePhotos import takePictures
import os
import glob
import time
import sys

from random import randrange
from twisted.internet.defer import DeferredQueue
from twisted.internet.task import deferLater, cooperate

#Picture taking method
import picamera
import datetime
import string
import numpy as np


#TCP network portion
class DataClientFactory(protocol.ReconnectingClientFactory):
	def __init__(self, data):
		self.data = data

	def buildProtocol(self, addr):
		return myProtocol(self)

	def clientConnectionFailed(self, connector, reason):
		print 'Connection failed at {0}:'.format(time.strftime("%Y-%m-%d-%H:%M:%S")), reason.getErrorMessage()
		for x in range(5):
			protocol.ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)
		else:
			reactor.stop()

	def clientConnectionLost(self, connector, reason):
		print 'Connection lost at {0}:'.format(time.strftime("%Y-%m-%d-%H:%M:%S")), reason.getErrorMessage()
		reactor.stop()

class myProtocol(protocol.Protocol):
	def __init__(self, factory):
		self.factory = factory
		self.fileList = []
		self.name = ""
		self.tag = False
		self.clientParams = ""
		self.resW = 0
		self.resH = 0
		self.framerate = 0
		self.numPics = 0
		self.secondList = []
		self.numPicsTaken = 0
		self.numPicsSent = 0
		self.sendStart = 0

	def connectionMade(self):
		#ip_address = subprocess.check_output("hostname --all-ip-addresses", shell=True).strip()
		#msg = "ip piGroup1 {0}".format(ip_address)
		msg = "ip piGroup1 temp"
		print msg
		self.transport.write(msg)

	def dataReceived(self, data):
		print "Data received from Server: {0}".format(data)
		msgFromServer = [data for data in data.split()]
		if msgFromServer[1] == "startTakingPictures":
			print "GOT A STARTTAKINGPICTURES"
			#TAKING PICTURES IN SEPARATE THREAD. Has errback handling here
			if msgFromServer[2] == "camera":
				print "this is a camera command"
				self.clientParams = "{0} {1} {2} {3} {4} {5}".format(\
				msgFromServer[3], msgFromServer[4],\
				msgFromServer[5], msgFromServer[6], msgFromServer[7], msgFromServer[8])
				print self.clientParams
			elif msgFromServer[2] == "video":
				self.clientParams = "{0} {1} {2} {3} {4}".format(\
				msgFromServer[2], msgFromServer[3], msgFromServer[4],\
				msgFromServer[5], msgFromServer[6])
			print self.clientParams
			# result = threads.deferToThread(self.run, self.clientParams)
			# result.addCallback(self.getFinStatus)
			# result.addErrback(self.failedMethod)
			#STARTS GATHERING PICTURES TO SEND OVER
			print "get list!"
			#self.run(self.clientParams)
			self.getList()
		else:
			print "Didn't write hi success.jpg to server"

	def getFinStatus(self, second):
		print "running GETFINSTATUS!!!!!!!!!!!!!!!!!!!"
		print second #end Token for capturePicture thread
		self.tag = second

	def failedMethod(self,failure):
		print "FAILURE: ERROR WITH PICTURE TAKING METHOD"
		#TODO: FIGURE OUT HOW TO DISTINGUISH BETWEEN DIFFERENT PICAM ERRORS
		self.transport.write("ERROR PICAMERA")
		sys.stderr.write(str(failure))

	def getTagStatus(self):
#		print "SELF TAG: {0}".format(self.tag)
		return self.tag

	def writeToServer(self, msg):
		print "WRITETOSERVER. Write message to server: {0}".format(msg)
		self.transport.write(msg)

#WOULD BE FUN TODO: REPLACE WHILE LOOP WITH PRINTING UPDATES ON FILE TO A GRAPH APPROACH.
#HAVE THE FPS UPDATED AT A CERTAIN TIME FRAME ON A GRAPH IF POSSIBLE.
#FOR DECREASING AMOUNT OF DATA: REPLACE ARRAYS WITH SMARTER MATH SOLUTIONS (KEEP SUM RUNNING)
	def run (self, args):
		try:
			#Specifying arguments for picture parameters
			serverArgs = args
			listServerArgs = [args for args in args.split()]
			self.resW = int(listServerArgs[1])
			self.resH = int(listServerArgs[2])
			self.numPics = int(listServerArgs[3])
			timeInterval = int(listServerArgs[4])
			self.frameRate = int(listServerArgs[5])

			#Keeps track of time for updates 
			timeStart = time.time() #When the program began
			totalTimeSec = int(listServerArgs[0])
			totalTimeMin = int(listServerArgs[0])/60
			timeNow = time.time() #Used to keep track of current time
			timeEnd = totalTimeSec+timeNow #When the program ends
			timePlusInt = timeNow #Keeps track of time increments

			timePlusTwentyMins = timeNow+600
			# print "Capturing {0}p for a total time of {1} min ({2} secs) at {3} "\
			# "frames per {4} second (({5} mins) at {6} framerate ".format(str(resH), \
			# 	str(totalTimeMin), str(totalTimeSec), str(numPics), str(timeInterval), \
			# 	str(float(timeInterval/60)), str(frameRate) )
			#print "TimePlusTwenty = {0}".format(str(timePlusTwentyMins) )
			numPicArray = []
			fpsArray = []
			timeAvg = []
			while timeNow < timePlusTwentyMins and timeNow < timeEnd:
				timeNow = time.time()
				if timeNow >= timePlusTwentyMins:
					endTwenty = time.time()
					twentyTime = endTwenty-timeStart
					twentyFPS = sum(numPicArray)/twentyTime
					#print "10.2 Twenty Min Update: Total number of pictures is {0},"\
					#" total time elapsed is {1}, totalFPS is {2}".format(str(sum(numPicArray)),\
					# str(twentyTime), str(twentyFPS) )
					timePlusTwentyMins = time.time()+600
				else:
					while timeNow > timePlusInt:
						timePlusInt = timeNow + timeInterval
						start=time.time()
						self.piCamTakePictures()
						finish = time.time()
						#Analyzing time and frames
						fpsTime = (finish-start)
						fps = self.numPics/fpsTime
						numPicArray.append(self.numPics)
						fpsArray.append(fps)
						timeAvg.append(fpsTime)
						#print 'Captured {0} frames at {1}fps in {2}secs'\
						#.format( str(sum(numPicArray)), str(self.numPics/(finish-start)), str(finish-start))
			endTime = time.time()
			totalTime = endTime-timeStart
			totalFPS = sum(numPicArray)/totalTime
			#print "10.2: Captured {0} total pictures.  Total time was {1}, total FPS is {2}"\
			#.format(str(sum(numPicArray)), str(totalTime), str(totalFPS) )
			print "CAMERA IS FINISHED. RETURN TRUE"
			return "True"
		except:
			print "noooooooooooooo break"
			print sys.exc_info()[0]
			raise

	def piCamTakePictures(self):
		startPics = time.time()
		print "PICAMTAKEPICTURES RUNNING"
		h = defer.Deferred()
		with picamera.PiCamera() as camera:
			camera.resolution = (self.resW, self.resH)
			camera.framerate = self.frameRate
			v = camera.capture_sequence([
				datetime.datetime.now().strftime ('%M_%S_%f') + '.jpg'
				# datetime.datetime.now().strftime ('%d-%m-%Y-%H_%M_%S_%f') + '_TT'\
				#  + str(listServerArgs[0]) + '_RES' + str(resH) + '_PIC' + str(numPics) +\
				#   '_TI' + str(timeInterval) + '_FR' + str(frameRate) + '.jpg'
				for i in range(self.numPics)
				], use_video_port=True)
			self.numPicsTaken+=1
		self.getList("foo")
		h.addCallback(self.poolingProcess)
		h.callback("FIRE")
		print "END"
		endPics = time.time()
		totalPicsTime = endPics - startPics
		#print "!!!!!!totalPicsTime: ", totalPicsTime

#Pooling process
	def worker(self, jobs):
		while True:
			yield jobs.get().addCallback(self.sendImg)

#TODO: DETERMINE WHAT THE OPTIMAL NUMBER OF PROCESSES TO RUN
#TODO: FIGURE OUT HOW TO TAKE IMAGE + SEND IMAGE AT THE SAME TIME
#TODO: NEED TO FIGURE OUT HOW TO STOP THE PROCESS OR DETERMINE IF THERE ARE ANY
#PICTURES LEFT
#NumPicsSent doesn't work
	# def poolingProcess(self, second):
	# 	startUpload = time.time()
	# 	print "method"
	# 	#print self.numPicsSent
	# 	#print "rest of method"
	# 	self.fileList = glob.glob('*.jpg')

	# 	#print len(self.fileList)
	# 	for i in range(len(self.fileList)):
	# 		#print "self.fileList[i]: ",self.fileList[i]
	# 		jobs.put(self.fileList.pop())

	# 	#TODO: RUN TEST TO FIGURE OUT WHAT THE OPTIMAL NUMBER IS
	# 	for j in range(2):
	# 		cooperate(self.worker(jobs))

	# 	endUpload = time.time()
	# 	UploadPt1Time = endUpload - startUpload
	# 	#print "!!!!!!UploadPt1Time: ", UploadPt1Time

		#Continue
	def getList(self, second):
		self.fileList = glob.glob('*.jpg')
		start = time.time()
		print start
		while len(self.fileList)>0:
			self.name = self.fileList.pop(0)
			jobs.put(self.name)
			for j in range(2):
				cooperate(self.worker(jobs))
			#self.sendImg(self.name)
		else:
			end = time.time()
			print end
			totaltime = end - start
			print "total time was {0}".format(totaltime)

	# def sendName(self):
	# 	#print self.fileList
	# 	print "RUNNING SENDNAME"
	# 	self.fileList = glob.glob('*.jpg')
	# 	self.name = self.fileList.pop(0)
	# 	print "Sending image over: {0}".format(self.name)
	# 	self.sendImg(self.name)

	def sendImg(self, imgName):
		print "RUNNING SENDIMG"
		print "imgName: ", imgName
		self.sendStart = time.time()
		agent = Agent(reactor)
		body = FileBodyProducer(open("/home/pi/UrbanFlows/slavePi3/{0}".format(imgName), 'rb'))
		postImg = agent.request(
		    'POST',
		    "http://18.189.105.211:8880/upload-image",
		    Headers({'User-Agent': ['Twisted Web Client Example'],
		    		'Content-Type': ['text/x-greeting'],
		    		'fileName': ['{0}'.format(imgName)]}),
		    body)
		self.numPicsSent+=1
		#print self.numPicsSent
		sendEnd = time.time()
		sendTotal = sendEnd - self.sendStart
		#print "!!!!!!Send Time: ", sendTotal
		postImg.addCallback(self.cbRequest)
		postImg.addErrback(self.failedMethod)

	def cbRequest(self, response):
		cbRequestTime = time.time()
		print 'Response code:', response.code
		if response.code == 200:
			#print "yes"
			#print self.numPicsSent
			CallbackTime = cbRequestTime - self.sendStart
			#print "!!!!!!CallbackTime: ", CallbackTime
		else:
			print "no"


if __name__ == '__main__':
	#f = open('ClientLog-{0}.txt'.format(time.strftime("%Y-%m-%d-%H:%M:%S")), 'w')
#	t1 = takePictures()

	jobs = DeferredQueue()

	#TCP network: Connects on port 8888. HTTP network: Connects on port 8880
	data = "start"
	reactor.connectTCP('18.189.105.211', 8888, DataClientFactory(data), timeout=200)

	reactor.run()

	
