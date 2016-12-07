#!/usr/bin/env python3

#readPiFace4
#Written by Michelle Sit
#Reads the values from the piFace and sends them to manualPic.py to trigger
#picture capture and sending file process between slavePies and masterPi
#Using the  LCDQuestion tool and determining if I need to use global variables

import globalVar as gv
import pifacecad 
from pifacecad.tools.question import LCDQuestion
import os
import string
import time
import sys

class callAll():

	def init(self):
		global resAnswers, timeAnswers, resolutionW, resolutionH, inputTime, TFanswers, inputFR, runMode, inputRun, currentMode
		resAnswers = ["1920x1080", "2592x1944", "1296x730", "640x480"]
		timeAnswers = ["1", "2", "3", "4", "5", "6", "7"]
		TFanswers = ["0"]
		runMode = ["CAM", "VID", "START", "Return menu"]
		p1.resolutionW = 0
		p1.resolutionH = 0
		p1.inputTime = 0
		p1.inputFR = 0
		p1.inputRun = ""
		p1.currentMode = "CAM"
		p1.cmdStr = ("sshpass -p 'raspberry' ssh pi@10.0.0.2:/home/pi/manualPics.py {0} {1} {2} {3} & sshpass -p 'raspberry' ssh pi@10.0.0.3:/home/pi/manualPics.py {0} {1} {2} {3}\
			 & sshpass -p 'raspberry' ssh pi@10.0.0.4:/home/pi/manualPics.py {0} {1} {2} {3} & sshpass -p 'raspberry' ssh pi@10.0.0.5:/home/pi/manualPics.py {0} {1} {2} {3}\
			".format(p1.inputTime, p1.resolutionW, p1.resolutionH, p1.inputFR))

	def homeScreen(self):
		cad.lcd.clear()
		cad.lcd.write("{0}: T:{1} TF:{2}\nW:{3} H:{4}".format(p1.currentMode, p1.inputTime, p1.inputFR, p1.resolutionW, p1.resolutionH))

	def setParameters(self, event):
		event.chip.lcd.set_cursor(0,0)
		#S2: SET RESOLUTION
		if event.pin_num == 1:
			cad.lcd.clear()
			#Takes input from piface
			question = LCDQuestion(question="Set resolution", answers=resAnswers)
			answer_index = question.ask()
			#Parses answer into resW and resH
			resolutionStr = resAnswers[answer_index]
			resParse = string.split(resolutionStr, 'x')
			p1.resolutionW = resParse[0]
			p1.resolutionH = resParse[1]
			cad.lcd.clear()
			#User feedback
			cad.lcd.write("Res selected: \n{0}x{1}".format(p1.resolutionW, p1.resolutionH))
			time.sleep(1)
			cad.lcd.clear()
			cad.lcd.write("Check frmrate\n is correct")
			time.sleep(1)
			cad.lcd.clear()
			p1.homeScreen()
		#S3: SET TIME
		#TODO: FIX TIME CHOICES TO APPROPRIATE VALUES
		if event.pin_num == 2:
			cad.lcd.clear()
			#Takes input
			question = LCDQuestion(question="Set time (mins)", answers=timeAnswers)
			answer_index = question.ask()
			cad.lcd.clear()
			#User feedback
			p1.inputTime = timeAnswers[answer_index]
			cad.lcd.write("Time selected: \n{0}".format(p1.inputTime))
			time.sleep(1)
			cad.lcd.clear()
			p1.homeScreen()
		#S4: SET TIMEFRAME
		if event.pin_num == 3:
			cad.lcd.clear()
			#Sets framerate values based on chosen resolution, takes input from piface
			p1.determineFR()
			question = LCDQuestion(question="Set Framerate", answers=p1.TFanswers)
			answer_index = question.ask()
			cad.lcd.clear()
			#User feedback
			p1.inputFR = p1.TFanswers[answer_index]
			cad.lcd.write("FRate selected: \n{0}".format(p1.inputFR))
			time.sleep(1)
			cad.lcd.clear()
			p1.homeScreen()
		#S1: SET CAMERA/VIDEO MODE OR START PROGRAM
		#TODO: Add error handling for video and camera options
		if event.pin_num == 0:
			cad.lcd.clear()
			question = LCDQuestion(question="VID/CAM or START:", answers=runMode)
			answer_index = question.ask()
			cad.lcd.clear()
			p1.inputRun = runMode[answer_index]
			#EXECUTE OS STRING
			#TO DO: NOT FUNCTIONAL
			if p1.inputRun == "START":
				cad.lcd.clear()
				cad.lcd.write("running program")
				os.system("{0}".format(p1.cmdStr))
				time.sleep(1)
				p1.homeScreen()
			#SET STRING TO VIDMODE
			#TODO: DOUBLE CHECK .FORMAT TO ENSURE IT IS SENDING CORRECT PARAMETER TO THE FUNCTION
			#TODO: MAKE FUNCTIONAL
			elif p1.inputRun == "VID":
				p1.currentMode = p1.inputRun
				p1.cmdStr = ("sshpass -p 'raspberry' ssh pi@10.0.0.2:/home/pi/videoMode.py {0} {1} {2} {3} & sshpass -p 'raspberry' ssh pI@10.0.0.3:/home/pi/videoMode.py {0} {1} {2} {3}\
					 & sshpass -p 'raspberry' ssh pi@10.0.0.4:/home/pi/videoMode.py {0} {1} {2} {3} & sshpass -p 'raspberry' ssh pi@10.0.0.5:/home/pi/videoMode.py {0} {1} {2} {3}\
					".format(p1.inputTime, p1.inputFR, p1.resolutionW, p1.resolutionH))
				print p1.cmdStr
				cad.lcd.clear()
				cad.lcd.write("Selected video")
				time.sleep(1)
				p1.homeScreen()
			#SET STRING TO MANUALPIC MODE
			#TODO: MAKE FUNCTIONAL
			elif p1.inputRun == "CAM":
				p1.currentMode = p1.inputRun
				print p1.cmdStr
				p1.cmdStr = ("sshpass -p 'raspberry' ssh pi@10.0.0.2:/home/pi/manualPics.py {0} {1} {2} {3} & sshpass -p 'raspberry' ssh pi@10.0.0.3:/home/pi/manualPics.py {0} {1} {2} {3}\
					 & sshpass -p 'raspberry' ssh pi@10.0.0.3:/home/pi/manualPics.py {0} {1} {2} {3} & sshpass -p 'raspberry' ssh pi@10.0.0.5:/home/pi/manualPics.py {0} {1} {2} {3}\
					".format(p1.inputTime, p1.resolutionW, p1.resolutionH, p1.inputFR))
				cad.lcd.clear()
				cad.lcd.write("Selected pictures")
				time.sleep(1)
				p1.homeScreen()
			#Returns to homescreen
			else:
				cad.lcd.clear()
				p1.homeScreen()
		#S5: SHUTDOWN BUTTON
		#TODO; NOT FUNCTIONAL
		if event.pin_num == 4:
			cad.lcd.clear()
