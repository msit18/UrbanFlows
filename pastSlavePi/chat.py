#import network
import sys
import time
import os

def heard(phrase):
	print ("heard:" + phrase)
	os.system("raspistill -o /home/pi/gitFolder/testPicture.jpg")

if (len(sys.argv) >= 2):
  network.call(sys.argv[1], whenHearCall=heard)
else:  
  network.wait(whenHearCall=heard)

while network.isConnected():
  phrase = input() # python3
  print("me:" + phrase)
  network.say(phrase)