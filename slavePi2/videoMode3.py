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
		self.runUpload = True

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
				print "CAMERA IS FINISHED. RETURN FALSE"
				self.runUpload = False
			except:
				print "error"
				self.runUpload = False
				print "Switched runUpload"
				raise

	def curlUpload (self, serverIP):
		print "curlUpload called"
		self.fileList = glob.glob('*.jpg')
		if len(self.fileList) > 0:
			print "fileList has customers: ", self.fileList
			for item in self.fileList:
				os.system(
					'if balExp=$(curl -X GET http://{0}:8880/upload-image);'\
					'then curl --header "filename: {1}" -y 10 --max-time 180 -X POST --data-binary @{1} http://{0}:8880/upload-image &'\
					'wait;'\
					#'rm {1};'\
					'else sudo ifup wlan0;'\
					'fi'.format(serverIP, item)
					)

	def sendUpload(self, inputStartTimePlusOne, serverIP):
		while time.time() < inputStartTimePlusOne:
			pass
		else:
			while self.runUpload == True:
				# print "while loop for runSenditem called"
				self.fileList = glob.glob('*.jpg')
				if len(self.fileList) > 0:
					print "fileList has customers: ", self.fileList
					for item in self.fileList:
						os.system(
							'if balExp=$(curl -X GET http://{0}:8880/upload-image);'\
							'then curl -C - --header "filename: {1}" -y 10 --max-time 180 -X POST --data-binary @{1} http://{0}:8880/upload-image &'\
							'wait;'\
							#'rm {1};'\
							'else sudo ifup wlan0;'\
							'fi'.format(serverIP, item)
							)
				print "sleeping for 1 seconds"
				time.sleep(1)
			else:
				print "runing last glob"
				self.curlUpload(serverIP)	
				self.curlUpload(serverIP)
				print "last catch"
				return "finished"


if __name__ == '__main__':
	tv = takeVideoClass()
	now = time.time() + 1
	tv.takeVideo(180, 1600, 1200, 15, now)
	# tv.takeVideo(180, 1024, 768, 15, now)
	# tv.takeVideo(180, 1280, 720, 30, now)
	# tv.takeVideo(180, 1920, 1080, 30, now)
