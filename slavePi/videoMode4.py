#/!/usr/bin/python

#Written by Michelle Sit

import time, datetime
import picamera, itertools
from twisted.internet import reactor, defer

#Takes video
class TakeVideoClass():
		
	def takeVideo (self, inputResW, inputResH, inputTotalTime, inputFramerate, inputStartTime, serverIP, piName, file):
		# d = defer.Deferred()
		
		while time.time() < inputStartTime:
			pass
		else:
			try:
				camera = picamera.PiCamera()
				print >>file, "inputTotalTime: ", inputTotalTime
				camera.resolution = (inputResW, inputResH)
				camera.framerate = inputFramerate
				camera.start_recording(str(piName) + '_RW' + str(inputResW) + '_RH' + str(inputResH)\
					+ '_TT' + str(inputTotalTime) + '_FR' + str(inputFramerate)\
					+ '_' + datetime.datetime.now().strftime ('%m_%d_%Y_%H_%M_%S_%f') + '.h264')
				print >>file, "camera wait recording"
				# camera.wait_recording(inputTotalTime)
				start = datetime.datetime.now()
				camera.annotate_background = picamera.Color('black')
				camera.annotate_text_size = 18
				while (datetime.datetime.now() - start).seconds < inputTotalTime:
					camera.annotate_text = datetime.datetime.now().strftime('%m_%d_%Y_%H_%M_%S_%f')
					camera.wait_recording(0.01)
				camera.stop_recording()
				camera.close()
				end = datetime.datetime.now()
				total = end-start
				print >>file, "CAMERA IS FINISHED: ", total
				return "Finished"
				# return d
			except picamera.exc.PiCameraMMALError as err:
				print >>file, "CAMERA ERROR: MMAL ERROR"
				self.CamError(err)
				# print "SYS LOG: ", sys.exc_info()
				errMsg = "Err Type: " + str(type(err)) + "\nFailure msg: " + str(err)
				print >>file, "errMsg: ", errMsg
				return errMsg
				# return d
			except:
				print >>file, "UNHANDLED CAMERA ERROR"
				raise

	def CamError(self, failure):
		print >>file, 'CAUGHT THE FUCKER'
		print >>file, "Failure: ", failure
		print >>file, "Failure type: ", type(failure)
		print >>file, "mmmmmmmmmmmm"
		# print "Failure args: ", failure.args

if __name__ == '__main__':
	tv = TakeVideoClass()
	now = time.time() + 1
	tv.takeVideo(1600, 1200, 30, 15, now, '18.89.4.173', 'pi')