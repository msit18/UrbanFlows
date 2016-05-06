import picamera
import time, datetime
from twisted.internet import defer, reactor
import os
import glob
import subprocess

def printSome(inputPrint, second):
	print "PRINTSOME: ", second

def sendImg(imgName):
	a = defer.Deferred()
	a.callback(lambda _: os.system('curl -X GET http://18.189.119.87:8880/upload-image'))
	a.addCallback(printSome, 'Upload')

def callbackImg():
	# subprocess.call('raspistill -o {0}.jpg -t 20000 -tl 1000 -w 640 -h 480'\
	# 				.format(datetime.datetime.now().strftime ('%M_%S_%f')), shell=True)
	# #subprocess.call('raspistill -o {:%M_%S_%f}.jpg -t 20000 -tl 1000 -w 640 -h 480'\
	# #				.format(datetime.datetime.now()), shell=True)
	# subprocess.call('raspistill -o %04d.jpg -t 20000 -tl 1000 -w 640 -h 480', shell=True)
	with picamera.PiCamera() as camera:
				camera.resolution = (2592, 1944)
				camera.framerate = 90
				v = camera.capture_sequence(runStuff(), use_video_port=False)
				# os.system('curl -X GET http://192.168.10.165:8880/upload-image')
				# d.addCallback(printSome)
				# d.callback("texttext2")
				# sendImg('yep')

def runStuff():
	for i in range(4):
		time.sleep(1)
		print "lols"
		yield 'image_{0}.jpg'.format(i)

callbackImg()
# serverIP = '18.189.71.62'
# fileList = glob.glob('*.jpg')
# for img in fileList:
# 	cmd = \
# 	'if balExp=$(curl -X GET http://{0}:8880/upload-image);'\
# 	' then curl --header "filename: {1}" -y 10 --max-time 180 -X POST --data-binary @{1} http://{0}:8880/upload-image &'\
# 	' wait;'\
# 	' else sudo ifup wlan0; fi'.format(serverIP, img)
# 	print cmd
# 	subprocess.call(cmd, shell=True)
