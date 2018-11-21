from tkinter import *
from tkinter.messagebox import *
import os

# Synthese vocale du texte saisi
def reneParle():
    os.system('./test.sh &quot;' + lblTexte.get() + '&quot;')

fen1=Tk()
lblTexte=Entry(fen1)
lblTexte.grid(row=3,column=1,padx=5,pady=5)
btnParle=Button(fen1,text=&quot;Rene, parle !&quot;, command=reneparleParle)
btnParle.grid(row=3,column=2,padx=5,pady=5)
fen1.mainloop()
