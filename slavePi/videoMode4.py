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
				print "inputTotalTime: ", inputTotalTime
				self.writeFile( "inputTotalTime: " + str(inputTotalTime))
				camera.resolution = (inputResW, inputResH)
				camera.framerate = inputFramerate
				camera.start_recording(str(piName) + '_RW' + str(inputResW) + '_RH' + str(inputResH)\
					+ '_TT' + str(inputTotalTime) + '_FR' + str(inputFramerate)\
					+ '_' + datetime.datetime.now().strftime ('%m_%d_%Y_%H_%M_%S_%f') + '.h264')
				print "camera wait recording"
				self.writeFile( "camera wait recording")
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
				print "CAMERA IS FINISHED: ", total
				self.writeFile( "CAMERA IS FINISHED: " + str(total))
				return "Finished"
				# return d
			except picamera.exc.PiCameraMMALError as err:
				print "CAMERA ERROR: MMAL ERROR"
				self.writeFile( "CAMERA ERROR: MMAL ERROR")
				self.CamError(err)
				# print "SYS LOG: ", sys.exc_info()
				errMsg = "Err Type: " + str(type(err)) + "\nFailure msg: " + str(err)
				print "errMsg: ", errMsg
				self.writeFile( "errMsg: ")
				self.writeFile(errMsg)
				return errMsg
				# return d
			except:
				print "UNHANDLED CAMERA ERROR"
				self.writeFile( "UNHANDLED CAMERA ERROR")
				raise

	def writeFile(self, msg):
		with open("runLog.txt", "a") as myfile:
			myfile.write(msg + "\n")

	def CamError(self, failure):
		print 'CAUGHT THE FUCKER'
		print "Failure: ", failure
		print "Failure type: ", type(failure)
		print "mmmmmmmmmmmm"
		self.writeFile( 'CAUGHT THE FUCKER')
		self.writeFile( "Failure: ")
		self.writeFile(failure)
		self.writeFile( "Failure type: ")
		self.writeFile(str(type(failure)))
		self.writeFile( "mmmmmmmmmmmm")
		# print "Failure args: ", failure.args

if __name__ == '__main__':
	tv = TakeVideoClass()
	now = time.time() + 1
	tv.takeVideo(1600, 1200, 30, 15, now, '18.89.4.173', 'pi')