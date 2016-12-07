#Convert time through user friendly method

import time, datetime

value = False
while value == False:
	inputTime = raw_input("Enter date and time that you would like to start the program (ex - 11/04/16 15:45:58). Current time is {0} : ".format(time.strftime("%x %X")))
	print inputTime
	try:
		endTime = datetime.datetime.strptime(inputTime, "%x %X")
		value = True
	except:
		value = False

#endTime = datetime.datetime.strptime(endTime, "%x %X")
print "endTime: ", endTime

nowTime = datetime.datetime.today()
print "nowTime: ", nowTime

difference = endTime - nowTime
print "difference: ", difference
print difference.total_seconds()