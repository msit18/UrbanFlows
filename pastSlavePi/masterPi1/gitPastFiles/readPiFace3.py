#!/usr/bin/env python3

#readPiFace3
#Written by Michelle Sit
#Reads the values from the piFace and sends them to manualPic.py to trigger
#picture capture and sending file process between slavePies and masterPi

import globalVar as gv
import pifacecad 
from pifacecad.tools.question import LCDQuestion
import os

class callAll():
	def askResolution(self, event):
		event.chip.lcd.set_cursor(0,0)
		if event.pin_num == 1:
			cad.lcd.clear()
#			question = LCDQuestion(question="Set resolution", answers=["1920x1080", "2592x1944", "1296x972", "1296x972", "1296x730", "640x480"])
			question = LCDQuestion(question="Set resolution", answers=answers)
			print answers
			answer_index = question.ask()
			print answer_index
			cad.lcd.write("Resolution: " + str(answers[answer_index]))

	def update_pin_text(self,event,res=1):
#		global res
		event.chip.lcd.set_cursor(0,0)
		#event.chip.lcd.write(str(event.pin_num))
	#Toggle resolution
		if event.pin_num == 1:
		#	res += 1
		#	print res
			cad.lcd.clear()
			gv.setTime = 120
			gv.resolutionW = 2594
			gv.resolutionH = 1944
			cad.lcd.write("M:CAM T:1\nR:{0}x{1}".format(gv.resolutionW, gv.resolutionH))
		elif event.pin_num == 2:
			cad.lcd.clear()
			cad.lcd.write("M:Vid T:1\nR:640x480")
			gv.setTime = 120;
			gv.resolutionW = 640
			gv.resolutionH = 480
		elif event.pin_num == 3:
			cad.lcd.clear()
			cad.lcd.write("start!")
			os.system("python /home/pi/manualPic.py {0} {1} {2}".format(gv.setTime, gv.resolutionW, gv.resolutionH))
		elif event.pin_num == 4:
			#os.system("sudo shutdown -h now")
			cad.lcd.clear()
			cad.lcd.write("shut down system")

	def init(self):
		global answers
		answers = ["1920x1080", "2592x1944", "1296x972", "1296x972", "1296x730", "640x480"]
#		gv.setTime = gv.setTime
#		gv.resolutionW = gv.resolutionW
#		gv.resolutionH = gv.resolutionH
#		gv.res = gv.res
#		print "readPiFace RW: " + str(gv.resolutionW)

	def main(self):
		global cad, p1
		cad = pifacecad.PiFaceCAD()
		cad.lcd.clear()
		p1.init()
		#cad.lcd.write("M:CAM T:1\nR:640x480")
		listener = pifacecad.SwitchEventListener(chip=cad)
		listener.register(1, pifacecad.IODIR_FALLING_EDGE, p1.askResolution)
#		for i in range(8):
#			listener.register(i, pifacecad.IODIR_FALLING_EDGE, p1.update_pin_text)
#			cad.lcd.clear()
		listener.activate()

if __name__ == '__main__': 
	gv.init()
	p1 = callAll()
	p1.main()







#cad = pifacecad.PiFaceCAD()
#cad.lcd.clear()
#cad.lcd.write("M:Cam T:1\nR:640x480")
	#cad.lcd.write("You pressed: ")
#listener = pifacecad.SwitchEventListener(chip=cad)
#for i in range(8):
#	listener.register(i, pifacecad.IODIR_FALLING_EDGE, update_pin_text)
#	cad.lcd.clear()
#listener.activate()