#			os.system("sudo shutdown -h now")
			cad.lcd.write("Ending program")
			time.sleep(1)
			cad.lcd.clear()

	#Helper methods:
	#getFR and determineFR pull different timeframe options depending on the resolutionW selected
	def getFR(self):
		return p1.resolutionH

	def determineFR(self):
		if p1.getFR() == "1080":
			p1.TFanswers = ["1", "5", "15", "30"]
		elif p1.getFR() == "1944":
			p1.TFanswers = ["0.16", "1", "5", "15"]
		elif p1.getFR() == "730":
			p1.TFanswers = ["1", "5", "15", "30", "49"]
		elif p1.getFR() == "480":
			p1.TFanswers = ["49", "60", "90"]
		else:
			p1.TFanswers = ["0"]

	def main(self):
		global cad, p1
		cad = pifacecad.PiFaceCAD()
		cad.lcd.clear()
		p1.init()
		p1.homeScreen()
		listener = pifacecad.SwitchEventListener(chip=cad)
		for i in range(8):
			listener.register(i, pifacecad.IODIR_FALLING_EDGE, p1.setParameters)
		listener.activate()

if __name__ == '__main__': 
	gv.init()
	p1 = callAll()
	try:
		p1.main()
	except (SystemExit):
		sys.exit()
