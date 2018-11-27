""" Shows frame with Capture class """

import os
import sys

import cv2

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + os.sep + '..')

import rene.capture as cap

def capture_camera():
    # initialize the camera and grab a reference to the raw camera capture
    camera = cap.Capture()


    # We acknowledge capturing a 30 fps video
    while True:
        #récupération de l'image fournie par la caméra
        has_frame, out_frame = camera.read()
        if has_frame:
            cv2.putText(out_frame, "Raspberry camera test", (5, 20), cv2.FONT_HERSHEY_SIMPLEX, .4, (255, 255, 255), 1)

            #affichage de l'image
            cv2.imshow("Face detection", out_frame)

            # interval to let the system process imshow
            key = cv2.waitKey(10)
            if key != -1:
                return

capture_camera()

