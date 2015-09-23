import time
import picamera
import picamera.array

with picamera.PiCamera() as camera:
	with picamera.array.PiYUVArray(camera) as stream:
		camera.resolution = (100, 100)
		time.sleep(2)
		camera.start_preview()
#		camera.framerate = 90
		camera.capture(stream, 'yuv')
		print(stream.array.shape)
		print(stream.rgb_array.shape)
