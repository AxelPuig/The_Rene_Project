"""
This file is the main python file to run on raspberry
"""
import app.rasp_speaking.talk as talk

talk.rene_parle('Bonjour les amis, je suis en train de démarrer')

import cv2
import app.recognizers.recognizer as recog

talk.rene_parle('Jai presque terminé, encore quelques secondes')

recognizer = recog.Recognizer(.6, recog.SMART_RECOGNITION)

while True:
    frame, data = recognizer.next_frame(data_on_frame=False, show_frame=False)
    print(data)

    if cv2.waitKey(1) != -1:
        break

recognizer.close_window()
