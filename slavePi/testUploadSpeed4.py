#Written by Michelle Sit

from twisted.internet import reactor, protocol, defer, threads, task
from twisted.internet.defer import DeferredQueue, DeferredList, DeferredSemaphore
from twisted.internet.task import LoopingCall

import subprocess, sys, os
import glob
import time, datetime

from manualPic_capturePhotos3 import takePictureClass
from videoMode4 import takeVideoClass



#TCP network portion
class DataClientFactory(protocol.ReconnectingClientFactory):
	def __init__(self, data):
		self.data = data

	def buildProtocol(self, addr):
		self.resetDelay()
		return myProtocol(self)

	#TO DO: NEED A BETTER HANDLING METHOD IF THE CONNECTION FAILS
	def clientConnectionFailed(self, connector, reason):
		print 'Connection failed at {0}:'.format(time.strftime("%Y-%m-%d-%H:%M:%S")), reason.getErrorMessage()
		protocol.ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)
		print "RESTARTING WIFI"
		os.system("./restartWifi.sh")

	def clientConnectionLost(self, connector, reason):
		print 'Connection lost at {0}:'.format(time.strftime("%Y-%m-%d-%H:%M:%S")), reason.getErrorMessage()
		print "still recording hopefully. Will stop sending files"
		reactor.stop()

