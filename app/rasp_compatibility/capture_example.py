# coding: utf-8
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import camera_utils as cam_utils

## Raspeberry Pi tests

def capture_camera():
    # initialize the camera and grab a reference to the raw camera capture
    cam = cam_utils.camera_init()


    # We acknowledge capturing a 30 fps video
    while True:
        #récupération de l'image fournie par la caméra
        _, out_frame = cam_utils.camera_get_frame(cam)
        print(type(out_frame))
        cv2.putText(out_frame, "Raspberry camera test", (5, 20), cv2.FONT_HERSHEY_SIMPLEX, .4, (255, 255, 255), 1)

        #affichage de l'image
        cv2.imshow("Face detection using TensorFlow", out_frame)

        # interval to let the system process imshow
        key = cv2.waitKey(10)


capture_camera()

