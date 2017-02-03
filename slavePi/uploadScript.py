#Written by Michelle Sit
#Server IP address is 18.89.4.173
#ServerSaveFilePath => I will email you the path when we receive our external hard drive

import datetime, glob, subprocess, sys

class UploadClass():
	def videoUpload (self, serverIP, serverSaveFilePath):
		print "videoUpload called"
		now = datetime.datetime.now()
		print "videoUpload Running. Time start is: ", now
		fileList = glob.glob('*.h264')
		fileList.sort()
		if len(fileList) > 0:
			print "fileList has customers: ", fileList
			for item in fileList:
				try:
					print "sending: ", item
					cmd = "rsync --remove-source-files --timeout=300 -vhe \"sshpass -p ravenclaw ssh\" {0} msit@{1}:{2}".format(item, serverIP, serverSaveFilePath)
					subprocess.call(cmd, shell=True)
				except:
					continue
		print "Upload finished"

if __name__ == '__main__':
	up2 = UploadClass()
# 	videoUpload(sys.argv[1], sys.argv[2])

#CRON/Flock cmd to run every x seconds
# * * * * * /usr/bin/flock --nonblock --wait 30 /tmp/fcj.lockfile /home/pi/UrbanFlows/slavePi/uploadScript.py $1 $2