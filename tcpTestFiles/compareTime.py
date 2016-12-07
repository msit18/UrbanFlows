import glob
import matplotlib.pyplot as plt
import numpy as np

tooLong = 0

list = glob.glob('*.jpg')
newList = []
for x in list:
	new = x.split('.')
	remove = new[0].split('_')
	newZ = int(remove[0]) + (int(remove[1])*0.01) + (int(remove[2])*0.00000001)
	#print newZ
	newList.append(newZ)
newList.sort()
print newList[1:]
# f = open('test2.txt', 'wr')
# for x in newList[1:]:
# 	f.write(str(x) + '\n')
# f.close()

differenceList = []
for item in range(1, len(newList)):
	difference = newList[item]-newList[item-1]
	print difference
	if difference > 0.01:
		tooLong += 1
		print "too large"
		#pass
	else:
		differenceList.append(difference)
print "DifferenceList: ", differenceList

stdDifferenceList = np.std(differenceList)
print stdDifferenceList
mean = np.mean(differenceList, axis=0)
print mean
print "TooLong: ", str(tooLong) + "/" + str(len(list))
plt.plot(x1, differenceList, x1, mean)
plt.plot(y=mean)
#plt.plot(stdDifferenceList)
#plt.axis([0, 105, 0.0000, 0.05])
plt.show()
