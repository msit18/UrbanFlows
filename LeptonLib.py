#!/usr/bin/python

import cv2
#from SimpleCV import *
#from SimpleCV.Shell import plot
import numpy as np
#import numpy.ma as ma
import datetime
import os
import glob

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import matplotlib.dates as md
import time
import struct
import mysql.connector


PIXEL_MAP = [255, 255, 255, 253, 253, 253, 251, 251, 251, 249, 249, 249, 247, 247, 247, 245, 245, 245, 243, 243, 243, 241, 241, 241, 239, 239, 239, 237, 237, 237, 235, 235, 235, 233, 233, 233, 231, 231, 231, 229, 229, 229, 227, 227, 227, 225, 225, 225, 223, 223, 223, 221, 221, 221, 219, 219, 219, 217, 217, 217, 215, 215, 215, 213, 213, 213, 211, 211, 211, 209, 209, 209, 207, 207, 207, 205, 205, 205, 203, 203, 203, 201, 201, 201, 199, 199, 199, 197, 197, 197, 195, 195, 195, 193, 193, 193, 191, 191, 191, 189, 189, 189, 187, 187, 187, 185, 185, 185, 183, 183, 183, 181, 181, 181, 179, 179, 179, 177, 177, 177, 175, 175, 175, 173, 173, 173, 171, 171, 171, 169, 169, 169, 167, 167, 167, 165, 165, 165, 163, 163, 163, 161, 161, 161, 159, 159, 159, 157, 157, 157, 155, 155, 155, 153, 153, 153, 151, 151, 151, 149, 149, 149, 147, 147, 147, 145, 145, 145, 143, 143, 143, 141, 141, 141, 139, 139, 139, 137, 137, 137, 135, 135, 135, 133, 133, 133, 131, 131, 131, 129, 129, 129, 126, 126, 126, 124, 124, 124, 122, 122, 122, 120, 120, 120, 118, 118, 118, 116, 116, 116, 114, 114, 114, 112, 112, 112, 110, 110, 110, 108, 108, 108, 106, 106, 106, 104, 104, 104, 102, 102, 102, 100, 100, 100, 98, 98, 98, 96, 96, 96, 94, 94, 94, 92, 92, 92, 90, 90, 90, 88, 88, 88, 86, 86, 86, 84, 84, 84, 82, 82, 82, 80, 80, 80, 78, 78, 78, 76, 76, 76, 74, 74, 74, 72, 72, 72, 70, 70, 70, 68, 68, 68, 66, 66, 66, 64, 64, 64, 62, 62, 62, 60, 60, 60, 58, 58, 58, 56, 56, 56, 54, 54, 54, 52, 52, 52, 50, 50, 50, 48, 48, 48, 46, 46, 46, 44, 44, 44, 42, 42, 42, 40, 40, 40, 38, 38, 38, 36, 36, 36, 34, 34, 34, 32, 32, 32, 30, 30, 30, 28, 28, 28, 26, 26, 26, 24, 24, 24, 22, 22, 22, 20, 20, 20, 18, 18, 18, 16, 16, 16, 14, 14, 14, 12, 12, 12, 10, 10, 10, 8, 8, 8, 6, 6, 6, 4, 4, 4, 2, 2, 2, 0, 0, 0, 9, 0, 0, 16, 0, 2, 24, 0, 4, 31, 0, 6, 38, 0, 8, 45, 0, 10, 53, 0, 12, 60, 0, 14, 67, 0, 17, 74, 0, 19, 82, 0, 21, 89, 0, 23, 96, 0, 25, 103, 0, 27, 111, 0, 29, 118, 0, 31, 120, 0, 36, 121, 0, 41, 122, 0, 46, 123, 0, 51, 124, 0, 56, 125, 0, 61, 126, 0, 66, 127, 0, 71, 128, 1, 76, 129, 1, 81, 130, 1, 86, 131, 1, 91, 132, 1, 96, 133, 1, 101, 134, 1, 106, 135, 1, 111, 136, 1, 116, 136, 1, 121, 137, 2, 125, 137, 2, 130, 137, 3, 135, 138, 3, 139, 138, 3, 144, 138, 4, 149, 139, 4, 153, 139, 5, 158, 139, 5, 163, 140, 5, 167, 140, 6, 172, 140, 6, 177, 141, 7, 181, 141, 7, 186, 137, 10, 189, 132, 13, 191, 127, 16, 194, 121, 19, 196, 116, 22, 198, 111, 25, 200, 106, 28, 203, 101, 31, 205, 95, 34, 207, 90, 37, 209, 85, 40, 212, 80, 43, 214, 75, 46, 216, 69, 49, 218, 64, 52, 221, 59, 55, 223, 49, 57, 224, 47, 60, 225, 44, 64, 226, 42, 67, 227, 39, 71, 228, 37, 74, 229, 34, 78, 230, 32, 81, 231, 29, 85, 231, 27, 88, 232, 24, 92, 233, 22, 95, 234, 19, 99, 235, 17, 102, 236, 14, 106, 237, 12, 109, 238, 12, 112, 239, 12, 116, 240, 12, 119, 240, 12, 123, 241, 12, 127, 241, 12, 130, 242, 12, 134, 242, 12, 138, 243, 13, 141, 243, 13, 145, 244, 13, 149, 244, 13, 152, 245, 13, 156, 245, 13, 160, 246, 13, 163, 246, 13, 167, 247, 13, 171, 247, 14, 175, 248, 15, 178, 248, 16, 182, 249, 18, 185, 249, 19, 189, 250, 20, 192, 250, 21, 196, 251, 22, 199, 251, 23, 203, 252, 24, 206, 252, 25, 210, 253, 27, 213, 253, 28, 217, 254, 29, 220, 254, 30, 224, 255, 39, 227, 255, 53, 229, 255, 67, 231, 255, 81, 233, 255, 95, 234, 255, 109, 236, 255, 123, 238, 255, 137, 240, 255, 151, 242, 255, 165, 244, 255, 179, 246, 255, 193, 248, 255, 207, 249, 255, 221, 251, 255, 235, 253, 255, 24, 255, 255]
#PIXEL_MAP = [74, 3, 1, 74, 3, 0, 75, 3, 0, 75, 3, 0, 76, 3, 0, 76, 3, 0, 77, 3, 0, 79, 3, 0, 82, 3, 0, 85, 5, 0, 88, 7, 0, 91, 10, 0, 94, 14, 0, 98, 19, 0, 100, 22, 0, 103, 25, 0, 106, 28, 0, 109, 32, 0, 112, 35, 0, 116, 38, 0, 119, 40, 0, 123, 42, 0, 128, 45, 0, 133, 49, 0, 134, 50, 0, 136, 51, 0, 137, 52, 0, 139, 53, 0, 142, 54, 0, 144, 55, 0, 145, 56, 0, 149, 58, 0, 154, 61, 0, 156, 63, 0, 159, 65, 0, 161, 66, 0, 164, 68, 0, 167, 69, 0, 170, 71, 0, 174, 73, 0, 179, 75, 0, 181, 76, 0, 184, 78, 0, 187, 79, 0, 188, 80, 0, 190, 81, 0, 194, 84, 0, 198, 87, 0, 200, 88, 0, 203, 90, 0, 205, 92, 0, 207, 94, 0, 208, 94, 0, 209, 95, 0, 210, 96, 0, 211, 97, 0, 214, 99, 0, 217, 102, 0, 218, 103, 0, 219, 104, 0, 220, 105, 0, 221, 107, 0, 223, 109, 0, 223, 111, 0, 223, 113, 0, 222, 115, 0, 221, 117, 0, 220, 118, 0, 219, 120, 1, 217, 122, 1, 216, 124, 2, 214, 126, 2, 212, 129, 3, 207, 131, 3, 205, 132, 4, 202, 133, 4, 197, 134, 4, 192, 136, 5, 185, 138, 6, 178, 141, 7, 172, 142, 8, 166, 144, 10, 162, 144, 10, 158, 145, 11, 153, 146, 12, 149, 147, 13, 140, 149, 15, 132, 151, 17, 120, 153, 22, 115, 154, 25, 109, 156, 28, 101, 158, 34, 94, 160, 40, 86, 162, 45, 79, 164, 51, 69, 167, 59, 60, 171, 67, 54, 173, 72, 48, 175, 78, 43, 177, 83, 39, 179, 89, 35, 181, 93, 31, 183, 98, 26, 185, 105, 23, 187, 109, 21, 188, 113, 19, 189, 118, 17, 191, 123, 14, 193, 128, 12, 195, 134, 10, 196, 138, 8, 197, 142, 6, 198, 146, 5, 200, 151, 4, 201, 155, 3, 203, 160, 2, 204, 164, 2, 205, 169, 1, 206, 173, 1, 207, 175, 1, 207, 178, 0, 208, 184, 0, 210, 190, 0, 211, 193, 0, 212, 196, 0, 212, 199, 1, 213, 202, 2, 214, 207, 3, 215, 212, 3, 214, 215, 3, 214, 218, 3, 213, 220, 4, 213, 222, 4, 212, 224, 5, 212, 225, 5, 212, 226, 5, 211, 229, 6, 211, 232, 6, 211, 232, 6, 211, 233, 6, 210, 234, 7, 210, 235, 7, 209, 236, 8, 208, 237, 8, 206, 239, 9, 204, 241, 9, 203, 242, 10, 202, 244, 10, 201, 244, 10, 200, 245, 11, 199, 245, 11, 198, 246, 12, 197, 247, 13, 194, 248, 14, 191, 249, 14, 189, 250, 15, 187, 251, 16, 185, 251, 17, 183, 252, 18, 178, 252, 19, 174, 253, 19, 171, 253, 20, 168, 254, 21, 165, 254, 21, 164, 254, 22, 163, 255, 22, 161, 255, 23, 159, 255, 23, 157, 255, 24, 155, 255, 25, 149, 255, 27, 143, 255, 28, 139, 255, 30, 135, 255, 31, 131, 255, 32, 127, 255, 34, 118, 255, 36, 110, 255, 37, 104, 255, 38, 101, 255, 39, 99, 255, 40, 93, 255, 42, 88, 255, 43, 82, 254, 45, 77, 254, 47, 69, 254, 49, 62, 254, 50, 57, 253, 52, 53, 253, 53, 49, 252, 55, 45, 252, 57, 39, 251, 59, 33, 251, 60, 32, 251, 60, 31, 251, 61, 30, 251, 61, 29, 251, 62, 28, 251, 63, 27, 250, 65, 27, 250, 66, 26, 249, 68, 26, 249, 70, 25, 248, 73, 24, 248, 75, 24, 247, 77, 25, 247, 79, 25, 247, 81, 26, 247, 83, 32, 247, 85, 35, 247, 86, 38, 247, 88, 42, 247, 90, 46, 247, 92, 50, 247, 94, 55, 248, 96, 59, 248, 98, 64, 248, 101, 72, 248, 104, 81, 249, 106, 87, 249, 108, 93, 250, 109, 95, 250, 110, 98, 250, 111, 100, 250, 112, 101, 251, 113, 102, 251, 117, 109, 251, 121, 116, 252, 123, 121, 252, 126, 126, 253, 128, 130, 253, 131, 135, 254, 133, 139, 254, 136, 144, 254, 140, 151, 254, 144, 158, 255, 146, 163, 255, 149, 168, 255, 152, 173, 255, 153, 176, 255, 155, 178, 255, 160, 184, 255, 165, 191, 255, 168, 195, 255, 172, 199, 255, 175, 203, 255, 179, 207, 255, 182, 211, 255, 185, 216, 255, 190, 218, 255, 196, 220, 255, 200, 222, 255, 202, 225, 255, 204, 227, 255, 206, 230, 255, 208, 233, 255]
COLOR_MAP = np.asarray(PIXEL_MAP, dtype=np.uint8).reshape(256, 1, 3)



