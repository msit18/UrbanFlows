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
	a = defer.Deferred()
	a.callback(lambda _: os.system('if balExp=$(curl -X GET http://{0}:8880/upload-image);' \
						' then : ; else sudo ifup wlan0; fi'.format(serverIP)))
	a.addCallback(lambda _: os.system('curl --header "filename: {0}" -y 10 --max-time 180 -X '\
					'POST --data-binary @{0} http://{1}:8880/upload-image'.format(img, serverIP)))
	a.addCallback(lambda _: os.system('rm {0}'.format(img)))
	a.addErrback(printSome, "I messed up")