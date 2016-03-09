import time, sys
from twisted.internet import reactor, protocol, defer

class doSomeRandom():
	def capturePictures(self, arg1):
		try:
			print "Running capturePictures"
			print arg1
			x = True
			while x == True:
				time.sleep(7)
				x = False
			print "finished capturePictures"
			#print val
			return "True"
		except:
			print "Noooooo wrong"

if __name__ == '__main__':
	l = doSomeRandom()
	l.capturePictures()