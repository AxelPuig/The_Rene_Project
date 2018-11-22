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
    if data[confidence_name] >= 0.95:
        if data[name] not in hello_said: #Si bonjour non dit pour cette personne
            if data[name] not in hello_in_process:
                hello_in_process[data[name]] = [1, 0] #[1 pour le nombre de fois reconnu, 0 à 2 pour les nombre de boucles parcourues depuis la dernière reconnaissance de data[name], au plus 2
            elif hello_in_process[data[name]][0] == 1:
                talk.rene_parle('Bonjour '+ data[name])
                hello_said.append(data[name])
            else :
                hello_in_process[data[name]] = [1,0]
    for i in hello_in_process :
        if i not in hello_said: #pour éviter du travail inutile.
            if hello_in_process[i][1] <= 1:
                hello_in_process[i][1] += 1 #indique qu'un boucle de plus a été parcourue
            else:
                hello_in_processe[i] = [0,0] #réinitialise si pas de 2ème reconnaissance en moins de 3 boucles parcourues.
    print(hello_said)
    print(hello_in_process)

    if cv2.waitKey(1) != -1:
        break

recognizer.close_window()
