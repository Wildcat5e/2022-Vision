import logging
import cv2
import numpy as np
from cscore import CameraServer
from networktables import NetworkTables
import time

#Make variables to control stuff that will break if its different
captureX = 640
captureY = 360
circles = None
anglePerPix = 62 / captureX #Microsoft lifecam hd 3000 Fov is 62*

#CameraServer init stuff
cs = CameraServer.getInstance()
cOut = cs.putVideo("Camera", captureX, captureY)

NetworkTables.initialize()
sd = NetworkTables.getTable("SmartDashboard")


#iniatilize and set camera to capture from with cv2
cap = cv2.VideoCapture(0)

#set resolution to capture with cv2
cap.set(3, captureX)
cap.set(4, captureY)

#Insert code logic here
kernelmatrix = np.ones((5, 5), np.uint8)
frame = None
gray = None
blurred = Noneoutput = None

while True:
	start = time.process_time()
	if frame is None:
		#capture frame
		_, frame = cap.read()
		gray = frame.copy()
		blurred = frame.copy()
	else:
		cap.read(image = frame)
	#timeaftercap = time.process_time() - start

	#blur then convert frame to b & w
	#blurred = cv2.GaussianBlur(frame, (7, 7), 0)
	
	#Convert image to B&W 
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	
	circlestart = time.process_time()
	#Find circles
	circles = cv2.HoughCircles(image = gray, 
							   method = cv2.HOUGH_GRADIENT, 
							   dp = 0.5, #Resolution scale factor
							   minDist = 50, #How far apart the circles are in pixels
							   param1 = 120, #Like param2, but it will return circles detected with this value first
							   param2 = 40, #How circular something is
							   minRadius = 10, #Minimum radius of the circles
							   maxRadius = 100) #Maximum radius of circles
	circlestime = time.process_time() - circlestart
	
	# ensure at least some circles were found
	if circles is None:
		continue
	# convert the (x, y) coordinates and radius of the circles to integers
	circles = np.round(circles[0, :]).astype("int")

	# loop over the (x, y) coordinates and radius of the circles
	for (x, y, r) in circles:
		if x < 0 or y < 0 or x > (captureX - 1) or y > (captureY - 1):
			continue
		color = frame[y, x]
		try:
			pass
			#For blue balls
			if color[2] < 100:
				# draw the circle in the frame image, then draw a rectangle
				# corresponding to the center of the circle
				cv2.circle(frame, (x, y), r, (255, 0, 0), 4)
				cv2.rectangle(frame, (x - 5, y - 5), (x + 5, y + 5), (0, 0, 255), -1)
			#For red balls
			elif color[0] < 60:
				# draw the circle in the output image, then draw a rectangle
				# corresponding to the center of the circle
				cv2.circle(frame, (x, y), r, (0, 0, 255), 4)
				cv2.rectangle(frame, (x - 5, y - 5), (x + 5, y + 5), (255, 0, 0), -1)

		except:
			pass


	
	cOut.putFrame(frame)
	print("Total = ", time.process_time() - start, " Total circles = ", circles.size, " Circle finding = ", circlestime)


	

cap.release()
