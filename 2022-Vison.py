import cv2
import numpy as np
from cscore import CameraServer

MAX_X = 640
MAX_Y = 360


def init_camera(name, path):
    cs = CameraServer.getInstance()
    camera = cs.startAutomaticCapture(name=name, path=path)
    camera.setResolution(MAX_X, MAX_Y)
    return camera


ball_cam = init_camera('ball', '/dev/video0')
hoop_cam = init_camera('hoop', '/dev/video0')

