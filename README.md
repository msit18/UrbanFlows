# UrbanFlows

For the 5Pi architecture, there are 4 slavePies and 1 MasterPi.
The files in slavePi 2-4 are identical while slavePi5's files have some
commands that trigger the end of the processes

#MasterPi files

Programs that control the piFace:   
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
All experimental files and sample codes for the Twisted framework   

TCP files:
*   quoteserver.py, quoteclient.py, tcpClient2.py, tcpClient3.py, tcpClient4.py tcpServer.py, tcpClient.py

HTTP files:
*   response.py - HTTP client code.  Tried to figure out GET and POST methods
*   sendBody.py - HTTP client example code
*   server2.py - Working HTTP code written by Vlatko Klabucar.  Runs a HTTP server.
*   newHTTPServer.py - Example Twisted Dev code.  Creates a HTTP server.
*   client2.py - HTTP code written by Vlatko Klabucar.  Runs a HTTP client but doesn't work.

SSH files:
*   sshsimpleserver.py, sshsimpleclient.py, echoclient_ssh.py, exampleConchCode.py, sshclient.py, sshsimpleclient3.py, sshsimpleserver2.py, exampleSSHClient.py, sshserver.py, sshserver2.py

Other files:
*   stringprod.py - Twisted producer/consumer example file
*   localServer - sets up a localhost server for TCP and SSH

#tcpTestFiles/WorkingFiles
All files work and are clearly labeled.

Relevant TCP files:
*   tcpServerEdit2.py, tcpClientEdit2.py - Working on these files as of 9/23/15 to create TCP client-server
*   tcpClientEditAlias.py, tcpClientEditAlias2.py, tcpClientEditAlias3.py - Used to test TCP server's ability to handle multiple clients

HTTP files written by Vlatko Klabucar:
*   send-image.sh - Uses curl to post image to HTTP server
*   client.py - HTTP client.  Needs to be debugged
*   server.py - HTTP server.  Handles POST and GET requests

ibtest.rar - Example php code from Iva
