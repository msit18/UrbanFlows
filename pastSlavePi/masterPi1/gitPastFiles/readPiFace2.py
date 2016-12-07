#!/usr/bin/env python3

#readPiFace2
#Written by Michelle Sit
#Reads the values from the piFace and sends them to manualPic.py to trigger
#picture capture and sending file process between slavePies and masterPi

import globalVar as gv
import pifacecad
import os

class callAll():

	def update_pin_text(self,event):
		event.chip.lcd.set_cursor(0,0)
		#event.chip.lcd.write(str(event.pin_num))
		if event.pin_num == 1:
			cad.lcd.clear()
			cad.lcd.write("M:Cam T:1\nR:2594x1944")
			gv.RPFsetTime = 120
#			print gv.setTime
			gv.resolutionW = 2594
			gv.resolutionH = 1944
		elif event.pin_num == 2:
			cad.lcd.clear()
			cad.lcd.write("M:Vid T:1\nR:640x480")
			gv.RPFsetTime = 120;
			gv.resolutionW = 640
			gv.resolutionH = 480
		elif event.pin_num == 3:
			cad.lcd.clear()
			cad.lcd.write("start!")
#			p1.init()
			os.system("python /home/pi/manualPic.py {0} {1} {2}".format(gv.RPFsetTime, gv.resolutionW, gv.resolutionH))
		elif event.pin_num == 4:
			os.system("sudo shutdown -h now")
#		cad = pifacecad.PiFaceCAD()
#		cad.lcd.clear()
#		cad.lcd.write("M:CAM  T:1\nR:640x480")
#		listener = pifacecad.SwitchEventListener(chip=cad)
#		for i in range(8):
#			listener.register(i,pifacecad.IODIR_FALLING_EDGE, c1.update_pin_text)
#			cad.lcd.clear()
#		listener.activate()

	def init(self):
		gv.setTime = gv.RPFsetTime
		gv.resolutionW = gv.resolutionW
		gv.resolutionH = gv.resolutionH
		print "readPiFace RW: " + str(gv.resolutionW)


#if __name__ == '__main__':
	def main(self):
#		gv.init()
		global cad, p1
		cad = pifacecad.PiFaceCAD()
		cad.lcd.clear()
		cad.lcd.write("M:CAM T:1\nR:640x480")
		listener = pifacecad.SwitchEventListener(chip=cad)
		p1 = callAll()
		for i in range(8):
			listener.register(i, pifacecad.IODIR_FALLING_EDGE, p1.update_pin_text)
			cad.lcd.clear()
		listener.activate()

if __name__ == '__main__':
#	gv.init()
#	print gv.setTime
	p1 = callAll()
	p1.main()

#	c1 = callAll()
#	c1.update_pin_text(event)

#cad = pifacecad.PiFaceCAD()
#cad.lcd.clear()
#cad.lcd.write("M:Cam T:1\nR:640x480")
	#cad.lcd.write("You pressed: ")
#listener = pifacecad.SwitchEventListener(chip=cad)
#for i in range(8):
#	listener.register(i, pifacecad.IODIR_FALLING_EDGE, update_pin_text)
#	cad.lcd.clear()
#listener.activate()

#class callAll():

#	def pifacecmd(self):
#		while True:
#			listener = pifacecad.InputEventListener(chip=cad)
#			listener.register(0, pifacecad.IODIR_RISING_EDGE, print)
#			listener.activate()
#			#s1 = cad.switches[1].value
			#print (s1)

	#def run(self):
	#	gv.setTime = 120
	#	gv.resolutionW = 640
	#	gv.resolutionH = 480
	#	print gv.setTime
	#	print gv.resolutionW
	#	print gv.resolutionH

#if __name__ == '__main__':

#	cad = pifacecad.PiFaceCAD()
	#gv.init()
	#c1 = callAll()
	#c1.run()
	#c1.pifacecmd()
