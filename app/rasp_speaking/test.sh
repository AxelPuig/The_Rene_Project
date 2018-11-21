#!/bin/bash
# Génère un fichier temporaire .wav 
pico2wave -l fr-FR -w ./app/rasp_speaking/temp.wav &quot;$1&quot;
# Règle le son 
amixer sset 'PCM' 95%
# Joue le son généré
aplay -q ./app/rasp_speaking/temp.wav
# Suppression du fichier temporaire
rm ./app/rasp_speaking/temp.wav