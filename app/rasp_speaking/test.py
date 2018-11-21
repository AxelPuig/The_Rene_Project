
import os

# Synthese vocale du texte saisi
def reneParle(text):
    os.system('sh test.sh &quot;' + text + '&quot;')

reneParle('Bonjour')
