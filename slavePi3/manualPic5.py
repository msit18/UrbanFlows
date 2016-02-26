import time
import datetime
import picamera
import sys
import math

class CamWork:
	def takePicture (self, inputTotalTime, inputResW, inputResH, inputNumPics, inputFPSTimeInterval, inputFramerate):
		#Keeps track of time for updates 
		prgmStartTime = time.time() #When the program began
		print "prgmStartTime: ", prgmStartTime
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
			print "timeNow: ", timeNow
			print "prgmEndTime: ", prgmEndTime
			#Provides updates in 10 minute increments
			if timeNow >= timePlusTenMin:
				endTenMinTime = time.time()
				tenMinTotalRunTime = endTenMinTime-prgmStartTime
				tenMinFPSUpdate = totalNumPicsTaken/tenMinTotalRunTime
				print "10.2 Ten second Update: Total number of pictures is {0},"\
				" total time elapsed is {1}, totalFPS is {2}".format(str(totalNumPicsTaken),\
				str(tenMinTotalRunTime), str(tenMinFPSUpdate) )
				#estimating PictureNumbers
				estTime = math.ceil(prgmEndTime-timeNow)
				if estTime > 0:
					expectedNumPicsToTakeNext = estTime*math.ceil(tenMinFPSUpdate)
				print "expectedNumPicsToTakeNext: ", expectedNumPicsToTakeNext
				print "totalNumPicsTaken: ", totalNumPicsTaken
				totalExpected = expectedNumPicsToTakeNext + totalNumPicsTaken
				print "totalExpected: ", totalExpected

				timePlusTenMin = time.time()+5
			elif: #Runs picture taking process as normal
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
		print "EndTime: ", endTime
		totalTime = endTime-prgmStartTime
		totalFPS = totalNumPicsTaken/totalTime
		print "10.2: Captured {0} total pictures.  Total time was {1}, total FPS is {2}"\
		.format(str(totalNumPicsTaken), str(inputTotalTime), str(totalFPS) )

		print "CAMERA IS FINISHED. RETURN TRUE"
		return "True"

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

if __name__ == '__main__':
	c = CamWork()
	c.takePicture(120, 640, 480, 60, 1, 90)