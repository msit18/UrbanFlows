#!/usr/bin/env python3

#readPiFace5.py - Derived from readPiFace4.py.  An old file and is no longer used.
#Written by Michelle Sit

#Reads the values from the piFace and sends them to manualPic.py to trigger
#picture capture or videoMode1.py to trigger video capture and sending file process between slavePies and masterPi
#Used on the 4Pi Master/SlavePi architecture
#Uses LCDQuestion and sys.argv to send arguments to either video or picture file

import pifacecad 
from pifacecad.tools.question import LCDQuestion
import os
import string
import time
import sys
from threading import Barrier
import subprocess

#TODO: All variable are messed up.  Need to fix.  Program is not functional
#TODO: FIX TESTRES AND TESTFR DOUBLE EXECUTION ERROR
#TODO: SETUP FPS/FRAMERATE FOR CAMERA
#TODO: DOUBLE CHECK FPS OPTIONS SELECTED AFTERWARD

class callAll():

	def init(self):
		global totalTimeEngAnswers, totalTimeAnswers, resAnswers, vidResAnswers, camResAnswers, numFramesAnswers, camTimeIntervalEngAnswers, camTimeIntervalAnswers
		global FRanswers, customNumFramesAnswers, customTimeIntervalAnswers, runMode, exitAnswers, exitConfirm, exitVerify
		global totalTime, totalTimeEng, videoTime, videoTimeEng, resolutionW, resolutionH, numFrames, timeInterval, inputFPS, inputFR
		global inputRun, currentMode, cmdStr, fileName, exitAns, emergencyAns, check

		#totalTime(Eng)Answers is used for total run time of the program and video time when specified		
		totalTimeEngAnswers = ["10S", "15S", "20S", "30S", "1M", "2M", "3M", "4M", "5M", "7M", "10M", "15M", "20M", "30M", "45M", "1H", "1.5H", "2H"] 
		totalTimeAnswers = ["10", "15", "20", "30", "60", "120", "180", "240", "300", "420", "900", "1200", "1800", "2700", "3600", "5400", "7200"]

		resAnswers = []
		vidResAnswers = ["1920x1080", "1296x730", "640x480"]
		camResAnswers = ["2592x1944", "1920x1080", "1296x730", "640x480"]
		numFramesAnswers = ["0"]

		camTimeIntervalEngAnswers = ["1S", "2S", "3S", "5S", "10S", "15S", "20S", "30S", "1M", "2M", "3M", "5M", "10M", "15M", "20M", "30M", "1H", "1.5H", "2H"]
		camTimeIntervalAnswers = ["1", "2", "3", "5", "10", "15", "20", "30", "60", "120", "180", "300", "600", "900", "1200", "1800", "3600", "5400", "7200"]

		FRanswers = ["0"]

		customNumFramesAnswers = ["1", "2", "3", "4", "5"]
		customTimeIntervalAnswers = ["2", "3", "4", "5"]
				
		runMode = ["CAM", "VID", "START", "Return menu"]
		exitAnswers = ["MPi exit prgm", "MPi restart", "Shutdown all", "Reboot all", "Return menu", "Num file in fldr", "Clear mvFolder"]
		exitConfirm = ["Yes", "Return menu"]
		exitVerify = ["Yes", "Continue"]

		p1.totalTime = 0 #total duration that the cameras run
		p1.totalTimeEng = 0
		p1.videoTime = 0 #time per video
		p1.videoTimeEng = 0
		p1.resolutionW = 0
		p1.resolutionH = 0
		#Used to set camera fps
		p1.numFrames = 0
		p1.timeInterval = 0
		p1.inputFR = 0 #Used to designate framerate (fps) for video.  Used to set internal camera framerate (different for fps for camera)


		p1.inputFPS = "{0}fps".format(p1.inputFR)

		p1.inputRun = ""
		p1.currentMode = "MODE"
		p1.cmdStr = ""
#		p1.fileName = ""
		p1.exitAns = ""
		p1.emergencyAns = ""
		p1.check = ["0"]

	def homeScreen(self):
		cad.lcd.clear()
		if p1.currentMode == "VID":
			cad.lcd.write("{0} TT{1} VT{2}\nRes:{3}p FR:{4}".format(p1.currentMode, p1.totalTimeEng, p1.videoTimeEng, p1.resolutionH, p1.inputFR))
		else:
			cad.lcd.write("{0} TT{1}\n{2} Res:{3}p".format(p1.currentMode, p1.totalTimeEng, p1.inputFPS, p1.resolutionH))

	def setParameters(self, event):
		event.chip.lcd.set_cursor(0,0)
