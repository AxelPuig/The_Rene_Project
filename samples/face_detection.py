"""
This files contains examples and tests of the detectors
"""
import cv2
import os, sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + os.sep + '..')

from rene.capture import Capture
from rene.detector import Detector

detector = Detector()
cap = Capture()

while cv2.waitKey(1) == -1:
    _, frame = cap.read()
    frame, _ = detector.process(frame, data_on_frame=True)
    cv2.imshow("image", frame)

detector.close_window()