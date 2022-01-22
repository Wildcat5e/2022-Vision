from networktables import NetworkTables
import logging
import cv2
import numpy as np
import math

#Calibrate camera
FocalLength = 533.2 * 35.75 / 17.375 #FocalLength = Calibration object width in pixels * Calibration object distance in inches / Calibration object width in inches

#Make variables to control stuff that will break if its different
captureX = 1280
captureY = 720

#For NetworkTables, not needed, but useful
logging.basicConfig(level=logging.DEBUG)

#NetworkTables init
NetworkTables.initialize()
sd = NetworkTables.getTable("SmartDashboard")

#iniatilize and set camera to capture from with cv2
cap = cv2.VideoCapture(0)

#set resolution to capture with cv2, Microsoft lifecam hd 3000 Fov is 62*
cap.set(3, captureX)
cap.set(4, captureY)

#Insert code logic here
while True:
	#capture frame
	_, frame = cap.read()

	#converts the BGR color space of image to HSV color space and blur it
	#hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	blurred = cv2.GaussianBlur(frame, (3, 3), 0)
	gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)

	# Threshold of blue in HSV space
	#lower_blue = np.array([60, 35, 25])
	#upper_blue = np.array([180, 255, 255])

	# preparing the mask to overlay; generates a black/white image(pixels w/i color range are white)
	#im = cv2.inRange(hsv, lower_blue, upper_blue)
	output = blurred.copy()
	#masked = cv2.bitwise_or(output, output, mask = im)

	#find contours in prev created mask
	#contours = cv2.findContours(im, mode = cv2.RETR_TREE, method = cv2.CHAIN_APPROX_NONE)
	circles = cv2.HoughCircles(image = gray,
								method = cv2.HOUGH_GRADIENT, 
								dp = 1.1, 
								minDist = 50, 
								param1 = 100,
								param2 = 30,
								minRadius = 10,
								maxRadius = 50)
	# ensure at least some circles were found
	if circles is not None:
		# convert the (x, y) coordinates and radius of the circles to integers
		circles = np.round(circles[0, :]).astype("int")
		# loop over the (x, y) coordinates and radius of the circles
		for (x, y, r) in circles:
			color = frame[y, x]
			try:
				if color[2] < 100:
					# draw the circle in the output image, then draw a rectangle
					# corresponding to the center of the circle
					cv2.circle(output, (x, y), r, (255, 0, 0), 4)
					cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 0, 255), -1)
					print("Blue ball at:", x, "  ", y)

				if color[0] < 60:
					# draw the circle in the output image, then draw a rectangle
					# corresponding to the center of the circle
					cv2.circle(output, (x, y), r, (0, 0, 255), 4)
					cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (255, 0, 0), -1)
					print("Red ball at:", x, "  ", y)
			except:
				pass
