#Used as an example to show how to use variables across files and how to use functions within functions and across files.
#Example files are resolutionS2.py, piFaceMain.py, and variables.py

#To use, type: python3 piFaceMain.py
#Written by Michelle Sit

import pifacecad 
from pifacecad.tools.question import LCDQuestion
from threading import Barrier

#importing files
import variables as v1
from camVidStartS1 import camVidStartS1
from resolutionS2 import resolutionS2
from timeS3 import timeS3
from setFpsS4 import setFpsS4
from shutdownS5 import shutdownS5

class callAll():

	def setParameters(self, event):
		print ("piFaceMain setParameters function")
		event.chip.lcd.set_cursor(0,0)
#		try:
		#S1: SET CAMERA/VIDEO MODE OR START PROGRAM
		if event.pin_num == 0:
			camVidStartS1.S1()
		#S2: SET RESOLUTION
		elif event.pin_num == 1:
			resolutionS2.S2()
		#S3: SET TIME
		elif event.pin_num == 2:
			timeS3.S3()
		#S4: SET TIMEFRAME
		elif event.pin_num == 3:
			setFpsS4.S4()
		#S5: SHUTDOWN BUTTON
		elif event.pin_num == 4:
			shutdownS5.S5()
		p1.printEverything()
#		except:
#			os.system("python flash.py error MPi")
#			end_barrier.wait()

	def printEverything(self):
		print ("From piFaceMain printEverything")
		print (v1.inputRun)
		print (v1.currentMode)
		print (v1.resolutionW)
		print (v1.resolutionH)
		print (v1.totalTime)
		print (v1.videoTime)
		print (v1.numFrames)
		print (v1.timeInterval)
		print (v1.inputFPS)
		print (v1.internalCamFR)

if __name__ == '__main__': 
	cad = pifacecad.PiFaceCAD()
	p1 = callAll()
	cad.lcd.clear()
	shutdownS5.homeScreen()

	#Note from pifacecad github:
	#listener cannot deactivate itself so we have to wait until it has finished using a barrier
	v1.end_barrier = Barrier(2)

	listener = pifacecad.SwitchEventListener(chip=cad)

	for i in range(8):
		listener.register(i, pifacecad.IODIR_FALLING_EDGE, p1.setParameters)	

	listener.activate()
	v1.end_barrier.wait() #Waiting until exit activated in the S5 method

	#Exit
	listener.deactivate()
