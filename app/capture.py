import os
import cv2
if os.uname()[1] == 'raspberrypi':
    import app.rasp_compatibility.camera_utils as cam_utils

OS_RASPBERRY = 'raspberrypi'


class Capture():
    def __init__(self, source=0):

        self.os = os.uname()[1]

        if self.os == OS_RASPBERRY:
            self.cap = cam_utils.camera_init()
        else:
            self.cap = cv2.VideoCapture(source)

    def read(self):
        if self.os == OS_RASPBERRY:
            return cam_utils.camera_get_frame_adapted(self.cap)
        else:
            return self.cap.read()

    def __del__(self):
        if self.os == OS_RASPBERRY:
            self.cap.release()