#		try:
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
#		except:
#			os.system("python flash.py error MPi")
#			end_barrier.wait()

#S1-5 PROGRAMMED COMMANDS:

	#SET RESOLUTION
	def S2(self):
		cad.lcd.clear()
		#Takes input from piface
		if p1.currentMode == "CAM":
			resAnswers = camResAnswers
		else:
			resAnswers = vidResAnswers
		question = LCDQuestion(question="Set resolution", answers=resAnswers)
		answer_index = question.ask()
		#Parses answer into resW and resH
		resolutionStr = resAnswers[answer_index]
		resParse = str.split(resolutionStr, 'x')
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
	#Uses two different arrays for time: one for user reading, one for file inputs
	def S3(self):
		cad.lcd.clear()
		#Takes input
		question = LCDQuestion(question="Set TotalTime", answers=totalTimeEngAnswers)
		answer_index = question.ask()
		cad.lcd.clear()
		p1.totalTimeEng = totalTimeEngAnswers[answer_index]
		p1.totalTime = totalTimeAnswers[answer_index]
		#User feedback
		cad.lcd.write("Time selected\n{0}".format(p1.totalTimeEng))
		time.sleep(1)
		cad.lcd.clear()
		#Setting individual video times
		if p1.currentMode == "VID":
			question = LCDQuestion(question= "Set Video Time", answers=totalTimeEngAnswers)
			answer_index = question.ask()
			p1.videoTimeEng = totalTimeEngAnswers[answer_index]
			p1.videoTime = totalTimeAnswers[answer_index]
			cad.lcd.clear()
			cad.lcd.write("VidTime selected\n{0}".format(p1.videoTimeEng))
			time.sleep(1)
			#Double check individual video time is not greater than total time
			if p1.totalTime <  p1.videoTime:
				cad.lcd.clear()
				cad.lcd.write("Error: vidTime\nis too large")
				time.sleep(1)
				p1.S3()
			else:
				p1.homeScreen()
		else:
			p1.homeScreen()

	#SET FRAMERATE
	def S4(self):
		cad.lcd.clear()
		#Sets framerate values based on chosen resolution, takes input from piface
		p1.determineFR()
		question = LCDQuestion(question="Set Framerate", answers=p1.FRanswers)
		answer_index = question.ask()
		cad.lcd.clear()
		#User feedback
		p1.inputFR = p1.FRanswers[answer_index]
		p1.setCamFramesAndTime()
		p1.manualFRSelect()
		cad.lcd.write("FRate selected: \n{0}".format(p1.inputFR))
		time.sleep(1)
		p1.homeScreen()

#TODO: NOT EDITED
	#SET CAMERA/VIDEO MODE OR START PROGRAM
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
			print (p1.cmdStr)
			if p1.updateCMD() == "":
				cad.lcd.clear()
				cad.lcd.write("No inputs given!")
			else:
				pass
#				os.system("{0}".format(p1.cmdStr))
		#Set string to video mode
		elif p1.inputRun == "VID":
			p1.currentMode = p1.inputRun
#			p1.fileName = "videoMode1.py"
			cad.lcd.clear()
			cad.lcd.write("Selected video\nCheck res")
			time.sleep(1)
			p1.homeScreen()
		#Set string to manual mode
		elif p1.inputRun == "CAM":
			p1.currentMode = p1.inputRun
