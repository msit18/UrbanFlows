import os
import glob

numPics = glob.glob ('*.jpg')
for img in numPics:
	print img
	os.system('curl --header "filename: {0}" -X POST --data-binary @{0} http://18.111.126.196:8880/upload-image'.format(img))
	os.system('rm {0}'.format(img))
