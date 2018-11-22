"""
This files contains examples and tests of the recognizers
"""
import cv2
import os, sys
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path)
import recognizer as rc

recognizer = rc.Recognizer(.6, rc.SMART_RECOGNITION)

while True:
    recognizer.next_frame(data_on_frame=True, show_frame=True)
    if cv2.waitKey(1) != -1:
        break

recognizer.close_window()