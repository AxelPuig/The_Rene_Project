#!/bin/bash
# G�n�re un fichier temporaire .wav 
pico2wave -l fr-FR -w ./temp.wav &quot;$1&quot;
# R�gle le son 
amixer sset 'PCM' 95%
# Joue le son g�n�r�
aplay -q ./temp.wav
# Suppression du fichier temporaire
rm ./temp.wav