"""
Main function running the full program.
To debug the program, arguments can be added:
- 'display', to display the frame taken by the pi
- 'gesture', to display the detection operations on the frame
- 'verbose', to print more information about what are the functions doing.
"""

# Importing talking functionality to inform that the program is running
from rene.talker import Talker

talker = Talker()
talker.inform_preparing()

import cv2
import sys

# Importing custom objects and function
from rene.capture import Capture
from rene.recognizers.recognizer import Recognizer
from rene.chooser import Chooser
from rene.controller import Controller
from rene.gesture_detector import gesture_detection

# Parsing
display_image = 'display' in sys.argv
display_gesture = 'gesture' in sys.argv
verbose = 'verbose' in sys.argv

# Objects initialisation
cap = Capture()  # To read the frames from camera
recognizer = Recognizer()  # To recognize people
chooser = Chooser()  # To choose someone to look at
controller = Controller()  # To control the servos

# Say we are ready
talker.inform_ready()

while True:
    # ---------- MAIN CODE ----------

    _, frame = cap.read()  # Reading the frame

    people, _ = recognizer.find_people(frame)  # Find people on frame

    person = chooser.choose(people)  # Choose a person to follow

    action = gesture_detection(frame, person, display_gesture)  # Detect gesture

    talker.talk(people, action, person, verbose=False)  # Eventually talk

    controller.move(person, frame)  # Move the camera

    # ---------- END MAIN CODE ----------

    # Display results eventually
    if verbose:
        print(people, person)
        print(action)
    if display_image:
        cv2.imshow("Debug window", frame)
    cv2.waitKey(1)
