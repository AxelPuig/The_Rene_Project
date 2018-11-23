""" Main function. Give an argument 'disp' when running to display the image """
import time

from talker import Talker
from app.gesture_detection import gesture_detection

talker = Talker()

talker.start()

import cv2
import argparse

parser = argparse.ArgumentParser(description="Rene")
parser.add_argument("display", help="display image",
                    type=str, nargs='?', default="no")
args = parser.parse_args()

display_image = 'disp' in args.display
display_gesture = 'gesture' in args.display
verbose = 'verbose' in args.display

from app.capture import Capture
from app.recognizers.recognizer import Recognizer
from chooseperson import ChoosePerson
from app.controllers.controller import Controller

cap = Capture()
recognizer = Recognizer(auto_capture=False)
chooser = ChoosePerson()
controller = Controller(.9, [-1, 2, 3], auto_capture=False)

talker.ready()

while True:
    # ---------- MAIN CODE ----------

    t = time.time()
    res, frame = cap.read()
    t1 = time.time() - t

    t = time.time()
    people, _ = recognizer.find_people(frame)
    t2 = time.time() - t

    t = time.time()
    person = chooser.choose(people)
    t3 = time.time() - t

    t = time.time()
    action = gesture_detection(frame, person, display_gesture)
    t4 = time.time() - t

    t = time.time()
    talker.talk(people, action, person, verbose=False)
    t5 = time.time() - t

    t = time.time()
    controller.move(person, frame)
    t6 = time.time() - t

    # ---------- END MAIN CODE ----------

    # Display results
    print(t1, t2, t3, t4, t5, t6)
    if verbose:
        print(people, person)
        print(action)
    if display_image:
        cv2.imshow("Debug window", frame)
    cv2.waitKey(1)
