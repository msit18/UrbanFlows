import pifacecad 
from pifacecad.tools.question import LCDQuestion
import os
import string
import time
import sys
from threading import Barrier
import subprocess

#Constructor
cad = pifacecad.PiFaceCAD()
resolutionW = 0
resolutionH = 0

resAnswers = []
vidResAnswers = ["1920x1080", "1296x730", "640x480"]
camResAnswers = ["2592x1944", "1920x1080", "1296x730", "640x480"]

class callAll():

	def __init__(self, cad):
		self.cad = cad
		self.resolutionW = resolutionW
		self.resolutionH = resolutionH

	def setParameters(self, event):
		event.chip.lcd.set_cursor(0,0)
		if event.pin_num == 1:
			p1.S2()
		else:
			pass

	def S2(self):
		cad.lcd.clear()
		#Takes input from piface
		# if p1.currentMode == "CAM":
		# 	resAnswers = camResAnswers
		# else:
		resAnswers = vidResAnswers
		question = LCDQuestion(question="Set resolution", answers=resAnswers)
		answer_index = question.ask()
		#Parses answer into resW and resH
		resolutionStr = resAnswers[answer_index]
		resParse = str.split(resolutionStr, 'x')
		self.resolutionW = resParse[0]
		self.resolutionH = resParse[1]
		cad.lcd.clear()
		#User feedback
		cad.lcd.write("Res selected: \n{0}x{1}".format(p1.resolutionW, p1.resolutionH))
		time.sleep(1)
		cad.lcd.clear()
		cad.lcd.write("Check frmrate\n is correct")
		time.sleep(1)
		p1.printResolutions()

	def printResolutions(self):
		print(self.resolutionW)
		print(self.resolutionH)

if __name__ == '__main__': 
	p1 = callAll(cad)
	cad.lcd.clear()

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
