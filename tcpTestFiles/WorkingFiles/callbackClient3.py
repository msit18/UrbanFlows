#Working TCP client that runs with callbackServer3
#Works to test callbacks

#TODO: Integration with manualPic and videoMode

#Written by Michelle Sit
#Many thanks to Vlatko Klabucar for helping me with the HTTP part!  Also many thanks to Nahom Marie
#for helping me with the architecture of this system!

#TCP
from twisted.internet import reactor, protocol
import subprocess
#HTTP
from twisted.web.client import Agent
from twisted.web.http_headers import Headers
from twisted.web.client import FileBodyProducer
#Threading for picture transfer
import threading
import Queue
import os
import glob
import time
#import manualPic_capturePhotos

#TCP network portion
class DataClientFactory(protocol.ClientFactory):
	def __init__(self, data):
		self.data = data

	def buildProtocol(self, addr):
		return myProtocol(self)

	def clientConnectionFailed(self, connector, reason):
		print 'connection failed:', reason.getErrorMessage()
		reactor.stop()

	def clientConnectionLost(self, connector, reason):
		print 'connection lost:', reason.getErrorMessage()
		reactor.stop()

class myProtocol(protocol.Protocol):
	def __init__(self, factory):
		self.factory = factory
		self._count = 1

	def connectionMade(self):
		ip_address = subprocess.check_output("hostname --all-ip-addresses", shell=True).strip()
		msg = "ip piGroup1 {0}".format(ip_address)
		self.transport.write(msg)

#TODO: SEND IMG NAME FROM ACTUAL FOLDER BETWEEN DEF
	def dataReceived(self, data):
		print "data Received from Server: {0}".format(data)
		msgFromServer = [data for data in data.split()]
		print msgFromServer[0]
		print msgFromServer[1]
		if msgFromServer[1] == "sendPicName":
			print "GOT A SENDPICNAME"
			#insert cmd to start manualPic5
			#self.transport.write("Hi success.jpg filler")
			#self.sendImg()
			self.runMETHOD()
		elif msgFromServer[1] == "imgToken":
			print "GOT A IMGTOKEN"
			print self._count
		else:
			print "Didn't write hi success.jpg to server"

#Need to rewrite logic for sending pictures and removing them
	def runMETHOD (self):
		print "RUNNING RUNMETHOD"
		imgToken = self._count
		print imgToken
		fileList = glob.glob('/home/michelle/gitFolder/UrbanFlows/tcpTestFiles/*.jpg')
		print fileList
		#This while loop doesn't work because it's waiting for the loop to end before it
		#sends out the message.  It's holding onto the message
		#Thoughts: see if I can change this to a if loop so that it can exit
		#See if I can run this process as a callBack and it calls back every time
		#See if I can pop the top item off the list without having to reverse the whole thing
		#See if I can do something to fix this
		if len(fileList) > 0:
			if imgToken == 1:
				global name
				name = fileList.pop(0)
				print "name: {0}".format(name)
				reactor.callLater(1, self.transport.write, " imgName {0}".format(name))
#				self.transport.write(" imgname {0}".format(name))
				self._count = 0
				imgToken = self._count
				print "end of imgtoken 1 part"
			else: 
				imgToken = self._count

# 		list = ""
# 		while True:
# 			runThread = self.queue.get()
# 			if runThread is 'beginT2':
# 				picsList = glob.glob('*.jpg')
# 				while len(picsList) > 0:
# 					list = ' '.join(picsList)
# 					print (list)
# 					# os.system("sshpass -p 'raspberry' scp -o StrictHostKeyChecking=no {0}"\
# 					# " pi@10.0.0.1:/home/pi/pastImages/".format(list) )
# 					os.system("rm {0}".format(list) )
# 					picsList = []
# 			elif runThread is 'T1closeT2':
# 				print >>self.f, '10.2: T2 recieved close message'
# #				self.f.close()
# 				break
# 			elif runThread is 'exit':
# 				print >>self.f, "10.2 broken"
# #				self.f.close()
# 				break

	def imgSendProcess(self, name):
		print "Running imgSendProcess"
		self.transport.write(" imgName {0}".format(name))
		print "sent name"
		#self.sendImg(name)
		#os.system('rm {0}'.format(name))

# #HTTP network portion
# class sendHTTPImage():
	def sendImg(self, name):
		print name
		agent = Agent(reactor)
		body = FileBodyProducer(open("{0}".format(name), 'rb'))
		postImg = agent.request(
		    'POST',
		    "http://localhost:8880/upload-image",
		    Headers({'User-Agent': ['Twisted Web Client Example'],
		    		'Content-Type': ['text/x-greeting']}),
		    body)

if __name__ == '__main__':
	#reactor.connectTCP('18.111.45.131', 8888, DataClientFactory(data), timeout=200)

	#manualPic setup
	queue = Queue.Queue()
	f = open('manualPic5Output.txt', 'w')
	# t1 = manualPic_capturePhotos.takePictures(queue, f)
	#t2 = queuePictures(queue, f)
	
	#TCP network.  Connects on port 8888
	data = "first data"
	reactor.connectTCP('localhost', 8888, DataClientFactory(data), timeout=200)

	#HTTP network.  Connects on port 8880
	# c = sendHTTPImage()

	reactor.run()