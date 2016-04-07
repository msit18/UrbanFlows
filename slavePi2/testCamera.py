import picamera
import time
from twisted.internet import defer, reactor
import os

def printSome(inputPrint):
	print "PRINTSOME: ", inputPrint

def sendImg(imgName):
	a = defer.Deferred()
	a.addCallback(lambda _: os.system('curl -X GET http://192.168.10.165:8880/upload-image'))
	a.addCallback(printSome)
	a.callback('UPLOAD')




#d = defer.Deferred()
#d.addCallback(printSome)
#d.callback("texttext")

#	with picamera.PiCamera() as camera:
#				camera.resolution = (2592, 1944)
#				camera.framerate = 90
#				v = camera.capture_sequence([
#					'image%02d.jpg' % i
#					for i in range(4)
#					], use_video_port=False)
#				os.system('curl -X GET http://192.168.10.165:8880/upload-image')
#				d.addCallback(printSome)
#				d.callback("texttext2")

sendImg('image00.jpg')
sendImg('image01.jpg')
