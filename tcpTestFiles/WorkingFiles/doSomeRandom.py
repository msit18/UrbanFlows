import time

class doSomeRandom():
	def capturePictures(self):
		print "Running capturePictures"
		time.sleep(10)
		print "finished capturePictures"
		#print val
		return "True"

if __name__ == '__main__':
	l = doSomeRandom()
	l.capturePictures()