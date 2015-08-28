import csv

#with open('image.csv', 'rb') as f:
#	reader = csv.reader(f)
#	for row in reader:
#		print row

with open('image.csv', 'r') as f:
	data = [row for row in csv.reader(f.read().splitlines())]
	print data
