import cv2
import app.detectors.detector as dt
import app.controllers.servo_controller as sct

# define what percent we rotate every servo around each axis per frame
percent_per_frame = .01

resolution = (1280,720)

class Controller():

    def __init__(self, conf_threshold, pins):
        self.rotation = [0,0,0]

        assert len(pins) == 3
        sct.setup_GPIO()
        self.servos = []
        for i in range(len(pins)):
            servo = sct.ServoController(pins[i])
            self.servos.append(servo)

        self.conf_threshold = conf_threshold
        self.detector = dt.Detector(conf_threshold, dt.FACE_DETECTION, path_to_models="..\\detectors\\")

    def get_rotation(self):
        return self.rotation

    def set_rotation(self, rotation):
        self.rotation = rotation

    def next_move(self):
        out_frame, faces = self.detector.next_frame(data_on_frame=True, show_frame=True)
        if faces:
            face = faces[0]
            x1,y1,x2,y2,confidence = faces[0]
            x,y = (x1+x2)/2, (y1+y2)/2
            rotation = self.get_rotation()
            if x > resolution[0]/2:
                if rotation[1] <= 1-percent_per_frame:
                    self.servos[1].set_percent(self.get_rotation()[1]+percent_per_frame)
                else:
                    self.servos[1].set_percent(1)
            else:
                if rotation[1] >= percent_per_frame:
                    self.servos[1].set_percent(self.get_rotation()[1]-percent_per_frame)
                else:
                    self.servos[1].set_percent(0)

            if y > resolution[1]/2:
                if rotation[2] <= 1-percent_per_frame:
                    self.servos[2].set_percent(self.get_rotation()[2]+percent_per_frame)
                else:
                    self.servos[2].set_percent(2)
            else:
                if rotation[2] >= percent_per_frame:
                    self.servos[2].set_percent(self.get_rotation()[2]-percent_per_frame)
                else:
                    self.servos[2].set_percent(0)


    def start(self):
        while True:
            print(self.next_move())
            if cv2.waitKey(1) != -1:
                break

        self.detector.close_window()
        sct.clear()