class myProtocol(protocol.Protocol):
	def __init__(self, factory):
		self.factory = factory
		self.recordTimes = []

	def connectionMade(self):
		msg = "clientName piGroup1 {0}".format(piName)
		print msg
		self.transport.write(msg)

	def dataReceived(self, data):
		print "Data received from Server: {0}".format(data)
		msgFromServer = [data for data in data.split()]
		if msgFromServer[0] == "recordTimes":
			self.recordTimes = msgFromServer[1:]
			print "recordTimes: ", self.recordTimes
			self.transport.write("receivedAllTimesReadytoStart")

		elif msgFromServer[0] == "startProgram":
			print "GOT A STARTTAKINGPICTURES"
			#self.ServerResW, self.ServerResH, self.ServerTotalTimeSec, self.ServerFrameRate,  \
			#self.ServerStartTime, serverIP, piName
			if msgFromServer[1] == "video":
				print "this is the video command"
				tv.runUpload = True
				startAtTime = self.calculateTimeDifference(msgFromServer[6], msgFromServer[7])

				self.recordTimes.insert(0, msgFromServer[7])
				self.recordTimes.insert(0, msgFromServer[6])
				print "recordTimes: ", self.recordTimes

				# upload_loop = LoopingCall(threads.deferToThread, self.callUpload)
				# upload_loop.start(60, now=True) #seconds



				# record_loop = LoopingCall(self.method, startAtTime)
				# record_loop.start(30, now=True)

				# deferred1 = defer.Deferred()
				# self.method(startAtTime)
				# deferred2 = defer.Deferred()
				# dl = defer.DeferredList([deferred1, deferred2], consumeErrors=True)
				# deferred1.callback(subprocess.call, "./uploadVideosBash.sh {0} {1}".format(serverIP, serverSaveFilePath))
				# deferred2.callback(tv.takeVideo, int(msgFromServer[2]), int(msgFromServer[3]), int(msgFromServer[4]),\
				#  	int(msgFromServer[5]), startAtTime, serverIP, piName)
				# deferred1.addCallback(lambda _: reactor.callLater(0.5, self.transport.write, 'boo'))
				# deferred2.addCallback(lambda _: reactor.callLater(0.5, self.transport.write, 'finished'))
				# def throwaway(ignored):
				# 	print "Starting deferred"
				# deferred1.callback(throwaway)
				# deferred1.addCallback(lambda _: tv.takeVideo(int(msgFromServer[2]), int(msgFromServer[3]), int(msgFromServer[4]),\
				# 	int(msgFromServer[5]), startAtTime, serverIP, piName))
				# # print "deferred1: ", deferred1
				# deferred1.addErrback(self.failedMethod)
				# def writeFin(ignored):
				# 	self.transport.write("finished")
				# deferred1.addCallback(writeFin)
				# print "sent write finished"
				# deferred1.addErrback(self.failedMethod)
				# deferred1.addCallback(lambda _: self.runFiles(int(msgFromServer[2]), int(msgFromServer[3]), int(msgFromServer[4]),\
				# 	int(msgFromServer[5]), serverIP, piName, self.recordTimes))
				# deferred1.addErrback(self.failedMethod)

				# dl = defer.DeferredList()
				self.runFiles(int(msgFromServer[2]), int(msgFromServer[3]), int(msgFromServer[4]),\
					int(msgFromServer[5]), serverIP, piName, self.recordTimes)

				# jobs = []
				# for runs in range(len(self.recordTimes)/2):
				# 	startAtTime = self.calculateTimeDifference(self.recordTimes.pop(0), self.recordTimes.pop(0))
				# 	jobs.append(self.method(startAtTime))
					# self.method(startAtTime)
					# result = tv.takeVideo(startAtTime)
					# result.addCallback(lambda _: reactor.callLater(0.5, self.transport.write, 'finished'))
					# result.addErrback(self.failedMethod)


				# for runs in range(len(self.recordTimes)/2):
				# 	# print "recordTimes:", recordTimesList
				# 	# recordTimeStartTime = recordTimesList.pop(0) + " " + recordTimesList.pop(0)
				# 	# print "start time: ", recordTimeStartTime
				# 	print "run: ", runs
				# 	startAtTime = self.calculateTimeDifference(self.recordTimes.pop(0), self.recordTimes.pop(0))
				# 	print "callback triggered"
				# 	deferred1.callback(throwaway)
				# 	deferred1.addCallback(lambda _: tv.takeVideo(int(msgFromServer[2]), int(msgFromServer[3]), int(msgFromServer[4]),\
				# 						int(msgFromServer[5]), startAtTime, serverIP, piName))
				# 	deferred1.addErrback(self.failedMethod)
				# 	print "end run"
				# print "boo"


				# result = threads.deferToThread(tv.takeVideo, int(msgFromServer[2]), int(msgFromServer[3]), int(msgFromServer[4]),\
				# 	int(msgFromServer[5]), startAtTime, serverIP, piName)
				# result.addCallback(lambda _: reactor.callLater(0.5, self.transport.write, 'finished'))
				# result.addErrback(self.failedMethod)



				# uploadingThread = threads.deferToThread(subprocess.call, "./uploadVideosBash.sh {0} {1}".format(serverIP, serverSaveFilePath), shell=True)
				# uploadingThread.addCallback(lambda _: reactor.callLater(0.5, self.transport.write, 'boo'))

				# runFiles(int(msgFromServer[2]), int(msgFromServer[3]), int(msgFromServer[4]),\
				# 	int(msgFromServer[5]), startAtTime, serverIP, piName)

				# # result = tv.takeVideo(int(msgFromServer[2]), int(msgFromServer[3]), int(msgFromServer[4]),\
				# 	# int(msgFromServer[5]), startAtTime, serverIP, piName)
				# result = threads.deferToThread(tv.takeVideo, int(msgFromServer[2]), int(msgFromServer[3]), int(msgFromServer[4]),\
				# 	int(msgFromServer[5]), startAtTime, serverIP, piName)
				# result.addCallback(lambda _: reactor.callLater(0.5, self.transport.write, 'finished'))
				# result.addErrback(self.failedMethod)

				# uploadingThread = threads.deferToThread(subprocess.call, "./uploadVideosBash.sh {0} {1}".format(serverIP, serverSaveFilePath), shell=True)
				# uploadingThread.addErrback(self.failedMethodUpload)
				#TODO: How to end upload process once everything is done? How to do error handling?
				#TODO: Fix upload process. Need to make sure the process is uploading everything correctly. What happens if it's interrupted?
				# subprocess.call("./home/pi/uploadVideosBash.sh {0} {1} &".format(serverIP, serverSaveFilePath), shell=True)
				# result.addCallback(lambda _: reactor.callLater(0.5, threads.deferToThread, tv.curlUpload2, serverIP, serverSaveFilePath))
				# result.addCallback(lambda _: reactor.callLater(0.5, threads.deferToThread, self.collectVideos, serverIP, serverSaveFilePath))


			elif msgFromServer[1] == "multiplexer" or msgFromServer[1] == "camera":
				print "this is the {0} method. It has been discontinued. Please exit the program and select video".format(msgFromServer[1])
				reactor.callLater(0.5, self.transport.write, "finished")

		else:
			print "CLIENT: Time: {0}. I don't know what this is: {1}".format(time.strftime("%Y-%m-%d-%H:%M:%S"), data)

	#Manage whole process
	def runFiles(self, resW, resH, totalTimeSec, framerate, serverIP, piName, recordTimesList):
		semi = DeferredSemaphore(1)

		jobs = []
		for runs in range(len(recordTimesList)/2):
			print "recordTimes runFiles:", recordTimesList

			startAtTime = self.calculateTimeDifference(recordTimesList.pop(0), recordTimesList.pop(0))
			jobs.append(semi.run(tv.takeVideo, int(resW), int(resH), int(totalTimeSec),\
					int(framerate), startAtTime, serverIP, piName))

		jobs = DeferredList(jobs)
		print "jobs: ", jobs
		def cbFinished(ignored):
			print 'Finishing job'
			reactor.callLater(0.5, self.transport.write, 'finished\n')
		jobs.addCallback(cbFinished)
		#TRANSPORT WRITE IS NOT BEING CALLED UNTIL THE END.
		return jobs

	# def method(self, startTime):
	# 	# result = threads.deferToThread(tv.takeVideo, int(msgFromServer[2]), int(msgFromServer[3]), int(msgFromServer[4]),\
	# 	# 	int(msgFromServer[5]), startAtTime, serverIP, piName)
	# 	result = threads.deferToThread(tv.takeVideo, startTime)
	# 	result.addCallback(lambda _: reactor.callLater(0.5, self.transport.write, 'finished'))
	# 	result.addErrback(self.failedMethod)


	def failedMethod(self,failure):
		print "FAILURE: ERROR WITH PICTURE TAKING METHOD"
		print failure
		# self.transport.write("CAMERROR {0}".format(piName))
		# os.system('echo "Camera for {1} is broken. Error message: \n {0} \n'\
		# 	'-------end of message --------- \n" | mail -s "Camera Broken" urbanFlowsProject@gmail.com'\
		# 	.format(str(failure), piName))

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

	def callUpload(self):
		# _d = defer.Deferred()
		subprocess.call("./uploadVideosBash.sh {0} {1}".format(serverIP, serverSaveFilePath), shell=True)
		print "finished with this method"
		# return _d

if __name__ == '__main__':
	print sys.argv[1]
	serverIP = sys.argv[1]
	piName = sys.argv[2]
	# serverSaveFilePath = "/media/msit/Seagate\ Backup\ Plus\ Drive/Lobby7/"
	serverSaveFilePath = "/media/senseable-beast/beast-brain-1/Data/OneWeekData/tmp/"
	tp = takePictureClass()
	tv = takeVideoClass()

	#TCP network: Connects on port 8888.
	data = "start"
	reactor.connectTCP(serverIP, 8888, DataClientFactory(data), timeout=200)

	reactor.run()

	