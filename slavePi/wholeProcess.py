from twisted.internet.defer import DeferredSemaphore, DeferredList
from twisted.internet.task import LoopingCall
# from twisted.internet import reactor, defer
import glob, time, datetime

class wholeProcess():

	def __init__(self):
		self.semi = DeferredSemaphore(1)
		#Should create a global queue list that items can be appended to. 
		#Then use methods to run process and append items to consecutively.

	def scp(self):
		print "stuff"
		time.sleep(0.5)
		return "done"

	def globProcess(self):
		print "globbing"
		file = glob.glob('*.py')
		dl = list()

		for item in range(len(files)):
			dl.append(self.semi.run(sendFiles, files[item]))

		dl = DeferredList(dl)
		def cbFinished(ignored):
			print 'Finishing job'
		dl.addCallback(cbFinished)
		return dl

	def manage(self):
		print "managing queue"
		file = glob.glob('*.py')
		self.semi.run(self.sendFiles, file) #Runs command


	def addToQueue(self):
		self.semi.run(sendFiles, files)



	#Manage whole process
	def runFiles():
	    semi = DeferredSemaphore(1)

	    jobs = []
	    for runs in range(5):
	        jobs.append(semi.run(collectFiles))

	    jobs = DeferredList(jobs)
	    def cbFinished(ignored):
	        print 'Finishing job'
	    jobs.addCallback(cbFinished)
	    return jobs

	#Glob + upload > every 45 mins run this process?
	def collectFiles():
	    semaphore = DeferredSemaphore(1)
	    files = glob.glob('*.py')
	    dl = list()

	    for item in range(len(files)):
	        #Queues list of things to be sent and runs it
	        dl.append(semaphore.run(sendFiles, files[item]))

	    # convert to a DefferedList. Allows for callback call
	    dl = DeferredList(dl)
	    def cbFinished(ignored):
	        print 'Finishing job'
	    dl.addCallback(cbFinished)
	    return dl



	# def runFiles(self, resW, resH, totalTimeSec, framerate, serverIP, piName, recordTimesList):
	def runFiles(self):
	    semi = DeferredSemaphore(1)

	    jobs = []
	    recordTimes = "01/24/17 12:00:00 01/24/17 12:15:00 01/24/17 12:30:00"
	    recordTimesList = [data for data in recordTimes.split()]
	    for runs in range(len(recordTimesList)/2):
	    	print "recordTimes:", recordTimesList
	    	# recordTimeStartTime = recordTimesList.pop(0) + " " + recordTimesList.pop(0)
	    	# print "start time: ", recordTimeStartTime

	    	startAtTime = self.calculateTimeDifference(recordTimesList.pop(0), recordTimesList.pop(0))
	    #     jobs.append(semi.run(tv.takeVideo, int(resW), int(resH), int(totalTimeSec),\
					# int(framerate), startAtTime, serverIP, piName))
	        jobs.append(semi.run(self.sendFiles, startAtTime))

	    jobs = DeferredList(jobs)
	    def cbFinished(ignored):
	        print 'Finishing job'
	        # reactor.callLater(0.5, self.transport.write, 'finished')
	    jobs.addCallback(cbFinished)
	    return jobs

	def calculateTimeDifference(self, dateToEnd, timeToEnd):
		fullString = dateToEnd + " " + timeToEnd
		endTime = datetime.datetime.strptime(fullString, "%x %X")
		nowTime = datetime.datetime.today()
		difference = endTime - nowTime
		return time.time() + difference.total_seconds()


	#Upload SCP files
	def sendFiles(self, img):
	    print "sending img: ", img
	    time.sleep(5)
	    return "finished"

if __name__ == '__main__':
	wp = wholeProcess()
	wp.runFiles()