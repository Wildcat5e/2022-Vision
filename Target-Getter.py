import cv2
import numpy as np
from time import sleep


#Make variables to control stuff that will break if its different
captureX = 640
captureY = 360
kernel = np.ones((5, 5), 'uint8')
ppdYaw = captureX / 62
ppdPitch = captureY / 34.875

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
    lower_blue = np.array([60, 30, 140])
    upper_blue = np.array([100, 255, 255])

    # preparing the mask to overlay; generates a black/white image(pixels w/i color range are white)
    im = cv2.inRange(hsv, lower_blue, upper_blue)
    #im = cv2.bilateralFilter(im, 20, 75, 75)
    im = cv2.erode(im ,kernel, iterations = 1)
    im = cv2.dilate(im, kernel, iterations = 1)
    
    

    #find contours in prev created mask
    squaresfound = 0
    contours, hierarchy = cv2.findContours(im, mode = cv2.RETR_TREE, method = cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.009 * cv2.arcLength(cnt, True), True)
        
        cv2.drawContours(output, [approx], 0, (0, 0, 255), 5)
        M = cv2.moments(cnt)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        if squaresfound == 0:
            listx = [cx]
            listy = [cy]
            squaresfound = 1

        else:
            listx.append(cx)
            listy.append(cy)


        meanx = np.mean(listx)
        meany = np.mean(listy)

        yawDegrees = int(meanx / ppdYaw) - 31
        pitchDegrees = int(34.875 - (meany / ppdPitch))
        dist = np.arctan(pitchDegrees * 106)

        
        print(yawDegrees)
        print(pitchDegrees)
        print(dist)
        print()
        

    

    cv2.imshow('Output', output)
    cv2.imshow('Mask', im)




    #Needed to function, do not remove, closes windows when q is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    sleep(0.5)

    
cv2.destroyAllWindows()
cap.release()