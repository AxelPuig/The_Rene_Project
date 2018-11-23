import os
import platform


def rene_parle(text):
    """Synthese vocale du texte saisi (text), par le Raspberry.
    Si on est sur l'ordi, ça print le texte
    :param text: text to synthetize"""

    if platform.uname()[1] == "raspberrypi":
        parole = open("parole.txt", "w")  # création d'un fichier texte

        parole.write("""#!/bin/bash\npico2wave -l fr-FR -w temp.wav '""" + text + """'
                     amixer sset 'PCM' 95%
                     omxplayer temp.wav
                     rm temp.wav""")

        parole.close()
        os.rename('parole.txt', 'parole.sh')  # fichier texte --> fichier shell
        os.system('sh parole.sh')  # execution du fichier shell
        os.remove('parole.sh')  # suppression du fichier shell

    else:
        print("[RASPI SAYS] " + text)


def read_file(file_name):
    """lecture d'un fichier audio par le Raspberry.
    Si on est sur l'ordi, ça print le nom du fichier
    :param file_name """

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

# rene_parle('Bonjour')
