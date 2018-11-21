import cv2
import app.detectors.detector as dt

# define what percent we rotate every servo around each axis per frame
percent_per_frame = .01

class Controller():

    def __init__(self, conf_threshold, pins):
        self.rotation = [0,0,0]
        self.pins = pins
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
            face_center = ((x1+x2)/2, (y1+y2)/2)
            return face_center

    def start(self):
        while True:
            print(self.next_move())
            if cv2.waitKey(1) != -1:
                break

        self.detector.close_window()