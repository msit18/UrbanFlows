#Written by Michelle Sit

#Works with piFaceMain.py in 5Pi architecture
#Sets resolution

import pifacecad 
from pifacecad.tools.question import LCDQuestion
import string
import time
import variables as v1
from shutdownS5 import shutdownS5

#Constructor
cad = pifacecad.PiFaceCAD()

class resolutionS2():

	def S2():
		print ("resolutionS2 S2 function")
		cad.lcd.clear()
		# Takes input from piface
		if v1.currentMode == "CAM":
			v1.resAnswers = v1.camResAnswers
		else:
			v1.resAnswers = v1.vidResAnswers
		print (v1.resAnswers)
		question = LCDQuestion(question="Set resolution", answers=v1.resAnswers)
		answer_index = question.ask()
		#Parses answer into resW and resH
		v1.resolutionStr = v1.resAnswers[answer_index]
		resParse = str.split(v1.resolutionStr, 'x')
		v1.resolutionW = resParse[0]
		v1.resolutionH = resParse[1]
		cad.lcd.clear()
		#User feedback
		cad.lcd.write("Res selected: \n{0}x{1}".format(v1.resolutionW, v1.resolutionH))
		time.sleep(1)
		cad.lcd.clear()
		cad.lcd.write("Check frmrate\n is correct")
		time.sleep(1)
		shutdownS5.homeScreen()