#			p1.fileName = "manualPic2.py"
			cad.lcd.clear()
			cad.lcd.write("Selected pictures\nCheck res")
			time.sleep(1)
			p1.homeScreen()
		#Returns to homescreen
		else:
			p1.homeScreen()

	#SHUTDOWN
	def S5(self):
		cad.lcd.clear()
		question = LCDQuestion(question="Choose cmd:", answers=exitAnswers)
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
				os.system("sshpass -p 'raspberry' ssh pi@10.0.0.2 -o StrictHostKeyChecking=no sudo halt & sshpass -p 'raspberry' ssh pi@10.0.0.3 -o StrictHostKeyChecking=no sudo halt & \
				sshpass -p 'raspberry' ssh pi@10.0.0.4 -o StrictHostKeyChecking=no sudo halt & sshpass -p 'raspberry' ssh pi@10.0.0.5 -o StrictHostKeyChecking=no sudo halt")
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
				os.system("sshpass -p 'raspberry' ssh pi@10.0.0.2 -o StrictHostKeyChecking=no sudo reboot & sshpass -p 'raspberry' ssh pi@10.0.0.3 -o StrictHostKeyChecking=no sudo reboot & \
					   sshpass -p 'raspberry' ssh pi@10.0.0.4 -o StrictHostKeyChecking=no sudo reboot & sshpass -p 'raspberry' ssh pi@10.0.0.5 -o StrictHostKeyChecking=no sudo reboot")
				os.system("sudo reboot")
			else:
				p1.homeScreen()
		elif p1.exitAns == "Num file in fldr":
			numFiles = subprocess.check_output("ls -1 /home/pi/pastImages/ | wc -l", shell=True)
			print (str(numFiles))
			cad.lcd.clear()
			cad.lcd.write("Num files:\n{0}".format(str(numFiles)))
			time.sleep(2)
			p1.homeScreen()
		elif p1.exitAns == "Clear mvFolder":
			os.system("rm /home/pi/pastImages/*.jpg & rm /home/pi/pastImages/*.h264")
			cad.lcd.clear()
			cad.lcd.write("Cleared folder")
			time.sleep(1)
			p1.homeScreen()
		else:
			p1.homeScreen()

#HELPER METHODS:
	#creates cmd str for START method.  Also checks for absent inputs
	def updateCMD(self):
		if p1.fileName == "" or p1.totalTime == 0 or p1.resolutionW == 0 or p1.resolutionH == 0 or p1.inputFR == 0 or \
					(p1.currentMode == "CAM" and p1.numFrames == 0) or (p1.currentMode == "VID" and p1.videoTime == 0):
			cad.lcd.clear()
			cad.lcd.write("Check inputs")
			time.sleep(2)
			p1.homeScreen()
		elif p1.inputFR != 0:
			p1.testFR()
			p1.testRes()

	#determines different timeframe options depending on resolutionW selected
	def determineFR(self):
		if p1.currentMode == "VID":
			if p1.resolutionH == "1080":
				p1.FRanswers = ["15", "30"]
			elif p1.resolutionH == "730":
				p1.FRanswers = ["15", "30", "49"]
			elif p1.resolutionH == "480":
				p1.FRanswers = ["1", "49", "60", "90"]
			else:
				p1.FRanswers = ["0"]	
		elif p1.currentMode == "CAM":
			if p1.resolutionH == "1080":
				p1.FRanswers = ["1", "2", "3", "5", "8", "Custom"]
				p1.frameRate = 90
			elif p1.resolutionH == "1944":
				p1.FRanswers = ["1", "2", "3", "5", "Custom"]
			elif p1.resolutionH == "730":
				p1.FRanswers = ["1", "3", "5", "15", "18", "Custom"]
			elif p1.resolutionH == "480":
				p1.FRanswers = ["10", "20"]
			else:
				p1.FRanswers = ["0"]
