#Still being written: callback server.  Used with callbackClient3.py to send data and messages

#TODO: NEED TO FIX LOST CONNECTIONS THING
#TODO: NEED TO INCORPORATE THE TEAM LEADER PI KEEPING TRACK OF CONNECTIONS
#TODO: TEST WITH RASPIES
#TODO: ERROR HANDLING

#Written by Michelle Sit
#Many thanks to Vlatko Klabucar for helping me with the HTTP part!  Also many thanks to Nahom Marie
#for helping me with the architecture of this system!

from twisted.internet.protocol import Factory
from twisted.internet import reactor, protocol, defer, threads
import sys, time
from masterVariables import MasterVariables
#from time import strftime

from twisted.web.server import Site, NOT_DONE_YET
from twisted.web.resource import Resource

import cgi

#sets up the Protocol class
class DataFactory(Factory):
	numConnections = 0

	def __init__(self, data=None):
		self.data = data

	def buildProtocol(self, addr):
		return DataProtocol(self, d)

class DataProtocol (protocol.Protocol):
	global dictFormat
	dictFormat = {}

	def __init__(self, factory, d):
		self.factory = factory
		self.d = defer.Deferred()

	def connectionMade(self):
		self.factory.numConnections += 1
		print >>log, "Connection made at {0}. Number of active connections: {1}".format(time.strftime("%Y-%m-%d-%H:%M:%S"), self.factory.numConnections)

	def connectionLost(self, reason):
		self.factory.numConnections -= 1
		print >>log, "Connection lost at {0}. Number of active connections: {1}".format(time.strftime("%Y-%m-%d-%H:%M:%S"), self.factory.numConnections)

	def dataReceived(self, data):
		print >>log, "DATARECEIVED. Server received data: {0}".format(data)
		msgFromClient = [data for data in data.split()]
		if msgFromClient[0] == "ip":
			print "FOUND AN IP"
			self.d.addCallback(self.gotIP, msgFromClient[2])
			self.d.addErrback(self.failedIP)
			self.d.callback(msgFromClient[1])
		elif msgFromClient[0] == 'imgName':
			print "FOUND AN IMGNAME"
			#print msgFromClient[1]
			f.finStatus = False
			self.setImgName(msgFromClient[1])
		elif msgFromClient[0] == 'finished':
			print >>log, "client is finished"
			endGame = threads.deferToThread(self.checkEnd)
		elif msgFromClient[0] == 'ERROR':
			print >>log, "ERROR FROM PICAMERA at {0}".format(time.strftime("%Y-%m-%d-%H:%M:%S"))
			#TODO: what to do if there is a camera error in one of them?
		else:
			print >>log, "Time: {0}. I don't know what this is: {1}".format(time.strftime("%Y-%m-%d-%H:%M:%S"), data)

	def gotIP(self, piGroup, ipAddr):
		print >>log, "RUNNING GOTIP"
		#adds key and a list containing IP address
		if (piGroup in dictFormat) == False:
			print >>log, "I didn't have this cluster key"
			dictFormat[piGroup] = [ipAddr]
		#appends new IP to the end of the key's list
		elif (piGroup in dictFormat) == True:
			print >>log, "it's true! I have this cluster in my keys"
			dictFormat[piGroup].append(ipAddr)
		else:
			print >>log, "Got something that wasn't an IP. Adding to dict anyway"
			dictFormat[piGroup] = [ipAddr]
		print dictFormat
		reactor.callInThread(self.checkConnections, piGroup)

	def failedIP(self, failure):
		print "FAILURE: NOTIP"
		sys.stderr.write(str(failure))

	#Called in seperate threads. TEST WITH RASPIES
	def checkConnections(self, dataKey):
		print >>log, "RUNNING CHECKCONNECTIONS"
		numValues = len(dictFormat[dataKey])
		while numValues < 0: #Set value to number of Raspies in each cluster
			numValues = len(dictFormat[dataKey])
		else:
			print "SENDING CMDS"
			self.d.addCallback(self.startTakingPictures)
		 	self.d.addErrback(self.failedSendCmds)
	
	#largely redundant method but provides a log of the message
	def writeToClient(self, msg):
		print >>log, "WRITETOCLIENT. Write message to client: {0}".format(msg)
		self.transport.write(msg)

	def startTakingPictures(self, data):
		print "STARTTAKINGPICTURES"
		sendMsg = "Okay startTakingPictures {0}".format(f.getParam())
		print sendMsg
		reactor.callLater(0.1, self.writeToClient, sendMsg)

#TODO: Put in a timeout to check if the msgs were received
	def failedSendCmds(self,failure):
		print "FAILURE: failedSendCmds"
		sys.stderr.write(str(failure))

	def setImgName(self, value):
		print "SETIMGNAME RUNNING"
		global imgName
		imgName = value
		print "This img name will be {0}".format(imgName)
		self.d.addCallback(a.check)
		self.d.addErrback(self.failedSendCmds)
		self.transport.write("Okay gotNameSendImg")

	def checkEnd(self):
		print "RUNNING CHECKEND"
		value = f.getFinStatus()
		print value
		while value == False:
			value = f.getFinStatus()
		else:
			print "end end end end end!"
			self.transport.loseConnection()
			return "done"

