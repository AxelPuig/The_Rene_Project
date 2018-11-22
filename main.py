from talker import Talker

talker = Talker()

talker.start()

import cv2
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

    # action = detect_action(frame, person)

    talker.talk(people, None, None, verbose=False)

    controller.move(person, frame)

    # ---------- END MAIN CODE ----------

    # Display results
    print(people, person)
    # cv2.imshow("Debug window", frame)

    cv2.waitKey(1)
