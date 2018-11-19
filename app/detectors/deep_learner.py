from imutils import paths
import face_recognition as fr
import imutils
import pickle
import time
import cv2
import sys
import os

# we won't use ts_detector because face_recognition is built to be better and does the same thing
# post-testing: well it isn't
database_path = "..\\..\\Data\\database\\train\\"
face_detection_method = 'cnn'

def serialize_database():
    # grab the paths to the input images in our dataset
    print("[INFO] quantifying faces...")
    image_paths = list(paths.list_files(database_path))

    # initialize the list of known encodings and known names
    known_encodings = []
    known_names = []

    # loop over the image paths
    for (i, image_path) in enumerate(image_paths):
        # extract the person name from the image path
        print("[INFO] processing image {}/{} :: {}".format(i + 1, len(image_paths), image_path))
        name = image_path.split(os.path.sep)[-2]

        # load the input image and convert it from RGB (OpenCV ordering)
        # to dlib ordering (RGB) + reduces it to allow it to pass through the cnn
        image = cv2.imread(image_path)
        sm_image = image
        rgb_image = cv2.cvtColor(sm_image, cv2.COLOR_BGR2RGB)

        # detect the (x, y)-coordinates of the bounding
        # corresponding to each face in the input image
        boxes = fr.face_locations(rgb_image, model=face_detection_method)

        # compute the facial embedding for the face
        encodings = fr.face_encodings(rgb_image, boxes)

        # loop over the encodings
        for encoding in encodings:
            # add each encoding + name to our database
            known_encodings.append(encoding)
            known_names.append(name)

    print("[INFO] serializing encodings...")
    data = {"encodings": known_encodings, "names": known_names}
    file = open(database_path + "encodings_" + face_detection_method + ".pickle", "wb+")
    file.write(pickle.dumps(data))
    file.close()
    print("[INFO] encodings written to {}".format(database_path + "encodings_" + face_detection_method + ".pickle"))

def load_database():
    print("[INFO] loading encodings...")
    return pickle.loads(open(database_path + "encodings_" + face_detection_method + ".pickle", "rb").read())

def process(image, database, resize=False, debug=False):
    # scale down the image to process it faster
    sm_image = image
    if resize:
        imutils.resize(image, height=720)
    rgb_image = cv2.cvtColor(sm_image, cv2.COLOR_BGR2RGB)

    # detect the (x, y)-coordinates of the bounding boxes corresponding
    # to each face in the input image, then compute the facial embeddings
    # for each face
    if debug:
        print("[INFO] recognizing faces...")
    boxes = fr.face_locations(rgb_image, model=face_detection_method)
    encodings = fr.face_encodings(rgb_image, boxes)

    # initialize the list of names for each face detected
    names = []

    # loop over the facial embeddings
    for encoding in encodings:
        # attempt to match each face in the input image to our known
        # encodings
        matches = fr.compare_faces(database["encodings"], encoding)
        name = "Unknown"

        # check to see if we have found a match
        if True in matches:
            # find the indexes of all matched faces then initialize a
            # dictionary to count the total number of times each face
            # was matched
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}

            # loop over the matched indexes and maintain a count for
            # each recognized face face
            for i in matchedIdxs:
                name = database["names"][i]
                counts[name] = counts.get(name, 0) + 1

            # determine the recognized face with the largest number of
            # votes (note: in the event of an unlikely tie Python will
            # select first entry in the dictionary)
            name = max(counts, key=counts.get)

        # update the list of names
        names.append(name)

    # loop over the recognized faces
    for ((top, right, bottom, left), name) in zip(boxes, names):
        # draw the predicted face name on the image
        cv2.rectangle(sm_image, (left, top), (right, bottom), (0, 255, 0), 2)
        y = top - 15 if top - 15 > 15 else top + 15
        cv2.putText(sm_image, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

    return sm_image

def recognize():
    database = load_database()
    source = 0
    if len(sys.argv) > 1:
        source = sys.argv[1]

    print("[INFO] started camera...")

    cap = cv2.VideoCapture(source)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 352);
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240);
    frame_count = 0
    tt = 0
    while True:
        has_frame, frame = cap.read()
        if not has_frame:
            break
        frame_count += 1

        t = time.time()
        out_frame = process(frame, database)
        tt += time.time() - t
        fps = frame_count / tt
        label = "FPS : {:.2f}".format(fps)
        cv2.putText(out_frame, label, (5, 20), cv2.FONT_HERSHEY_SIMPLEX, .4, (255, 255, 255), 1)

        cv2.imshow(face_detection_method + " detection method", out_frame)

        if frame_count == 1:
            tt = 0

        k = cv2.waitKey(10)
        if k == 27:
            break
    cv2.destroyAllWindows()

#database has already been serialized using 'hog' face locations detector
serialize_database()

#recognize()