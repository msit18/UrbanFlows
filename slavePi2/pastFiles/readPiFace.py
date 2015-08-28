#!/usr/bin/python

#Written by Michelle Sit
#Reads the values from the piFace and sends them to manualPic.py to trigger
#picture capture and sending file process between slavePies and masterPi

import globalVar as gv
import pifacecad as p
#from manualPic import *

class callAll():
	def pifacecmd():
		cad = p.PiFaceCAD()
		s1 = cad.switch_port.value
		print s1

	def run(self):
		gv.setTime = 120
		gv.resolutionW = 640
		gv.resolutionH = 480
		print gv.setTime
		print gv.resolutionW
		print gv.resolutionH

if __name__ == '__main__':
	gv.init()
	c1 = callAll()
	c1.run()
	c1.pifacecmd()
