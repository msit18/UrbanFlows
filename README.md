# UrbanFlows

For the 5Pi architecture, there are 4 slavePies and 1 MasterPi.
The files in slavePi 2-4 are identical while slavePi5's files have some
commands that trigger the end of the processes

#MasterPi files

Programs that control the piFace:   
*   camVidStartS1.py - Responsible for S1 functions (Cam/Vid/Clear Options)   
*   resolutionS2.py - Responsible for S2 functions (Resolution)   
*   timeS3.py - Responsible for S3 functions (time)   
*   setFpsS4.py - Responsible for S4 functions (setting frames/sec and custom)   
*   shutdownS5.py - Responsible for S5 functions (shutting down/restarting)   
*   piFaceMain.py - Calls appropriate S1-5 files   
*   variables.py - Holds all variables for S1-5   
*   (missing) flash.py - Flashes the piFace and shows an error msg if there's something wrong or if it finishes

Bash scripts:
*   clrPics.sh - removes all .jpg files from all the slavePies   
*   removePics.sh - removes all .jpg and .h264 (video) files from the current Pi   
*   wifiRestart.sh - restarts wifi for that Pi.  After 3 tries, triggers flash.py to restart all Pies   

#SlavePi2 files

Programs related to writing YUV images:   
*   openjpeg-2.0.1 folder - program folder.  Used when I was installing PIL (Python Imaging Library)   
*   makeGarbageFile.py - Testing file for writing images

Programs related to piFace:
*   manualPic3.py - Past iteration of manualPic4.py
*   manualPic4.py - Takes 5 parameters when executing file.  Produces a text file with fps updates when running
*   videoMode2.py - Takes 4 parameters when executing file.

Bash scripts:
*   removePics.sh - removes all .jpg and .h264 (video) files from the current Pi

Programs used for testing ssh:
*   sshserver.py - Old iteration.  Used for testing sshserver
*   sshsimpleclient.py - Old iteration.  Used for testing ssh client

Useful programs for testing cameras:
*   preview.py - turns on camera for 90 seconds.  Does not take pictures
*   takePic.py - Takes a picture.  Used for testing if a command has been executed.
