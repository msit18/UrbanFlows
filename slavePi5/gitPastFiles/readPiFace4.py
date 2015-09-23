#!/usr/bin/env python3

#readPiFace4 - Final program in series.  Used for field testing
#Written by Michelle Sit
#Reads the values from the piFace and sends them to manualPic.py to trigger
#picture capture or videoMode1.py to trigger video capture and sending file process between slavePies and masterPi
#Uses LCDQuestion and sys.argv to send arguments to either video or picture file

import pifacecad 
from pifacecad.tools.question import LCDQuestion
import os
import string
import time
import sys
from threading import Barrier

class callAll():

	def init(self):
		global resAnswers, timeAnswers, vidTimeAnswers, TFanswers, runMode, exitAnswers, exitConfirm
		global resolutionW, resolutionH, inputTime, videoTime, inputFR, inputRun, currentMode, cmdStr, fileName, exitAns
		resAnswers = ["1920x1080", "2592x1944", "1296x730", "640x480"]
		timeAnswers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "13", "15", "17", "20", "23", "25", "30", "45", "60"] #insert forever option at some point
		vidTimeAnswers = ["0.167", "0.33", "0.5", "1", "2", "3", "4", "5", "7", "10", "15", "20"]
		TFanswers = ["0"]
		runMode = ["CAM", "VID", "START", "Return menu"]
		exitAnswers = ["MPi exit prgm", "MPi restart", "Shutdown all", "Reboot all", "Return menu"]
		exitConfirm = ["Yes", "Return menu"]
		p1.resolutionW = 0
		p1.resolutionH = 0
		p1.inputTime = 0 #total duration that the cameras run
		p1.videoTime = 0 #each individual video time (only avail for video optino)
		p1.inputFR = 0
		p1.inputRun = ""
		p1.currentMode = "MODE"
		p1.cmdStr = ""
		p1.fileName = ""
		p1.exitAns = ""

	def homeScreen(self):
	#TODO: FIX THE RESOLUTION NUMBER ISSUE (MAKE SIMPLER).  TEST TO MAKE SURE THE PROGRAM WORKS.
		cad.lcd.clear()
		if p1.currentMode == "VID":
			cad.lcd.write("{0}: TT:{1} TF:{2}\nRes:{3}p VT:{4}".format(p1.currentMode, p1.inputTime, p1.inputFR, p1.resolutionH, p1.videoTime))
		else:
			cad.lcd.write("{0}: TT:{1} TF:{2}\nW:{3} H:{4}".format(p1.currentMode, p1.inputTime, p1.inputFR, p1.resolutionW, p1.resolutionH))

	def setParameters(self, event):
		event.chip.lcd.set_cursor(0,0)
		#S2: SET RESOLUTION
		if event.pin_num == 1:
			p1.S2()
		#S3: SET TIME
		elif event.pin_num == 2:
			p1.S3()
		#S4: SET TIMEFRAME
		elif event.pin_num == 3:
			p1.S4()
		#S1: SET CAMERA/VIDEO MODE OR START PROGRAM
		elif event.pin_num == 0:
			p1.S1()
		#S5: SHUTDOWN BUTTON
		elif event.pin_num == 4:
			p1.S5()

