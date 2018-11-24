# The René Project (project completed)
Educative project built during second CentraleSupélec 2018 coding week. The main objective was to use
a raspberry pi for image recognition features.

## Description
-   René is a little robot composed of a *camera*

## Base features (MVP)
-	Follow a face with the camera in term of orientation `done`
-	Say “Hello” to every new face `done`
-	Take a picture on command `done`

## Extended features
-	Follow a conversation with the camera (and interact with commentaries)
-	Move in space with wheels only
-	Take simple orders with gestures `done`
-   follow another person/ scan/ search and find (on clapping)
-	Say “Hello” with the name of the person `done`

## Structure of the code
-   The main loop is in the file `main.py` in the root.
-   This loop calls only a few functions or methods which are stored in the `rene` module.
-   Some examples of these tools are given in `samples` directory.

## Dependencies
This project was built using:
* Python `3.6.4`
* OpenCV `3.4.3`
* SKLearn `0.0`
* IMUtils `0.5.1`
* numpy `1.14.2`
* Pillow `5.1.0`
* Click `7.0`
* Svoxpico

### Authors
* **Deschandol** Rémi (Servo control)
* **Niglio** Fabien (Gesture recognition)
* **Puig** Axel (Coordination)
* **Briffod** Alexis (Audio features)
* **Milon** Romain (AI features)
