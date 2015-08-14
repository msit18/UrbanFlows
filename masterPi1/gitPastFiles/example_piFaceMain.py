#Used as an example to show how to use variables across files and how to use functions within functions and across files.
#Example files are resolutionS2.py, piFaceMain.py, and variables.py

#To use, type: python3 piFaceMain.py
#Written by Michelle Sit

import pifacecad 
from pifacecad.tools.question import LCDQuestion
import os
import string
import time
import sys
from threading import Barrier
import subprocess
from resolutionS2 import resolutionS2
import variables as v1

#Constructor
cad = pifacecad.PiFaceCAD()

class callAll():

	def __init__(self, cad):
		self.cad = cad

	def setParameters(self, event):
		event.chip.lcd.set_cursor(0,0)
		if event.pin_num == 1:
			resolutionS2.S2(self)
			print("haha!")
			p1.printRes()
		else:
			pass

	def printRes(self):
		print(v1.resolutionW)
		print(v1.resolutionH)

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
