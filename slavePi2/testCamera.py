import picamera
import time



with picamera.PiCamera() as camera:
			camera.resolution = (2592, 1944)
			camera.framerate = 90
			camera.start_preview()
			start = time.time()
			v = camera.capture_sequence([
				'image%02d.jpg' % i
				for i in range(10)
				], use_video_port=False)
			end = time.time()
			totalTime = end-start
			print "total time in: ", totalTime 
			camera.stop_preview()