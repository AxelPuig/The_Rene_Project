'''

    Recognizer class using different NN (see database)

'''
import cv2

import imutils
import os
import sys
import numpy as np
import time

# update system path to allow imports from raspberry
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path)
import database as db

dir_path_capture = dir_path + os.sep + '..'
sys.path.append(dir_path_capture)
from capture import Capture

font = cv2.FONT_HERSHEY_DUPLEX
SMART_RECOGNITION = 1

class Recognizer():

    def __init__(self, conf_threshold=0.2, method=1, source=-1, auto_capture=True):
        """ :param method corresponds to the detection method used"""

        self.method = method
        self.conf_threshold = conf_threshold
        self.data = db.load_database()

        if auto_capture:
            # by default we use 0 but we never know if there's any camera added to device, use it

            print("[INFO] starting camera...")
            self.cap = Capture()

    def process(self, image, data_on_frame=False):
        """
        Processes frame and returns faces recognized
        :param image: image to process
        :param data: database
        :param data_on_frame: returns the frame with rectangles and names around faces
        :return: tuple with frame and list of dicts like :
            "box": tuple (x1, y1, x2, y2)
            "confidence_face": float (proba that the box corresponds to a face)
            "name": str (name of the person detected)
            "confidence_name": float (proba that the name corresponds to the face)
        """
        database, recognizer, le = self.data

        # resize the frame to have a width of 600 pixels (while
        # maintaining the aspect ratio), and then grab the image
        # dimensions
        frame = imutils.resize(image, width=600)
        (h, w) = frame.shape[:2]

        # construct a blob from the image
        image_blob = cv2.dnn.blobFromImage(cv2.resize(frame, db.frame_process_size), 1.0, db.frame_process_size,
                                           (104.0, 177.0, 123.0), swapRB=False, crop=False)

        # apply OpenCV's deep learning-based face detector to localize
        # faces in the input image
        db.net.setInput(image_blob)
        detections = db.net.forward()

        # List of tuples to return
        dicts = []

        # loop over the detections
        for i in range(0, detections.shape[2]):
            # extract the confidence (i.e., probability) associated with
            # the prediction
            confidence = detections[0, 0, i, 2]

            if confidence > self.conf_threshold:
                # compute the (x, y)-coordinates of the bounding box for
                # the face
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                x1, y1, x2, y2 = box.astype("int")

                # extract the face ROI
                face = frame[y1:y2, x1:x2]
                fH, fW = face.shape[:2]

                # ensure the face width and height are sufficiently large
                if fW < 20 or fH < 20:
                    continue

                # construct a blob for the face ROI, then pass the blob
                # through our face embedding model to obtain the 128-d
                # quantification of the face
                face_blob = cv2.dnn.blobFromImage(face, 1.0 / 255, db.face_process_size, (0, 0, 0), swapRB=True,
                                                 crop=False)
                db.embedder.setInput(face_blob)
                vec = db.embedder.forward()

                # perform classification to recognize the face
                preds = recognizer.predict_proba(vec)[0]
                j = np.argmax(preds)
                proba = preds[j]
                name = le.classes_[j]

                dicts.append({"box": (x1, y1, x2, y2),
                              "confidence_face": confidence,
                              "name": name,
                              "confidence_name": proba})

                if data_on_frame:
                    # draw the bounding box of the face along with the
                    # associated probability
                    text = "{}: {:.2f}%".format(name.upper(), proba * 100)
                    box_color = (0, 255 * proba, 255 * (1 - proba))
                    if confidence < self.conf_threshold:
                        box_color = (0, 0, 255)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), box_color, 2, 8)
                    cv2.rectangle(frame, (x1, int(y1 + (y1 - y2) / 8)), (x2, y1), box_color, -1, 8)
                    cv2.putText(frame, text, (int(x1 + (x2 - x1) / 40), int(y1 + (y1 - y2) / 40)), font,
                                (y2 - y1) / 420.,
                                (255, 255, 255), 1)
        return (frame, dicts)

    def find_people(self, frame, data_on_frame=False):
        """
        Returns None if end of video, else returns a tuple (list of dicts, frame),
        where the list of dicts contains a dict for each face recognized containing this :
            "box": tuple (x1, y1, x2, y2)
            "confidence_face": float (proba that the box corresponds to a face)
            "name": str (name of the person detected)
            "confidence_name": float (proba that the name corresponds to the face)
        """

        if self.method == SMART_RECOGNITION:

            out_frame, results = self.process(frame, data_on_frame)

            return results, out_frame


    def next_frame(self, data_on_frame=True, show_frame=False):
        """
        Returns None if end of video, else returns a tuple (frame, list of dicts),
        where the list of dicts contains a dict for each face recognized containing this :
            "box": tuple (x1, y1, x2, y2)
            "confidence_face": float (proba that the box corresponds to a face)
            "name": str (name of the person detected)
            "confidence_name": float (proba that the name corresponds to the face)
        """

        if self.method == SMART_RECOGNITION:

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
                cv2.imshow("Face recognition", out_frame)

            return out_frame, results

    def close_window(self):
        cv2.destroyAllWindows()
