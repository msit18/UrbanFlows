#/!/usr/bin/python

#Written by Michelle Sit

import time, datetime
import picamera
import glob
import subprocess

from twisted.internet import reactor, defer

#Takes video
class takeVideoClass():
	def __init__(self):
		self.runUpload = True
		
#TODO: NEED ERROR HANDLING HERE FOR WHEN CAMERA FUNCTION FAILS. HOW TO HANDLE THIS? SHOULD NOT RAISE THE ISSUE. SHOULD BE ABLE TO WORK AUTONOMOUSLY
	def takeVideo (self, inputResW, inputResH, inputTotalTime, inputFramerate, inputStartTime, serverIP, piName):
	# def takeVideo (self, inputStartTime):
		# d = defer.Deferred()
		camera = picamera.PiCamera()
		while time.time() < inputStartTime:
			pass
		else:
			try:
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
				self.runUpload = False
				# d.addCallback(lambda _: reactor.callLater(0.5, self.transport.write, 'finished'))
				return "Finished"
				# return d
			except:
				print "error"
				self.runUpload = False
				print "Switched runUpload"
				camera.close()
				raise
				# return d

	# def curlUpload2 (self, serverIP, serverSaveFilePath):
	# 	print "curlUploadImg called"
	# 	self.fileList = glob.glob('*.h264')
	# 	self.fileList.extend(glob.glob('*.bin'))
	# 	self.fileList.sort()
	# 	if len(self.fileList) > 0:
	# 		print "fileList has customers: ", self.fileList
	# 		for item in self.fileList:
	# 			subprocess.call("sshpass -p 'ravenclaw' scp {0} msit@{1}:\"{2}\"".format(item, serverIP, serverSaveFilePath), shell=True)

if __name__ == '__main__':
	tv = takeVideoClass()
	# now = time.time() + 1
	# tv.takeVideo(1600, 1200, 30, 15, now, '18.89.4.173', 'pi')