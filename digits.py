import json
import cv2
import numpy as np
max_value = 255
max_value_H = 360//2
low_H = 0
low_S = 0
low_V = 0
high_H = max_value_H
high_S = max_value
high_V = max_value
window_capture_name = 'Video Capture'
window_detection_name = 'Object Detection'
low_H_name = 'Low H'
low_S_name = 'Low S'
low_V_name = 'Low V'
high_H_name = 'High H'
high_S_name = 'High S'
high_V_name = 'High V'
cv2.namedWindow(window_detection_name)

def on_low_H_thresh_trackbar(val):
    global low_H
    global high_H
    low_H = val
    low_H = min(high_H-1, low_H)
    cv2.setTrackbarPos(low_H_name, window_detection_name, low_H)
def on_high_H_thresh_trackbar(val):
    global low_H
    global high_H
    high_H = val
    high_H = max(high_H, low_H+1)
    cv2.setTrackbarPos(high_H_name, window_detection_name, high_H)
def on_low_S_thresh_trackbar(val):
    global low_S
    global high_S
    low_S = val
    low_S = min(high_S-1, low_S)
    cv2.setTrackbarPos(low_S_name, window_detection_name, low_S)
def on_high_S_thresh_trackbar(val):
    global low_S
    global high_S
    high_S = val
    high_S = max(high_S, low_S+1)
    cv2.setTrackbarPos(high_S_name, window_detection_name, high_S)
def on_low_V_thresh_trackbar(val):
    global low_V
    global high_V
    low_V = val
    low_V = min(high_V-1, low_V)
    cv2.setTrackbarPos(low_V_name, window_detection_name, low_V)
def on_high_V_thresh_trackbar(val):
    global low_V
    global high_V
    high_V = val
    high_V = max(high_V, low_V+1)
    cv2.setTrackbarPos(high_V_name, window_detection_name, high_V)

def determineBallLocation(frame):
	# cap = cv2.imread('ball.jpg')
	# cv2.imshow('test', cap)

	orangeMask = cv2.inRange(frame, (low_H, low_S, low_V), (high_H, high_S, high_V))
	center = [ np.average(indices) for indices in np.where(orangeMask >= 255) ]
	print(center)
	cv2.circle(orangeMask,(center[0].astype(int), center[1].astype(int)), 5, (0,0,255), -1)

	cv2.imshow(window_detection_name, orangeMask)

def determineMBOTLocation(frame):
		qcd = cv2.QRCodeDetector()
		img = np.zeros((int(vc.get(3)),int(vc.get(4)),3), np.uint8)

		retval, decoded_info, points, straight_qrcode = qcd.detectAndDecodeMulti(frame)
  
		print(retval)
		if retval:

			# print(len(decoded_info))
			for i, p in zip(decoded_info,points):
				if(i != ''):
					text = (((i.split("["))[1].split("]"))[0]).split(",")

					cog = np.mean(p.astype(int), axis=0)
					# print(cog)
					print(text[1] == " 'RED'")
					if text[1] == " 'RED'":
						cv2.putText(img, text[0],cog.astype(int), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2,cv2.LINE_AA)
						cv2.circle(img,(cog.astype(int)), 5, (0,0,255), -1)

					if text[1] == '"Blue"':
						cv2.putText(img, text[0],cog.astype(int), cv2.FONT_HERSHEY_SIMPLEX , 1,(255,255,255),2,cv2.LINE_AA)
						cv2.circle(img,(cog.astype(int)), 5, (255,0,0), -1)
				
		cv2.imshow('Location Overlay', img)


cv2.namedWindow("preview")
vc = cv2.VideoCapture('qrVideo.avi') # TEMPORARY

### INITIALISATION
cv2.createTrackbar("Low H", window_detection_name, low_H, max_value_H, on_low_H_thresh_trackbar)
cv2.createTrackbar("High H", window_detection_name, high_H, max_value_H, on_high_H_thresh_trackbar)
cv2.createTrackbar("Low S", window_detection_name, low_S, max_value, on_low_S_thresh_trackbar)
cv2.createTrackbar("High S", window_detection_name, high_S, max_value, on_high_S_thresh_trackbar)
cv2.createTrackbar("Low V", window_detection_name, low_V, max_value, on_low_V_thresh_trackbar)
cv2.createTrackbar("High V", window_detection_name, high_V, max_value, on_high_V_thresh_trackbar)


##### MAIN PROGRAMME
while True:
    
	if vc.isOpened(): # try to get the first frame
		rval, frame = vc.read()
	else:
		rval = False
	
	im = cv2.resize(frame, (512,512))

	if rval:
		cv2.imshow('preview', frame)
		determineMBOTLocation(frame)
		determineBallLocation(frame)
    
	# cv2.imshow('res', img)
	cv2.waitKey(25)
				
