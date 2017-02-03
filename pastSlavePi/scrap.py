timesToTakeVideo = "01/24/17 12:00:00 01/25/17 12:15:00 01/24/17 12:30:00"
list = [data for data in timesToTakeVideo.split()]
for x in range(len(list)/2):
	print x
	print list
	print list.pop(0)
	print list.pop(0)
	print "next"


print list