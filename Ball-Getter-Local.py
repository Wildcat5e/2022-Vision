import logging
import cv2
import numpy as np
import time


#Make variables to control stuff that will break if its different
captureX = 640
captureY = 360
circles = None
anglePerPix = 62 / captureX #Microsoft lifecam hd 3000 Fov is 62*


#iniatilize and set camera to capture from with cv2
cap = cv2.VideoCapture(0)

#set resolution to capture with cv2
cap.set(3, captureX)
cap.set(4, captureY)

#Insert code logic here
kernelmatrix = np.ones((5, 5), np.uint8)
while True:
	times = []

	#capture frame
	_, frame = cap.read()
	#blur then convert frame to b & w

	blurred = cv2.GaussianBlur(frame, (3, 3), 0)
	#Dilate the image(make it look funky)
	#blurred = cv2.dilate(blurred, kernelmatrix)
	#Convert image to B&W 
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	output = blurred.copy()

	#Find circles
	
	times.append(time.process_time())
	circles = cv2.HoughCircles(image = gray, 
							   method = cv2.HOUGH_GRADIENT, 
							   dp = 0.5, #Resolution scale factor
							   minDist = 50, #How far apart the circles are in pixels
							   param1 = 100, #Like param2, but it will return circles detected with this value first
							   param2 = 35, #How circular something is
							   minRadius = 10, #Minimum radius of the circles
							   maxRadius = 100) #Maximum radius of circles
	times.append(time.process_time())
	
	
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
			if color[2] < 100:
				# draw the circle in the output image, then draw a rectangle
				# corresponding to the center of the circle
				cv2.circle(output, (x, y), r, (255, 0, 0), 4)
				cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 0, 255), -1)
				#print("Blue ball at:", x, "  ", y)

			if color[0] < 60:
				# draw the circle in the output image, then draw a rectangle
				# corresponding to the center of the circle
				cv2.circle(output, (x, y), r, (0, 0, 255), 4)
				cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (255, 0, 0), -1)
				#print("Red ball at:", x, "  ", y)
		except:
			pass


	
	cv2.imshow('Contours', output)
		#Needed to function, do not remove, closes windows when q is pressed
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break


	times.append(time.process_time())

	print(times)
	time.sleep(0.1)
cap.release()
