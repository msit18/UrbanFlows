#/!/usr/bin/python

#Written by Michelle Sit

import time
import picamera
import datetime
import glob
import os
import sys
import subprocess

#Takes video
class takeVideoClass():
	def __init__(self):
		self.runUpload = True

	# self.camVid, self.ServerVidTimeSec, self.ServerResW,\
	# self.ServerResH, self.ServerTotalTimeSec, self.ServerFrameRate, \
	# self.ServerStartTime, self.numRaspiesInCluster

	def takeVideo (self, inputResW, inputResH, inputTotalTime, inputFramerate, inputStartTime, serverIP):
		while time.time() < inputStartTime:
			pass
		else:
			try:
				#numCycles = int(inputTotalTime)/int(inputVidTimeChunk)
				print "inputTotalTime: ", inputTotalTime
				#print "inputVidTimeChunk: ", inputVidTimeChunk
				#print "numCycles: ", numCycles
				with picamera.PiCamera() as camera:
					camera.resolution = (inputResW, inputResH)
					camera.framerate = inputFramerate
					videoName = 'slavePi2_RW' + str(inputResW) + '_RH' + str(inputResH)\
						+ '_TT' + str(inputTotalTime) + '_FR' + str(inputFramerate)\
						+ '_' + datetime.datetime.now().strftime ('%m_%d_%Y_%H_%M_%S_%f') + '.h264'
					camera.start_recording(videoName)
					start = time.time()
					print "camera wait recording"
					camera.wait_recording(inputTotalTime)
					end = time.time()
					total = end-start
					print "camera is finished: ", total
				print "CAMERA IS FINISHED. RETURN FALSE"
				self.runUpload = False
				return videoName
			except:
				print "error"
				self.runUpload = False
				print "Switched runUpload"
				raise

	def curlUpload (self, serverIP):
		print "curlUploadImg called"
		self.fileList = glob.glob('*.h264')
		#self.fileList.extend(glob.glob('*.bin'))
		self.fileList.sort()
		if len(self.fileList) > 0:
			print "fileList has customers: ", self.fileList
			for item in self.fileList:
				cmd = \
					'if balExp=$(curl -X GET http://{0}:8880/upload-image);'\
					' then curl -C - --header "filename: {1}" -y 10 --max-time 180 -X POST --data-binary @{1} http://{0}:8880/upload-image &'\
					' wait;'\
					' rm {1};'\
					' wait;'\
					' else sudo ifup wlan0;'\
					' fi'.format(serverIP, item)
				#print "cmd: ", cmd
				subprocess.call(cmd, shell=True)

	def curlUpload2 (self, serverIP):
		print "curlUploadImg called"
		self.fileList = glob.glob('*.h264')
		#self.fileList.extend(glob.glob('*.bin'))
		self.fileList.sort()
		if len(self.fileList) > 0:
			print "fileList has customers: ", self.fileList
			for item in self.fileList:
				subprocess.call("sshpass -p 'ravenclaw' scp {0} msit@18.132.1.9:/home/msit/".format(item), shell=True)
		return self.fileList

	def sendUpload2(self, serverIP):
		while self.runUpload == True:
			self.fileList = glob.glob('*.h264')
			self.fileList.sort()
			if len(self.fileList) > 0:
				print "fileList has customers: ", self.fileList
				for item in self.fileList:
					subprocess.call("sshpass -p 'ravenclaw' scp {0} msit@18.132.1.9:/home/msit/".format(item), shell=True)
			#print "sleeping for 1 seconds"
			time.sleep(1)
		else:
			print "runing last glob"
			self.curlUpload(serverIP)	
			self.curlUpload(serverIP)
			print "last catch"
			return "finished"

	def sendUpload(self, inputStartTimePlusOne, serverIP):
		while time.time() < inputStartTimePlusOne:
			pass
		else:
			while self.runUpload == True:
				self.fileList = glob.glob('*.h264')
				self.fileList.extend(glob.glob('*.bin'))
				self.fileList.sort()
				if len(self.fileList) > 0:
					print "fileList has customers: ", self.fileList
					for item in self.fileList:
						cmd = \
							'if balExp=$(curl -X GET http://{0}:8880/upload-image);'\
							' then curl -C - --header "filename: {1}" -y 10 --max-time 180 -X POST --data-binary @{1} http://{0}:8880/upload-image &'\
							' wait;'\
							' rm {1};'\
							' wait;'\
							' else sudo ifup wlan0;'\
							' fi'.format(serverIP, item)
						#print "cmd: ", cmd
						subprocess.call(cmd, shell=True)
				#print "sleeping for 1 seconds"
				time.sleep(1)
			else:
				print "runing last glob"
				self.curlUpload(serverIP)	
				self.curlUpload(serverIP)
				print "last catch"
				return "finished"


if __name__ == '__main__':
	tv = takeVideoClass()
	# now = time.time() + 1
	# tv.takeVideo(30, 1600, 1200, 120, 15, now)
	# tv.takeVideo(180, 1024, 768, 15, now)
	# tv.takeVideo(180, 1280, 720, 30, now)
	# tv.takeVideo(180, 1920, 1080, 30, now)
