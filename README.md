# The René Project
Educative project built during second CentraleSupélec 2018 coding week

## Base features
-	Follow a face with the camera in term of orientation
-	Say “Hello” to every new face
-	Take a picture on command

## Extended features
-	Follow a conversation with the camera (and interact with commentaries)
-	Move in space with wheels only
-	Take orders with gestures, follow another person/ scan/ search and find (on clapping)
-	Say “Hello” with the name of the person

## Main structure
```python
while True:
	frame = get_frame()
	persons = recognize(frame) # returns list of dicts
	person = choose_person(persons)
	action = detect_action(frame, person)
	talk(action, persons, person)
	move(person, action)
 ```
The functions can eventualy be class methods

## Dependencies
This project was built using:
* Python **3.6.4**
* OpenCV **3.4.3**
* SKLearn **0.0**
* IMUtils **0.5.1**
* numpy **1.14.2**
* Pillow **5.1.0**
* Click **7.0**

### Authors
* **Deschandol** *Rémi*
* **Niglio** *Fabien*
* **Puig** *Axel*
* **Briffod** *Alexis*
* **Milon** *Romain*

## Raspberry Pi SSH access
- Wifi : Honor6X
- ip : 192.168.43.70
- id : pi
- password : umdpsn'aps
