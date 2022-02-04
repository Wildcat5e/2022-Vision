import cv2
import numpy as np


class CircleFinder:

    def __init__(self, width=640, height=480):
        self.capture = cv2.VideoCapture(0)
        self.capture.set(3, width)
        self.capture.set(4, width)
        self.image = None

    def inside_image(self, circle):
        x = circle[0]
        y = circle[1]
        r = circle[2]
        return 0 <= x - r and x + r <= self.capture.get(3) and \
               0 <= y - r and y + r <= self.capture.get(4)

    def find(self):
        image_exists, self.image = self.capture.read()
        if not image_exists:
            return None
        # converts the BGR color space of image to HSV color space and blur it
        # hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        blurred = cv2.GaussianBlur(self.image, (3, 3), 0)
        gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
        circles = cv2.HoughCircles(image=gray,
                                   method=cv2.HOUGH_GRADIENT,
                                   dp=1.1,
                                   minDist=50,
                                   param1=100,
                                   param2=30,
                                   minRadius=10,
                                   maxRadius=50)
        if circles is None:
            return None
        # convert the (x, y, radius) tuples to integers
        c2 = np.round(circles[0, :]).astype("int")
        # only keep circles completely inside the image
        c3 = (c for c in c2 if self.inside_image(c))
        return c3
