import time
import picamera

frames = 99

print time.asctime(time.localtime(time.time()))

with picamera.PiCamera() as camera:
	camera.resolution = (640, 480)
	camera.framerate = 90
	camera.start_preview()
	time.sleep(2)
	start = time.time()
	camera.capture_sequence([
		'image%02d.jpg' %i
		for i in range(frames)
		], use_video_port=True)
	finish = time.time()
print('Captured %d frames at %.3ffps' % (
	frames,
	frames / (finish - start)))

print time.asctime(time.localtime(time.time()))
