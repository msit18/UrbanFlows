import network
import sys
import picamera
import time

camera = picamera.PiCamera()

def heard(phrase):
	print "heard:" + phrase

if (len(sys.argv) >= 2):
  network.call(sys.argv[1], whenHearCall=heard)
else:  
  network.wait(whenHearCall=heard)

while network.isConnected():
  phrase = input() # python3
  print("me:" + phrase)
  camera.start_preview()
  time.sleep(10)
  camera.stop_preview()
  network.say(phrase)
