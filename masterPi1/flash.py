#Written by Michelle Sit
#Controls the piface to provide user feedback.
#Slavepi 10.0.0.5 sends error messages and finished messages when it encounters an error or
#has finished taking pictures.  Attempts to move all the current pictures in the MasterPi home
#folder to a new labeled folder.

#Also triggerd by wifiRestart.sh to provide feedback on its processes

import pifacecad
import os
import time
import sys
import datetime
import subprocess
#from threading import Barrier

def main():
	global cad
	cad = pifacecad.PiFaceCAD()
	#CAMERA ERROR MESSAGE
	if str(sys.argv[1]) == "camError":
		cad.lcd.write("Camera Error:\nPi{0}".format(sys.argv[2]))
		flashScreen(0.25)
		cad.lcd.clear()
		cad.lcd.write("Shutting down\nall Raspies")
		os.system("sshpass -p 'raspberry' ssh pi@10.0.0.2 sudo halt & sshpass -p 'raspberry' ssh pi@10.0.0.3 sudo halt & \
			   sshpass -p 'raspberry' ssh pi@10.0.0.4 sudo halt & sshpass -p 'raspberry' ssh pi@10.0.0.5 sudo halt")
		os.system("sudo halt")

	#GENERAL ERROR MESSAGE
	elif str(sys.argv[1]) == ('error'):
		cad.lcd.write("Error Pi {0}\nTry Again".format(sys.argv[2]))
		flashScreen(0.25)

	#FINISHED MESSAGE
	elif str(sys.argv[1]) == ('fin'):
		cad.lcd.write("Finished capture\nPlease wait")
		#PICTURES MODE
		if len(sys.argv) == 6:
			camParam = "_T" + str(sys.argv[2]) + "_RW" + str(sys.argv[3]) + "_RH" + str(sys.argv[4]) + "_FR" + str(sys.argv[5])
			numImages = subprocess.check_output("ls -1 /home/pi/pastImages/ | wc -l", shell=True)
			print ("NUMIMAGES: " + str(numImages))
			totalTime = int(sys.argv[2])
			print ("TOTALTIME: " + str(totalTime))
			totalFiles = totalTime*20  #normally is 1200
			print ("TOTALFILES: " + str(totalFiles))
			while True:
				if (int(numImages) < totalFiles):
					numImages = subprocess.check_output("ls -1 /home/pi/pastImages/ | wc -l", shell=True)
					print ("MASTERPI NUMIMAGES: " + str(numImages))
					cad.lcd.clear()
					cad.lcd.write("Pics recieved:\n{0}".format(numImages))
					time.sleep(1)
				elif (int(numImages) >= totalFiles):
					print ("moving files")
					cad.lcd.clear()
					cad.lcd.write("Storing files\nPlease wait")
					folderName = datetime.datetime.now().strftime('%d-%m-%Y-%H_%M_%S_%f') + camParam
					os.system("mkdir {0}".format(folderName))
					os.system("mv /home/pi/pastImages/*.jpg /home/pi/{0}/".format(folderName))
					break
			print ("while loop broken")
			cad.lcd.clear()
			cad.lcd.write("finished\nTurning off all")
			flashScreen(0.65)
		#VIDEO MODE
		elif len(sys.argv) == 7:
			camParam = "_T" + str(sys.argv[2]) + "_RW" + str(sys.argv[3]) + "_RH" + str(sys.argv[4]) + "_FR" + str(sys.argv[5]) + "_VT" + str(sys.argv[6])
			numVid = subprocess.check_output("ls -1 /home/pi/pastImages/ | wc -l", shell=True)
			print ("NUMVID: " + str(numVid))
#			totalTime = int(sys.argv[2])*60
#			print ("TOTALTIME: " + str(totalTime))
			vidTime = int(float(sys.argv[6])*60)
			print ("VIDTIME: " + str(vidTime))
#			totalFiles = (totalTime//vidTime)*4
			totalFiles = 4
			print ("TOTALFILES: " + str(totalFiles))
			while True:
				if (int(numVid) < totalFiles):
					numVid = subprocess.check_output("ls -1 /home/pi/pastImages/ | wc -l", shell=True)
					print ("MASTERPI NUMVID: " + str(numVid))
					cad.lcd.clear()
					cad.lcd.write("Vids received:\n{0}".format(numVid))
					time.sleep(1)
				elif (int(numVid) >= totalFiles):
					print ("moving files")
					cad.lcd.clear()
					cad.lcd.write("Storing files\nPlease wait")
					folderName = datetime.datetime.now().strftime('%d-%m-%Y-%H_%M_%S_%f') + camParam
					os.system("mkdir {0}".format(folderName))
					os.system("mv /home/pi/pastImages/*.h264 /home/pi/{0}/".format(folderName))
					break
			print ("while loop broken")
			cad.lcd.clear()
			cad.lcd.write("finished\nTurning off all")
			flashScreen(0.65)

	#WIFI ERROR.  TRIGGERED BY wifiRestart.sh
	elif str(sys.argv[1]) == ('wifiError'):
		cad.lcd.clear()
		cad.lcd.write("Wifi error\nNo wifi")
		flashScreen(0.25)

	#WIFI START MESSAGE.  TRIGGERED BY wifiRestart.sh
	elif str(sys.argv[1]) == ('wifiConnect'):
		cad.lcd.clear()
		cad.lcd.write("Setting up wifi\nPlease wait")

	#CATCH ALL MESSAGE
	else:
		cad.lcd.write("Cmd received:\n{0}".format(sys.argv[1]))
		flashScreen(0.25)
		
def flashScreen(sleepTime):
	for i in range(6):
		cad.lcd.backlight_on()
		time.sleep(sleepTime)
		cad.lcd.backlight_off()
		time.sleep(sleepTime)
	time.sleep(30)
	os.system("sshpass -p 'raspberry' ssh pi@10.0.0.2 -o StrictHostKeyChecking=no sudo halt & sshpass -p 'raspberry' ssh pi@10.0.0.3 -o StrictHostKeyChecking=no sudo halt & \
		   sshpass -p 'raspberry' ssh pi@10.0.0.4 -o StrictHostKeyChecking=no sudo halt & sshpass -p 'raspberry' ssh pi@10.0.0.5 -o StrictHostKeyChecking=no sudo halt")
	os.system("sudo halt")
	os.system("python3 readPiFace4.py")


def home(event):
	os.system("python3 readPiFace4.py")

if __name__ == '__main__':
	main()

#	global end_barrier
#	end_barrier = Barrier(2)
#
#	listener = pifacecad.SwitchEventListener(chip=cad)
#	listener.register(5, pifacecad.IODIR_FALLING_EDGE, home)
#
#	listener.activate()
#	end_barrier.wait()
#
#	listener.deactivate()
