"""
This files contains examples and tests of the recognizers
"""
import cv2
import app.recognizers.recognizer as rc

recognizer = rc.Recognizer(conf_threshold=.6, method=rc.SMART_RECOGNITION)

while 1:
    recognizer.next_frame(data_on_frame=True, show_frame=True)
    if cv2.waitKey(1) != -1:
        break

recognizer.close_window()