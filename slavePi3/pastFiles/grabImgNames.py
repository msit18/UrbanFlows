import glob

file = open('imgList.txt', 'w')
print >> file, glob.glob('*.jpg')
file.close()
