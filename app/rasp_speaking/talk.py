
import os

def rene_parle(text):
    """Synthese vocale du texte saisi (text), par le Raspberry"""
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


#rene_parle('Bonjour')
