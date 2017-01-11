#!/usr/bin/python

#Written by Michelle Sit
#Shows a camera preview for a specified time.  No images or videos recorded

import picamera
import time, sys

camera = picamera.PiCamera()
camera.start_preview()
recTime = float(sys.argv[1])
time.sleep(float(sys.argv[1]))
camera.stop_preview()
camera.close()
