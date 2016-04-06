#/!/usr/bin/python

#Written by Michelle Sit

#wORK IN PROGRESS

#Edited from manualPic_capturePhotos.py

#WOULD BE FUN TODO: REPLACE WHILE LOOP WITH PRINTING UPDATES ON FILE TO A GRAPH APPROACH.
#HAVE THE FPS UPDATED AT A CERTAIN TIME FRAME ON A GRAPH IF POSSIBLE.

import time
import picamera
import datetime
import os
import sys
import glob

class takePictureClass():
	def __init__(self):
		self.runSendImg = True
		# self.fileList = []

	def takePicture (self, inputTotalTime, inputResW, inputResH, inputNumPics,\
						inputFPSTimeInterval, inputFramerate, inputStartTime):
		#print "takePicture method!"
		while time.time() < inputStartTime:
			pass
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
							print 'Captured {0} frames at {1}fps in {2}secs'\
							.format(str(totalNumPicsTaken), str(inputNumPics/fpsTime), str(fpsTime))
				endTime = time.time()
				totalTime = endTime-prgmStartTime
				totalFPS = totalNumPicsTaken/totalTime
				print "10.2: Captured {0} total pictures.  Total time was {1}, total FPS is {2}"\
				.format(str(totalNumPicsTaken), str(inputTotalTime), str(totalFPS) )
				print "CAMERA IS FINISHED. RETURN FALSE"
				self.runSendImg = False
			except:
				print "noooooooooooooo break"
				self.runSendImg = False
				print "Switched runSendImg"
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
				], use_video_port=False)

	def curlUploadImg (self, serverIP):
		self.fileList = glob.glob('*.jpg')
		if len(self.fileList) > 0:
			print "fileList has customers: ", self.fileList
			for img in self.fileList:
				os.system('if balExp=$(curl -X GET http://{1}:8880/upload-image);' \
					' then balExp=$(curl --header "filename: {0}" -y 10 --max-time 180 -X POST --data-binary @{0}' \
					' http://{1}:8880/upload-image); rm {0}; else sudo ifup wlan0; fi'.format(img, serverIP))
				# os.system('curl --header "filename: {0}" -v -y 10 --max-time 180 -X POST --data-binary @{0}' \
				# 	' http://{1}:8880/upload-image'.format(img, serverIP))


	def sendImages(self, inputStartTimePlusOne, serverIP):
		while time.time() < inputStartTimePlusOne:
			pass
		else:
			#print "sendImages method!"
			while self.runSendImg == True:
				#print "runSendImg is true"
				self.curlUploadImg(serverIP)
			else:
				#print "runing last glob"
				self.curlUploadImg(serverIP)	
				self.curlUploadImg(serverIP)
				print "last catch"
				return "finished"

if __name__ == '__main__':
	t = takePictureClass()
	now = time.time()+1
	t.takePicture(10, 2594, 1944, 3, 1, 90, now)
	#camLog = open('CamLog-{0}.txt'.format(time.strftime("%Y-%m-%d-%H:%M:%S")), 'w')