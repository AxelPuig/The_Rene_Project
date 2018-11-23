import cv2
import numpy as np
import math
import imutils
import argparse

font = cv2.FONT_HERSHEY_SIMPLEX

lower = np.array([0, 44, 95], dtype="uint8")  # Define the range of colors that seems to be skin color
upper = np.array([12, 129, 186], dtype="uint8")

kernel = np.ones((3, 3), np.uint8)


def skin_detector(frame):  # define a function to blur the "non-skin" pixels
    converted = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    skinMask = cv2.inRange(converted, lower, upper)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (8, 8))
    skinMask = cv2.erode(skinMask, kernel, iterations=1)
    skinMask = cv2.dilate(skinMask, kernel, iterations=2)
    skinMask = cv2.GaussianBlur(skinMask, (3, 3), 0)
    skin = cv2.bitwise_and(frame, frame, mask=skinMask)
    # new_frame = np.hstack([frame, skin])
    return skin


def is_the_hand_open(region, frame, display):
    x1, y1, x2, y2 = region
    width, height, _ = frame.shape
    x1 = int(min(max(x1, 0), width-2))
    x2 = int(min(max(x2, 1), width-1))
    y1 = int(min(max(y1, 0), height-2))
    y2 = int(min(max(y2, 1), height-1))
    print(x1, x2, y1, y2, frame.shape)
    roi = frame[x1:x2, y1:y2]
    if display:
        cv2.imshow("roi", roi)
        cv2.rectangle(frame, (region[0], region[1]), (region[2], region[3]), (0, 255, 0), 0)
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    # define range of skin color in HSV
    lower_skin = lower
    upper_skin = upper

    # extract skin colur image
    mask = cv2.inRange(hsv, lower_skin, upper_skin)

    # extrapolate the hand to fill dark spots within
    mask = cv2.dilate(mask, kernel, iterations=4)

    # blur the image
    mask = cv2.GaussianBlur(mask, (5, 5), 100)

    # find contours
    _, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # find contour of max area(hand)
    if len(contours) == 0:
        return 0
    cnt = max(contours, key=lambda x: cv2.contourArea(x))

    # approx the contour a little
    epsilon = 0.0005 * cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, epsilon, True)

    # make convex hull around hand
    hull = cv2.convexHull(cnt)

    # define area of hull and area of hand
    areahull = cv2.contourArea(hull)
    areacnt = cv2.contourArea(cnt)

    # find the percentage of area not covered by hand in convex hull
    arearatio = ((areahull - areacnt) / areacnt) * 100

    # find the defects in convex hull with respect to hand
    hull = cv2.convexHull(approx, returnPoints=False)
    defects = cv2.convexityDefects(approx, hull)

    if defects is None:
        return 0
    approx = np.array(approx)
    # print(approx)
    largeur = max(approx[:, 0, 0]) - min(approx[:, 0, 0])
    longueur = max(approx[:, 0, 1]) - min(approx[:, 0, 1])
    ratio = longueur / largeur
    if ratio > 1.1:
        return 1  # Hand open
    if 0.8 < ratio < 1.1:
        return 2  # Hand closed


def gesture_detection(frame, person, display=False):
    if not person:
        return 0
    # frame = imutils.resize(frame)
    frame = skin_detector(frame)
    region = list(person['box'])
    largeur = region[2] - region[0]
    hauteur = region[3] - region[1]
    region[0] = int(region[0] - largeur * 1.75)
    region[1] = int(region[1] - hauteur * 0.5)
    region[2] = int(region[2] - largeur * 1.25)
    region[3] = int(region[3])

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
