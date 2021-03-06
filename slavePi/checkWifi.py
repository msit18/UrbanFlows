import subprocess, datetime, time

def fixWifi():
	writeFile("Running check {0}".format(datetime.datetime.now()))
	try:
		writeFile(subprocess.check_output(["ping", "-c", "3", "8.8.8.8"]))
		checkWifiDown = subprocess.call("[\"$(/bin/ping -c 3 8.8.8.8)\"]", shell=True)
		writeFile("checkWifiDown " + str(checkWifiDown))
	except subprocess.CalledProcessError, e:
		writeFile("Ping stdout output:\n" + e.output)
		checkWifiDown = 0

	if int(checkWifiDown) == 2:
		writeFile("Wifi is working")
	else:
		writeFile("---------------Wifi is not working. Restarting wifi process.")
		restartWifiTries = 0
		while restartWifiTries < 4:
			writeFile("---------------Num times tried to restart wifi: {0}/3".format(restartWifiTries))
			_checkWifiDown = restartWifi()
			writeFile("_checkWifiDown second time: " + str(_checkWifiDown))
			if int(_checkWifiDown) == 2:
				writeFile("Reconnected successfully. Connecting to server again.")
				break
			else:
				writeFile("---------------Wifi did not connect. Restarting again.")
				restartWifiTries += 1
		else:
			writeFile("WIFI ERROR: Could not connect to the internet.")

def restartWifi():
	subprocess.call("sudo ifdown eth0; sudo ifdown wlan0; sudo ifup wlan0; sudo ifup eth0", shell=True)
	writeFile("sleeping...")
	time.sleep(10)
	try:
		writeFile(subprocess.check_output(["ping", "-c", "3", "8.8.8.8"]))
	except subprocess.CalledProcessError, e:
	    writeFile("Ping stdout output:\n" + e.output)
	return subprocess.call("[\"$(/bin/ping -c 3 8.8.8.8)\"]", shell=True)

def writeFile(msg):
	print msg
	try:
		with open("/home/pi/UrbanFlows/slavePi/wifiLog.txt", "a") as myfile:
			myfile.write(msg + "\n")
	except:
		with open("/home/pi/UrbanFlows/slavePi/wifiLog.txt", "a") as myfile:
			myfile.write("This msg could not be printed \n")

fixWifi()
