"""

    This file contains a function to create the database, and a function to load it

    Caffe CNN used to recognize faces on webcam

    We first need to serialize embeddings produced by the network from the images from @database_path
    @frame_process_size and @face_process_size can be changed to other sizes from the list to enhance performances
    !! If you change it, don't forget to serialize database to use new process size and make sure you have the best results !!
    Thus, @process_size_suffix is used to save embeddings corresponding to different process sizes

"""

from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
import imutils
import numpy as np
import pickle
import cv2
import time
import sys
import os

# Constants
frame_process_size = [(192, 108), (256, 144), (320, 180), (300, 300), (426, 240), (640, 360), (1280, 720)][3]
face_process_size = [(72, 72), (96, 96)][1]
process_size_suffix = "_" + str(frame_process_size[0]) + "_" + str(frame_process_size[1])

database_path = "..\\..\\Data\\database\\learn\\"

# load our serialized face detector from disk
proto_txt = "models\\deploy.prototxt"
config_file = "models\\res10_300x300_ssd_iter_140000.caffemodel"
net = cv2.dnn.readNetFromCaffe(proto_txt, config_file)

# load our serialized face embedding model from disk
embedder_file = "models\\openface_nn4.small2.v1.t7"
embedder = cv2.dnn.readNetFromTorch(embedder_file)

def serialize(conf_threshold, *names):
    # grab the paths to the input images in our dataset
    print("[INFO] quantifying faces...")

    # initialize the list of known encodings and known names
    known_embeddings = []
    known_names = []

    total = 0
    # loop over the image paths
    for name in names:
        print("[INFO] serializing {}...".format(name))
        video_path = database_path + name + "\\face.avi"
        video = cv2.VideoCapture(video_path)
        has_frame, frame = video.read()
        index = 1

        while has_frame:
            embedding = serialize_face(frame, name, conf_threshold, index)
            if embedding is not None:
                known_embeddings.append(embedding)
                known_names.append(name)
                total += 1
            has_frame, frame = video.read()
            index += 1

    # dump the facial embeddings + names to disk
    print("[INFO] serializing {} encodings...".format(total))
    data = {"embeddings": known_embeddings, "names": known_names}
    f = open(database_path + "embeddings" + process_size_suffix + ".pickle", "wb+")
    f.write(pickle.dumps(data))
    f.close()

    # encode the labels
    print("[INFO] encoding labels...")
    le = LabelEncoder()
    labels = le.fit_transform(known_names)

    # train the model used to accept the 128-d embeddings of the face and
    # then produce the actual face recognition
    print("[INFO] training model...")
    recognizer = SVC(C=1.0, kernel="linear", probability=True)
    recognizer.fit(known_embeddings, labels)

    # write the actual face recognition model to disk
    f = open(database_path + "recognizer" + process_size_suffix + ".pickle", "wb")
    f.write(pickle.dumps(recognizer))
    f.close()

    # write the label encoder to disk
    f = open(database_path + "le" + process_size_suffix + ".pickle", "wb")
    f.write(pickle.dumps(le))
    f.close()

def serialize_face(frame, name, conf_threshold, index, smiling=False):
    # extract the person name from the image path
    print("[INFO] processing image {}".format(index))

    image = imutils.resize(frame, width=600)
    h, w = image.shape[:2]

    blob = cv2.dnn.blobFromImage(cv2.resize(image, frame_process_size), 1.0, frame_process_size, (104.0, 177.0, 123.0), swapRB=False, crop=False)
    net.setInput(blob)
    detections = net.forward()
    # ensure at least one face was found
    if len(detections) > 0:
        # we're making the assumption that each image has only ONE
        # face, so find the bounding box with the largest probability
        i = np.argmax(detections[0, 0, :, 2])
        confidence = detections[0, 0, i, 2]

        # ensure that the detection with the largest probability also
        # means our minimum probability test (thus helping filter out
        # weak detections)
        if confidence > conf_threshold:
            # compute the (x, y)-coordinates of the bounding box for
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            # the face
            (startX, startY, endX, endY) = box.astype("int")

            # extract the face ROI and grab the ROI dimensions
            face = image[startY:endY, startX:endX]
            (fH, fW) = face.shape[:2]

            # ensure the face width and height are sufficiently large
            if fW < 20 or fH < 20:
                return None

            faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255, face_process_size, (0, 0, 0), swapRB=True, crop=False)
            embedder.setInput(faceBlob)
            vec = embedder.forward()

            return vec.flatten()

def record(name):
    """Saves the video extracted from the video source to file at @database_path, then used to learn the face"""

    source = 0
    #By default we use 0 but we never know if there's any camera added to device, use it
    if len(sys.argv) > 1:
        source = sys.argv[1]

    print("[INFO] started camera...")

    cap = cv2.VideoCapture(source)
    has_frame, frame = cap.read()

    filename = "face.avi"

    vid_writer = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 15, (frame.shape[1], frame.shape[0]))

    frame_count = 0
    t = time.time()
    tt = 0
    recording = False
    while True:
        has_frame, frame = cap.read()
        if not has_frame:
            break
        frame_count += 1

        out_frame = frame.copy()
        tt += time.time() - t
        fps = frame_count / tt
        t = time.time()
        if not recording:
            label = "Press spacebar to start recording   FPS : {:.2f}".format(fps)
            cv2.putText(out_frame, label, (5, 20), cv2.FONT_HERSHEY_SIMPLEX, .4, (0, 0, 255), 1)
        else:
            label = "Press spacebar to stop recording   FPS : {:.2f}".format(fps)
            cv2.putText(out_frame, label, (5, 20), cv2.FONT_HERSHEY_SIMPLEX, .4, (0, 255, 0), 1)
            vid_writer.write(out_frame)

        cv2.imshow("Recording face", out_frame)

        if frame_count == 1:
            tt = 0

        k = cv2.waitKey(10)
        if k == 27:
            break
        elif k == 32:
            if recording:
                break
            else:
                recording = True
    cv2.destroyAllWindows()
    vid_writer.release()

    os.rename(filename, database_path + "{}\\".format(name) + filename)

def load_database():
    """Loads embeddings and labels from disk"""
    print("[INFO] loading encodings...")
    database = pickle.loads(open(database_path + "embeddings" + process_size_suffix + ".pickle", "rb").read())

    # load the actual face recognition model along with the label encoder
    recognizer = pickle.loads(open(database_path + "recognizer" + process_size_suffix + ".pickle", "rb").read())
    le = pickle.loads(open(database_path + "le" + process_size_suffix + ".pickle", "rb").read())
    return database, recognizer, le

serialize(.95, "Romain", "Alexis", "Axel", "Remi", "Fabien")