#			p1.manualFRSelect()
#			p1.setCamFramesAndTime()
		else:
			p1.FRanswers = ["0"]

	#If 'Custom' is selected as the framerate, asks user questions to get framerate
	def manualFRSelect(self):
		if p1.inputFR == "Custom":
			question = LCDQuestion(question="Set numFrames", answers = customNumFramesAnswers)
			answer_index = question.ask()
			p1.numFrames = customNumFramesAnswers[answer_index]
			cad.lcd.clear()
			question = LCDQuestion(question="Set time (sec)", answers = customTimeIntervalAnswers)
			answer_index = question.ask()
			p1.timeInterval = customTimeIntervalAnswers[answer_index]
			cad.lcd.clear()
			cad.lcd.write("Selected framerate:\n{0} frames/{1} secs".format(p1.numFrames, p1.timeInterval) )
			p1.inputFPS = "{0}F/{1}S".format(p1.numFrames, p1.timeInterval)
			time.sleep(2)
			p1.homeScreen()
		else:
			pass

	#Takes the selected framerate for camera mode and sets the appropriate number of frames and time interval
	def setCamFramesAndTime(self):
		#default time interval is 1 second
		p1.timeInterval = 1
		if p1.inputFR == "1":
			p1.numFrames = 1
		if p1.inputFR == "2" and p1.resolutionH != "1944":
			p1.numFrames = 2

		if p1.resolutionH == "1080":
			if p1.inputFR == "3":
				p1.numFrames = 4
			elif p1.inputFR == "5":
				p1.numFrames = 8
			elif p1.inputFR == "8":
				p1.numFrames = 50
				p1.timeInterval = 2

		elif p1.resolutionH == "1944":
			if p1.inputFR == "2":
				p1.numFrames = 3
			elif p1.inputFR == "3":
				p1.numFrames = 7
			elif p1.inputFR == "5":
				p1.numFrames = 25

		elif p1.resolutionH == "730":
			if p1.inputFR == "5":
				p1.numFrames = 5
			elif p1.inputFR == "15":
				p1.numFrames = 30
			elif p1.inputFR == "18":
				p1.numFrames = 40
				p1.timeInterval = 2

		elif p1.resolutionH == "480":
			if p1.inputFR == "10":
				p1.numFrames = 10
			elif p1.inputFR == "20":
				p1.numFrames = 20
		print ("numFrames selected: " + str(p1.numFrames) )
		p1.inputFPS = "{0}fps".format(p1.inputFR)

	#Checks that the framerate is correct for that resolution
	#0 indicates false, 1 indicates true statement
	def testFR(self):
		p1.determineFR()
		if p1.inputFR == "Custom":
			pass
		else:
			if p1.FRanswers.count(p1.inputFR) == 0:
				cad.lcd.clear()
				cad.lcd.write("Wrong frameRate\nTry again")
				time.sleep(1)
				p1.homeScreen()
			elif p1.FRanswers.count(p1.inputFR) > 0:
				pass

#TODO: NOT TESTED YET
#TESTRES AND TESTFR ARE EXECUTING TWICE
	#Checks that current mode and resolution are appropriate
	def testRes(self):
		print ("Running testRes")
		if p1.currentMode == "VID" and p1.resolutionH == "1944":
			cad.lcd.clear()
			cad.lcd.write("Wrong res\nTry again")
			time.sleep(1)
			p1.homeScreen()
		else:
			p1.runCMD()

	#Sends commands to the slavePies with two different modes for camera or video.  For camera mode, sets the frameRate (different from framerate specified in this code)
	#depending on the resolution selected
	def runCMD(self):
		if p1.currentMode == "VID":
			p1.cmdStr = "sshpass -p 'raspberry' ssh pi@10.0.0.2 -o StrictHostKeyChecking=no python /home/pi/videoMode1.py {0} {1} {2} {3} {4} & \
				     sshpass -p 'raspberry' ssh pi@10.0.0.3 -o StrictHostKeyChecking=no python /home/pi/videoMode1.py {0} {1} {2} {3} {4} & \
				     sshpass -p 'raspberry' ssh pi@10.0.0.4 -o StrictHostKeyChecking=no python /home/pi/videoMode1.py {0} {1} {2} {3} {4} & \
				     sshpass -p 'raspberry' ssh pi@10.0.0.5 -o StrictHostKeyChecking=no python /home/pi/videoMode1.py {0} {1} {2} {3} {4}\
			".format(p1.videoTime, p1.resolutionW, p1.resolutionH, p1.totalTime, p1.inputFR)
		elif p1.currentMode == "CAM":
			if p1.resolutionH == "730" or p1.resolutionH == "1944":
				p1.inputFR = 50
			elif p1.resolutionH == "1080" or p1.resolutionH == "480":
				p1.inputFR = 90
			p1.cmdStr = "sshpass -p 'raspberry' ssh pi@10.0.0.2 -o StrictHostKeyChecking=no python /home/pi/manualPic2.py {0} {1} {2} {3} {4} {5} & \
				     sshpass -p 'raspberry' ssh pi@10.0.0.3 -o StrictHostKeyChecking=no python /home/pi/manualPic2.py {0} {1} {2} {3} {4} {5} & \
				     sshpass -p 'raspberry' ssh pi@10.0.0.4 -o StrictHostKeyChecking=no python /home/pi/manualPic2.py {0} {1} {2} {3} {4} {5} & \
				     sshpass -p 'raspberry' ssh pi@10.0.0.5 -o StrictHostKeyChecking=no python /home/pi/manualPic2.py {0} {1} {2} {3} {4} {5}\
			".format(p1.totalTime, p1.resolutionW, p1.resolutionH, p1.numFrames, p1.timeInterval, p1.inputFR)


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
