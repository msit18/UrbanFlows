#Written by Michelle Sit

#Stores variables for the piFaceMain program.  Shared across several files.

from threading import Barrier
#Used to exit the whole program at the end
end_barrier = Barrier(2)

###TIME
#totalTime(Eng)Answers is used for total run time of the program and video time when specified		
totalTimeEngAnswers = ["10S", "15S", "20S", "30S", "1M", "2M", "3M", "4M", "5M", "7M", "10M", "15M", "20M", "30M", "45M", "1H", "1.5H", "2H"] 
totalTimeAnswers = ["10", "15", "20", "30", "60", "120", "180", "240", "300", "420", "900", "1200", "1800", "2700", "3600", "5400", "7200"]

camTimeIntervalEngAnswers = ["1S", "2S", "3S", "5S", "10S", "15S", "20S", "30S", "1M", "2M", "3M", "5M", "10M", "15M", "20M", "30M", "1H", "1.5H", "2H"]
camTimeIntervalAnswers = ["1", "2", "3", "5", "10", "15", "20", "30", "60", "120", "180", "300", "600", "900", "1200", "1800", "3600", "5400", "7200"]

#total duration that the cameras run
totalTime = 0
totalTimeEng = 0
videoTime = 0
videoTimeEng = 0

###RESOLUTION
resAnswers = []
vidResAnswers = ["1920x1080", "1296x730", "640x480"]
camResAnswers = ["2592x1944", "1920x1080", "1296x730", "640x480"]

resolutionW = 0
resolutionH = 0

###FPS AND INTERNAL FRAMERATE
FPSanswers = ["0"]

customNumFramesAnswers = ["1", "2", "3", "4", "5"]
customTimeIntervalAnswers = ["2", "3", "4", "5"]

#In the context of this system, inputFPS refers to the fps selected by the user and is used for both video and camera.
#For camera, inputFPS sets numFrames and timeInterval variables internally to achieve the desired fps.  When the user picks a custom fps, inputFPS is used as a
#display holder for the chosen numFrames on the homeScreen
#internalCamFR is used to set framerate for the camera option (an internal variable that is separate from the user selected fps.  See manualPic code for reference)
inputFPS = 0
#Used to set camera fps.
numFrames = 0
timeInterval = 0
internalCamFR = 0 #Used to set internal camera framerate (different than fps for camera)

###PIFACE DIRECT COMMANDS
runMode = ["CAM", "VID", "START", "Reset variables", "Return menu"]
exitAnswers = ["MPi exit prgm", "MPi restart", "Shutdown all", "Reboot all", "Num file in fldr", "Clear mvFolder", "Return menu"]
exitConfirm = ["Yes", "Return menu"]
exitVerify = ["Yes", "Continue"]

inputRun = ""
currentMode = "MODE"
cmdStr = ""
exitAns = ""
emergencyAns = ""