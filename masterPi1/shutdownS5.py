#Written by Michelle Sit

import pifacecad 
from pifacecad.tools.question import LCDQuestion
import os
import time
#import sys
from threading import Barrier
import subprocess
import variables as v1

#Constructor
cad = pifacecad.PiFaceCAD()

class shutdownS5():

	#SHUTDOWN
	def S5():
		print ("shutdownS5 S5 function")
		cad.lcd.clear()
		question = LCDQuestion(question="Choose cmd:", answers=v1.exitAnswers)
		answers_index = question.ask()
		v1.exitAns = v1.exitAnswers[answers_index]
		cad.lcd.clear()
		if v1.exitAns == "MPi exit prgm":
			question = LCDQuestion(question="MPi exit prgm?", answers=v1.exitConfirm)
			answers_index = question.ask()
			v1.exitAns = v1.exitConfirm[answers_index]
			if v1.exitAns == "Yes":
				cad.lcd.clear()
				cad.lcd.write("Exiting program")
				time.sleep(1)
				cad.lcd.clear()
				v1.end_barrier.wait()
			else:
				shutdownS5.homeScreen()
		elif v1.exitAns == "MPi restart":
			question = LCDQuestion(question="Restart MPi?", answers=v1.exitConfirm)
			answers_index = question.ask()
			v1.exitAns = v1.exitConfirm[answers_index]
			if v1.exitAns == "Yes":
				cad.lcd.clear()
				cad.lcd.write("Restarting MPi")
				time.sleep(1)
				cad.lcd.clear()
				print ("os reboot masterPi")
#				# os.system("sudo reboot")
			else:
				shutdownS5.homeScreen()
		elif v1.exitAns == "Shutdown all":
			question = LCDQuestion(question="Shutdown all?", answers=v1.exitConfirm)
			answers_index = question.ask()
			v1.exitAns = v1.exitConfirm[answers_index]
			if v1.exitAns == "Yes":
				cad.lcd.clear()
				cad.lcd.write("Shutting down\nall")
				time.sleep(1)
				cad.lcd.clear()
				print ("os shutdown all")
#				# os.system("sshpass -p 'raspberry' ssh pi@10.0.0.2 -o StrictHostKeyChecking=no sudo halt & sshpass -p 'raspberry' ssh pi@10.0.0.3 -o StrictHostKeyChecking=no sudo halt & \
#				# sshpass -p 'raspberry' ssh pi@10.0.0.4 -o StrictHostKeyChecking=no sudo halt & sshpass -p 'raspberry' ssh pi@10.0.0.5 -o StrictHostKeyChecking=no sudo halt")
#				# os.system("sudo shutdown -h now")
			else:
				shutdownS5.homeScreen()
		elif v1.exitAns == "Reboot all":
			question = LCDQuestion(question="Reboot all?", answers=v1.exitConfirm)
			answers_index = question.ask()
			v1.exitAns = v1.exitConfirm[answers_index]
			if v1.exitAns == "Yes":
				cad.lcd.clear()
				cad.lcd.write("Rebooting all")
				time.sleep(1)
				cad.lcd.clear()
				print ("Os rebooted")
#				# os.system("sshpass -p 'raspberry' ssh pi@10.0.0.2 -o StrictHostKeyChecking=no sudo reboot & sshpass -p 'raspberry' ssh pi@10.0.0.3 -o StrictHostKeyChecking=no sudo reboot & \
#				# 	   sshpass -p 'raspberry' ssh pi@10.0.0.4 -o StrictHostKeyChecking=no sudo reboot & sshpass -p 'raspberry' ssh pi@10.0.0.5 -o StrictHostKeyChecking=no sudo reboot")
#				# os.system("sudo reboot")
			else:
				shutdownS5.homeScreen()
		elif v1.exitAns == "Num file in fldr":
			numFiles = subprocess.check_output("ls -1 /home/pi/pastImages/ | wc -l", shell=True)
			print (str(numFiles))
			cad.lcd.clear()
			cad.lcd.write("Num files: {0}".format(str(numFiles)))
			time.sleep(2)
			shutdownS5.homeScreen()
		elif v1.exitAns == "Clear mvFolder":
			os.system("rm /home/pi/pastImages/*.jpg & rm /home/pi/pastImages/*.h264")
			cad.lcd.clear()
			cad.lcd.write("Cleared folder")
			time.sleep(1)
			shutdownS5.homeScreen()
		else:
			shutdownS5.homeScreen()


	def homeScreen():
		print ("resolutionS2 S2 function")
		cad.lcd.clear()
		if v1.currentMode == "VID":
			cad.lcd.write("{0} TT{1} VT{2}\nRes:{3}p FR:{4}".format(v1.currentMode, v1.totalTimeEng, v1.videoTimeEng, v1.resolutionH, v1.inputFPS))
		else:
			cad.lcd.write("{0} TT{1}\n{2}F/{3}S Res:{4}p".format(v1.currentMode, v1.totalTimeEng, v1.inputFPS, v1.timeInterval, v1.resolutionH))