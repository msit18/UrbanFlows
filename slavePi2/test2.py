from picamera import PiCamera
import time
from picamera.array import PiYUVArray

import numpy as np

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiYUVArray(camera, size=(640, 480) )

for frame in camera.capture_continuous(rawCapture, format="yuv", use_video_port=True):
	image = frame.array
	print image
	with file('test.txt', 'w') as outfile:
		outfile.write('#Array shape:{0}\n'.format(image.shape) )
		for data_slice in image:
			np.savetxt(outfile, data_slice, fmt='%-7.2f')
			outfile.write('# New slice\n')
	rawCapture.truncate(0)
	print "rawCapture truncate"
	exit()
print "last exit"
exit()
#with picamera.PiCamera() as camera:
#	camera.resolution = (640, 480)
#	camera.resolution = (1920, 1080)
#	start = time.time()
#	camera.capture_sequence('image.csv', format="raw")
#	finish = time.time()
#	final = finish-start
#	print final
