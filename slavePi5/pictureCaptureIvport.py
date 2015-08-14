#!/usr/bin/python
#
# This file is part of Ivport.
# Copyright (C) 2015 Ivmech Mechatronics Ltd. <bilgi@ivmech.com>
#
# Ivport is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ivport is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Edited by Michelle Sit
# Gets information from the piFace to take pictures with certain parameters

# sys.argv[1] = framerates
# sys.argv[2] = resW
# sys.argv[3] = resH
# sys.argv[4] = timeLength

#title           :ivport_capture_sequence_A.py
#description     :the closest approach to simultaneous capturing
#author          :Caner Durmusoglu
#date            :20150425
#version         :0.1
#usage           :python ivport_capture_sequence_A.py
#notes           :A indicates that Ivport jumper setting
#python_version  :2.7
#==============================================================================

import time
import picamera
import sys
import datetime
import subprocess

import RPi.GPIO as gp

gp.setwarnings(False)
gp.setmode(gp.BOARD)

gp.setup(7, gp.OUT)
gp.setup(11, gp.OUT)
gp.setup(12, gp.OUT)

gp.output(7, False)
gp.output(11, False)
gp.output(12, True)

#Inputs
frames = int(sys.argv[1])
resW = int(sys.argv[2])
resH = int(sys.argv[3])
timeLength = int(sys.argv[4])

cam = 1

def cam_change():
    global cam
    gp.setmode(gp.BOARD)
    if cam == 1:
        # CAM 1 for A Jumper Setting
        gp.output(7, False)
        gp.output(11, False)
        gp.output(12, True)

    elif cam == 2:
        # CAM 2 for A Jumper Setting
        gp.output(7, True)
        gp.output(11, False)
        gp.output(12, True)

    elif cam == 3:
        # CAM 3 for A Jumper Setting
        gp.output(7, False)
        gp.output(11, True)
        gp.output(12, False)

    elif cam == 4:
        # CAM 4 for A Jumper Setting
        gp.output(7, True)
        gp.output(11, True)
        gp.output(12, False)

    cam += 1
    if cam > 4:
        cam = 1

def filenames():
    frame = 0
    while frame < frames:
        time.sleep(0.007)   # SD Card Bandwidth Correction Delay
        cam_change()        # Switching Camera
        time.sleep(0.007)   # SD Card Bandwidth Correction Delay
#        yield 'image%02d.jpg' % frame
        yield '/home/pi/ivport/pictures/' + datetime.datetime.now().strftime ('%d-%m-%Y-%H_%M_%S_%f') + '_TT' + str(timeLength) + '_RW' + str(resW) + '_RH' + str(resH) + '_FR' + str(frames) + '.jpg'
        frame += 1


#Start of main process
start = time.time()
print start
testTime = start+timeLength
print testTime
while time.time() < testTime:
    with picamera.PiCamera() as camera:
         camera.resolution = (resW, resH)
         camera.framerate = frames
         camera.capture_sequence(filenames(), use_video_port=True)
#    camera.start_preview()

    # Optional Camera LED OFF
    #gp.setmode(gp.BCM)
    #camera.led = False

#   time.sleep(2)    # Camera Initialize
#    start = time.time()
#         print start
#         camera.capture_sequence(filenames(), use_video_port=True)

finish = time.time()
print finish

numFiles = subprocess.check_output("ls -1 /home/pi/ivport/pictures/ | wc -l", shell=True)

print('Captured %s pictures. %d frames at total %.2ffps and %.2f secs' % (numFiles, frames, frames / (finish - start), (finish-start)))
