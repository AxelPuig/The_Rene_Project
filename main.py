import cv2

from app.capture import Capture
from app.recognizers.recognizer import Recognizer

cap = Capture()
recognizer = Recognizer(auto_capture=False)

while True:
    # ---------- MAIN CODE ----------

    frame = cap.read()

    people, _ = recognizer.find_people(frame)

    # Add choose person



    # ---------- END MAIN CODE ----------

    # Display results
    print(people)
    cv2.imshow("coucou", frame)
    cv2.waitKey(1)