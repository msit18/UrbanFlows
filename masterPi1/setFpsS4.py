#Written by Michelle Sit

import pifacecad 
from pifacecad.tools.question import LCDQuestion
import os
import string
import time
import sys
from threading import Barrier
import subprocess
import variables as v1
from shutdownS5 import shutdownS5

#Constructor
cad = pifacecad.PiFaceCAD()

class setFpsS4():

	#SET FPS
	def S4():
		print ("setFpsS4 S4 function")
		cad.lcd.clear()
		#Sets fps values based on chosen resolution, takes input from piface
		setFpsS4.determineFPS()
		question = LCDQuestion(question="Set FPS", answers=v1.FPSanswers)
		answer_index = question.ask()
		cad.lcd.clear()
		v1.inputFPS = v1.FPSanswers[answer_index]
		#Only for camera mode:
		#Internally sets v1.numFrames and v1.timeInterval based on the chosen fps from the above options.  If v1.inputFPS is "Custom",
		# the user chooses fps options.  For camera, internal framerate is set through runCMD when the resolution is sent to the slavePies.
		setFpsS4.setCamFramesAndTime()	
		setFpsS4.manualFpsSelect()
		#User feedback
		cad.lcd.write("FPS selected: \n{0}".format(v1.inputFPS))
		time.sleep(1)
		shutdownS5.homeScreen()

	#determines different fps options depending on resolutionH selected.  For camera, also sets the internal framerate
	def determineFPS():
		print ("setFpsS4 determineFPS function")
		if v1.currentMode == "VID":
			if v1.resolutionH == "1080":
				v1.FPSanswers = ["15", "30"]
			elif v1.resolutionH == "730":
				v1.FPSanswers = ["15", "30", "49"]
			elif v1.resolutionH == "480":
				v1.FPSanswers = ["1", "49", "60", "90"]
			else:
				v1.FPSanswers = ["0"]	
		elif v1.currentMode == "CAM":
			if v1.resolutionH == "1080":
				v1.FPSanswers = ["1", "2", "3", "5", "8", "Custom"]
				v1.internalCamFR = 90
			elif v1.resolutionH == "1944":
				v1.FPSanswers = ["1", "2", "3", "5", "Custom"]
				v1.internalCamFR = 50
			elif v1.resolutionH == "730":
				v1.FPSanswers = ["1", "3", "5", "15", "18", "Custom"]
				v1.internalCamFR = 50
			elif v1.resolutionH == "480":
				v1.FPSanswers = ["10", "20"]
				v1.internalCamFR = 90
			else:
				v1.FPSanswers = ["0"]
		else:
			v1.FPSanswers = ["0"]

	#Takes the selected fps for camera mode and sets the appropriate number of frames and time interval
	#default time interval is already set to 1 second when resolution is set to camera in camVidStartS1
	def setCamFramesAndTime():
		print ("setFpsS4 setCamFramesAndTime function")
		if v1.inputFPS == "Custom":
			pass
		else:
			print ("inputFPS is :" + str(v1.inputFPS))
			if v1.inputFPS == "1":
				v1.numFrames = 1
				print ("Selected numFrames = 1")
			elif v1.inputFPS == "2" and v1.resolutionH != "1944":
				print ("v1.inputFPS ==2")
				v1.numFrames = 2

			if v1.resolutionH == "1080":
				print ("if resH == 1080")
				if v1.inputFPS == "3":
					v1.numFrames = 4
				elif v1.inputFPS == "5":
					v1.numFrames = 8
				elif v1.inputFPS == "8":
					v1.numFrames = 50
					v1.timeInterval = 2

			elif v1.resolutionH == "1944":
				print ("Hi self! 5MP")
				if v1.inputFPS == "2":
					print ("Ive reached inside the loop")
					print (v1.inputFPS)
					v1.numFrames = 3
				elif v1.inputFPS == "3":
					v1.numFrames = 7
				elif v1.inputFPS == "5":
					v1.numFrames = 25

			elif v1.resolutionH == "730":
				print ("if resH == 730")
				if v1.inputFPS == "5":
					v1.numFrames = 5
				elif v1.inputFPS == "15":
					v1.numFrames = 30
				elif v1.inputFPS == "18":
					v1.numFrames = 40
					v1.timeInterval = 2

			elif v1.resolutionH == "480":
				print ("if resH == 480")
				if v1.inputFPS == "10":
					v1.numFrames = 10
				elif v1.inputFPS == "20":
					v1.numFrames = 20
			else:
				print ("I'm not in any of the loops")
			print ("numFrames selected: " + str(v1.numFrames) )
			print ("timeInterval: " + str(v1.timeInterval))

	#If 'Custom' is selected as the fps, asks user questions to get fps
	def manualFpsSelect():
		print ("setFpsS4 manualFpsSelect function")
		if v1.inputFPS == "Custom":
			question = LCDQuestion(question="Set numFrames", answers = v1.customNumFramesAnswers)
			answer_index = question.ask()
			v1.numFrames = v1.customNumFramesAnswers[answer_index]
			cad.lcd.clear()
			question = LCDQuestion(question="Set time (sec)", answers = v1.customTimeIntervalAnswers)
			answer_index = question.ask()
			v1.timeInterval = v1.customTimeIntervalAnswers[answer_index]
			cad.lcd.clear()

			v1.inputFPS = v1.numFrames
			cad.lcd.write("Selected fps:\n{0} frames/{1} secs".format(v1.numFrames, v1.timeInterval) )
			time.sleep(2)
			shutdownS5.homeScreen()
		else:
			pass
