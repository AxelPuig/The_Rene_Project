
import os

# Synthese vocale du texte saisi
def reneParle(text):
    parole = open("parole.txt", "w")
    parole.write("""#!/bin/bash
pico2wave -l fr-FR -w temp.wav '""" + text +
"""'
amixer sset 'PCM' 95%
aplay -q temp.wav
rm temp.wav""")
    parole.write("pico2wave -l fr-FR -w temp.wav ")
    parole.write(text)
    parole.close()
    os.rename('parole.txt','parole.sh')
    os.system('sh parole.sh')
    os.remove('parole.sh')


reneParle('Bonjour')
