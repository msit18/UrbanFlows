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
		self.clientParams = ""
		self.numPicsTaken = 0
		self.runSendImg = True

	def connectionMade(self):
		#ip_address = subprocess.check_output("hostname --all-ip-addresses", shell=True).strip()
		#msg = "ip piGroup1 {0}".format(ip_address)
		msg = "ip piGroup1 slavePi3"
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
				callLaterTimeCollectImgs = float(msgFromServer[9]) + 1
				result = threads.deferToThread(self.takePicture, int(msgFromServer[3]), int(msgFromServer[4]),\
					int(msgFromServer[5]), int(msgFromServer[6]), int(msgFromServer[7]), int(msgFromServer[8]), float(msgFromServer[9]))
			elif msgFromServer[2] == "video":
				print "this is the video method. Video method has not been completed"
				self.clientParams = "{0} {1} {2} {3} {4}".format(\
				msgFromServer[2], msgFromServer[3], msgFromServer[4],\
				msgFromServer[5], msgFromServer[6])
			self.sendImages(callLaterTimeCollectImgs)
		else:
			print "Didn't write hi success.jpg to server"

	def failedMethod(self,failure):
		print "FAILURE: ERROR WITH PICTURE TAKING METHOD"
		#TODO: FIGURE OUT HOW TO DISTINGUISH BETWEEN DIFFERENT PICAM ERRORS
		self.transport.write("ERROR PICAMERA")
		sys.stderr.write(str(failure))

	def writeToServer(self, msg):
		print "WRITETOSERVER. Write message to server: {0}".format(msg)
		self.transport.write(msg)

#WOULD BE FUN TODO: REPLACE WHILE LOOP WITH PRINTING UPDATES ON FILE TO A GRAPH APPROACH.
#HAVE THE FPS UPDATED AT A CERTAIN TIME FRAME ON A GRAPH IF POSSIBLE.
	def takePicture (self, inputTotalTime, inputResW, inputResH, inputNumPics, inputFPSTimeInterval, inputFramerate, inputStartTime):
		print "takePicture method!"
		startPictures = time.time()
		while time.time() < inputStartTime:
			startPictures = time.time()
		else:
			try:
				#Keeps track of time for updates 
				prgmStartTime = time.time() #When the program began
				totalTimeSec = int(inputTotalTime)
				totalTimeMin = int(inputTotalTime)/60
				timeNow = time.time() #Used to keep track of current time
				prgmEndTime = totalTimeSec+timeNow #When the program ends
				timePlusFPSTimeInterval = timeNow #Keeps track of time increments

				timePlusTenMin = timeNow+5
				# print "Capturing {0}p for a total time of {1} min ({2} secs) at {3} "\
				# "frames per {4} second (({5} mins) at {6} framerate ".format(str(resH), \
				# 	str(totalTimeMin), str(totalTimeSec), str(numPics), str(timeInterval), \
				# 	str(float(timeInterval/60)), str(frameRate) )
				totalNumPicsTaken = 0
				#Limits program from going over the designated time period and over the update time
				while timeNow < timePlusTenMin and timeNow < prgmEndTime:
					timeNow = time.time()
					#Provides updates in 10 minute increments
					if timeNow >= timePlusTenMin:
						endTenMinTime = time.time()
						tenMinTotalRunTime = endTenMinTime-prgmStartTime
						tenMinFPSUpdate = totalNumPicsTaken/tenMinTotalRunTime
						#print "10.2 Ten Min Update: Total number of pictures is {0},"\
						#" total time elapsed is {1}, totalFPS is {2}".format(str(totalNumPicsTaken),\
						# str(tenMinTotalRunTime), str(tenMinFPSUpdate) )
						timePlusTenMin = time.time()+5
					else: #Runs picture taking process as normal
						while timeNow > timePlusFPSTimeInterval:
							timePlusFPSTimeInterval = timeNow + inputFPSTimeInterval
							start = time.time()
							self.piCamTakePictures(inputResW, inputResH, inputNumPics, inputFramerate)
							finish = time.time()
							#Analyzing time and frames
							fpsTime = (finish-start)
							fps = inputNumPics/fpsTime
							totalNumPicsTaken += inputNumPics
							#print 'Captured {0} frames at {1}fps in {2}secs'\
							#.format(str(totalNumPicsTaken), str(inputNumPics/fpsTime), str(fpsTime))
				endTime = time.time()
				totalTime = endTime-prgmStartTime
				totalFPS = totalNumPicsTaken/totalTime
				#print "10.2: Captured {0} total pictures.  Total time was {1}, total FPS is {2}"\
				#.format(str(totalNumPicsTaken), str(inputTotalTime), str(totalFPS) )
				print "CAMERA IS FINISHED. RETURN FALSE"
				self.runSendImg = False
			except:
				print "noooooooooooooo break"
				print sys.exc_info()[0]
				raise

	def piCamTakePictures(self, inputResW, inputResH, inputNumPics, inputFramerate):
		with picamera.PiCamera() as camera:
			camera.resolution = (inputResW, inputResH)
			camera.framerate = inputFramerate
			v = camera.capture_sequence([
				datetime.datetime.now().strftime ('%M_%S_%f') + '.jpg'
				# datetime.datetime.now().strftime ('%d-%m-%Y-%H_%M_%S_%f') + '_TT'\
				#  + str(listServerArgs[0]) + '_RES' + str(resH) + '_PIC' + str(numPics) +\
				#   '_TI' + str(timeInterval) + '_FR' + str(frameRate) + '.jpg'
				for i in range(inputNumPics)
				], use_video_port=True)

	def getRunSendImgMethod(self):
		return self.runSendImg

	def sendImages(self, inputStartTimePlusOne):
		startSend = time.time()
		while startSend < inputStartTimePlusOne:
			startSend = time.time()
		else:
			print "sendImages method!"
			while self.runSendImg == True:
				self.fileList = glob.glob('*.jpg')
				if len(self.fileList) > 0:
					for img in self.fileList:
							print img
							os.system('curl --header "filename: {0}" -X POST --data-binary @{0} http://18.111.29.234:8880/upload-image'.format(img))
							os.system('rm {0}'.format(img))
				print self.getRunSendImgMethod()
			else: #if self.runSendImg is False
				self.fileList = glob.glob('*.jpg')
				if len(self.fileList) > 0:
					for img in self.fileList:
							print img
							os.system('curl --header "filename: {0}" -X POST --data-binary @{0} http://18.111.29.234:8880/upload-image'.format(img))
							os.system('rm {0}'.format(img))		
				else:
					print "tadaaaa"
					reactor.stop()

if __name__ == '__main__':
	jobs = DeferredQueue()

	#TCP network: Connects on port 8888. HTTP network: Connects on port 8880
	data = "start"
	reactor.connectTCP('18.111.29.234', 8888, DataClientFactory(data), timeout=200)

	reactor.run()

	
