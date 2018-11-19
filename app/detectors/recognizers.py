"""
This file contains different recognizer methods.
"""
import numpy as np
import sys
import time

import cv2
from app.detectors.database import frame_process_size, net, conf_threshold, embedder, load_database, face_process_size, \
    font
import imutils


def process(image, data, data_on_frame=False):
    """
    Process frame and returns faces detected
    :param image: Image to process
    :param data: DataBase
    :param data_on_frame: Returns the frame with rectangles and names around faces
    :return: tuple with frame and list of dicts like :
        "box": tuple (x1, y1, x2, y2)
        "confidence_face": float (proba that the box corresponds to a face)
        "name": str (name of the person detected)
        "confidence_name": float (proba that the name corresponds to the face)
    """
    database, recognizer, le = data

    # resize the frame to have a width of 600 pixels (while
    # maintaining the aspect ratio), and then grab the image
    # dimensions
    frame = imutils.resize(image, width=600)
    (h, w) = frame.shape[:2]

    # construct a blob from the image
    image_blob = cv2.dnn.blobFromImage(cv2.resize(frame, frame_process_size), 1.0, frame_process_size,
                                       (104.0, 177.0, 123.0), swapRB=False, crop=False)

    # apply OpenCV's deep learning-based face detector to localize
    # faces in the input image
    net.setInput(image_blob)
    detections = net.forward()

    # List of tuples to return
    dicts = []

    # loop over the detections
    for i in range(0, detections.shape[2]):
        # extract the confidence (i.e., probability) associated with
        # the prediction
        confidence = detections[0, 0, i, 2]

        if confidence > conf_threshold:
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
            faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255, face_process_size, (0, 0, 0), swapRB=True, crop=False)
            embedder.setInput(faceBlob)
            vec = embedder.forward()

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
                if confidence < conf_threshold:
                    box_color = (0, 0, 255)
                cv2.rectangle(frame, (x1, y1), (x2, y2), box_color, 2, 8)
                cv2.rectangle(frame, (x1, int(y1 + (y1 - y2) / 8)), (x2, y1), box_color, -1, 8)
                cv2.putText(frame, text, (int(x1 + (x2 - x1) / 40), int(y1 + (y1 - y2) / 40)), font, (y2 - y1) / 420.,
                            (255, 255, 255), 1)
    return (frame, dicts)


def recognize():
    """Recognizes faces present in the video source"""
    data = load_database()

    source = 0
    # By default we use 0 but we never know if there's any camera added to device, use it
    if len(sys.argv) > 1:
        source = sys.argv[1]

    print("[INFO] started camera...")

    cap = cv2.VideoCapture(source)

    frame_count = 0
    tt = 0
    while True:
        has_frame, frame = cap.read()
        if not has_frame:
            break
        frame_count += 1

        t = time.time()
        out_frame, _ = process(frame, data, True)
        tt += time.time() - t
        fps = frame_count / tt
        label = "FPS : {:.2f}".format(fps)
        cv2.putText(out_frame, label, (5, 20), cv2.FONT_HERSHEY_SIMPLEX, .4, (255, 255, 255), 1)

        cv2.imshow("Face detection using TensorFlow", out_frame)

        if frame_count == 1:
            tt = 0

        k = cv2.waitKey(10)
        if k == 27:
            break
    cv2.destroyAllWindows()
