import datetime
import time

print time.time()
print datetime.datetime.today()
end = datetime.datetime.strptime("06/01/16 19:16:00", "%x %X")
print end
print end > datetime.datetime.today()

while (datetime.datetime.today() < end) == True:
	print "not ready"
	print datetime.datetime.today()
else:
	print "ready"


def calculateTimeDifference(self, dateToEnd, timeToEnd):
	fullString = dateToEnd + " " + timeToEnd
	endTime = datetime.datetime.strptime(fullString, "%x %X")
	nowTime = datetime.datetime.today()
	difference = endTime - nowTime
	return time.time() + difference.total_seconds()

times = [datetime.datetime.strptime("06/01/16 19:16:00", "%x %X"), datetime.datetime.strptime("06/02/16 01:00:00", "%x %X"), \
datetime.datetime.strptime("06/03/16 02:00:00", "%x %X")]
print times.pop(0)
print times.pop(0)
print times.pop(0)