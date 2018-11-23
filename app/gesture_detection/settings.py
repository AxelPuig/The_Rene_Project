import cv2
import imutils
import numpy as np

from app.gesture_detection.color_choosing import Settings

def skin_detector(grabbed,frame): #define a function to blur the "non-skin" pixels
    frame = imutils.resize(frame, width = 400)
    converted = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    skinMask = cv2.inRange(converted, lower, upper)
    skin = cv2.bitwise_and(frame, frame, mask = skinMask)
    new_frame = np.hstack([frame, skin])
    return ret, new_frame


s = Settings(6)

k = -1
while k == -1:
    # get frame
    v1, v2, v3, v4, v5, v6 = s.get_settings_window_values()

    lower = np.array([v1, v3, v5], dtype = "uint8")       #Define the range of colors that seems to be skin color
    upper = np.array([v2, v4, v6], dtype = "uint8")
    ret = None
    frame = cv2.imread("C:\\Users\\aypee\\PycharmProjects\\The_Rene_Project\\app\\gesture_detection\\image.jpg")

    _, new_frame = skin_detector(ret,frame)

    k = s.update_settings_window(new_frame)

cv2.destroyAllWindows()