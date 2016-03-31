#/!/usr/bin/python

#Written by Michelle Sit

import time
import picamera
import datetime
import glob
import os
import sys

#Takes video
class takeVideoClass():
	def __init__(self):
		self.runSendVid = True

	#def takeVideo (self, inputVidTime, inputResW, inputResH, inputTotalRunTime, inputFramerate, inputStartTime):
	def takeVideo (self, inputVidTime, inputResW, inputResH, inputFramerate, inputStartTime):
		while time.time() < inputStartTime:
			pass
		else:
			try:
	#			numCycles = (inputTotalRunTime*60)/inputVidTime
				with picamera.PiCamera() as camera:
					camera.resolution = (inputResW, inputResH)
					camera.framerate = inputFramerate
					for filename in camera.record_sequence([
						datetime.datetime.now().strftime ('%M_%S_%f') + '.h264']):
						#datetime.datetime.now().strftime('%d-%m-%Y-%H_%M_%S_%f') + '_TT' + str(inputTotalTime) + '_VT' + str(inputVidTime) + '_RH' + str(inputResH) + '_FR' + str(inputFramerate) + ".h264"]):
	#					for k in range(numCycles)]):
						camera.wait_recording(inputVidTime)
			except:
				print "error"
				os.system('echo "Camera for PI2 is broken. Error message: \n {0} \n'\
				'-------end of message --------- \n" | mail -s "Camera Broken" msit@wellesley.edu'\
				.format(sys.exc_info()))

	def getRunSendVidMethod(self):
		return self.runSendVid

	def curlUploadVid (self, serverIP):
		self.fileList = glob.glob('*.h264')
		if len(self.fileList) > 0:
			for video in self.fileList:
				os.system('curl --header "filename: {0}" -X POST --data-binary @{0} http://{1}:8880/upload-image'.format(video, serverIP))
				os.system('rm {0}'.format(video))

	def sendVideos(self, inputStartTimePlusOne, serverIP):
		while time.time() < inputStartTimePlusOne:
			pass
		else:
			print "sendImages method!"
			while self.runSendVid == True:
				self.curlUploadVid(serverIP)
				print self.getRunSendVidMethod()
			else: #if self.runSendVid is False
				print "runing last glob"
				self.curlUploadVid()	
				print "done! :D"


if __name__ == '__main__':
	tv = takeVideoClass()