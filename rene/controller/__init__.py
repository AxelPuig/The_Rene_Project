import time
import cv2
import os
import sys
import platform

ON_RASPBERRY = platform.uname()[1] == 'raspberrypi'

dir_path = os.path.dirname(os.path.realpath(__file__)) + os.sep + '..' + os.sep + '..'
sys.path.append(dir_path)

if ON_RASPBERRY:
    import rene.detector as detector
    import rene.controller.servo_controller as sct

# define what percent we rotate every servo around each axis per frame
coefficient_proportionnel_y = 0.3
coefficient_proportionnel_z = 0.5


class Controller():
    def __init__(self, conf_threshold=.9, pins=None, auto_capture=False):
        # Checks we are on raspberry, else control makes no sense
        if not ON_RASPBERRY:
            return

        # Default pins for servo control
        if pins is None:
            pins = [-1, 2, 3]
        assert len(pins) == 3

        # Servo setup
        sct.setup_GPIO()
        self.servos = []
        for i in range(len(pins)):
            if pins[i] != -1:
                servo = sct.ServoController(pins[i])
                self.servos.append(servo)

        self.conf_threshold = conf_threshold

        if auto_capture:
            self.detector = detector.Detector(conf_threshold, detector.FACE_DETECTION)

        self.nobody_frame_count = 0

    def move(self, person, frame):
        if not ON_RASPBERRY:
            return

        if person:
            # Center of face computed
            x1, y1, x2, y2 = person['box']
            height, width = frame.shape[0], frame.shape[1]
            x, y = (x1 + x2) / 2, (y1 + y2) / 2
            x, y = x / width, y / height

            # Operate the move
            delta_x = x - 0.5
            delta_y = y - 0.5
            self.servos[0].add_ratio(delta_x * coefficient_proportionnel_z)
            self.servos[1].add_ratio(delta_y * coefficient_proportionnel_y)

            self.nobody_frame_count = 0
        else:
            self.nobody_frame_count += 1

        if self.nobody_frame_count >= 5:
            # If nobody for a long time, looking around (useless but funny)
            self.servos[0].set_ratio(0.2)
            time.sleep(0.5)
            self.servos[0].set_ratio(0.8)
            time.sleep(0.5)
            self.servos[0].set_ratio(0.5)
            self.servos[1].set_ratio(0.5)
            self.nobody_frame_count = 0
