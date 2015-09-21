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
