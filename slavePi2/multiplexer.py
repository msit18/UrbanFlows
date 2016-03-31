#Original code from ivport_capture_sequence_A.py. Edits made by Nahom Marie and Michelle Sit

import time
import picamera
import datetime
import glob
import os
import sys
import RPi.GPIO as gp

#Setup for the pi camera, taken from the 'ivport_capture_sequence_A.py' file
gp.setwarnings(False)
gp.setmode(gp.BOARD)

gp.setup(7, gp.OUT)
gp.setup(11, gp.OUT)
gp.setup(12, gp.OUT)

gp.output(7, False)
gp.output(11, False)
gp.output(12, True)

#More for testing purposes for now; number of pictures to be taken. Stupid high value so that there's essentially no end to the loop. 
frames = 200000000000000

#Begins the camera on picamera 1
cam = 1

class multiplexerClass():
	def __init__(self):
		self.runSendMP = True

	#Switches cameras. Taken from 'ivport_capture_sequence_A.py'
	def cam_change(self):
		global cam
		gp.setmode(gp.BOARD)
		if cam == 1:
		        # CAM 1 for A Jumper Setting
		        gp.output(7, False)
		        gp.output(11, False)
		        gp.output(12, True)
		elif cam == 2:
		        # CAM 2 for A Jumper Setting
		        gp.output(7, True)
		        gp.output(11, False)
		        gp.output(12, True)
		elif cam == 3:
		    	# CAM 3 for A Jumper Setting
		        gp.output(7, False)
		        gp.output(11, True)
		        gp.output(12, False)
		elif cam == 4:
		        # CAM 4 for A Jumper Setting
		        gp.output(7, True)
		        gp.output(11, True)
		        gp.output(12, False)
		cam += 1
		if cam > 4:
			cam = 1

	def takePicturesMP(self, inputTotalTime, inputResW, inputResH,  inputFramerate, inputStartTime):
		while time.time() < inputStartTime:
			pass
		else:
			try:
				# Multiplexer architecture capturing sequence
				with picamera.PiCamera() as camera:
					camera.resolution = (inputResW, inputResH)
					camera.framerate = inputFramerate

					startTime = time.time()
					camera.capture_sequence(filenames(), use_video_port=True)
					finishTime = time.time()
					timeRan = finishTime - startTime
					# print 'Program captured %d images at %.2f fps' % (frame, frame / timeRan)
					# print 'Finished running in %.02f seconds' % timeRan
			except:
				print "error"
				self.runSendMP = False
				print "Switched runSendMP"
				raise

	#Changes cameras and names the written files; FILE NAMES SHOULD BE MORE SUBSTANTIVELY NAMED. 
	#Updated to test to make sure we can limit the running to a certain amount of time.
	#Original model goes while frame < frames
	def filenames(self, inputFPSTimeInterval):
		#Current number of pics taken
	    	global frame
	    	#global fpspc
	    	frame = 0
	    	#fpspc = []
	    	start = time.time()
	    	now = start
		while now - start < inputFPSTimeInterval:
			time.sleep(0.007)    # Used to correct delays
			cam_change()        # Switching Camera
			time.sleep(0.007)
			#timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S:%f')
			timestamp = datetime.datetime.now().strftime ('%M_%S_%f')
			#fpspc.append('cam %d' % cam + ' ' + datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S:%f'))
			yield 'cam%d_%s.jpg' % (cam, timestamp)
			frame += 1
			#Prints a statment for every 20 pictures captured to update total FPS
			# if frame % 20 == 0:
			# 	print 'Captured %d images so far, at %.02f fps' % (frame, frame / (now - start))
			now = time.time()

if __name__ == '__main__':
	m = multiplexerClass()