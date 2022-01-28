import cv2
import numpy as np
from time import sleep


#Calibrate camera
FocalLength = 533.2 * 35.75 / 17.375 #FocalLength = Calibration object width in pixels * Calibration object distance in inches / Calibration object width in inches

#Make variables to control stuff that will break if its different
captureX = 1280
captureY = 720
kernelmatrix = np.ones((5, 5), np.uint8)

#iniatilize and set camera to capture from with cv2
cap = cv2.VideoCapture(0)

#set resolution to capture with cv2, Microsoft lifecam hd 3000 Fov is 62*
cap.set(3, captureX)
cap.set(4, captureY)


while True:
    #capture frame
    _, frame = cap.read()

    #converts the BGR color space of image to HSV color space and blur it
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #hsv = cv2.GaussianBlur(hsv, (5, 5), 0)

    # Threshold of blue in HSV space
    lower_blue = np.array([60, 35, 140])
    upper_blue = np.array([180, 255, 255])

    # preparing the mask to overlay; generates a black/white image(pixels w/i color range are white)
    im = cv2.inRange(hsv, lower_blue, upper_blue)
    im = cv2.dilate(im, kernelmatrix)

    #find contours in prev created mask
    contours, hierarchy = cv2.findContours(im, mode = cv2.RETR_TREE, method = cv2.CHAIN_APPROX_NONE)


    #finds biggest contour, worship this logic
    #loops through the contours, saving contours and their area(biggest and 2nd biggest contour)
    ln = 0
    bc = 0
    bcid = None
    for x in contours:
        contourNum = contours[ln]#crashes if no contours are found, may cause divide by zero issues later, try except pass everything that references cx, cy, cx2, cy2
        area = cv2.contourArea(contourNum)
        if area >= bc:
            bc = area
            bcid = contourNum
        ln = ln + 1
    #Converts black&white img to RGB
    imwbb = cv2.cvtColor(im, cv2.COLOR_GRAY2RGB)

    if bcid is None:
        continue

    #Draw box around biggest contour
    rect = cv2.minAreaRect(bcid)
    (x, y), (w, h), angle = rect
    #print(angle)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    cv2.drawContours(imwbb, [box], 0, (0, 0, 255), 2)

    x = x - 640
    y = y - 360

    if w > h:
        correctW = w
        correctH = h
    elif h > w:
        correctW = h
        correctH = w
    
    #Calculates angle to camera
    anglePerPixY= 62 / captureY
    anglePerPix = 62 / captureX
    Angle = x * anglePerPix
    AngleY = -y * anglePerPixY
    

    #Find distance from camera to contour, the int is the width of the object your measuring distance too
    Distance = 17.375 * FocalLength / correctW
    Distance = int(Distance)


    #Uses pythagorean thereum to find the horizontal distanc to target
    C = Distance * Distance
    B = 83 * 83
    D = C - B
    HorizontalDistance = 0
    try:
        HorizontalDistance = math.sqrt(D)
    except:
        pass
        #print("To close to target")

    #print(x, " ", y, " ", w, " ", h)
    print(int(bc), " ", Angle, " ", AngleY)
    #shows image
    cv2.imshow('Contours', imwbb)

    #Needed to function, do not remove, closes windows when q is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    
cv2.destroyAllWindows()
cap.release()