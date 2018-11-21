import cv2
import app.detectors.detector as dt
import app.controllers.servo_controller as sct

# define what percent we rotate every servo around each axis per frame
percent_per_frame = .01

class Controller():

    def __init__(self, conf_threshold, pins):
        assert len(pins) == 3
        sct.setup_GPIO()
        self.servos = []
        for i in range(len(pins)):
            if pins[i] != -1:
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
            height,width = out_frame.shape[0],out_frame.shape[1]
            x,y = (x1+x2)/2, (y1+y2)/2
            rotation = self.get_rotation()
            if x > width/2:
                self.servos[1].add_ratio(percent_per_frame)
            else:
                self.servos[1].add_ratio(-percent_per_frame)

            if y > height/2:
                self.servos[2].add_ratio(percent_per_frame)
            else:
                self.servos[2].add_ratio(-percent_per_frame)


    def start(self):
        while True:
            print(self.next_move())
            if cv2.waitKey(1) != -1:
                break

        self.detector.close_window()
        sct.clear()