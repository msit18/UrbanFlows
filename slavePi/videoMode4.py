#/!/usr/bin/python

#Written by Michelle Sit

import time, datetime
import picamera
import glob
import os, sys, subprocess

from twisted.internet.defer import DeferredSemaphore, gatherResults, DeferredList
from twisted.internet.task import deferLater, LoopingCall
from twisted.internet import reactor, defer

#Takes video
class takeVideoClass():
	def __init__(self):
		self.runUpload = True
		self.uploadVideo = False
		
#TODO: NEED ERROR HANDLING HERE FOR WHEN CAMERA FUNCTION FAILS. HOW TO HANDLE THIS? SHOULD NOT RAISE THE ISSUE. SHOULD BE ABLE TO WORK AUTONOMOUSLY
	#def takeVideo (self, inputResW, inputResH, inputTotalTime, inputFramerate, inputStartTime, serverIP, piName):
	def takeVideo (self, inputStartTime):
		# d = defer.Deferred()
		camera = picamera.PiCamera()
		inputResW = 1600
		inputResH = 1200
		inputTotalTime = 20
		inputFramerate = 15
		serverIP = "18.89.4.173"
		piName = "pi9"

		while time.time() < inputStartTime:
			pass
		else:
			try:
				print "inputTotalTime: ", inputTotalTime
				# with picamera.PiCamera() as camera:
				# camera = picamera.PiCamera()
				camera.resolution = (inputResW, inputResH)
				camera.framerate = inputFramerate
				camera.start_recording(str(piName) + '_RW' + str(inputResW) + '_RH' + str(inputResH)\
					+ '_TT' + str(inputTotalTime) + '_FR' + str(inputFramerate)\
					+ '_' + datetime.datetime.now().strftime ('%m_%d_%Y_%H_%M_%S_%f') + '.h264')
				start = time.time()
				print "camera wait recording"
				camera.wait_recording(inputTotalTime)
				camera.stop_recording()
				end = time.time()
				total = end-start
				print "CAMERA IS FINISHED: ", total
				# self.curlUpload2(serverIP, serverSaveFilePath)
				self.runUpload = False
				time.sleep(1)
				# d.addCallback(lambda _: reactor.callLater(0.5, self.transport.write, 'finished'))
				return "Finished"
				# return d
			except:
				print "error"
				self.runUpload = False
				print "Switched runUpload"
				time.sleep(1)
				raise
				# return d
			# finally:
			# 	# d.addCallback(lambda _: reactor.callLater(0.5, self.transport.write, 'finished'))
			# 	camera.stop_recording()
			# 	# print "returning D: ", d
			# 	# return d

	def curlUpload2 (self, serverIP, serverSaveFilePath):
		print "curlUploadImg called"
		self.fileList = glob.glob('*.h264')
		self.fileList.extend(glob.glob('*.bin'))
		self.fileList.sort()
		if len(self.fileList) > 0:
			print "fileList has customers: ", self.fileList
			for item in self.fileList:
				subprocess.call("sshpass -p 'ravenclaw' scp {0} msit@{1}:\"{2}\"".format(item, serverIP, serverSaveFilePath), shell=True)

	# #Run CRON on a file to collect things and upload them. Use Flock to manage the CRON script.
	# #TO DO: Test if the upload scp process actually runs one at a time.
	# #Manage whole process
	# def runFiles():
	#     semi = DeferredSemaphore(1)

	#     jobs = []
	#     for runs in range(5):
	#         jobs.append(semi.run(collectFiles))

	#     jobs = DeferredList(jobs)
	#     def cbFinished(ignored):
	#         print 'Finishing job'
	#     jobs.addCallback(cbFinished)
	#     return jobs

	# #Glob + upload > every 45 mins run this process?
	# def collectFiles():
	#     semaphore = DeferredSemaphore(1)
	#     files = glob.glob('*.py')
	#     dl = list()

	#     for item in range(len(files)):
	#         #Queues list of things to be sent (one item at a time-for loop)
	#         dl.append(semaphore.run(sendFiles, files[item]))

	#     # get a DefferedList
	#     dl = DeferredList(dl)
	#     def cbFinished(ignored):
	#         print 'Finishing job'
	#     dl.addCallback(cbFinished)
	#     return dl

	# #Upload SCP files
	# def sendFiles(img):
	#     print "sending img: ", img
	#     time.sleep(0.5)
	#     return "finished"

if __name__ == '__main__':
	tv = takeVideoClass()
	# now = time.time() + 1
	# tv.takeVideo(1600, 1200, 30, 15, now, '18.89.4.173', 'pi')