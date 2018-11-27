"""
Code working, but not optimal with redundant functions.
"""

import cv2
import numpy as np

font = cv2.FONT_HERSHEY_SIMPLEX

# Thresholds to isolate skin (HSV)
lower1 = np.array([0, 44, 95], dtype="uint8")  # Define the range of colors that seems to be skin color
upper1 = np.array([12, 129, 186], dtype="uint8")
lower2 = np.array([165, 44, 95], dtype="uint8")  # Define the range of colors that seems to be skin color
upper2 = np.array([180, 129, 186], dtype="uint8")

kernel = np.ones((3, 3), np.uint8)


def skin_detector(frame):  # define a function to blur the "non-skin" pixels
    converted = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    skinMask = cv2.inRange(converted, lower1, upper1)
    skinMask += cv2.inRange(converted, lower2, upper2)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (8, 8))
    skinMask = cv2.erode(skinMask, kernel, iterations=1)
    skinMask = cv2.dilate(skinMask, kernel, iterations=2)
    skinMask = cv2.GaussianBlur(skinMask, (3, 3), 0)
    skin = cv2.bitwise_and(frame, frame, mask=skinMask)
    return skin


def is_the_hand_open(region, frame, display):
    x1, y1, x2, y2 = region
    width, height, _ = frame.shape
    x1 = int(min(max(x1, 0), width - 1))
    x2 = int(min(max(x2, 0), width - 1))
    y1 = int(min(max(y1, 0), height - 1))
    y2 = int(min(max(y2, 0), height - 1))
    if x1 - x2 == 0 or y1 - y2 == 0:
        return 0
    roi = frame[y1:y2, x1:x2]
    if display:
        cv2.rectangle(frame, (region[0], region[1]), (region[2], region[3]), (0, 255, 0), 0)
        cv2.imshow("roi", roi)
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, lower1, upper1)
    mask += cv2.inRange(hsv, lower2, upper2)

    # Extrapolate the hand to fill dark spots within
    mask = cv2.dilate(mask, kernel, iterations=4)

    # Blur the image
    mask = cv2.GaussianBlur(mask, (5, 5), 100)

    # Find contours
    _, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Find contour of max area(hand)
    if len(contours) == 0:
        return 0
    cnt = max(contours, key=lambda x: cv2.contourArea(x))

    # Approx the contour a little
    epsilon = 0.0005 * cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, epsilon, True)

    # Make convex hull around hand
    hull = cv2.convexHull(cnt)

    # Define area of hull and area of hand
    areahull = cv2.contourArea(hull)
    if areahull < (roi.shape[0] * roi.shape[1]) / 10:
        return 0

    # Find the defects in convex hull with respect to hand
    hull = cv2.convexHull(approx, returnPoints=False)
    defects = cv2.convexityDefects(approx, hull)

    if defects is None:
        return 0
    approx = np.array(approx)

    # Determining if the hand is open or closed by calculating the ratio height / width of the bounding box
    width = max(approx[:, 0, 0]) - min(approx[:, 0, 0])
    height = max(approx[:, 0, 1]) - min(approx[:, 0, 1])
    ratio = height / width
    if ratio > 1.2:
        return 1  # Hand open
    if 0.6 < ratio < 1.2:
        return 2  # Hand closed


def gesture_detection(frame, person, display=False):
    """
    Main function used in main.py.
    It detects a hand in a zone int the right side of the head
    :returns:
        - 0 if no hand detected
        - 1 if hand raised
        - 2 if hand closed
    """

    if not person:
        return 0
    frame = skin_detector(frame)
    region = list(person['box']).copy()
    largeur = region[2] - region[0]
    hauteur = region[3] - region[1]
    region[0] = int(region[0] - largeur * 2)
    region[1] = int(region[1] - hauteur * 0.5)
    region[2] = int(region[2] - largeur * 1.2)
    region[3] = int(region[3] + hauteur * 0.5)

    if is_the_hand_open(region, frame, display) == 1:
        if display:
            cv2.putText(frame, 'Say Hello', (10, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)
        return 1
    if is_the_hand_open(region, frame, display) == 2:
        if display:
            cv2.putText(frame, 'Take a picture', (10, 50), font, 2, (0, 0, 255), 3, cv2.LINE_AA)
        return 2
    if display:
        cv2.imshow("Skin", frame)
    return 0
