#/!/usr/bin/python

#Written by Michelle Sit

#WORK IN PROGRESS

#Edited from manualPic4.py.  Takes pictures on
#one thread and on another thread moves/removes them to the server.  Picture resolution,
#fps, and time are controlled by inputs

#Update: also provides updates every twenty minutes (CURRENTLY SET TO EVERY 10 MINUTES) on
#the program's fps progress while the program is running

import time
import threading
import Queue
import picamera
import datetime
import glob
import os
import string
import sys
import numpy as np

from twisted.web.client import Agent
from twisted.web.http_headers import Headers
from twisted.web.client import FileBodyProducer

#Checks to see if any pictures have been taken and moves/removes them to the MasterPi
#Checks the folder to see if there are any pictures, sends that group to the MasterPi, removes them,
#checks again, repeat picsList is an arrray, list is a string
class queuePictures(threading.Thread):
	def __init__(self, queue, f):
		threading.Thread.__init__(self)
		self.queue = queue
		self.f = f

	def run (self):
		list = ""
		while True:
			runThread = self.queue.get()
			if runThread is 'beginT2':
				picsList = glob.glob('*.jpg')
				while len(picsList) > 0:
					list = ' '.join(picsList)
					print (list)
					os.system("sshpass -p 'raspberry' scp -o StrictHostKeyChecking=no {0}"\
					" pi@10.0.0.1:/home/pi/pastImages/".format(list) )
					os.system("rm {0}".format(list) )
					picsList = []
			elif runThread is 'T1closeT2':
				print >>self.f, '10.2: T2 recieved close message'
#				self.f.close()
				break
			elif runThread is 'exit':
				print >>self.f, "10.2 broken"
#				self.f.close()
				break

	def sendImg(self):
		agent = Agent(reactor)
		body = FileBodyProducer(open("./cute_otter.jpg", 'rb'))
		postImg = agent.request(
		    'POST',
		    "http://localhost:8880/upload-image",
		    Headers({'User-Agent': ['Twisted Web Client Example'],
		    		'Content-Type': ['text/x-greeting']}),
		    body)