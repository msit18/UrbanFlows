#/!/usr/bin/python

#Written by Michelle Sit

import time, datetime
import picamera

from twisted.internet import reactor, defer

#Takes video
class TakeVideoClass():
		
	def takeVideo (self, inputResW, inputResH, inputTotalTime, inputFramerate, inputStartTime, serverIP, piName):
		# d = defer.Deferred()
		
		while time.time() < inputStartTime:
			pass
		else:
			try:
				camera = picamera.PiCamera()
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
				return "Finished"
				# return d
			except picamera.exc.PiCameraMMALError as err:
				print "CAMERA ERROR: MMAL ERROR"
				self.CamError(err)
				# print "SYS LOG: ", sys.exc_info()
				errMsg = "Err Type: " + str(type(err)) + "\nFailure msg: " + str(err)
				print "errMsg: ", errMsg
				return errMsg
				# return d
			except:
				print "UNHANDLED CAMERA ERROR"
				raise

	def CamError(self, failure):
		print 'CAUGHT THE FUCKER'
		print "Failure: ", failure
		print "Failure type: ", type(failure)
		print "mmmmmmmmmmmm"
		# print "Failure args: ", failure.args

if __name__ == '__main__':
	tv = takeVideoClass()
	# now = time.time() + 1
	# tv.takeVideo(1600, 1200, 30, 15, now, '18.89.4.173', 'pi')