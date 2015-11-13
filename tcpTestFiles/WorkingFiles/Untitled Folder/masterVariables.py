#Written by Michelle Sit
#Stores the Finished variable for callbackServer3.py
#Also stores all the user inputs for the camera

class MasterVariables():
	def __init__(self):
		self.finStatus = False
		self.ServerTotalTimeSec = ""
		self.ServerResW = ""
		self.ServerResH = ""
		self.ServerNumPics = ""
		self.ServerTimeInterval = ""
		self.ServerFrameRate = ""
		self.goInput = ""
		self.param = ""
		self.camVid = ""

	def getFinStatus(self):
		return self.finStatus

	def getTotalTimeSec(self):
		return self.ServerTotalTimeSec

	def getResW(self):
		return self.ServerResW

	def getResH(self):
		return self.ServerResH

	def getNumPics(self):
		return self.ServerNumPics

	def getTimeInterval(self):
		return self.ServerTimeInterval

	def getFR(self):
		return self.ServerFrameRate

	def getVidTimeSec(self):
		return self.ServerVidTimeSec

	def getCamVid(self):
		return self.camVid

	def getParam(self):
		var = self.getCamVid()
		if var == "camera":
			self.param = "{0} {1} {2} {3} {4} {5} {6}".format(self.getCamVid(), self.getTotalTimeSec(),\
			 self.getResW(), self.getResH(), self.getNumPics(), self.getTimeInterval(),\
			 self.getFR())
		elif var == "video":
			self.param = "{0} {1} {2} {3} {4}".format(self.getCamVid(), self.getVidTimeSec(),\
			self.getResW(), self.getResH(), self.getFR())
		return self.param

	def userInput(self):
		self.camVid = raw_input ('Enter camera or video: ')
		if self.camVid == "camera":
			self.ServerTotalTimeSec = raw_input('Enter total run time in seconds: ')
			self.ServerResW = raw_input('Enter resolution width: ')
			self.ServerResH = raw_input('Enter resolution height: ')
			self.ServerNumPics = raw_input ('Enter number of pictures to take (fps): ')
			self.ServerTimeInterval = raw_input ("Enter time interval (seconds) for frames"\
			" to be taken in (fps): ")
			self.ServerFrameRate = raw_input ('Enter framerate: ')
			print "Thank you for your input. Please check the following"
			print "{0} | TotalTime(sec): {1} | ResW: {2} | ResH: {3} | NumPics: {4} |"\
			"TimeInterval(sec): {5} | FR: {6}".format(self.getCamVid(), \
			self.getTotalTimeSec(), self.getResW(), self.getResH(),\
			self.getNumPics(), self.getTimeInterval(), self.getFR())

		elif self.camVid == "video":
			self.ServerVidTimeSec = raw_input('Enter individual video time(sec): ')
			self.ServerResW = raw_input('Enter resolution width: ')
			self.ServerResH = raw_input('Enter resolution height: ')
			#self.ServerTotalTimeSec = input('Enter total run time in seconds: ')
			self.ServerFrameRate = raw_input ('Enter framerate: ')
			print "Thank you for your input. Please check the following"
			print "{0} | VidTime(sec): {1} | ResW: {2} | ResH: {3} | FR: {4}"\
			.format(self.getCamVid(), self.getVidTimeSec(), self.getResW(),\
			self.getResH(), self.getFR())

		else:
			print "Wrong input. Please try again"
			self.userInput()

		goInput = raw_input ('Run server? Yes or no: ')
		if goInput == "yes":
			print self.getParam()
			print "Running server now"
		elif goInput == "no":
			self.userInput()