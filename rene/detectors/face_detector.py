"""
This files contains examples and tests of the detectors
"""
import cv2
import os, sys
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path)
import detector as dt

detector = dt.Detector(.9, dt.FACE_DETECTION)

while True:
    detector.next_frame(data_on_frame=True, show_frame=True)
    if cv2.waitKey(1) != -1:
        break

detector.close_window()