#Convert time through user friendly method

import time, datetime

endTime = raw_input("Enter date and time that you would like to start the program (ex - 11/04/16 15:45:58). Current time is {0} : ".format(time.strftime("%x %X")))
endTime = datetime.datetime.strptime(endTime, "%x %X")
print "endTime: ", endTime

nowTime = datetime.datetime.today()
print "nowTime: ", nowTime

difference = endTime - nowTime
print "difference: ", difference
print difference.total_seconds()


03/02/16 12:30:00