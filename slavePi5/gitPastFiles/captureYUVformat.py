import picamera

with picamera.PiCamera() as camera:
	camera.resolution = (1920, 1080)
	camera.framerate = 90
	camera.capture_sequence(['jpgImg1.jpg', 'jpgImg2.jpg'], format='jpeg', use_video_port=True)
