#Written by Michelle Sit
#not finished yet

#To be used with callbackServer3.py to check if user inputs are valid or not.

class inputChecks():

	def __init__(self):
		self.finStatus = False
		self.camVid = ""
		self.ServerTotalTimeSec = ""
		self.ServerResW = ""
		self.ServerResH = ""
		self.ServerNumPics = ""
		self.ServerTimeInterval = ""
		self.ServerFrameRate = ""

	def getCamVid(self):
		return self.camVid

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

	def start(self):
		self.camVid = input('Camera or Video: ').lower()
		print self.camVid
		if self.camVid = "camera":
			pass
		elif self.camVid = "video":
			pass

#TODO: Check for negative numbers
	def totalTimeCheck(self):
		self.ServerTotalTimeSec = input('Enter total run time in seconds: ')
		if self.ServerTotalTimeSec == '0':
			print "Sorry, total time cannot be 0. Please enter a different time."
			self.totalTimeCheck()

	def resWCheck(self)
:		

