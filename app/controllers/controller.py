import cv2
import os
import sys

dir_path = os.path.dirname(os.path.realpath(__file__)) + os.sep + '..' + os.sep + '..'
sys.path.append(dir_path)

import app.detectors.detector as dt
import app.controllers.servo_controller as sct

# define what percent we rotate every servo around each axis per frame
coefficient_proportionnel = 0.5


class Controller():

    def __init__(self, conf_threshold, pins, auto_capture=True):
        assert len(pins) == 3

        sct.setup_GPIO()
        self.servos = []
        for i in range(len(pins)):
            if pins[i] != -1:
                servo = sct.ServoController(pins[i])
                self.servos.append(servo)

        self.conf_threshold = conf_threshold

        if auto_capture:
            self.detector = dt.Detector(conf_threshold, dt.FACE_DETECTION)


    def move(self, person, frame):
        if person:
            x1, y1, x2, y2 = person['box']
            height, width = frame.shape[0], frame.shape[1]

            x, y = (x1+x2)/2, (y1+y2)/2
            x, y = x/width, y/height
            delta_x = x - 0.5
            delta_y = y - 0.5

            self.servos[0].add_ratio(delta_x * coefficient_proportionnel)
            self.servos[1].add_ratio(delta_y * coefficient_proportionnel)


    def start_example(self):
        while True:
            self.next_move()
            if cv2.waitKey(1) != -1:
                break

        self.detector.close_window()
        sct.clear()
