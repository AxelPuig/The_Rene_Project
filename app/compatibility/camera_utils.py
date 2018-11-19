# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time



## Raspeberry Pi

def camera_init():
    # initialize the camera and grab a reference to the raw camera capture
    cam = PiCamera()
    cam.resolution = (640, 480)
    cam.framerate = 32

    time.sleep(0.1)
    return cam

def camera_get_frame(cam):
    #récupération de l'image fournie par la caméra
    #puis conversion en array numpy
    raw_capture = PiRGBArray(cam, size=(640, 480))
    cam.capture(raw_capture, format="bgr")
    frame = raw_capture.array
    return frame
