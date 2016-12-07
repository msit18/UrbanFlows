#/!/usr/bin/python

#Written by Michelle Sit

#WOULD BE FUN TODO: REPLACE WHILE LOOP WITH PRINTING UPDATES ON FILE TO A GRAPH APPROACH.
#HAVE THE FPS UPDATED AT A CERTAIN TIME FRAME ON A GRAPH IF POSSIBLE.

import time
import picamera
import datetime
import os
import sys
import glob
from twisted.internet import defer
import subprocess

class takePictureClass():
	def __init__(self):
		self.runUpload = True

	def filenames(self, inputTotalTime, inputResW, inputResH, inputFramerate):
		print "took some images"
		nowPlusInputTotalTime = time.time() + inputTotalTime
		while time.time() < nowPlusInputTotalTime:
			yield 'slavePi2_RW' + str(inputResW) + '_RH' + str(inputResH) + '_TT' +\
				str(inputTotalTime) + '_FR' + str(inputFramerate) + '_' + \
				datetime.datetime.now().strftime ('%M_%S_%f') + '.jpg'

	def takePicture_filenames(self, inputTotalTime, inputResW, inputResH,\
							inputFramerate, inputStartTime):
		while time.time() < inputStartTime:
			pass
		else:
			print "running"
			# try:
			with picamera.PiCamera() as camera:
			    camera.resolution = (inputResW, inputResH)
			    camera.framerate = inputFramerate
			    camera.start_preview()
			    # Give the camera some warm-up time
			    time.sleep(2)
			    start = time.time()
			    camera.capture_sequence(self.filenames(inputTotalTime, inputResW, inputResH, inputFramerate), use_video_port=True)
			    finish = time.time()
			    frames = len(glob.glob('*.jpg'))
			print('Captured %d frames at %.2ffps' % (frames, frames / (finish - start)))
			self.runUpload = False
			print "runUpload is false. Finished"
			# except:
			# 	print "noooooooooooooo break"
			# 	self.runUpload = False
			# 	print "Switched runUpload"
			# 	raise

	def takePicture_cc (self, inputTotalTime, inputResW, inputResH,\
							inputNumPics, inputFPSTimeInterval, inputStartTime):
		while time.time() < inputStartTime:
			pass
		else:
			try:
				prgmEndTime = int(inputTotalTime)+time.time() #When the program ends
				calculatedFpsTimeInterval = float(inputFPSTimeInterval)/inputNumPics
				print "the calculatedFpsTimeInterval will be :", calculatedFpsTimeInterval
				with picamera.PiCamera() as camera:
					camera.resolution = (inputResW, inputResH)
					camera.framerate = 10
					start = time.time()
					while time.time() < prgmEndTime:
						print time.time()
						print prgmEndTime
						for filename in camera.capture_continuous ('slavePi2_RW' + str(inputResW) +\
						'_RH' + str(inputResH) + '_TT' + str(inputTotalTime) + '_FR' + str(inputFramerate) + \
						'_{timestamp:%M_%S_%f}.jpg', burst=True):
							print ('Captured {0}'.format(filename))
							time.sleep(calculatedFpsTimeInterval)
							if time.time() > prgmEndTime:
								print "break!"
								break
						print "outside for loop, inside while loop"
					print "finished!"
					finished = time.time()
					totalNumPics = len(glob.glob('*.jpg'))
					totalTime = finished-start
					fpsTotal = totalNumPics/totalTime
					print "totalNumPics: {0}. totalTime: {1}. fpsTotal: {2}".format(totalNumPics, totalTime, fpsTotal)
					self.runUpload = False
					print "runUpload is false. Finished"
			except:
				print "noooooooooooooo break"
				self.runUpload = False
				print "Switched runUpload"
				raise

	# def takePicture (self, inputTotalTime, inputResW, inputResH, inputNumPics,\
	# 					inputFPSTimeInterval, inputFramerate, inputStartTime):
	# 	#print "takePicture method!"
	# 	while time.time() < inputStartTime:
	# 		pass
	# 	else:
	# 		try:
	# 			#Keeps track of time for updates 
	# 			prgmStartTime = time.time() #When the program began
	# 			totalTimeSec = int(inputTotalTime)
	# 			totalTimeMin = int(inputTotalTime)/60
	# 			timeNow = time.time() #Used to keep track of current time
	# 			prgmEndTime = totalTimeSec+timeNow #When the program ends
	# 			timePlusFPSTimeInterval = timeNow #Keeps track of time increments

	# 			timePlusTenMin = timeNow+5
	# 			# print "Capturing {0}p for a total time of {1} min ({2} secs) at {3} "\
	# 			# "frames per {4} second (({5} mins) at {6} framerate ".format(str(resH), \
	# 			# 	str(totalTimeMin), str(totalTimeSec), str(numPics), str(timeInterval), \
	# 			# 	str(float(timeInterval/60)), str(frameRate) )
	# 			totalNumPicsTaken = 0
	# 			#Limits program from going over the designated time period and over the update time
	# 			while timeNow < timePlusTenMin and timeNow < prgmEndTime:
	# 				timeNow = time.time()
	# 				#Provides updates in 10 minute increments
	# 				timePlusFPSTimeInterval = timeNow + inputFPSTimeInterval
	# 				start = time.time()
	# 				self.piCamTakePictures(inputResW, inputResH, inputNumPics, inputFramerate)
	# 				finish = time.time()
	# 				#Analyzing time and frames
	# 				fpsTime = (finish-start)
	# 				fps = inputNumPics/fpsTime
	# 				totalNumPicsTaken += inputNumPics
	# 				# print 'Captured {0} frames at {1}fps in {2}secs'\
	# 				# .format(str(totalNumPicsTaken), str(inputNumPics/fpsTime), str(fpsTime))
	# 			endTime = time.time()
	# 			totalTime = endTime-prgmStartTime
	# 			totalFPS = totalNumPicsTaken/totalTime
	# 			# print "10.2: Captured {0} total pictures.  Total time was {1}, total FPS is {2}"\
	# 			# .format(str(totalNumPicsTaken), str(inputTotalTime), str(totalFPS) )
	# 			print "CAMERA IS FINISHED. RETURN FALSE"
	# 			self.runUpload = False
	# 		except:
	# 			print "noooooooooooooo break"
	# 			self.runUpload = False
	# 			print "Switched runUpload"
	# 			raise

	# def piCamTakePictures(self, inputResW, inputResH, inputNumPics, inputFramerate):
	# 	with picamera.PiCamera() as camera:
	# 		camera.resolution = (inputResW, inputResH)
	# 		camera.framerate = inputFramerate
	# 		v = camera.capture_sequence([
	# 			datetime.datetime.now().strftime ('%M_%S_%f') + '.jpg'
	# 			# datetime.datetime.now().strftime ('%d-%m-%Y-%H_%M_%S_%f') + '_TT'\
	# 			#  + str(listServerArgs[0]) + '_RES' + str(resH) + '_PIC' + str(numPics) +\
	# 			#   '_TI' + str(timeInterval) + '_FR' + str(frameRate) + '.jpg'
	# 			for i in range(inputNumPics)
	# 			], use_video_port=False)

	def curlUpload (self, serverIP):
		print "curlUploadImg called"
		self.fileList = glob.glob('*.jpg')
		self.fileList.extend(glob.glob('*.bin'))
		self.fileList.sort()
		if len(self.fileList) > 0:
			print "fileList has customers: ", self.fileList
			for item in self.fileList:
				cmd = \
					'if balExp=$(curl -X GET http://{0}:8880/upload-image);'\
					' then curl -C - --header "filename: {1}" -y 10 --max-time 180 -X POST --data-binary @{1} http://{0}:8880/upload-image &'\
					' wait;'\
					' rm {1};'\
					' wait;'\
					' else sudo ifup wlan0;'\
					' fi'.format(serverIP, item)
				#print "cmd: ", cmd
				subprocess.call(cmd, shell=True)

	def sendUpload(self, inputStartTimePlusOne, serverIP):
		while time.time() < inputStartTimePlusOne:
			pass
		else:
			while self.runUpload == True:
				self.fileList = glob.glob('*.jpg')
				self.fileList.extend(glob.glob('*.bin'))
				self.fileList.sort()
				if len(self.fileList) > 0:
					print "fileList has customers: ", self.fileList
					for item in self.fileList:
						cmd = \
							'if balExp=$(curl -X GET http://{0}:8880/upload-image);'\
							' then curl -C - --header "filename: {1}" -y 10 --max-time 180 -X POST --data-binary @{1} http://{0}:8880/upload-image &'\
							' wait;'\
							' rm {1};'\
							' wait;'\
							' else sudo ifup wlan0;'\
							' fi'.format(serverIP, item)
						#print "cmd: ", cmd
						subprocess.call(cmd, shell=True)
				print "sleeping for 1 seconds"
				time.sleep(1)
			else:
				print "runing last glob"
				self.curlUpload(serverIP)	
				self.curlUpload(serverIP)
				print "last catch"
				return "finished"


if __name__ == '__main__':
	t = takePictureClass()
	now = time.time()+1
	t.takePicture_filenames(10, 2592, 1944, 1, now)
	#camLog = open('CamLog-{0}.txt'.format(time.strftime("%Y-%m-%d-%H:%M:%S")), 'w')
