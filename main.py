from pynput.mouse import Button, Controller
import cv2


# import cyberpi

import time

cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)
# vc = cv2.imread('qr.png')

while True:

	if vc.isOpened(): # try to get the first frame
		rval, frame = vc.read()
	else:
		rval = False

	while rval:
		cv2.imshow("preview", frame)
		rval, frame = vc.read()
		key = cv2.waitKey(20)
		qcd = cv2.QRCodeDetector()

		retval, decoded_info, points, straight_qrcode = qcd.detectAndDecodeMulti(frame)

		print(retval)
		if retval:
			print(decoded_info)
			cv2.imshow("QR", straight_qrcode)

	coordinate = []
	# cyberpi.wifi_broadcast.set("message", coordinate)




# if vc.isOpened(): # try to get the first frame
#     rval, frame = vc.read()
# else:
#     rval = False

# while rval:
#     cv2.imshow("preview", frame)
#     rval, frame = vc.read()
#     key = cv2.waitKey(20)
#     if key == 27: # exit on ESC
#         break

# vc.release()
# cv2.destroyWindow("preview")