"""
This file is the main python file to run on raspberry
"""
import os, sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + os.sep + '..')

import rene.talker as talk
from rene.capture import Capture

talk.rene_parle('Bonjour les amis, je suis en train de démarrer')

import cv2
import rene.recognizers.recognizer as recog

cap = Capture()

talk.rene_parle('Jai presque terminé, encore quelques secondes')

recognizer = recog.Recognizer(.6, recog.SMART_RECOGNITION)
hello_said = []
hello_in_process = {}

while cv2.waitKey(1) == -1:
    _, frame = cap.read()
    data, frame = recognizer.find_people(frame, data_on_frame=True)
    print(data)
    cv2.imshow("Recognizer", frame)

recognizer.close_window()
