import cv2
import numpy as np
from time import sleep


#Calibrate camera
FocalLength = 533.2 * 35.75 / 17.375 #FocalLength = Calibration object width in pixels * Calibration object distance in inches / Calibration object width in inches

#Make variables to control stuff that will break if its different
captureX = 640
captureY = 360
kernel = np.ones((5, 5), 'uint8')

#iniatilize and set camera to capture from with cv2
cap = cv2.VideoCapture(0)

#set resolution to capture with cv2, Microsoft lifecam hd 3000 Fov is 62*
cap.set(3, captureX)
cap.set(4, captureY)


while True:
    #capture frame
    _, frame = cap.read()
    output = frame.copy()

    #converts the BGR color space of image to HSV color space and blur it
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #hsv = cv2.GaussianBlur(hsv, (5, 5), 0)

    # Threshold of blue in HSV space
    lower_blue = np.array([60, 35, 100])
    upper_blue = np.array([160, 255, 255])

    # preparing the mask to overlay; generates a black/white image(pixels w/i color range are white)
    im = cv2.inRange(hsv, lower_blue, upper_blue)
    #im = cv2.bilateralFilter(im, 20, 75, 75)
    im = cv2.erode(im ,kernel, iterations = 1)
    im = cv2.dilate(im, kernel, iterations = 1)
    
    

    #find contours in prev created mask
    contours, hierarchy = cv2.findContours(im, mode = cv2.RETR_TREE, method = cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.009 * cv2.arcLength(cnt, True), True)
        if(len(approx) == 4): 
            cv2.drawContours(output, [approx], 0, (0, 0, 255), 5)
    

    cv2.imshow('Output', output)
    cv2.imshow('Mask', im)




    #Needed to function, do not remove, closes windows when q is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    
cv2.destroyAllWindows()
cap.release()