#S1-5 PROGRAMMED COMMANDS:

	#SET RESOLUTION
	def S2(self):
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
		p1.homeScreen()

	#SET TIME
	#Two different time selection modes depending on if video, camera, or nothing is chosen
	def S3(self):
		cad.lcd.clear()
		#Takes input
		question = LCDQuestion(question="Set TotalTime(M)", answers=timeAnswers)
		answer_index = question.ask()
		cad.lcd.clear()
		#User feedback
		if p1.currentMode == "VID":
			#Takes the first time input as total running time 
			p1.inputTime = timeAnswers[answer_index]
			cad.lcd.write("Total Time (min)\n{0}".format(p1.inputTime))
			time.sleep(1)
			cad.lcd.clear()
			question = LCDQuestion(question="Set VideoTime(M)", answers=vidTimeAnswers)
			answer_index = question.ask()
			p1.videoTime = vidTimeAnswers[answer_index]
			cad.lcd.clear()
			cad.lcd.write("Video Time (min)\n{0}".format(p1.videoTime))
			time.sleep(1)
			p1.homeScreen()
		else:
			p1.inputTime = timeAnswers[answer_index]
			cad.lcd.write("Time selected: \n{0}".format(p1.inputTime))
			time.sleep(1)
			p1.homeScreen()

	#SET TIMEFRAME
	def S4(self):
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
		p1.homeScreen()

	#SET CAMERA/VIDEO MODE OR START PROGRAM
	#TODO: Add error handling for video and camera options	
	def S1(self):
		cad.lcd.clear()
		question = LCDQuestion(question="VID/CAM or START:", answers=runMode)
		answer_index = question.ask()
		cad.lcd.clear()
		p1.inputRun = runMode[answer_index]
		#Execute os string
		if p1.inputRun == "START":
			cad.lcd.clear()
			cad.lcd.write("Running program")
			#Updates cmdStr with camera or vid inputs first before executing cmd
			p1.updateCMD()
			print p1.cmdStr
			if p1.updateCMD() == "":
				cad.lcd.clear()
				cad.lcd.write("No inputs given!")
			os.system("{0}".format(p1.cmdStr))
			time.sleep(1)
			p1.homeScreen()
		#Set string to video mode
		#TODO: DOUBLE CHECK .FORMAT TO ENSURE IT IS SENDING CORRECT PARAMETER TO THE FUNCTION
		elif p1.inputRun == "VID":
			p1.currentMode = p1.inputRun
			p1.fileName = "videoMode1.py"
			cad.lcd.clear()
			cad.lcd.write("Selected video\nCheck time again")
			time.sleep(2)
			p1.homeScreen()
		#Set string to manual mode
		elif p1.inputRun == "CAM":
			p1.currentMode = p1.inputRun
			p1.fileName = "manualPic.py"
			cad.lcd.clear()
			cad.lcd.write("Selected pictures")
			time.sleep(1)
			p1.homeScreen()
		#Returns to homescreen
		else:
			p1.homeScreen()

	#SHUTDOWN
	def S5(self):
		cad.lcd.clear()
		question = LCDQuestion(question="Choose exit:", answers=exitAnswers)
		answers_index = question.ask()
		p1.exitAns = exitAnswers[answers_index]
		cad.lcd.clear()
		if p1.exitAns == "MPi exit prgm":
			question = LCDQuestion(question="MPi exit prgm?", answers=exitConfirm)
			answers_index = question.ask()
			p1.exitAns = exitConfirm[answers_index]
			if p1.exitAns == "Yes":
				cad.lcd.clear()
				cad.lcd.write("Exiting program")
				time.sleep(1)
				cad.lcd.clear()
				end_barrier.wait()
				
			else:
				p1.homeScreen()
		elif p1.exitAns == "MPi restart":
			question = LCDQuestion(question="Restart MPi?", answers=exitConfirm)
			answers_index = question.ask()
			p1.exitAns = exitConfirm[answers_index]
			if p1.exitAns == "Yes":
				cad.lcd.clear()
				cad.lcd.write("Restarting MPi")
				time.sleep(1)
				cad.lcd.clear()
				os.system("sudo reboot")
			else:
				p1.homeScreen()
		elif p1.exitAns == "Shutdown all":
			question = LCDQuestion(question="Shutdown all?", answers=exitConfirm)
			answers_index = question.ask()
			p1.exitAns = exitConfirm[answers_index]
			if p1.exitAns == "Yes":
				cad.lcd.clear()
				cad.lcd.write("Shutting down\nall")
				time.sleep(1)
				cad.lcd.clear()
				os.system("sshpass -p 'raspberry' ssh pi@10.0.0.2 sudo halt & sshpass -p 'raspberry' ssh pi@10.0.0.3 sudo halt & \
				sshpass -p 'raspberry' ssh pi@10.0.0.4 sudo halt & sshpass -p 'raspberry' ssh pi@10.0.0.5 sudo halt")
				os.system("sudo shutdown -h now")
			else:
				p1.homeScreen()
		elif p1.exitAns == "Reboot all":
			question = LCDQuestion(question="Reboot all?", answers=exitConfirm)
			answers_index = question.ask()
			p1.exitAns = exitConfirm[answers_index]
			if p1.exitAns == "Yes":
				cad.lcd.clear()
				cad.lcd.write("Rebooting all")
				time.sleep(1)
				cad.lcd.clear()
				os.system("sshpass -p 'raspberry' ssh pi@10.0.0.2 sudo reboot & sshpass -p 'raspberry' ssh pi@10.0.0.3 sudo reboot & \
				sshpass -p 'raspberry' ssh pi@10.0.0.4 sudo reboot & sshpass -p 'raspberry' ssh pi@10.0.0.5 sudo reboot")
				os.system("sudo reboot")
			else:
				p1.homeScreen()
		else:
			p1.homeScreen()

	#HELPER METHODS:
	#creates cmd str for START method
	def updateCMD(self):
		p1.cmdStr = "sshpass -p 'raspberry' ssh pi@10.0.0.2 python /home/pi/{0} {1} {2} {3} {4} {5} & sshpass -p 'raspberry' ssh pi@10.0.0.3 python /home/pi/{0} {1} {2} {3} {4} {5} \
		& sshpass -p 'raspberry' ssh pi@10.0.0.4 python /home/pi/{0} {1} {2} {3} {4} {5} & sshpass -p 'raspberry' ssh pi@10.0.0.5 python /home/pi/{0} {1} {2} {3} {4} {5}\
		".format(p1.fileName, p1.inputTime, p1.resolutionW, p1.resolutionH, p1.inputFR, p1.videoTime)

	#determines different timeframe options depending on resolutionW selected
	def determineFR(self):
		if p1.resolutionH == "1080":
			p1.TFanswers = ["1", "5", "15", "30"]
		elif p1.resolutionH == "1944":
			p1.TFanswers = ["0.16", "1", "5", "15"]
		elif p1.resolutionH == "730":
			p1.TFanswers = ["1", "5", "15", "30", "49"]
		elif p1.resolutionH == "480":
			p1.TFanswers = ["49", "60", "90"]
		else:
			p1.TFanswers = ["0"]
		
	def main(self):
		global cad, p1, listener
		cad = pifacecad.PiFaceCAD()
		cad.lcd.clear()
		p1.init()
		p1.homeScreen()

		#Note from pifacecad github:
		#listener cannot deactivate itself so we have to wait until it has finished using a barrier
		global end_barrier
		end_barrier = Barrier(2)

		listener = pifacecad.SwitchEventListener(chip=cad)
		for i in range(8):
			listener.register(i, pifacecad.IODIR_FALLING_EDGE, p1.setParameters)

		listener.activate()
		end_barrier.wait() #Waiting until exit activated in the S5 method

		#Exit
		listener.deactivate()

if __name__ == '__main__': 
	p1 = callAll()
	p1.main()