#Used for HTTP network.  Receives images and saves them to the server
class UploadImage(Resource):

	def check(self, second):
		print "UPLOADIMAGE CHECK. This is the imageName: {0}".format(imgName)

	def render_GET(self, request):
		print "RENDER GETTING"
		return '<html><body><p>This is the server for the MIT SENSEable City Urban Flows Project.'\
		'  It receives images and saves them to the server.</p></body></html>'

	def render_POST(self, request):
		print "RENDER Posting: {0}".format(imgName)
		print f.getFinStatus()
		with open(imgName, "wb") as file:
			file.write(request.content.read())
		v = request.notifyFinish()
		v.addCallback(self.fin)
		v.addErrback(self.errFin)
		request.finish()
		print "finished writing file"
		return NOT_DONE_YET

	def fin(self, notifyFinStat):
		print "FIN"
		#print notifyFinStat
		print f.finStatus
		f.finStatus = True
		print f.getFinStatus()

	def errFin (self, err):
		print "ERR"
		print err

# class MasterVariables():
# 	def __init__(self):
# 		self.finStatus = False
# 		self.ServerTotalTimeSec = ""
# 		self.ServerResW = ""
# 		self.ServerResH = ""
# 		self.ServerNumPics = ""
# 		self.ServerTimeInterval = ""
# 		self.ServerFrameRate = ""
# 		self.goInput = ""
# 		self.param = ""
# 		self.camVid = ""

# 	def getFinStatus(self):
# 		return self.finStatus

# 	def getTotalTimeSec(self):
# 		return self.ServerTotalTimeSec

# 	def getResW(self):
# 		return self.ServerResW

# 	def getResH(self):
# 		return self.ServerResH

# 	def getNumPics(self):
# 		return self.ServerNumPics

# 	def getTimeInterval(self):
# 		return self.ServerTimeInterval

# 	def getFR(self):
# 		return self.ServerFrameRate

# 	def getVidTimeSec(self):
# 		return self.ServerVidTimeSec

# 	def getCamVid(self):
# 		return self.camVid

# 	def getParam(self):
# 		var = self.getCamVid()
# 		if var == "camera":
# 			self.param = "{0} {1} {2} {3} {4} {5} {6}".format(self.getCamVid(), self.getTotalTimeSec(),\
# 			 self.getResW(), self.getResH(), self.getNumPics(), self.getTimeInterval(),\
# 			 self.getFR())
# 		elif var == "video":
# 			self.param = "{0} {1} {2} {3} {4}".format(self.getCamVid(), self.getVidTimeSec(),\
# 			self.getResW(), self.getResH(), self.getFR())
# 		return self.param

# 	def userInput(self):
# 		self.camVid = raw_input ('Enter camera or video: ')
# 		if self.camVid == "camera":
# 			self.ServerTotalTimeSec = raw_input('Enter total run time in seconds: ')
# 			self.ServerResW = raw_input('Enter resolution width: ')
# 			self.ServerResH = raw_input('Enter resolution height: ')
# 			self.ServerNumPics = raw_input ('Enter number of pictures to take (fps): ')
# 			self.ServerTimeInterval = raw_input ("Enter time interval (seconds) for frames"\
# 			" to be taken in (fps): ")
# 			self.ServerFrameRate = raw_input ('Enter framerate: ')
# 			print "Thank you for your input. Please check the following"
# 			print "{0} | TotalTime(sec): {1} | ResW: {2} | ResH: {3} | NumPics: {4} |"\
# 			"TimeInterval(sec): {5} | FR: {6}".format(self.getCamVid(), \
# 			self.getTotalTimeSec(), self.getResW(), self.getResH(),\
# 			self.getNumPics(), self.getTimeInterval(), self.getFR())

# 		elif self.camVid == "video":
# 			self.ServerVidTimeSec = raw_input('Enter individual video time(sec): ')
# 			self.ServerResW = raw_input('Enter resolution width: ')
# 			self.ServerResH = raw_input('Enter resolution height: ')
# 			#self.ServerTotalTimeSec = input('Enter total run time in seconds: ')
# 			self.ServerFrameRate = raw_input ('Enter framerate: ')
# 			print "Thank you for your input. Please check the following"
# 			print "{0} | VidTime(sec): {1} | ResW: {2} | ResH: {3} | FR: {4}"\
# 			.format(self.getCamVid(), self.getVidTimeSec(), self.getResW(),\
# 			self.getResH(), self.getFR())

# 		else:
# 			print "Wrong input. Please try again"
# 			self.userInput()

# 		goInput = raw_input ('Run server? Yes or no: ')
# 		if goInput == "yes":
# 			print self.getParam()
# 			print "Running server now"
# 		elif goInput == "no":
# 			self.userInput()

if __name__ == '__main__':
	log = open('ServerLog-{0}.txt'.format(time.strftime("%Y-%m-%d-%H:%M:%S")), 'w')
	f = MasterVariables()
	f.userInput()

	#TCP network
	d = defer.Deferred()
	b = DataFactory()
	reactor.listenTCP(8888, b, 200, 'localhost')

	#HTTP network
	a = UploadImage()
	root = Resource()
	root.putChild("upload-image", a)
	factory = Site(root)
	reactor.listenTCP(8880, factory, 200, 'localhost')

	reactor.run()

#self.d.errback(ValueError("Couldn't process your IP request"))