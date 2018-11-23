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

    res, frame = cap.read()

    people, _ = recognizer.find_people(frame)

    person = chooser.choose(people)

    action = gesture_detection(frame, person, display_gesture)

    talker.talk(people, action, person, verbose=False)

    controller.move(person, frame)

    # ---------- END MAIN CODE ----------

    # Display results
    if verbose:
        print(people, person)
        print(action)
    if display_image:
        cv2.imshow("Debug window", frame)
    cv2.waitKey(1)
