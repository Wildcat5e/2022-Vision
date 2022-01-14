from networktables import NetworkTables
import logging
import cv2
import numpy as np
from cscore import CameraServer
import math

#Calibrate camera
FocalLength = 533.2 * 35.75 / 17.375 #FocalLength = Calibration object width in pixels * Calibration object distance in inches / Calibration object width in inches

#Make variables to control stuff that will break if its different
captureX = 1280
captureY = 720

#CameraServer init stuff
cs = CameraServer.getInstance()
output = cs.putVideo("Camera", captureX, captureY)

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
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Threshold of blue in HSV space
    lower_blue = np.array([60, 35, 140])
    upper_blue = np.array([180, 255, 255])

    # preparing the mask to overlay; generates a black/white image(pixels w/i color range are white)
    im = cv2.inRange(hsv, lower_blue, upper_blue)

    #find contours in prev created mask
    contours = cv2.findContours(im, mode = cv2.RETR_TREE, method = cv2.CHAIN_APPROX_NONE)


    print("running")



cap.release()