def getThermalImages(namePattern, secondly = False):
	filter = os.path.join(namePattern)
	files = sorted(glob.glob(filter), key=os.path.getmtime)

	filtered = []
	prev_second = -1
	for tfile in files:
		if (os.stat(tfile).st_size == 9606):
			if secondly:
				name = tfile.split('/')[-1];
				second = datetime.datetime.strptime(name[4:19], '%Y%m%d-%H%M%S').second
				if second != prev_second:
					prev_second = second
					filtered.append(tfile)
			else:
				filtered.append(tfile)

	return filtered



def createVideo(files, videoName, scale  = 5, colorMap=-1, segments = None):

	#files = getThermalImages(namePattern)
	polys = []
	if segments:
		for segment in segments:
			segment = [(b, a) for a, b in segment]
			polys.append(np.array(segment) * scale)



	fps = 15
	capSize = (80 * scale, 60 * scale)
	fourcc = cv2.cv.CV_FOURCC('m', 'p', '4', 'v') 
	video = cv2.VideoWriter()
	success = video.open(videoName,fourcc,fps,capSize,True) 

	i = 0
	for tfile in files:
		data, pic_datetime, _ = parseRawFile(tfile)
		colored_img = createImage(data, colorMap)
		if segments:
			for poly in polys:
				cv2.polylines(colored_img, [poly], 1, (255,255,255))
		#colored_img = applyCustomColorMap(data, colorMap)
		#colored_img = cv2.resize(colored_img, (0,0), fx=scale, fy=scale)
		cv2.putText(colored_img, pic_datetime.isoformat(' '), (5, 35),cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,255,255))
		video.write(colored_img)

	cv2.destroyAllWindows()
	video.release()

	return

