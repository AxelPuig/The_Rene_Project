"""
This files contains examples and tests of the recognizers
"""
import cv2

import app.recognizers.database
from app.recognizers.recognizer import Recognizer

recognizer = Recognizer(method=1)

while 1:
    recognizer.next_frame(data_on_frame=True, show_frame=True)
    if cv2.waitKey(1) != -1:
        break

recognizer.close_window()