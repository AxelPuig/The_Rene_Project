"""
Main function running the full program.
To debug the program, an argument word can be added, containing:
- 'd' for display, to display the frame taken by the pi
- 'g' for gesture, to display the detection operations on the frame
- 'v' for verbose, to print more information about what are the functions doing.
"""

# Importing talking functionality to inform that the program is running
from talker import Talker

talker = Talker()
talker.start()

import cv2
import argparse

# Importing custom objects and function
from app.capture import Capture
from app.recognizers.recognizer import Recognizer
from chooser import Chooser
from app.controllers.controller import Controller
from app.gesture_detection import gesture_detection

# Parsing
parser = argparse.ArgumentParser(description="Rene")
parser.add_argument("display", help="display image", type=str, nargs='?', default="no")
args = parser.parse_args()
display_image = 'd' in args.display
display_gesture = 'g' in args.display
verbose = 'v' in args.display

# Objects initialisation
cap = Capture()  # To read the frames from camera
recognizer = Recognizer()  # To recognize people
chooser = Chooser()  # To choose someone to look at
controller = Controller()  # To control the servos

# Say we are ready
talker.ready()

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