def plotBrightness(files):

	#files = getThermalImages(namePattern)
	brightness = []
	for tfile in files:
		data, pic_datetime, fpa_temperature = parseRawFile(tfile)

		data = applyCalibration(data, fpa_temperature)

		win5 = data[5:26, 44:50] 
		win7 = data[4:26, 52:58] 
		brightness.append([pic_datetime, np.sum(data) / 4800,np.sum(win5) / (21 * 6) , np.sum(win7) / (22 * 6) ])

	npBrightnessList = np.array(brightness)
	ax=plt.gca()
	xfmt = md.DateFormatter('%H:%M')
	ax.xaxis.set_major_formatter(xfmt)
	plt.plot(npBrightnessList[:,0], npBrightnessList[:,1], 'b-', label='Total')
	plt.plot(npBrightnessList[:,0], npBrightnessList[:,2], 'r-', label='Window 5')
	plt.plot(npBrightnessList[:,0], npBrightnessList[:,3], 'g-', label='Window 7')
	legend = ax.legend(loc='upper right', shadow=True)
	plt.show()

	return 


def plotCameraTemperature(files):
	#files = getThermalImages(nameFilter)

	data = []
	for tfile in files:
		_, pic_datetime, temp = parseRawFile(tfile)
		data.append([pic_datetime, temp])


	npData = np.array(data)
	ax = plt.gca()
	xfmt = md.DateFormatter('%H:%M')
	ax.xaxis.set_major_formatter(xfmt)
	fpa = ax.plot(npData[:,0], npData[:,1], 'r-', label='FPA temperature (Kelvin)')
	legend = ax.legend(loc='upper right', shadow=True)
	plt.show()
	return



