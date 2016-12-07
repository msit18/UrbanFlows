import picamera
import time

camera = picamera.PiCamera()
camera.start_preview()
print "started preview"
time.sleep(90)
camera.stop_preview()
print "exiting"
