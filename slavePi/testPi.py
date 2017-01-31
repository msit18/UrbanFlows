from twisted.internet.defer import DeferredSemaphore, DeferredList
from twisted.internet.task import LoopingCall
from twisted.internet import reactor, defer
# from twisted.internet import reactor, defer
import glob, time, datetime, picamera

recordTimes = "01/24/17 12:00:00 01/24/17 12:15:00 01/24/17 12:30:00"

def takeVideo (startTime):
	print "startTime: ", startTime
	d = defer.Deferred()
	camera = picamera.PiCamera()
	
	inputResW = 1600
	inputResH = 1200
	inputTotalTime = 20
	inputFramerate = 15
	serverIP = "18.89.4.173"
	piName = "pi9"

	while time.time() < startAtTime:
		pass
	else:
		# try:
		print "inputTotalTime: ", inputTotalTime
		camera.resolution = (inputResW, inputResH)
		camera.framerate = inputFramerate
		camera.start_recording(str(piName) + '_RW' + str(inputResW) + '_RH' + str(inputResH)\
			+ '_TT' + str(inputTotalTime) + '_FR' + str(inputFramerate)\
			+ '_' + datetime.datetime.now().strftime ('%m_%d_%Y_%H_%M_%S_%f') + '.h264')
		start = time.time()
		print "camera wait recording"
		camera.wait_recording(inputTotalTime)
		camera.stop_recording()
		camera.close()
		end = time.time()
		total = end-start
		print "CAMERA IS FINISHED: ", total
		d.addCallback(lambda _: reactor.callLater(0.5, self.transport.write, 'finished'))
	return "Finished"
		# return d
		# except:
		# 	print "error"
		# 	print "Switched runUpload"
		# 	raise
			# return d

def run():
	with picamera.PiCamera() as camera:
	    camera.resolution = (1600, 1200)
	    camera.start_recording('my_video.h264')
	    camera.wait_recording(20)
	    camera.stop_recording()	


def method(startTime):
	# result = threads.deferToThread(tv.takeVideo, int(msgFromServer[2]), int(msgFromServer[3]), int(msgFromServer[4]),\
	# 	int(msgFromServer[5]), startAtTime, serverIP, piName)
	# flockRecordCMD = "/usr/bin/flock --nonblock --wait 5 /tmp/fcj.lockfile python /home/pi/UrbanFlows/slavePi/recordVideoBash.sh.py $1 $2"
	# call
	result = threads.deferToThread(takeVideo, startTime)
	# result.addCallback(lambda _: reactor.callLater(0.5, self.transport.write, 'finished'))
	# result.addErrback(self.failedMethod)
	# return result

def calculateTimeDifference(dateToEnd, timeToEnd):
	fullString = dateToEnd + " " + timeToEnd
	endTime = datetime.datetime.strptime(fullString, "%x %X")
	nowTime = datetime.datetime.today()
	difference = endTime - nowTime
	return time.time() + difference.total_seconds()

recordTimesList = [data for data in recordTimes.split()]
times = []
for runs in range(len(recordTimesList)/2):
	print "recordTimes:", recordTimesList
	# recordTimeStartTime = recordTimesList.pop(0) + " " + recordTimesList.pop(0)
	# print "start time: ", recordTimeStartTime
	startAtTime = calculateTimeDifference(recordTimesList.pop(0), recordTimesList.pop(0))
	times.append(startAtTime)
	# method(startAtTime)
	takeVideo(startAtTime)


# print takeVideo(time.time())
# time.sleep(1)
# print takeVideo(time.time())
# run()