""" Parse the captured bin files 

Args:
	filename 

Returns:
	raw_data, time of capture, camera temperature in Kelvin, min value, max value 
"""
def parseRawFile(fileName):

	name = fileName.split('/')[-1];
	time = datetime.datetime.strptime(name[4:19], '%Y%m%d-%H%M%S')

	with open(fileName, mode='rb') as file: 
		content = file.read()
		# header : Camera FPA temperature (K), Min value, Max value 
		header = struct.unpack(">HHH", content[:6])
		buffer_data = struct.unpack("H" * 4800, content[6:])
		data = np.asarray(buffer_data, dtype=np.uint32).reshape(60, 80, 1)

	return data, time, header[0]/100.0


""" Create an image from raw data

Args: 
	raw data, colorMap
"""
def createImage(data, colorMap = -1, resizeScale = 5):
	if colorMap >=0:
		data = np.uint8(data)
		img_color = cv2.applyColorMap(data, colorMap)
	else:
		img_color = applyCustomColorMap(data)

	img = cv2.resize(img_color, (0,0), fx=resizeScale, fy=resizeScale) 
	return img



def applyCustomColorMap(raw_data):

#	if (colorMap >= 0):
#		data = np.uint8(raw_data)
#		img_color = cv2.applyColorMap(data, colorMap)
#		return img_color

	#cv2.normalize( data, data, 0, 65535, cv2.NORM_MINMAX)
	#np.right_shift(data, 8, data)

	maxVal = np.amax(raw_data)
	minVal = np.amin(raw_data)
	diff = maxVal - minVal + 1
	scaledValue = (raw_data - minVal) * 256 /diff


	gray = np.ndarray(shape=(60,80,3), dtype=np.uint8)

	for i in range(0,60):
		for j in range (0,80):
			val = scaledValue[i,j]
			gray[i,j] = [val, val, val]

	global COLOR_MAP
	img_color = cv2.LUT(gray, COLOR_MAP)


	return img_color


""" Calibrate the target temperature basedon the camera temperature and raw data

Args: 
	raw data, camera temperature in Kelvin

Returns:
	calibrated data

"""
def applyCalibration(raw_data, camera_temperature):
	camera_fahrenheit =  (camera_temperature - 273.15) * 1.8 + 32

	calibrated =  (0.05872 * raw_data) - 479.22999 + camera_fahrenheit 
	return calibrated

