#Written by Michelle Sit

#Works with piFaceMain.py
#Sets camera or video mode, resets variables, and sends commands to slavePies after checking if parameters are permissable

import pifacecad 
from pifacecad.tools.question import LCDQuestion
import time
import os
import variables as v1
from setFpsS4 import setFpsS4
from shutdownS5 import shutdownS5

#Constructor
cad = pifacecad.PiFaceCAD()

class camVidStartS1():

	#SET CAMERA/VIDEO MODE, START PROGRAM, OR RESET ALL VARIABLES
	def S1():
		print ("camVidStartS1 S1 function")
		cad.lcd.clear()
		question = LCDQuestion(question="VID/CAM or START:", answers=v1.runMode)
		answer_index = question.ask()
		cad.lcd.clear()
		v1.inputRun = v1.runMode[answer_index]
		#Execute os string
		if v1.inputRun == "START":
			#Updates cmdStr with camera or vid inputs first before executing cmd
			#Also runs a series of checks to make sure all the inputs are correct
			camVidStartS1.updateCMD()
			cad.lcd.clear()
			cad.lcd.write("Running program")
			print (v1.cmdStr)
			if camVidStartS1.updateCMD() == "":
				cad.lcd.clear()
				cad.lcd.write("No inputs given!")
			else:
				pass
#				os.system("{0}".format(v1.cmdStr))
		#Video mode
		elif v1.inputRun == "VID":
			v1.currentMode = v1.inputRun
			cad.lcd.clear()
			cad.lcd.write("Selected video\nCheck res")
			time.sleep(1)
			shutdownS5.homeScreen()
		#Camera mode
		elif v1.inputRun == "CAM":
			v1.currentMode = v1.inputRun
			#Sets up timeInterval to be 1 in preparation for selecting the fps
			v1.timeInterval = 1
			cad.lcd.clear()
			cad.lcd.write("Selected pictures\nCheck res")
			time.sleep(1)
			shutdownS5.homeScreen()
		elif v1.inputRun == "Reset variables":
			print ("hi")
			v1.totalTime = 0
			v1.totalTimeEng = 0
			v1.videoTime = 0
			v1.videoTimeEng = 0
			v1.resolutionW = 0
			v1.resolutionH = 0
			v1.inputFPS = 0
			v1.numFrames = 0
			v1.timeInterval = 0
			v1.internalCamFR = 0
			v1.inputRun = ""
			v1.currentMode = "MODE"
			v1.cmdStr = ""
			shutdownS5.homeScreen()
		#Returns to homescreen
		else:
			shutdownS5.homeScreen()


#HELPER METHODS:
	#creates cmd str for START method.  Checks for absent inputs
	def updateCMD():
		print ("camVidStartS1 updateCMD function")
		if v1.totalTime == 0 or v1.resolutionW == 0 or v1.resolutionH == 0 or v1.inputFPS == 0 or \
					(v1.currentMode == "CAM" and v1.numFrames == 0):
			cad.lcd.clear()
			cad.lcd.write("Check inputs")
			time.sleep(2)
			shutdownS5.homeScreen()
		#Checks fps is correct for resolution
		elif v1.inputFPS != 0:
			camVidStartS1.testFPS()

	#Checks that the fps is correct for that resolution
	#0 indicates false, 1 indicates true statement
	def testFPS():
		print ("camVidStartS1 testFPS function")
		if v1.inputFPS == "Custom":
			pass
		else:
			setFpsS4.determineFPS()
			if v1.FPSanswers.count(v1.inputFPS) == 0:
				cad.lcd.clear()
				cad.lcd.write("Wrong frameRate\nTry again")
				time.sleep(1)
				shutdownS5.homeScreen()
			elif v1.FPSanswers.count(v1.inputFPS) > 0:
				camVidStartS1.testRes()

#TESTRES AND TESTFR ARE EXECUTING TWICE
	#Checks that current mode and resolution are appropriate
	def testRes():
		print ("camVidStartS1 testRes function")
		if v1.currentMode == "VID" and v1.resolutionH == "1944":
			cad.lcd.clear()
			cad.lcd.write("Wrong res\nTry again")
			time.sleep(1)
			shutdownS5.homeScreen()
		else:
			camVidStartS1.runCMD()

	#Sends commands to the slavePies with two different modes for camera or video.
	def runCMD():
		print("camVidStartS1 runCMD function")
		if v1.currentMode == "VID":
			v1.cmdStr = "sshpass -p 'raspberry' ssh pi@10.0.0.2 -o StrictHostKeyChecking=no python /home/pi/videoMode1.py {0} {1} {2} {3} {4} & \
				     sshpass -p 'raspberry' ssh pi@10.0.0.3 -o StrictHostKeyChecking=no python /home/pi/videoMode1.py {0} {1} {2} {3} {4} & \
				     sshpass -p 'raspberry' ssh pi@10.0.0.4 -o StrictHostKeyChecking=no python /home/pi/videoMode1.py {0} {1} {2} {3} {4} & \
				     sshpass -p 'raspberry' ssh pi@10.0.0.5 -o StrictHostKeyChecking=no python /home/pi/videoMode1.py {0} {1} {2} {3} {4}\
			".format(v1.videoTime, v1.resolutionW, v1.resolutionH, v1.totalTime, v1.inputFPS)
		elif v1.currentMode == "CAM":
			v1.cmdStr = "sshpass -p 'raspberry' ssh pi@10.0.0.2 -o StrictHostKeyChecking=no python /home/pi/manualPic2.py {0} {1} {2} {3} {4} {5} & \
				     sshpass -p 'raspberry' ssh pi@10.0.0.3 -o StrictHostKeyChecking=no python /home/pi/manualPic2.py {0} {1} {2} {3} {4} {5} & \
				     sshpass -p 'raspberry' ssh pi@10.0.0.4 -o StrictHostKeyChecking=no python /home/pi/manualPic2.py {0} {1} {2} {3} {4} {5} & \
				     sshpass -p 'raspberry' ssh pi@10.0.0.5 -o StrictHostKeyChecking=no python /home/pi/manualPic2.py {0} {1} {2} {3} {4} {5}\
			".format(v1.totalTime, v1.resolutionW, v1.resolutionH, v1.numFrames, v1.timeInterval, v1.internalCamFR)
