#Written by Michelle Sit

#Works with piFaceMain.py for the 5Pi architecture
#Sets time

import pifacecad 
from pifacecad.tools.question import LCDQuestion
import time
import variables as v1
from shutdownS5 import shutdownS5

#Constructor
cad = pifacecad.PiFaceCAD()

class timeS3():
	#SET TIME
	#Two different time selection modes depending on if video, camera, or nothing is chosen
	#Uses two different arrays for time: one for user reading, one for file inputs
	def S3():
		print ("timeS3 S3 function")
		cad.lcd.clear()
		#Takes input
		question = LCDQuestion(question="Set TotalTime", answers=v1.totalTimeEngAnswers)
		answer_index = question.ask()
		cad.lcd.clear()
		v1.totalTimeEng = v1.totalTimeEngAnswers[answer_index]
		v1.totalTime = v1.totalTimeAnswers[answer_index]
		#User feedback
		cad.lcd.write("Time selected\n{0}".format(v1.totalTimeEng))
		time.sleep(1)
		cad.lcd.clear()
		#Setting individual video times
		if v1.currentMode == "VID":
			question = LCDQuestion(question= "Set Video Time", answers=v1.totalTimeEngAnswers)
			answer_index = question.ask()
			v1.videoTimeEng = v1.totalTimeEngAnswers[answer_index]
			v1.videoTime = v1.totalTimeAnswers[answer_index]
			cad.lcd.clear()
			cad.lcd.write("VidTime selected\n{0}".format(v1.videoTimeEng))
			time.sleep(1)
			#Double check individual video time is not greater than total time
			if v1.totalTime <  v1.videoTime:
				cad.lcd.clear()
				cad.lcd.write("Error: vidTime\nis too large")
				time.sleep(1)
				timeS3.S3()
			else:
				shutdownS5.homeScreen()
		else:
			shutdownS5.homeScreen()