""" determine the point inside a given polygon 

Args: 
	Polygon as a list of (x,y) pairs

Returns:
	masked array for filtering points of raw data matrix

"""
def inside_points(points):
	mask = np.ones((60,80))
	for x in range(0,60):
		for y in range(0,80):
			n = len(points)
			inside = False
			p1x, p1y = points[0]
			for i in range(1, n + 1):
				p2x, p2y = points[i % n]
				if y > min(p1y, p2y):
					if y <= max(p1y, p2y):
						if x <= max(p1x, p2x):
							if p1y != p2y:
								xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
							if p1x == p2x or x <= xinters:
								inside = not inside
				p1x, p1y = p2x, p2y
			if (inside == True):
				mask[x,y] = 0
	return mask


def dbConnect(db_name = 'lepton'):
	return mysql.connector.connect(user='root', password='', host='localhost',database=db_name)



def storeThermalData(files, db_name='lepton', periods=[[datetime.datetime(1970,1,1,0,0), datetime.datetime(2050,1,1,0,0)]], segments= [[[(-1,-1),(0,80),(60,80),(60, 0)]]]):
	#masks = [[]]
	#mask_pixels = [[]]
	masks = [[] for x in range(len(periods))]
	mask_pixels = [[] for x in range(len(periods))]
	for i in range(0,len(periods)):
		for j,segment in enumerate(segments[i]):
			print j
			mask = inside_points(segment)
			masks[i].append(mask)
			mask_pixels[i].append(float(4800 - mask.sum()))


	conn = dbConnect(db_name)
	cursor = conn.cursor()

	#files = getThermalImages(nameFilter)

	data = []
	for tfile in files:
		print tfile
		data, pic_datetime, temperature = parseRawFile(tfile)

		period_index = 0
		for i,p in enumerate(periods):
			if pic_datetime >= p[0] and pic_datetime < p[1]:
				period_index = i
				break


		filename = tfile.split('/')[-1]
		ffc_id = tfile[tfile.rindex('_')+1:tfile.index('.')]
		cursor.execute("INSERT INTO images(id, filename, captured, temperature, ffc_id, period_id) VALUES (NULL, %s, %s, %s, %s, %s)", (filename, pic_datetime, temperature, ffc_id, period_index))
		image_id = cursor.lastrowid

		for segment_index,mask in enumerate(masks[period_index]):
			pixels = mask_pixels[period_index][segment_index]

			if pixels > 0:
				a = np.ma.masked_array(data, mask)
				avrg = a.sum() / pixels
				cursor.execute("INSERT INTO segments VALUES (%s, %s, %s, %s, %s)", (image_id, segment_index, int(a.min()), int(a.max()), float(avrg)))

		conn.commit()


	cursor.close()
	conn.close()
	return



def loadSegmentData(segment_id, db_name='lepton'):
	conn = dbConnect(db_name)
	cursor = conn.cursor()

	cursor.execute("SELECT captured, temperature, min_val, max_val, avrg_val FROM segments LEFT JOIN images ON image_id = images.id WHERE segment_id = %s AND avrg_val < 10000", (segment_id,))

	brightness = []

	for (captured, temperature, min_val, max_val, avrg_val ) in cursor:
		brightness.append([captured, temperature, min_val, max_val, avrg_val])

	cursor.close()
	conn.close()
	
	return np.array(brightness)


def plotSegment(segment_id, db_name='lepton'):

	npBrightnessList = loadSegmentData(segment_id, db_name)
	ax=plt.gca()
	xfmt = md.DateFormatter('%m-%d %H:%M:%S')
	ax.xaxis.set_major_formatter(xfmt)
	#plt.plot(npBrightnessList[:,0], npBrightnessList[:,1], 'y-', label='Camera Temperature')
	plt.plot(npBrightnessList[:,0], npBrightnessList[:,2], 'b.', label='Min Value')
	plt.plot(npBrightnessList[:,0], npBrightnessList[:,3], 'r.', label='Max Value')
	plt.plot(npBrightnessList[:,0], npBrightnessList[:,4], 'g.', label='Average Value')
	legend = ax.legend(loc='upper right', shadow=True)
	plt.show()

	return 

def plotSegments(segments, db_name='lepton'):

	formats = ['b-','g-','r-','b:','g:','r:']
	fig, ax = plt.subplots()

	for i,segment in enumerate(segments):
		data = loadSegmentData(segment, db_name)
		ax.plot_date(data[:,0], data[:,4], formats[i],label = 'Segment #'+str(segment))

	ax.xaxis.set_major_formatter(md.DateFormatter('%H:%M:%S'))
	legend = ax.legend(loc='upper right', shadow=True)
	plt.show()


	return	
