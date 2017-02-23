#Written by Michelle Sit

from twisted.internet import reactor, protocol, defer, threads, task
from twisted.internet.defer import DeferredList, DeferredSemaphore
from twisted.internet.task import LoopingCall

import subprocess, sys, os
import glob
import time, datetime

from manualPic_capturePhotos3 import takePictureClass
from videoMode4 import TakeVideoClass
from uploadScript import UploadClass


class DataClientFactory(protocol.ReconnectingClientFactory):
	def __init__(self, data):
		self.data = data

	def buildProtocol(self, addr):
		self.resetDelay()
		return myProtocol(self)

	#This method runs if the connection to the internet has been severed or if it cannot connect to the server
	def clientConnectionFailed(self, connector, reason):
		print  'CONNECTION ERROR: Connection failed at {0}: {1}'.format(time.strftime("%Y-%m-%d-%H:%M:%S"), reason.getErrorMessage())
		file.write('CONNECTION ERROR: Connection failed at {0}:'.format(time.strftime("%Y-%m-%d-%H:%M:%S")) + "\n")
		if serverIP != "18.89.4.173":
			print  "IP ERROR: This is the wrong IP address. Try again!"
			file.write("IP ERROR: This is the wrong IP address. Try again!" + "\n")
			reactor.stop()
		else:
			self.fixWifi()

	def fixWifi(self):
		checkWifiDown = subprocess.call("[\"$(/bin/ping -c 3 8.8.8.8)\"]", shell=True)
		print  "checkWifiDown ", checkWifiDown
		file.write("checkWifiDown " + str(checkWifiDown) + "\n")
		if int(checkWifiDown) == 2:
			print  "SERVER ERROR: Wifi is working. Check that the server is running."
			file.write("SERVER ERROR: Wifi is working. Check that the server is running." + "\n")
			reactor.stop()
		else:
			print  "---------------Wifi is not working. Restarting wifi process."
			file.write("---------------Wifi is not working. Restarting wifi process." + "\n")
			restartWifiTries = 0
			while restartWifiTries < 4:
				print "---------------Num times tried to restart wifi: {0}/3".format(restartWifiTries)
				file.write("---------------Num times tried to restart wifi: {0}/3".format(restartWifiTries) + "\n")
				_checkWifiDown = self.restartWifi()
				print  "_checkWifiDown second time: ", _checkWifiDown
				file.write("_checkWifiDown second time: ", str(_checkWifiDown) + "\n")
				if int(_checkWifiDown) == 2:
					print  "Reconnected successfully. Connecting to server again."
					file.write("Reconnected successfully. Connecting to server again." + "\n")
					reactor.connectTCP(serverIP, 8888, DataClientFactory(data), timeout=200)
					break
				else:
					print "---------------Wifi did not connect. Restarting again."
					file.write("---------------Wifi did not connect. Restarting again." + "\n")
					restartWifiTries += 1
			else:
				print  "WIFI ERROR: Could not connect to the internet."
				file.write("WIFI ERROR: Could not connect to the internet." + "\n")
				# reactor.stop()

	def restartWifi(self):
		subprocess.call("sudo ifdown eth0; sudo ifdown wlan0; sudo ifup wlan0; sudo ifup eth0", shell=True)
		print  "sleeping..."
		file.write("sleeping..." + "\n")
		time.sleep(10)
		return subprocess.call("[\"$(/bin/ping -c 3 8.8.8.8)\"]", shell=True)

	def connEmailError(self, piName, errorMsg):
		os.system('echo "Connection for {0} was lost at {2}. Error message: \n {1} \n'\
			'-------end of message --------- \n" | mail -s "ConnectionLost" urbanFlowsProject@gmail.com'\
			.format(piName, errorMsg, time.strftime("%Y-%m-%d-%H:%M:%S")))

	#This method runs if the connection to the server has been severed
	def clientConnectionLost(self, connector, reason):
		print  'Connection lost at {0}:'.format(time.strftime("%Y-%m-%d-%H:%M:%S")), reason.getErrorMessage()
		file.write('Connection lost at {0}:'.format(time.strftime("%Y-%m-%d-%H:%M:%S")) + str(reason.getErrorMessage()) + "\n")
		print  "CONNECTION ERROR: Connection has been lost but still recording hopefully. Will stop sending files"
		file.write("CONNECTION ERROR: Connection has been lost but still recording hopefully. Will stop sending files")
		self.connEmailError(piName, "CONNECTION LOST: {0}".format(reason.getErrorMessage()) + "\n")

