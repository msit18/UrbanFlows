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
from videoMode4 import takeVideoClass
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
		self.runUploadVideo = False
		self.fileList = []

	def connectionMade(self):
		#ip_address = subprocess.check_output("hostname --all-ip-addresses", shell=True).strip()
		#msg = "ip piGroup1 {0}".format(ip_address)
		msg = "clientName piGroup1 {0}".format(piName)
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
			
			#self.ServerResW (2),\
			#self.ServerResH (3), self.ServerTotalTimeSec (4), self.ServerFrameRate (5),  \
			#self.ServerStartTime (6), serverIP (7), piName (8)
			elif msgFromServer[1] == "video":
				print "this is the video command"
				tv.runUpload = True
				startAtTime = self.calculateTimeDifference(msgFromServer[6], msgFromServer[7])
				result = threads.deferToThread(tv.takeVideo, int(msgFromServer[2]), int(msgFromServer[3]), int(msgFromServer[4]),\
					int(msgFromServer[5]), startAtTime, serverIP, piName)
				result.addErrback(self.failedMethod)
				result.addCallback(lambda _: reactor.callLater(0.5, self.transport.write, 'finished'))
				uploadingThread = threads.deferToThread(subprocess.call, "./uploadVideosBash.sh {0} {1}".format(serverIP, serverSaveFilePath), shell=True)
				uploadingThread.addErrback(self.failedMethodUpload)
				
				#TODO: How to end upload process once everything is done? How to do error handling?


				# subprocess.call("./home/pi/uploadVideosBash.sh {0} {1} &".format(serverIP, serverSaveFilePath), shell=True)
				# result.addCallback(lambda _: reactor.callLater(0.5, threads.deferToThread, tv.curlUpload2, serverIP, serverSaveFilePath))
				# result.addCallback(lambda _: reactor.callLater(0.5, threads.deferToThread, self.collectVideos, serverIP, serverSaveFilePath))

			elif msgFromServer[1] == "multiplexer":
				print "this is the multiplexer method. Has not been implemented"
				reactor.callLater(0.5, self.transport.write, "finished")

		elif msgFromServer[0] == "checkCamera":
			# startAtTime = self.calculateTimeDifference(msgFromServer[1], msgFromServer[2])
			# callLaterTimeCollectImgs = startAtTime + 1
			# result = threads.deferToThread(tp.takePicture_filenames, 2, 640, 480, 1, startAtTime)
			# result.addCallback(lambda _: reactor.callLater(0.5, self.transport.write, "checkCamPi"))
			# result.addErrback(self.failedMethod)
			# tp.sendUpload(callLaterTimeCollectImgs, serverIP)
			self.transport.write("checkCamPi")
			print "run the thing"

		else:
			print "Didn't write hi success.jpg to server"


	def failedMethod(self,failure):
		print "FAILURE: ERROR WITH PICTURE TAKING METHOD"
		self.transport.write("CAMERROR {0}".format(piName))
		os.system('echo "Camera for {1} is broken. Error message: \n {0} \n'\
			'-------end of message --------- \n" | mail -s "Camera Broken" urbanFlowsProject@gmail.com'\
			.format(str(failure), piName))

	def failedMethodUpload(self, failure):
		print "FAILURE: ERROR WITH UPLOADING METHOD"
		self.transport.write("UPLOADERROR {0}".format(piName))
		os.system('echo "Upload method for {1} is broken. Error message: \n {0} \n'\
			'-------end of message --------- \n" | mail -s "Upload Broken" urbanFlowsProject@gmail.com'\
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
	# serverSaveFilePath = "/media/msit/Seagate\ Backup\ Plus\ Drive/Lobby7/"
	serverSaveFilePath = "/media/senseable-beast/beast-brain-1/Data/OneWeekData/tmp/"
	tp = takePictureClass()
	tv = takeVideoClass()

	#TCP network: Connects on port 8888. HTTP network: Connects on port 8880
	data = "start"
	reactor.connectTCP(serverIP, 8888, DataClientFactory(data), timeout=200)

    # loop_upload = LoopingCall(tv.thing_that_does_http)
    # loop_upload.start(10)

	reactor.run()

	