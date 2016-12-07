# UrbanFlows

Server-client network. The working code for the server resides in tcpTestFiles/WorkingFiles/Untitled Folder.
The most up to date client code resides in the slavePi folder. The code in the other folders is old.

#slavePi files:

Basic raspi functions
*   preview.py - Shows camera image for a specified time.  Doesn't store the images.   
*   removePics.sh - Removes all .jpg and .h264 (video) files from the current Pi   
*   restartWifi.sh - Restarts wifi if wifi is down and Pi is connected by ethernet   
*	sendIP.py - Sends IP address of pi in an email
*   takePic.py - Takes a picture.  Used for testing if a command has been executed.

Client functions
*	manualPic_capturePhotos3.py - takes pictures based on inputs. Uploads them to a server
*	testUploadSpeed3.py - 
*	videoMode4.py - takes video based on inputs

#tcpTestFiles/WorkingFiles/UntitiedFolder:
*	callbackServer4.py - earlier version. Does not send time to take pictures.
*	callbackServer5.py - most up to date server