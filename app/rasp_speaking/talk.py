import os
import platform

def rene_parle(text):
    """Synthese vocale du texte saisi (text), par le Raspberry.
    Si on est sur l'ordi, ça print le texte
    :param text: text to synthetize"""

    if platform.uname()[1] == "raspberrypi":
        parole = open("parole.txt", "w") #création d'un fichier texte

        parole.write("""#!/bin/bash
pico2wave -l fr-FR -w temp.wav '""" + text +
"""'
amixer sset 'PCM' 95%
omxplayer temp.wav
rm temp.wav""")
    
        parole.close()
        os.rename('parole.txt','parole.sh') #fichier texte --> fichier shell
        os.system('sh parole.sh') #execution du fichier shell
        os.remove('parole.sh') # suppression du fichier shell

    else:
        print("[RASPI SAYS] " + text)

#rene_parle('Bonjour')