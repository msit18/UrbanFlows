import LeptonLib as lep
import cv2

data,_,_ = lep.parseRawFile('/home/michelle/gitFolder/UrbanFlows/raw_20160524-075225-1.bin')
img = lep.createImage(data)
cv2.imwrite('test.png', img)