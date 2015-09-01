import network
import sys
import time
import os

def heard(phrase):
	print "heard:" + phrase
	print "def heard phrase"

if(len(sys.argv) >= 2):
  network.call(sys.argv[1], whenHearCall=heard)
else:
  network.wait(whenHearCall=heard)

while network.isConnected():
  phrase = input()
  print("me:" + phrase)
  network.say(phrase)
