#Written by Michelle Sit
#Many thanks to Vlatko Klabucar for helping me with the HTTP part!  Also many thanks to Nahom Marie
#for helping me with the architecture of this system!

#TCP
from twisted.internet import reactor, protocol, defer, threads
import subprocess
#HTTP
#from twisted.web.client import Agent
#from twisted.web.http_headers import Headers
#from twisted.web.client import FileBodyProducer

#Threading for picture transfer
from manualPic_capturePhotos3 import takePictureClass
from videoMode3 import takeVideoClass
import os
import glob
import time
import sys

from twisted.internet.defer import DeferredQueue

#Picture taking method
import datetime


#TCP network portion
class DataClientFactory(protocol.ReconnectingClientFactory):
	def __init__(self, data):
		self.data = data

	def buildProtocol(self, addr):
		self.resetDelay()
		return myProtocol(self)

	def clientConnectionFailed(self, connector, reason):
		print 'Connection failed at {0}:'.format(time.strftime("%Y-%m-%d-%H:%M:%S")), reason.getErrorMessage()
		print "TWISTED CONNECTING METHOD"
		protocol.ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)
		print "RESTARTING WIFI"
		os.system("./restartWifi.sh")

	def clientConnectionLost(self, connector, reason):
		print 'Connection lost at {0}:'.format(time.strftime("%Y-%m-%d-%H:%M:%S")), reason.getErrorMessage()
		reactor.stop()

class myProtocol(protocol.Protocol):
	def __init__(self, factory):
		self.factory = factory

	def connectionMade(self):
		#ip_address = subprocess.check_output("hostname --all-ip-addresses", shell=True).strip()
		#msg = "ip piGroup1 {0}".format(ip_address)
		msg = "ip piGroup1 {0}".format(piName)
		print msg
		self.transport.write(msg)

	def dataReceived(self, data):
		print "Data received from Server: {0}".format(data)
		msgFromServer = [data for data in data.split()]
		if msgFromServer[0] == "startProgram":
			print "GOT A STARTTAKINGPICTURES"
			#inputTotalTime(1), inputResW(2), inputResH(3), inputNumPics(4), inputFPSTimeInterval(5), inputFramerate(6), inputStartTime(7)
			if msgFromServer[1] == "camera":
				print "this is a camera command"
				tp.runUpload = True
				startAtTime = self.calculateTimeDifference(msgFromServer[8], msgFromServer[9])
				callLaterTimeCollectImgs = startAtTime + 1
				result = threads.deferToThread(tp.takePicture_filenames, int(msgFromServer[2]), int(msgFromServer[3]),\
					int(msgFromServer[4]), int(msgFromServer[7]), startAtTime)
				result.addErrback(self.failedMethod)
				endOfProcess = tp.sendUpload(callLaterTimeCollectImgs, serverIP)
				print endOfProcess
				result.addCallback(lambda _: reactor.callLater(0.5, self.transport.write, endOfProcess))
			
			#self.ServerVidTimeSec (2), self.ServerResW (3),\
			#self.ServerResH (4), self.ServerFrameRate (5), \
			#self.ServerStartTime (6) (7)
			elif msgFromServer[1] == "video":
				print "this is the video command"
				tv.runUpload = True
				#WHAT IS THIS? HOW DO I TAKE CARE OF THIS?
				startAtTime = self.calculateTimeDifference(msgFromServer[7], msgFromServer[8])
				callLaterTimeCollectImgs = startAtTime + 1
				result = threads.deferToThread(tp.takeVideo, int(msgFromServer[2]), int(msgFromServer[3]), int(msgFromServer[4]),\
					int(msgFromServer[5]), int(msgFromServer[6]), startAtTime)
				result.addErrback(self.failedMethod)
				endOfProcess = tv.sendUpload(callLaterTimeCollectImgs, serverIP)
				print endOfProcess
				result.addCallback(lambda _: reactor.callLater(0.5, self.transport.write, endOfProcess))

			elif msgFromServer[1] == "multiplexer":
				print "this is the multiplexer method. Has not been implemented"
				reactor.callLater(0.5, self.transport.write, "finished")

		elif msgFromServer[0] == "checkCamera":
			startAtTime = self.calculateTimeDifference(msgFromServer[1], msgFromServer[2])
			callLaterTimeCollectImgs = startAtTime + 1
			result = threads.deferToThread(tp.takePicture_filenames, 2, 640, 480, 1, startAtTime)
			result.addCallback(lambda _: reactor.callLater(0.5, self.transport.write, "checkCamPi"))
			result.addErrback(self.failedMethod)
			tp.sendUpload(callLaterTimeCollectImgs, serverIP)

		else:
			print "Didn't write hi success.jpg to server"

	def printSome (self, inputHere):
		print "PRINTSOME: ", inputHere

	def failedMethod(self,failure):
		print "FAILURE: ERROR WITH PICTURE TAKING METHOD"
		self.transport.write("CAMERROR {0}".format(piName))
		os.system('echo "Camera for {1} is broken. Error message: \n {0} \n'\
			'-------end of message --------- \n" | mail -s "Camera Broken" msit@wellesley.edu'\
			.format(str(failure), piName))

	def calculateTimeDifference(self, dateToEnd, timeToEnd):
		fullString = dateToEnd + " " + timeToEnd
		endTime = datetime.datetime.strptime(fullString, "%x %X")
		nowTime = datetime.datetime.today()
		difference = endTime - nowTime
		return time.time() + difference.total_seconds()

if __name__ == '__main__':
	jobs = DeferredQueue()
	print sys.argv[1]
	serverIP = sys.argv[1]
	piName = sys.argv[2]
#	serverIP = "18.189.104.190"
	tp = takePictureClass()
	tv = takeVideoClass()

	#TCP network: Connects on port 8888. HTTP network: Connects on port 8880
	data = "start"
	reactor.connectTCP(serverIP, 8888, DataClientFactory(data), timeout=200)

	reactor.run()

	