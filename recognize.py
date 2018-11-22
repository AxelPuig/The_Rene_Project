"""
This file is the main python file to run on raspberry
"""
import app.rasp_speaking.talk as talk

talk.rene_parle('Bonjour les amis, je suis en train de démarrer')

import cv2
import app.recognizers.recognizer as recog

talk.rene_parle('Jai presque terminé, encore quelques secondes')

recognizer = recog.Recognizer(.6, recog.SMART_RECOGNITION)
hello_said = []
hello_in_process = {}

while True:
    frame, data = recognizer.next_frame(data_on_frame=False, show_frame=False)
    print(data)
    if data[0]['confidence_name'] >= 0.95:
        if data[0]['name'] not in hello_said: #Si bonjour non dit pour cette personne
            if data[0]['name'] not in hello_in_process:
                hello_in_process[data[0]['name']] = [1, 0] #[1 pour le nombre de fois reconnu, 0 à 2 pour les nombre de boucles parcourues depuis la dernière reconnaissance de data[name], au plus 2
            elif hello_in_process[data[0]['name']][0] == 1:
                talk.rene_parle('Bonjour '+ data[0]['name'])
                hello_said.append(data[0]['name'])
            else :
                hello_in_process[data[0]['name']] = [1,0]
    for i in hello_in_process :
        if i not in hello_said: #pour éviter du travail inutile.
            if hello_in_process[i][1] <= 1:
                hello_in_process[i][1] += 1 #indique qu'une boucle de plus a été parcourue
            else:
                hello_in_process[i] = [0,0] #réinitialise si pas de 2ème reconnaissance en moins de 3 boucles parcourues.
    print(hello_said)
    print(hello_in_process)

    if cv2.waitKey(1) != -1:
        break

recognizer.close_window()
