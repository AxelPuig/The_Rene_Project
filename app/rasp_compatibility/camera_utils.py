# coding: utf-8
from picamera.array import PiRGBArray
from picamera import PiCamera
import time


## Raspeberry Pi

def camera_init():
    """initialize the camera and grab a reference to the raw camera capture and return a camera object"""
    cam = PiCamera()
    cam.resolution = (640, 480)
    cam.framerate = 32

    time.sleep(0.1)
    return cam


def camera_get_frame(cam):
    """return a frame took by the camera in a numpy array format"""
    raw_capture = PiRGBArray(cam, size=(640, 480))
    cam.capture(raw_capture, format="bgr")
    frame = raw_capture.array
    return frame
