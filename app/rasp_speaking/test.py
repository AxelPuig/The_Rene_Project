
import os

# Synthese vocale du texte saisi
def reneParle(text):
    os.system('./app/rasp_speaking/test.sh &quot;' + text + '&quot;')


reneParle('Bonjour')
