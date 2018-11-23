""" Main function. Give an argument 'disp' when running to display the image """

from talker import Talker
from app.gesture_detection import gesture_detection

talker = Talker()

talker.start()

import cv2
import argparse

parser = argparse.ArgumentParser(description="Rene")
parser.add_argument("display", help="display image",
                    type=str, nargs='?', default="no_display")
args = parser.parse_args()

display_image = args.display = 'disp'

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

    action = gesture_detection(frame, person)

    talker.talk(people, None, None, verbose=False)

    controller.move(person, frame)

    # ---------- END MAIN CODE ----------

    # Display results
    print(people, person)
    print(action)
    if display_image:
        cv2.imshow("Debug window", frame)

    cv2.waitKey(1)
