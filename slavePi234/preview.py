#!/usr/bin/python

#Written by Michelle Sit
#Shows a camera preview for a specified time.  No images or videos recorded

import picamera
import time

camera = picamera.PiCamera()
camera.start_preview()
time.sleep(30)
camera.stop_preview()
