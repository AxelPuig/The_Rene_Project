#!/bin/bash
# G�n�re un fichier temporaire .wav 
pico2wave -l fr-FR -w ./app/rasp_speaking/temp.wav &quot;$1&quot;
# R�gle le son 
amixer sset 'PCM' 95%
# Joue le son g�n�r�
aplay -q ./app/rasp_speaking/temp.wav
# Suppression du fichier temporaire
rm ./app/rasp_speaking/temp.wav