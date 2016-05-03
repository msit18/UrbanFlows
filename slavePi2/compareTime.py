import glob

list = glob.glob('*.jpg')
newList = []
for x in list:
	new = x.split('.')
	remove = new[0].split('_')
	newZ = int(remove[0]) + (int(remove[1])*0.01) + (int(remove[2])*0.00000001)
	print newZ
	newList.append(newZ)
newList.sort()
print newList

differenceList = []
for item in range(len(newList)):
	difference = newList[item]-newList[item-1]
	print difference
	differenceList.append(difference)
print differenceList

