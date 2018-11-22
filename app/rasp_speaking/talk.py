
import os
import platform


def rene_parle(text):
    """Synthese vocale du texte saisi (text), par le Raspberry.
    Si on est sur l'ordi, ça print le texte"""

    if platform.uname()[1] == "raspberrypi":
        parole = open("parole.txt", "w") #création d'un fichier text

        parole.write("""#!/bin/bash
pico2wave -l fr-FR -w temp.wav '""" + text +
"""'
amixer sset 'PCM' 95%
aplay -q temp.wav
rm temp.wav""")
    
        parole.close()
        os.rename('parole.txt','parole.sh') #fichier text --> fichier shell
        os.system('sh parole.sh') #execution du fichier shell
        os.remove('parole.sh') # suppression du fichier shell

    else:
        print("[RASPI SAYS] " + text)


#rene_parle('Bonjour')