class myProtocol(protocol.Protocol):
	def __init__(self, factory):
		self.factory = factory
		self.recordTimes = []

	def connectionMade(self):
		msg = "clientName piGroup1 {0}\n".format(piName)
		print  msg
		file.write(msg + "\n")
		self.transport.write(msg)

	def dataReceived(self, data):
		print  "Data received from Server: {0}".format(data)
		file.write("Data received from Server: {0}".format(data) + "\n")
		msgFromServer = [data for data in data.split()]
		if msgFromServer[0] == "recordTimes":
			self.recordTimes = msgFromServer[1:]
			# print "recordTimes: ", self.recordTimes
			self.transport.write("receivedAllTimesReadytoStart\n")

		elif msgFromServer[0] == "startProgram":
			print  "GOT A STARTTAKINGPICTURES"
			file.write("GOT A STARTTAKINGPICTURES" + "\n")
			#self.ServerResW, self.ServerResH, self.ServerTotalTimeSec, self.ServerFrameRate,  \
			#self.ServerStartTime, serverIP, piName
			if msgFromServer[1] == "video":
				print  "this is the video command"
				file.write("this is the video command" + "\n")

				self.recordTimes.insert(0, msgFromServer[7])
				self.recordTimes.insert(0, msgFromServer[6])
				# print "recordTimes: ", self.recordTimes

				def uploadThread(serverIP, serverSaveFilePath):
					uploadThread = threads.deferToThread(up.videoUpload, serverIP, serverSaveFilePath)
					uploadThread.addErrback(self.upFail, piName)

				upload_loop = LoopingCall(uploadThread, serverIP, serverSaveFilePath)
				upload_loop.start(1800) #seconds

				videoThread = threads.deferToThread(self.recordVideoProcess, int(msgFromServer[2]), int(msgFromServer[3]), int(msgFromServer[4]),\
					int(msgFromServer[5]), serverIP, piName, self.recordTimes, file)
				videoThread.addErrback(self.vtFail, piName)

			elif msgFromServer[1] == "multiplexer" or msgFromServer[1] == "camera":
				print  "this is the {0} method. It has been discontinued. Please exit the program and select video".format(msgFromServer[1])
				file.write("this is the {0} method. It has been discontinued. Please exit the program and select video".format(msgFromServer[1]) + "\n")
				reactor.callLater(0.5, self.transport.write, "finished\n")

		else:
			print  "CLIENT: Time: {0}. I don't know what this is: {1}".format(time.strftime("%Y-%m-%d-%H:%M:%S"), data)
			file.write("CLIENT: Time: {0}. I don't know what this is: {1}".format(time.strftime("%Y-%m-%d-%H:%M:%S"), data) + "\n")

	def recordVideoProcess(self, resW, resH, totalTimeSec, framerate, serverIP, piName, recordTimesList, file):
		semi = DeferredSemaphore(1)

		jobs = []
		for runs in range(len(recordTimesList)/2):
			print  "recordTimes recordVideoProcess:", recordTimesList
			file.write("recordTimes recordVideoProcess:" + "\n")
			try:
				startAtTime = self.calculateTimeDifference(recordTimesList.pop(0), recordTimesList.pop(0))
				jobs.append(semi.run(tv.takeVideo, int(resW), int(resH), int(totalTimeSec),\
						int(framerate), startAtTime, serverIP, piName, file))
			except:
				print  "That time was not valid. Calling next time."
				file.write("That time was not valid. Calling next time." + "\n")
				print "len recordTimesList: ", len(recordTimesList)
				file.write("len recordTimesList: " + str(len(recordTimesList)) + "\n")
				if len(recordTimesList)%2>0:
					print  "odd number"
					file.write("odd number" + "\n")
					recordTimesList.pop(0)
					print  "new len: ", len(recordTimesList)
					file.write("new len: " + str(len(recordTimesList)) + "\n")
					reactor.callLater(0.5, self.transport.write, "TIMEINPUTERROR {0}\n".format(piName))
				continue
			
		jobs = DeferredList(jobs)

		print  "Results: ", jobs.addCallback(self.getResults, piName)
		# file.write("Results: ", jobs.addCallback(self.getResults, piName))
		jobs.addCallback(lambda _: reactor.callLater(5, reactor.stop))

		# reactor.stop()

	def getResults(self, res, piName):
		print  "We got: ", res
		file.write("We got: " + "\n")
		for x in res:
			file.write(str(x))
		print  "We got piName: ", piName
		file.write("We got piName: " + piName + "\n")
		recordSuccess = False
		for resLen in range(len(res)):
			print   "RESLEN1: ", res[resLen][1]
			file.write("RESLEN1: " + res[resLen][1] + "\n")
			if res[resLen][1] != "Finished":
				print  "errrrrrrrr"
				file.write("errrrrrrrr" + "\n")
				reactor.callLater(0.5, self.transport.write, "CAMERROR {0} {1}\n".format(piName, res[resLen][1]))
				self.emailError(piName, res[resLen][1])
				break
			recordSuccess = True
		if recordSuccess:
			print  "Nothing went wrong. Send Finished message"
			file.write("Nothing went wrong. Send Finished message" + "\n")
			reactor.callLater(0.5, self.transport.write, 'finished\n')
		return "done"

	def failedMethod(self,failure):
		print  "FAILURE: ERROR WITH PICTURE TAKING METHOD"
		file.write("FAILURE: ERROR WITH PICTURE TAKING METHOD" + "\n")
		print  failure
		file.write(str(failure) + "\n")
		# self.transport.write("CAMERROR {0}".format(piName))
		# os.system('echo "Camera for {1} is broken. Error message: \n {0} \n'\
		# 	'-------end of message --------- \n" | mail -s "Camera Broken" urbanFlowsProject@gmail.com'\
		# 	.format(str(failure), piName))

	def vtFail(self, failure, piName):
		print  "VTFAIL"
		file.write("VTFAIL" + "\n")
		print  failure
		file.write(str(failure) + "\n")
		reactor.callLater(0.5, self.transport.write, "THREADERROR {0} {1}\n".format(piName, failure))

	def upFail(self, failure, piName):
		print  "UPFAIL"
		file.write("UPFAIL" + "\n")
		print  failure
		file.write(str(failure) + "\n")
		reactor.callLater(0.5, self.transport.write, "THREADERROR {0} {1}\n".format(piName, failure))

	def emailError(self, piName, errorMsg):
		os.system('echo "Camera for {0} is broken. Error message: \n {1} \n'\
			'-------end of message --------- \n" | mail -s "Camera Broken" urbanFlowsProject@gmail.com'\
			.format(piName, errorMsg))

	def calculateTimeDifference(self, dateToEnd, timeToEnd):
		fullString = dateToEnd + " " + timeToEnd
		print  "RUNNING RECORDING AT: ", fullString
		file.write("RUNNING RECORDING AT: " + fullString + "\n")
		endTime = datetime.datetime.strptime(fullString, "%x %X")
		nowTime = datetime.datetime.today()
		difference = endTime - nowTime
		return time.time() + difference.total_seconds()

if __name__ == '__main__':
	try:
		file = open('runLog.txt', 'w')
		print  sys.argv[1]
		file.write(sys.argv[1] + "\n")
		serverIP = sys.argv[1]
		if serverIP != "18.89.4.173":
			print  "IP ERROR: This is the wrong IP address. Try again!"
			file.write("IP ERROR: This is the wrong IP address. Try again!" + "\n")
			reactor.stop()

		piName = sys.argv[2]
		serverSaveFilePath = "/media/msit/PhilipsData/TrafficIntersection17/"
		#serverSaveFilePath = "/media/senseable-beast/beast-brain-1/Data/OneWeekData/tmp/"
		tp = takePictureClass()
		tv = TakeVideoClass()
		up = UploadClass()


		#TCP network: Connects on port 8888.
		data = "start"
		reactor.connectTCP(serverIP, 8888, DataClientFactory(data), timeout=200)

		reactor.run()
	finally:
		print  "closing file"
		file.write("CLOSE" + "\n")
		file.close()
