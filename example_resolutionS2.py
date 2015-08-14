#Used as an example to show how to use variables across files and how to use functions within functions and across files.
#Example files are resolutionS2.py, piFaceMain.py, and variables.py

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

#Constructor
cad = pifacecad.PiFaceCAD()

class resolutionS2():

	def __init__(self, cad):
		self.cad = cad

	def S2(self):
		cad.lcd.clear()
		#Takes input from piface
		# if p1.currentMode == "CAM":
		# 	resAnswers = camResAnswers
		# else:
		resAnswers = v1.vidResAnswers
		question = LCDQuestion(question="Set resolution", answers=resAnswers)
		answer_index = question.ask()
		#Parses answer into resW and resH
		resolutionStr = resAnswers[answer_index]
		resParse = str.split(resolutionStr, 'x')
		v1.resolutionW = resParse[0]
		v1.resolutionH = resParse[1]
		cad.lcd.clear()
		#User feedback
		cad.lcd.write("Res selected: \n{0}x{1}".format(v1.resolutionW, v1.resolutionH))
		time.sleep(1)
		cad.lcd.clear()
		cad.lcd.write("Check frmrate\n is correct")
		time.sleep(1)
		resolutionS2.printResolutions(self)

	def printResolutions(self):
		print(v1.resolutionW)
		print(v1.resolutionH)
