#Attempting to write all the yuv pixel numbers to a text file

#Written by Michelle Sit

import time
import picamera
import picamera.array
import numpy as np
from PIL import Image
import numpy

with picamera.PiCamera() as camera:
	camera.resolution = (640, 480)
	with picamera.array.PiYUVArray(camera) as output:
		start = time.time()
		camera.capture(output, 'yuv')
#		print output.array[1]
#		print output.array[2]
#		print output.array[3]
		a = numpy.asarray(output.array[1]) 
		b = numpy.asarray(output.array[2])
		c = numpy.asarray(output.array[3])
		threeArray = numpy.concatenate( (a, b, c), axis=0)
		switchedArray = numpy.concatenate( (b, a, c), axis=0)
		numpy.savetxt("fooThreeArray.csv", threeArray, delimiter=",")
		numpy.savetxt("foodSwitchedArray.csv", switchedArray, delimiter=",")
#		numpy.savetxt("foo1920.csv", b, delimiter=",")
#		numpy.savetxt("foo3.csv", c, delimiter=",")
		finish = time.time()
		#print (output.array.shape[1], output.array.shape[0])
		totalTime = finish-start
		print(totalTime)
		print(output.array.shape)
#		print(output.rgb_array.shape)
