# UrbanFlows

Server-client relationship. The working code for the server resides in tcpTestFiles/WorkingFiles/Untitled Folder.
The most up to date client code resides in the slavePi2 folder. The code in the other folders is either old or
outdated.

#MasterPi files

Programs that control the piFace for the 5Pi architecture:   
*   camVidStartS1.py - Sets camera or video mode, resets variables, and sends commands to slavePies after checking if parameters are permissable (S1)   
*   resolutionS2.py - Sets resolution (S2)   
*   timeS3.py - Sets time (S3)   
*   setFpsS4.py - Sets frames/sec and custom fps    
*   shutdownS5.py - Responsible for S5 functions (shutting down/restarting)   
*   piFaceMain.py - Calls appropriate S1-5 files   
*   variables.py - Stores variables for the piFaceMain program.  Shared across several files.  
*   flash.py - Flashes the piFace and shows an error msg if there's something wrong or if it finishes   

Other programs:   
*   clrPics.sh - Triggers removePics on all slavePies.  Removes all jpg files from the home/specified folder   
*   removePics.sh - Removes all .jpg and .h264 (video) files from the current Pi   
*   wifiRestart.sh - Restarts wifi for that Pi.  After 3 tries, triggers flash.py to restart all Pies   
*   restartWifi.sh - Restarts wifi if wifi is down and Pi is connected by ethernet   

#SlavePi2 files

Relevant files:
manualPic_capturePhotos2.py/manualPic_capturePhotos3.py, testUploadSpeed2.py, videoMode3.py
testCamera.py is used as a testing ground for many of the functions that are inputted into manualPic files.

#Common files in all SlavePi folders:   
The common files here are almost identical across slavePi2-4.  slavePi5 has these files but with an additional
section of code that sends parameters to flash.py on the MasterPi   

Programs related to piFace:   
*   manualPic4.py - Takes 6 parameters.  Produces a text file with fps updates when running   
*   videoMode2.py - Takes 5 parameters.   

Other programs:   
*   preview.py - Shows camera image for a specified time.  Doesn't store the images.   
*   removePics.sh - Removes all .jpg and .h264 (video) files from the current Pi   
*   restartWifi.sh - Restarts wifi if wifi is down and Pi is connected by ethernet   

#Programs specific to each Raspi:   

SlavePi2 Files:   
*   openjpeg-2.0.1 folder - program folder.  Used when I was installing PIL (Python Imaging Library)   
*   sshserver.py - Old iteration.  Used for testing sshserver   
*   sshsimpleclient.py - Old iteration.  Used for testing ssh client   
*   takePic.py - Takes a picture.  Used for testing if a command has been executed.   

SlavePi3 Files:   
*   takeVideo.sh - Takes video, sends it to the MasterPi, and sends a finished msg to flash.py   

SlavePi4 Files:    
*   sshclient.py - Old ssh client file   

SlavePi5 Files:   
*   takeVideo.sh - Takes video, sends it to the MasterPi, and sends a finished msg to flash.py  

#tcpTestFiles
Relevant server files in WorkingFiles/Untitled Folder:
callbackServer4.py, masterVariables2.py

HTTP files written by Vlatko Klabucar:
*   send-image.sh - Uses curl to post image to HTTP server
*   client.py - HTTP client.  Needs to be debugged
*   server.py - HTTP server.  Handles POST and GET requests

ibtest.rar - Example php code from Iva
