import datetime, time, glob, subprocess, sys

def curlUpload2 (serverIP, serverSaveFilePath):
	print "curlUploadImg called"
	now = datetime.datetime.now()
	print "CurlUpload2 Running. Time start is: ", now
	fileList = glob.glob('*.h264')
	fileList.extend(glob.glob('*.bin'))
	fileList.sort()
	if len(fileList) > 0:
		print "fileList has customers: ", fileList
		for item in fileList:
			print "sending: ", item
			subprocess.call("sshpass -p 'ravenclaw' scp {0} msit@{1}:\"{2}\"".format(item, serverIP, serverSaveFilePath), shell=True)
	# time.sleep(30)
	end = datetime.datetime.now()
	overall = end-now
	print "CurlUpload2 finished at: ", end
	print "All time: ", overall
	print "delete videos now ........."
	time.sleep(20)
	print "restarting process again"

curlUpload2(sys.argv[1], sys.argv[2])

#CRON/Flock cmd to run every x seconds
# * * * * * /usr/bin/flock --nonblock --wait 30 /tmp/fcj.lockfile /home/pi/UrbanFlows/slavePi/uploadScript.py