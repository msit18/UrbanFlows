import datetime
import time

print time.time()
print datetime.datetime.today()
end = datetime.datetime.strptime("06/01/16 19:16:00", "%x %X")
print "end: ", end
print end > datetime.datetime.today()

while (datetime.datetime.today() < end) == True:
	print "not ready"
	print datetime.datetime.today()
else:
	print "ready"


def calculateTimeDifference(dateToEnd, timeToEnd):
	fullString = dateToEnd + " " + timeToEnd
	endTime = datetime.datetime.strftime(fullString, "%x %X")
	print "endTime: ", endTime
	nowTime = datetime.datetime.today()
	difference = endTime - nowTime
	return time.time() + difference.total_seconds()

print "calculate diff: ", calculateTimeDifference(datetime.datetime.strptime("06/01/16", "%x"), datetime.datetime.strptime("19:16:00", "%X"))

times = [datetime.datetime.strptime("06/01/16 19:16:00", "%x %X"), datetime.datetime.strptime("06/02/16 01:00:00", "%x %X"), \
datetime.datetime.strptime("06/03/16 02:00:00", "%x %X")]
print times.pop(0)
print times.pop(0)
print times.pop(0)