#Written by Michelle Sit
#480p tests at 20, 25, 30, 35, 38, 40
#730p tests at 5fps, 10fps, 15fps, 20fps
#1080p tests at 1, 3, 5, 7, 8, 9, 10fps
#5MP tests at 1, 2, 3, 4, 5

import os
import glob

#fpsTestArray = [20, 25, 30, 35, 38, 40, 5, 10, 15, 20, 1, 3, 4, 7, 8, 9, 10, 1, 2, 3, 4, 5]
#testRuns = [6, 4, 7, 5]
#resW = [640, 1296, 1920, 2592]
#resH = [480, 730, 1080, 1944]
#framerates = [90, 50, 90, 50]

fpsTestArray = [91, 51, 31, 11]
resW = [640, 1296, 1920, 2592]
resH = [480, 730, 1080, 1944]
framerates = [90, 90, 90, 90]

testRunPlaceHolder = 0
x = 1
print fpsTestArray[testRunPlaceHolder]
while x < fpsTestArray[testRunPlaceHolder]:
	print "NEW RUN"
	print "testRunPlaceHolder:", testRunPlaceHolder
	parameters = "600 {0} {1} {2} 1 90".format(resW[testRunPlaceHolder], resH[testRunPlaceHolder], x)
	print "Parameters: ", parameters
	#run program
	os.system('python testPiManualPic.py {0}'.format(parameters))

	pictureList = glob.glob("*.jpg")
	pictureName = "{0}p_{1}fps_FR{2}.txt".format(resH[testRunPlaceHolder], x, framerates[testRunPlaceHolder] )
	file = open("{0}".format(pictureName), 'w')
	for z in pictureList:
		file.write("{0}\n".format(z))
	file.close()
	os.system('rm *.jpg')

	x += 1
	if x >= fpsTestArray[testRunPlaceHolder]:
		testRunPlaceHolder += 1
		x = 1
	if testRunPlaceHolder > 3:
		exit()
