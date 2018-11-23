'''

    Detector class using different NN models

'''
import time
import cv2
import os, sys

import imutils

dir_path = os.path.dirname(os.path.realpath(__file__))
dir_path_capture = dir_path + os.sep + '..'
sys.path.append(dir_path_capture)
from capture import Capture

frame_process_size = [(192, 108), (256, 144), (320, 180), (300, 300), (426, 240), (640, 360), (1280, 720)][4]
net_models = [(dir_path + os.sep + "models" + os.sep + "deploy.prototxt",
               dir_path + os.sep + "models" + os.sep + "res10_300x300_ssd_iter_140000.caffemodel")]
font = cv2.FONT_HERSHEY_DUPLEX
FACE_DETECTION = 0
RATIO_DETECTION = 0.5
class Detector():

    def __init__(self, conf_threshold, method, source=-1):
        """ Method corresponds to the detection method used"""

        self.method = method
        self.conf_threshold = conf_threshold
        proto, model = net_models[self.method]

        self.net = cv2.dnn.readNetFromCaffe(proto, model)

        print("[INFO] starting camera...")
        self.cap = Capture(source=source)

    def process(self, image, data_on_frame=False):
        """
        Processes frame and returns faces detected
        :param image: image to process
        :param data_on_frame: returns the frame with rectangles and names around faces
        :return: tuple with frame and list of tuples like : (x1, y1, x2, y2, confidence)
        """
        out_frame = image.copy()
        out_frame = imutils.resize(out_frame, height=480*RATIO_DETECTION)
        height = out_frame.shape[0]
        width = out_frame.shape[1]
        # shrink the image down to size @frame_process_size
        blob = cv2.dnn.blobFromImage(out_frame, 1.0, out_frame.shape, [104, 117, 123], False, False)
        self.net.setInput(blob)
        detections = self.net.forward()
        faces = []
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > self.conf_threshold:  # definition of the left-top and right-bottom corners
                x1 = int(detections[0, 0, i, 3] * width)
                y1 = int(detections[0, 0, i, 4] * height)
                x2 = int(detections[0, 0, i, 5] * width)
                y2 = int(detections[0, 0, i, 6] * height)
                faces.append((x1, y1, x2, y2, confidence))

                if data_on_frame:
                    ratio = (confidence - self.conf_threshold) / (1 - self.conf_threshold)
                    box_color = (0, 255 * ratio, 255 * (1 - ratio))
                    if confidence < self.conf_threshold:
                        box_color = (0, 0, 255)
                    cv2.rectangle(out_frame, (x1, y1), (x2, y2), box_color, 2, 8)
                    cv2.rectangle(out_frame, (x1, int(y1 + (y1 - y2) / 8)), (int(x1 + 2 * (x2 - x1) / 3), y1),
                                  box_color, -1, 8)
                    cv2.putText(out_frame, str((confidence // 0.0001) / 100) + '%',
                                (int(x1 + (x2 - x1) / 20), int(y1 + (y1 - y2) / 40)), cv2.FONT_HERSHEY_DUPLEX,
                                (y2 - y1) / 300., (255, 255, 255), 1)
        return out_frame, faces

    def next_frame(self, data_on_frame=True, show_frame=False):
        """
        Returns None if end of video, else returns a tuple (frame, list tuples),
        where the list of tuples contains a tuple for each face detected containing (x1,y1,x2,y2,confidence)
        """

        if self.method == FACE_DETECTION:

            t = time.time()

            has_frame, frame = self.cap.read()
            if not has_frame:
                return None

            out_frame, results = self.process(frame, True)

            delta_t = time.time() - t
            fps = 1 / delta_t

            if data_on_frame:
                label = "FPS : {:.2f}".format(fps)
                cv2.putText(out_frame, label, (5, 20), font, .4, (255, 255, 255), 1)

            if show_frame:
                cv2.imshow("Face detection", out_frame)

            return out_frame, results

    def close_window(self):
        cv2.destroyAllWindows()
