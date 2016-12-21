import subprocess

def onStart():
	try:
		print "running subprocess"
		subprocess.call("echo \"SENDING EMAIL WITH WIFI\"; \
				echo \"error message\" | mail -s \"title of email\" urbanflowsproject@gmail.com", shell=True)

	finally:
		print "running bluetooth"
		subprocess.call("echo \"RUNNING BLUETOOTH\"; \
				sudo hciconfig hci0 piscan;\
				sudo hciconfig -a", shell=True)

onStart()
