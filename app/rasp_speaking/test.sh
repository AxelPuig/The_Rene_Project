#!/bin/bash
# Génère un fichier temporaire .wav 
pico2wave -l fr-FR -w ./temp.wav &quot;$1&quot;
# Règle le son 
amixer sset 'PCM' 95%
# Joue le son généré
aplay -q ./temp.wav
# Suppression du fichier temporaire
rm ./temp.wav