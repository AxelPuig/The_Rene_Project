"""
This file is the main python file to run on raspberry
"""
import os, sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + os.sep + '..')

import app.rasp_speaking.talk as talk

talk.rene_parle('Bonjour les amis, je suis en train de démarrer')

import cv2
import app.detectors.detector as detect

talk.rene_parle('Jai presque terminé, encore quelques secondes')

detector = detect.Detector(.6, detect.FACE_DETECTION)

while True:
    frame, data = detector.next_frame(data_on_frame=False, show_frame=False)
    print(data)

    if cv2.waitKey(1) != -1:
        break

detector.close_window()
