import os
import platform

class Talker:
    """ Makes the raspberry talk """

    def __init__(self):
        self.hello_said = []
        self.hello_in_process = {}
        self.nobody_rate = 0
        self.time_since_last_action = 0

    def inform_preparing(self):
        rene_parle("Salut a vous les copains ! Je me prépare.")

    def inform_ready(self):
        rene_parle("Je suis prêt !")

    def talk(self, people, action, person):
        """ Says something adapted to the situation """

        # Say hello if meeting someone for the first time since last run
        for person in people:
            if person['confidence_name'] >= 0.95:
                if person['name'] not in self.hello_said:  # Says hello to this person
                    if person['name'] not in self.hello_in_process:
                        self.hello_in_process[person['name']] = [1, 0]
                        # 1 pour le number of times he has been recognized,
                        # 0 to 2 for the number of loops iterations since recognition of data[name], maximum 2
                    elif self.hello_in_process[person['name']][0] == 1:
                        rene_parle('Bonjour ' + person['name'])
                        self.hello_said.append(person['name'])
                    else:
                        self.hello_in_process[person['name']] = [1, 0]
        for i in self.hello_in_process:
            if i not in self.hello_said and self.hello_in_process[i][0] != 0:  # To avoid useless work
                if self.hello_in_process[i][1] <= 2:
                    self.hello_in_process[i][1] += 1  # Remembers a loop has been run
                else:
                    self.hello_in_process[i] = [0, 0]  # Reset if still no recognition after 2 loops

        # Checking if someone in the frame
        if len(people) == 0:
            self.nobody_rate += 1
        else:
            self.nobody_rate = 0

        if self.nobody_rate >= 5:
            self.nobody_rate = 0

            # Says he can't find anyone !
            read_file("rene/speaking/nobody")

        if action == 1 and self.time_since_last_action > 1:
            # Says how are you if hand raised and has waited since last action
            if person['confidence_name'] > 0.95:
                rene_parle("Comment ça va " + person['name'] + " ?")
            else:
                rene_parle("Comment ça va ?")
            self.time_since_last_action = 0

        elif action == 2 and self.time_since_last_action > 1:
            # Says photo taken (that's wrong) if hand closed and has waited since last action
            rene_parle("Ok, je vous ai pris en photo !")
            self.time_since_last_action = 0

        else:
            self.time_since_last_action += 1

def rene_parle(text):
    """
    On the raspberry, text read by vocal synthesis
    On computer, text printed
    :param text: text to say
    """

    if platform.uname()[1] == "raspberrypi":
        parole = open("parole.txt", "w")  #  Creating text file

        parole.write("""#!/bin/bash\npico2wave -l fr-FR -w temp.wav '""" + text + """'
                     amixer sset 'PCM' 95%
                     omxplayer temp.wav
                     rm temp.wav""")

        parole.close()
        os.rename('parole.txt', 'parole.sh')  # text file --> shell file
        os.system('sh parole.sh')  # run shell
        os.remove('parole.sh')  # remove shell

    else:
        print("[RASPI SAYS] " + text)


def read_file(file_name):
    """
    File reading on raspberry pi.
    On computer, printing file name
    :param file_name
    """

    if platform.uname()[1] == "raspberrypi":
        lecture = open("lecture.txt", "w")  # création d'un fichier texte

        lecture.write("""#!/bin/bash
amixer sset 'PCM' 95%
omxplayer """ + file_name + """.wav""")

        lecture.close()
        os.rename('lecture.txt', 'lecture.sh')  # fichier texte --> fichier shell
        os.system('sh lecture.sh')  # execution du fichier shell
        os.remove('lecture.sh')  # suppression du fichier shell

    else:
        print("[RASPI SAYS] " + file_name)