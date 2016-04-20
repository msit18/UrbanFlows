import picamera
import time
from twisted.internet import defer, reactor
import os
import glob

def printSome(inputPrint, second):
	print "PRINTSOME: ", second

def sendImg(imgName):
	a = defer.Deferred()
	# a.callback('start')
	a.callback(lambda _: os.system('curl -X GET http://18.189.119.87:8880/upload-image'))
	a.addCallback(printSome, 'Upload')

def callbackImg():
	with picamera.PiCamera() as camera:
				camera.resolution = (2592, 1944)
				camera.framerate = 90
				v = camera.capture_sequence([
					'image%02d.jpg' % i
					for i in range(4)
					], use_video_port=False)
				# os.system('curl -X GET http://192.168.10.165:8880/upload-image')
				# d.addCallback(printSome)
				# d.callback("texttext2")
				# sendImg('yep')

callbackImg()
serverIP = '18.189.119.87'
fileList = glob.glob('*.jpg')
for img in fileList:
	subprocess.call(
	'if balExp=$(curl -X GET http://{0}:8880/upload-image);'\
	'then curl --header "filename: {1}" -y 10 --max-time 180 -X POST --data-binary @{1} http://{0}:8880/upload-image &'\
	'wait;'\
	# 'rm {1};'\
	'else sudo ifup wlan0;'\
	'fi'.format(serverIP, item)
	)