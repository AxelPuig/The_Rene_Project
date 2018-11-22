from talker import Talker

talker = Talker()

talker.start()

import cv2
from app.capture import Capture
from app.recognizers.recognizer import Recognizer

cap = Capture()
recognizer = Recognizer(auto_capture=False)

talker.ready()

while True:
    # ---------- MAIN CODE ----------

    res, frame = cap.read()

    people, _ = recognizer.find_people(frame)

    # Add choose person

    talker.talk(people, None, None, verbose=False)

    # ---------- END MAIN CODE ----------

    # Display results
    print(people)
    cv2.imshow("Debug window", frame)
    cv2.waitKey(1)
